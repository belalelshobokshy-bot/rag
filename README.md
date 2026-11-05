# 🏗️ Scaffolding RAG AI Assistant

**مساعد ذكي متخصص في مجال السقالات (Scaffolding)، يعتمد على تقنية Retrieval-Augmented Generation (RAG) للإجابة عن الأسئلة بالاعتماد على مستندات وبيانات متخصصة.**

يتيح المشروع للمستخدم طرح الأسئلة باللغة العربية أو الإنجليزية، واسترجاع المعلومات ذات الصلة من قاعدة المعرفة باستخدام البحث الدلالي، ثم توليد إجابات مدعومة بالمصادر باستخدام Google Gemini.

---

## ✨ Features

- **RAG Architecture:** ربط نماذج الذكاء الاصطناعي بقاعدة معرفة متخصصة.
- **Semantic Search:** البحث الدلالي باستخدام Embeddings.
- **Vector Database:** تخزين واسترجاع البيانات باستخدام ChromaDB.
- **AI-Powered Answers:** توليد الإجابات باستخدام Google Gemini.
- **Source Retrieval:** عرض المستندات والمصادر المسترجعة مع الإجابات.
- **Bilingual Support:** دعم الأسئلة باللغة العربية والإنجليزية.
- **REST API:** توفير API باستخدام FastAPI.
- **Interactive Chat Interface:** واجهة محادثة باستخدام Streamlit.
- **Modular Architecture:** فصل API عن منطق معالجة واسترجاع البيانات.
- **Configurable Settings:** التحكم في إعدادات المشروع من خلال Environment Variables.

---

## 🛠️ Tech Stack

| Technology | Purpose |
|---|---|
| Python | Core Programming Language |
| FastAPI | REST API Development |
| Streamlit | Chat Interface |
| ChromaDB | Vector Database |
| Sentence Transformers | Embedding Generation |
| BAAI/bge-m3 | Embedding Model |
| Google Gemini | AI Response Generation |
| Pydantic | Data Validation |
| Pandas | Dataset Processing |
| Uvicorn | ASGI Server |

---

## 🏛️ Project Structure

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
├── requirements.txt
├── .env
├── .gitignore
└── README.md
```

---

## ⚙️ Requirements

- Python 3.10 or newer.
- Google Gemini API Key.
- Internet connection for Gemini API.
- CSV dataset used to build the knowledge base.
- Sufficient disk space for the embedding model and ChromaDB.

---

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

Activate on Windows:

```powershell
.venv\Scripts\Activate.ps1
```

Activate on Linux / macOS:

```bash
source .venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 🔐 Environment Variables Configuration

أنشئ ملفًا باسم `.env` في المجلد الرئيسي للمشروع، وأضف الإعدادات التالية:

```env
GEMINI_API_KEY=your_gemini_api_key

GEMINI_MODEL=gemini-flash-latest

EMBED_MODEL_NAME=BAAI/bge-m3

EMBED_LOCAL_FILES_ONLY=False

# ChromaDB Configuration
CHROMA_PATH=./chroma_db
COLLECTION_NAME=scaffolding_data

# Data Ingestion Configuration
CSV_FILE=scaffolding_chunks (1).csv

# Retrieval Configuration
TOP_K_RESULTS=3
```

### Environment Variables Explanation

| Variable | Description |
|---|---|
| `GEMINI_API_KEY` | مفتاح الوصول إلى Google Gemini API |
| `GEMINI_MODEL` | اسم نموذج Gemini المستخدم لتوليد الإجابات |
| `EMBED_MODEL_NAME` | اسم نموذج إنشاء Embeddings |
| `EMBED_LOCAL_FILES_ONLY` | تحديد تحميل النموذج محليًا فقط أو السماح بالتنزيل |
| `CHROMA_PATH` | مسار تخزين قاعدة بيانات ChromaDB |
| `COLLECTION_NAME` | اسم Collection داخل ChromaDB |
| `CSV_FILE` | اسم ملف CSV المستخدم في تجهيز البيانات |
| `TOP_K_RESULTS` | عدد المستندات المسترجعة لكل سؤال |

**Important Notes:**

- استبدل `your_gemini_api_key` بمفتاح Gemini API الخاص بك.
- تأكد من أن اسم ملف CSV يطابق الملف الموجود فعليًا.
- عند ضبط `EMBED_LOCAL_FILES_ONLY=False` قد يحتاج النظام إلى الإنترنت لتنزيل نموذج Embedding.
- لا ترفع ملف `.env` إلى GitHub أو تشارك مفاتيح API.
- استخدم ملف `.env.example` لمشاركة إعدادات المشروع دون بيانات سرية.

---

## 📚 Knowledge Base Preparation

قبل تشغيل النظام، يجب تجهيز قاعدة المعرفة.

ضع ملف CSV في المسار المحدد في `CSV_FILE`، ثم شغّل:

```bash
python ingest.py
```

تقوم عملية Ingestion بالخطوات التالية:

1. قراءة البيانات من ملف CSV.
2. التحقق من البيانات وتجهيز النصوص.
3. إنشاء Embeddings باستخدام BAAI/bge-m3.
4. تخزين النصوص والمتجهات في ChromaDB.
5. تجهيز قاعدة المعرفة للاسترجاع.

---

## ▶️ Running the Application

### 1. Start FastAPI Server

```bash
python -m uvicorn app:app --reload
```

بعد تشغيل السيرفر:

- **API:** http://127.0.0.1:8000
- **Swagger Documentation:** http://127.0.0.1:8000/docs

### 2. Start Streamlit Interface

افتح Terminal جديدًا، وفعّل البيئة الافتراضية، ثم شغّل:

```bash
streamlit run ui.py
```

ستظهر واجهة المحادثة في المتصفح.

---

## 🔌 API Documentation

### Ask Endpoint

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

---

## 🧠 How RAG Works

يعتمد النظام على المراحل التالية:

1. **User Query:** يستقبل النظام سؤال المستخدم.
2. **Embedding Generation:** يحوّل السؤال إلى Vector باستخدام BAAI/bge-m3.
3. **Semantic Retrieval:** يبحث في ChromaDB عن المستندات الأكثر ارتباطًا بالسؤال.
4. **Context Construction:** يجمع المعلومات المسترجعة في سياق واحد.
5. **LLM Generation:** يرسل السؤال والسياق إلى Google Gemini.
6. **Response Generation:** ينشئ Gemini إجابة اعتمادًا على السياق المتاح.
7. **Source Display:** يعرض النظام الإجابة والمصادر المسترجعة للمستخدم.

---

## 🔒 Security

- تخزين مفاتيح API في Environment Variables.
- استثناء `.env` والملفات الحساسة من Git.
- عدم مشاركة بيانات الاعتماد أو مفاتيح الخدمات.
- التحقق من مدخلات API.
- عدم نشر قواعد البيانات أو الملفات التي تحتوي على بيانات خاصة.

---

## 👨‍💻 Developer

**Belal El-Shobokshy**

Full-Stack Developer & AI Engineer

GitHub: [@belalelshobokshy-bot](https://github.com/belalelshobokshy-bot)

Project Repository: [Scaffolding RAG AI Assistant](https://github.com/belalelshobokshy-bot/rag)

---

*Built with Python, FastAPI, ChromaDB, Sentence Transformers, and Google Gemini.*
