from fastapi import FastAPI, File, UploadFile, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import os
import json
from typing import Optional
from dotenv import load_dotenv


load_dotenv()

from app.services.classifier import classify_email
from app.utils.file_parser import parse_file

app = FastAPI(
    title="Classificador de Emails API",
    description="API para classificação automática de emails",
    version="1.0.0"
)

frontend_url = os.getenv("FRONTEND_URL", "http://localhost:5173")
app.add_middleware(
    CORSMiddleware,
    allow_origins=[frontend_url, "http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ClassificationResponse(BaseModel):
    category: str
    suggested_response: str
    confidence: float | None = None

class TextRequest(BaseModel):
    text: str

@app.post("/api/classify")
async def classify_email_endpoint(request: Request):
    try:
        content_type = request.headers.get("content-type", "").lower()
        text: Optional[str] = None
        file: Optional[UploadFile] = None
        
        if "application/json" in content_type:
            body = await request.json()
            text = body.get("text")
        elif "multipart/form-data" in content_type:
            form_data = await request.form()
            
            if "file" in form_data:
                file = form_data["file"]
            if "text" in form_data:
                text = form_data.get("text")
        
        if not file and not text:
            return JSONResponse(
                status_code=400,
                content={"error": "É necessário fornecer um arquivo ou texto"}
            )
        
        email_content = ""
        
        if file:
            if hasattr(file, 'filename'):
                if file.filename and not file.filename.endswith(('.txt', '.pdf')):
                    return JSONResponse(
                        status_code=400,
                        content={"error": "Tipo de arquivo não suportado. Use .txt ou .pdf"}
                    )
            try:
                email_content = await parse_file(file)
            except ValueError as e:
                return JSONResponse(
                    status_code=400,
                    content={"error": str(e)}
                )
        
        elif text:
            if len(text) > 800:
                return JSONResponse(
                    status_code=400,
                    content={"error": "Texto muito longo. Máximo 800 caracteres"}
                )
            email_content = text
        
        result = await classify_email(email_content)
        
        return result
    
    except json.JSONDecodeError:
        return JSONResponse(
            status_code=400,
            content={"error": "Formato JSON inválido"}
        )
    except ValueError as e:
        return JSONResponse(
            status_code=400,
            content={"error": str(e)}
        )
    except Exception as e:
        error_message = str(e)
        if "OPENAI_API_KEY" in error_message or "api key" in error_message.lower():
            return JSONResponse(
                status_code=500,
                content={"error": "Erro de configuração: OPENAI_API_KEY não encontrada. Verifique o arquivo .env"}
            )
        return JSONResponse(
            status_code=500,
            content={"error": f"Erro ao processar: {error_message}"}
        )

@app.get("/")
async def root():
    return {"message": "Classificador de Emails API", "status": "running"}

@app.get("/health")
async def health():
    return {"status": "healthy"}