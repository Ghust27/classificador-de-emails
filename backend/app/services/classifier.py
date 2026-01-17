from app.models.email import ClassificationResponse
from app.services.ai_service import get_ai_classification, generate_response

async def classify_email(email_content: str) -> ClassificationResponse:
    if not email_content or not email_content.strip():
        raise ValueError("Conteúdo do email não pode estar vazio")
    
    classification_result = await get_ai_classification(email_content.strip())
    
    suggested_response = await generate_response(
        email_content=email_content.strip(),
        category=classification_result["category"]
    )
    
    return ClassificationResponse(
        category=classification_result["category"],
        suggested_response=suggested_response,
        confidence=classification_result.get("confidence", 0.8)
    )