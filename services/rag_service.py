"""
services/rag_service.py
------------------------
المنطق الأساسي لـ RAG: تحويل السؤال لـ embedding، البحث في ChromaDB،
ثم استدعاء Gemini بالسياق المسترجع.
"""

from google import genai
from sentence_transformers import SentenceTransformer

from core.config import (
    EMBED_LOCAL_FILES_ONLY,
    EMBED_MODEL_NAME,
    GEMINI_API_KEY,
    GEMINI_MODEL,
    TOP_K_RESULTS,
)
from db.chroma import get_collection
from models.schemas import QueryResponse

SYSTEM_PROMPT = """
أنت خبير ومساعد ذكي متخصص حصرياً في الإجابة عن استفسارات الـ Scaffolding (السقالات).

التعليمات الصارمة:
1. الإجابة يجب أن تعتمد تماماً وبدقة على "السياق المرفق" فقط دون استخدام أي معلومات خارجية.
2. إذا ألقى المستخدم التحية، رحّب به بأدب واعرض مساعدة متعلقة بأسئلة السقالات.
3. إذا كان السؤال متعلقاً بمجال آخر خارج السقالات أو خارج السياق المرفق، اعتذر بوضوح وقل: "عذراً، أنا متخصص فقط في الإجابة عن استفسارات السقالات بناءً على البيانات المتاحة."
4. إذا كانت المعلومات في السياق غير كافية للإجابة، قل: "عذراً، هذه المعلومة غير متوفرة في قاعدة البيانات المتاحة لدي."
5. حافظ على صيغة إجابة منظمة، مباشرة، وواضحة (استخدم النقاط القصيرة).
6. أجب بنفس اللغة التي سأل بها المستخدم (العربية أو الإنجليزية).
7. حاول تخلي الاجابة هيا اعادة صياغة لكلام بدل متقول كلمتين بس، وركز على تقديم معلومات دقيقة ومفيدة.
8. حاول متبينش ان في مصدر بترجع له كده كده المصدر بيظهر بعد ما تجاوب
"""


class RagService:
    """
    نلفّو كل حاجة (موديل الـ embeddings، عميل Gemini، الكولكشن) جوة class
    ونحمّلهم مرة وحدة بس عند أول استعمال (lazy init)، باش:
    - السيرفر ما يوقعش عند الإقلاع لو الكولكشن ماشي موجودة (يبان الخطأ وقت
      أول طلب فقط، أو تقدر تستدعي .warmup() بنفسك عند الإقلاع).
    - نقدر نعمل mock/stub للكلاس هذا بسهولة في الاختبارات.
    """

    def __init__(self) -> None:
        self._embed_model: SentenceTransformer | None = None
        self._genai_client: genai.Client | None = None

    @property
    def embed_model(self) -> SentenceTransformer:
        if self._embed_model is None:
            print("جاري تحميل نموذج الـ Embeddings...")
            self._embed_model = SentenceTransformer(
                EMBED_MODEL_NAME, local_files_only=EMBED_LOCAL_FILES_ONLY
            )
        return self._embed_model

    @property
    def genai_client(self) -> genai.Client:
        if self._genai_client is None:
            self._genai_client = genai.Client(api_key=GEMINI_API_KEY)
        return self._genai_client

    def warmup(self) -> None:
        """تحميل الموديل والتحقق من الكولكشن عند إقلاع السيرفر، مش عند أول طلب."""
        _ = self.embed_model
        _ = get_collection()

    def ask(self, question: str) -> QueryResponse:
        # 1. تحويل السؤال لمتجه والبحث في ChromaDB
        query_vector = self.embed_model.encode(question).tolist()
        collection = get_collection()
        results = collection.query(query_embeddings=[query_vector], n_results=TOP_K_RESULTS)

        fetched_docs = (
            results.get("documents", [[]])[0]
            if results and "documents" in results
            else []
        )

        if not fetched_docs:
            return QueryResponse(
                question=question,
                answer="لم يتم العثور على أي بيانات ذات صلة بالسؤال.",
                sources=[],
            )

        context = "\n---\n".join(fetched_docs)

        # 2. استدعاء Gemini API
        prompt_content = f"السياق المتاح:\n{context}\n\nسؤال المستخدم: {question}"

        response = self.genai_client.models.generate_content(
            model=GEMINI_MODEL,
            contents=prompt_content,
            config={"system_instruction": SYSTEM_PROMPT, "temperature": 0.2},
        )

        return QueryResponse(
            question=question,
            answer=response.text,
            sources=fetched_docs,
        )


# وحدة مشتركة (singleton) يستعملها كل المشروع
rag_service = RagService()
