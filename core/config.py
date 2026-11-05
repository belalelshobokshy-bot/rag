import os
import sys

from dotenv import load_dotenv

# تحميل متغيرات البيئة من ملف .env (مرة وحدة، لكل المشروع)
load_dotenv()

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")


def _get_bool(name: str, default: bool) -> bool:
    val = os.getenv(name)
    if val is None:
        return default
    return val.strip().lower() in {"1", "true", "yes", "on"}


# --- Gemini ---
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    raise ValueError("❌ لم يتم العثور على GEMINI_API_KEY في ملف .env")

GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-flash-latest")

# --- Embeddings ---
EMBED_MODEL_NAME = os.getenv("EMBED_MODEL_NAME", "BAAI/bge-m3")

EMBED_LOCAL_FILES_ONLY = _get_bool("EMBED_LOCAL_FILES_ONLY", False)

# --- ChromaDB ---
CHROMA_PATH = os.getenv("CHROMA_PATH", "./chroma_db")
COLLECTION_NAME = os.getenv("COLLECTION_NAME", "scaffolding_data")

# --- Ingest ---

CSV_FILE = os.getenv("CSV_FILE", "scaffolding_chunks.csv")

# --- Retrieval ---
TOP_K_RESULTS = int(os.getenv("TOP_K_RESULTS", "3"))
