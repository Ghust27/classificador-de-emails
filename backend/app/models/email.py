from pydantic import BaseModel, Field
from typing import Literal

EmailCategory = Literal["Produtivo", "Improdutivo"]

class ClassificationRequest(BaseModel):
    text: str = Field(..., min_length=1, max_length=800)

class ClassificationResponse(BaseModel):
    category: EmailCategory
    suggested_response: str
    confidence: float | None = Field(None, ge=0.0, le=1.0)

class ErrorResponse(BaseModel):
    error: str
    detail: str | None = None
