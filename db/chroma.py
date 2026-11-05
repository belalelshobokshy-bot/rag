

import chromadb
from chromadb.api.models.Collection import Collection

from core.config import CHROMA_PATH, COLLECTION_NAME


def get_chroma_client() -> chromadb.PersistentClient:
    return chromadb.PersistentClient(path=CHROMA_PATH)


def get_collection(create_if_missing: bool = False) -> Collection:
    """
    يرجع الـ collection الخاصة بالمشروع.

    - create_if_missing=False (الافتراضي): يُستعمل في app.py. لو الـ collection
      مش موجودة (يعني ما شغلتش ingest.py قبل)، كيرفع خطأ واضح بدل ما يكره
      السيرفر بخطأ chromadb مبهم.
    - create_if_missing=True: يُستعمل في ingest.py لإنشاء الـ collection.
    """
    client = get_chroma_client()

    if create_if_missing:
        return client.get_or_create_collection(name=COLLECTION_NAME)

    try:
        return client.get_collection(name=COLLECTION_NAME)
    except Exception as e:
        raise RuntimeError(
            f"❌ لم يتم العثور على الكولكشن '{COLLECTION_NAME}' في '{CHROMA_PATH}'. "
            "شغّل 'python ingest.py' أولاً باش تبني قاعدة البيانات قبل تشغيل الـ API."
        ) from e


def reset_collection() -> Collection:
    """يحذف الكولكشن (لو موجودة) ويرجع وحدة جديدة فارغة. يُستعمل في ingest.py."""
    client = get_chroma_client()
    try:
        client.delete_collection(name=COLLECTION_NAME)
        print(f"🗑️ تم حذف الكولكشن القديمة '{COLLECTION_NAME}' لإعادة البناء من الصفر.")
    except Exception:
        pass
    return client.get_or_create_collection(name=COLLECTION_NAME)
