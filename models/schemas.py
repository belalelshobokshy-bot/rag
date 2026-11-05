from pydantic import BaseModel, Field


class QueryRequest(BaseModel):
    question: str = Field(
        ..., json_schema_extra={"example": "ما هي شروط السلامة عند تركيب السقالات؟"}
    )


class QueryResponse(BaseModel):
    status: str = "success"
    question: str
    answer: str
    sources: list[str] = []
