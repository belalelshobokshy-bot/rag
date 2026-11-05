

from fastapi import APIRouter, HTTPException

from models.schemas import QueryRequest, QueryResponse
from services.rag_service import rag_service

router = APIRouter(tags=["chat"])


@router.post("/ask", response_model=QueryResponse, summary="إرسال سؤال واسترجاع الإجابة عبر RAG")
async def ask_rag(request: QueryRequest) -> QueryResponse:
    if not request.question.strip():
        raise HTTPException(status_code=400, detail="السؤال لا يمكن أن يكون فارغاً.")

    try:
        return rag_service.ask(request.question)
    except Exception as e:
        print(f"\nError Details: {type(e).__name__} - {str(e)}\n")
        raise HTTPException(
            status_code=500, detail=f"حدث خطأ أثناء معالجة الطلب: {str(e)}"
        )
