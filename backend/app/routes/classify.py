from fastapi import APIRouter, File, UploadFile, Form, HTTPException
from app.models.email import ClassificationResponse
from app.services.classifier import classify_email
from app.utils.file_parser import parse_file

router = APIRouter(prefix="/api", tags=["classification"])

@router.post("/classify", response_model=ClassificationResponse)
async def classify_email_route(
    file: UploadFile | None = File(None),
    text: str | None = Form(None)
):
    if not file and not text:
        raise HTTPException(
            status_code=400,
            detail="É necessário fornecer um arquivo ou texto"
        )
    
    try:
        email_content = ""
        
        if file:
            if not file.filename.endswith(('.txt', '.pdf')):
                raise HTTPException(
                    status_code=400,
                    detail="Tipo de arquivo não suportado. Use .txt ou .pdf"
                )
            
            email_content = await parse_file(file)
        
        elif text:
            if len(text) > 800:
                raise HTTPException(
                    status_code=400,
                    detail="Texto muito longo. Máximo 800 caracteres"
                )
            email_content = text
        
        result = await classify_email(email_content)
        
        return result
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Erro ao classificar email: {str(e)}"
        )