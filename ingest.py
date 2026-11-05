
import os

import pandas as pd
from sentence_transformers import SentenceTransformer

from core.config import CSV_FILE, EMBED_LOCAL_FILES_ONLY, EMBED_MODEL_NAME
from db.chroma import reset_collection

print("⚡ جاري تحميل موديل الـ Embeddings...")
embed_model = SentenceTransformer(EMBED_MODEL_NAME, local_files_only=EMBED_LOCAL_FILES_ONLY)

# نحذف الكولكشن القديمة (لو موجودة) عشان نضمن عدم تكرار البيانات، ونبنيها من جديد
collection = reset_collection()

if not os.path.exists(CSV_FILE):
    raise FileNotFoundError(
        f"❌ لم يتم العثور على الملف: {CSV_FILE}\n"
        "تأكد من اسم الملف في .env (متغير CSV_FILE) أو ضعه بجانب ingest.py."
    )

df = pd.read_csv(CSV_FILE)

if "text" not in df.columns:
    raise ValueError(
        f"❌ لا يوجد عامود باسم 'text' في الملف. الأعمدة الموجودة: {df.columns.tolist()}"
    )

# نتجاهل أي صفوف فاضية في عمود النص
df = df.dropna(subset=["text"]).reset_index(drop=True)

if df.empty:
    raise ValueError("❌ الملف لا يحتوي على أي صفوف صالحة بعد تنظيف القيم الفارغة في عمود 'text'.")

print(f"📦 جاري معالجة {len(df)} عنصر وتحويلهم لـ Embeddings دفعة واحدة (batch)...")

texts = df["text"].astype(str).tolist()
vectors = embed_model.encode(texts, show_progress_bar=True).tolist()

# نستخدم chunk_id كمعرف فريد لو موجود، وإلا نستخدم رقم الصف
if "chunk_id" in df.columns and df["chunk_id"].is_unique:
    ids = [f"doc_{cid}" for cid in df["chunk_id"].astype(str).tolist()]
else:
    ids = [f"doc_{i}" for i in range(len(df))]

# نخزن أي أعمدة إضافية مفيدة (العنوان والمصدر) كـ metadata عشان تفيد في الاسترجاع لاحقاً
metadata_cols = [
    c
    for c in ["section_title", "source", "section_id", "chunk_index"]
    if c in df.columns
]
metadatas = (
    df[metadata_cols].astype(str).to_dict(orient="records") if metadata_cols else None
)

collection.add(
    documents=texts,
    embeddings=vectors,
    ids=ids,
    metadatas=metadatas,
)

print(
    f"✅ تم تحويل {len(texts)} نص لـ Embeddings وتخزينهم بنجاح داخل الكولكشن '{collection.name}'!"
)
print(f"📊 إجمالي عدد المستندات في الكولكشن الآن: {collection.count()}")
