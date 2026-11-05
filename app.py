from fastapi import FastAPI
import uvicorn

from api.routes import chat

app = FastAPI(
    title="Scaffolding RAG API",
    description="API مخصص للاستعلام عن بيانات الـ Scaffolding باستخدام ChromaDB و Gemini",
    version="1.0.0",
)

app.include_router(chat.router)


@app.get("/", summary="فحص صحة السيرفر")
async def health_check():
    return {"status": "ok", "service": "Scaffolding RAG API"}


if __name__ == "__main__":
    uvicorn.run("app:app", host="127.0.0.1", port=8000, reload=True)
