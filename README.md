# 🏗️ Scaffolding RAG AI Assistant

**مساعد ذكي متخصص في مجال السقالات (Scaffolding)، يعتمد على تقنيات Retrieval-Augmented Generation (RAG) للإجابة عن الأسئلة بالاعتماد على مستندات وبيانات متخصصة.**

يهدف المشروع إلى توفير تجربة تفاعلية تُمكّن المستخدم من طرح الأسئلة باللغة العربية أو الإنجليزية، واسترجاع المعلومات ذات الصلة من قاعدة المعرفة، ثم توليد إجابات باستخدام نموذج Google Gemini مع عرض المصادر المسترجعة.

---

## ✨ المميزات الرئيسية

- **RAG Architecture:** ربط نموذج الذكاء الاصطناعي بقاعدة معرفة متخصصة.
- **Semantic Search:** البحث الدلالي باستخدام Embeddings.
- **Vector Database:** تخزين واسترجاع البيانات باستخدام ChromaDB.
- **AI-Powered Answers:** توليد إجابات باستخدام Google Gemini.
- **Source Retrieval:** عرض المستندات والمصادر المستخدمة في الإجابة.
- **Bilingual Support:** دعم الأسئلة باللغة العربية والإنجليزية.
- **REST API:** توفير API باستخدام FastAPI.
- **Interactive Chat Interface:** واجهة محادثة باستخدام Streamlit.
- **Modular Architecture:** فصل واجهات API عن منطق معالجة واسترجاع البيانات.

## 🛠️ التقنيات المستخدمة

| التقنية | الاستخدام |
|---|---|
| Python | لغة البرمجة الأساسية |
| FastAPI | تطوير REST API |
| Streamlit | واجهة المحادثة |
| ChromaDB | قاعدة بيانات المتجهات |
| Sentence Transformers | إنشاء Embeddings |
| BAAI/bge-m3 | نموذج تحويل النصوص إلى متجهات |
| Google Gemini | توليد الإجابات |
| Pydantic | التحقق من البيانات |

## 🏛️ هيكل المشروع

```text
rag/
│
├── api/
│   └── routes/
│       └── chat.py
│
├── core/
│   └── config.py
│
├── db/
│   └── chroma.py
│
├── models/
│   └── schemas.py
│
├── services/
│   └── rag_service.py
│
├── app.py
├── ingest.py
├── ui.py
├── .gitignore
└── README.md
```

## ⚙️ متطلبات التشغيل

- Python 3.10 أو أحدث.
- Google Gemini API Key.
- اتصال بالإنترنت عند استخدام Gemini.
- نموذج Embedding: `BAAI/bge-m3`.
- ملف البيانات CSV المستخدم في عملية تجهيز قاعدة المعرفة.

## 🚀 Installation & Setup

### 1. Clone Repository

```bash
git clone https://github.com/belalelshobokshy-bot/rag.git
```

```bash
cd rag
```

### 2. Create Virtual Environment

```bash
python -m venv .venv
```

تفعيل البيئة على Windows:

```powershell
.venv\Scripts\Activate.ps1
```

### 3. Install Dependencies

```bash
pip install fastapi uvicorn chromadb sentence-transformers google-genai python-dotenv streamlit requests pandas
```

### 4. Configure Environment Variables

أنشئ ملف `.env` داخل مجلد المشروع:

```env
GEMINI_API_KEY=your_gemini_api_key
```

استبدل القيمة بمفتاح Gemini الخاص بك.

**تنبيه:** لا ترفع ملف `.env` إلى GitHub أو تشارك مفتاح API مع أي شخص.

### 5. Prepare Knowledge Base

ضع ملف البيانات CSV في المسار المتوقع داخل إعدادات `ingest.py`، ثم نفّذ:

```bash
python ingest.py
```

تقوم هذه الخطوة بمعالجة البيانات وإنشاء Embeddings وتخزينها في ChromaDB.

### 6. Run FastAPI Server

```bash
python -m uvicorn app:app --reload
```

بعد التشغيل:

- API: http://127.0.0.1:8000
- Swagger Documentation: http://127.0.0.1:8000/docs

### 7. Run Streamlit Interface

افتح Terminal جديدًا، وفعّل البيئة الافتراضية، ثم:

```bash
streamlit run ui.py
```

## 🔌 API Usage

### Endpoint

```http
POST /ask
```

### Request Body

```json
{
  "question": "ما هي شروط السلامة عند تركيب السقالات؟"
}
```

### Response Example

```json
{
  "status": "success",
  "question": "ما هي شروط السلامة عند تركيب السقالات؟",
  "answer": "الإجابة المولدة اعتمادًا على المعلومات المسترجعة...",
  "sources": [
    "المصدر الأول...",
    "المصدر الثاني..."
  ]
}
```

## 🧠 How RAG Works

يعتمد المشروع على المراحل التالية:

1. **User Query:** يستقبل النظام سؤال المستخدم.
2. **Embedding Generation:** يحوّل السؤال إلى Vector باستخدام BGE-M3.
3. **Semantic Retrieval:** يبحث في ChromaDB عن أكثر المستندات ارتباطًا بالسؤال.
4. **Context Construction:** يجمع المعلومات المسترجعة في سياق واحد.
5. **LLM Generation:** يرسل السياق والسؤال إلى Gemini لتوليد الإجابة.
6. **Response:** يعرض الإجابة والمصادر من خلال API وواجهة المحادثة.

## 🔒 Security Notes

- تخزين مفاتيح API داخل Environment Variables.
- استثناء الملفات الحساسة من Git.
- عدم مشاركة بيانات الاعتماد أو مفاتيح الخدمات.
- التحقق من مدخلات API قبل معالجتها.

## 👨‍💻 Developer

**Belal El-Shobokshy**

Full-Stack Developer & AI Engineer

GitHub: [@belalelshobokshy-bot](https://github.com/belalelshobokshy-bot)

---

*Built with Python, FastAPI, ChromaDB, and Google Gemini.*
