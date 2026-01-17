from fastapi import FastAPI, File, UploadFile, Request, Form, Body
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
import os
import json
from typing import Optional, Literal
from dotenv import load_dotenv


load_dotenv()

from app.services.classifier import classify_email
from app.utils.file_parser import parse_file


class ClassificationResponse(BaseModel):
    """Resposta da classificação do email"""
    category: Literal["Produtivo", "Improdutivo"] = Field(
        ..., 
        description="Categoria do email: 'Produtivo' para emails que requerem ação, 'Improdutivo' para emails sem ação necessária"
    )
    suggested_response: str = Field(
        ..., 
        description="Resposta sugerida gerada pela IA para o email"
    )
    confidence: float = Field(
        ..., 
        ge=0.0, 
        le=1.0, 
        description="Nível de confiança da classificação (0.0 a 1.0)"
    )

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "category": "Produtivo",
                    "suggested_response": "Prezado cliente, agradecemos seu contato. Estamos analisando sua solicitação e retornaremos em breve.",
                    "confidence": 0.95
                }
            ]
        }
    }

class TextRequest(BaseModel):
    """Requisição com texto do email"""
    text: str = Field(
        ..., 
        min_length=1, 
        max_length=800, 
        description="Conteúdo do email a ser classificado (máximo 800 caracteres)"
    )

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "text": "Olá, estou tendo problemas para acessar o sistema. Podem me ajudar?"
                }
            ]
        }
    }

class ErrorResponse(BaseModel):
    """Resposta de erro"""
    error: str = Field(..., description="Mensagem de erro")
    detail: Optional[str] = Field(None, description="Detalhes adicionais do erro")


app = FastAPI(
    title="Classificador de Emails API",
    description="""
## API para classificação automática de emails usando IA

Esta API classifica emails em duas categorias:
- **Produtivo**: Emails que requerem uma ação ou resposta (suporte técnico, dúvidas, solicitações)
- **Improdutivo**: Emails que não necessitam de ação imediata (felicitações, agradecimentos, spam)

### Funcionalidades:
- 📧 Classificação automática de emails
- 💬 Geração de respostas sugeridas
- 📊 Nível de confiança da classificação
- 📄 Suporte a arquivos .txt e .pdf
    """,
    version="1.0.0",
    contact={
        "name": "André",
        "url": "https://github.com/Ghust27/classificador-de-emails"
    },
    license_info={
        "name": "MIT"
    }
)

frontend_url = os.getenv("FRONTEND_URL", "http://localhost:5173")
app.add_middleware(
    CORSMiddleware,
    allow_origins=[frontend_url, "http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post(
    "/api/classify",
    response_model=ClassificationResponse,
    responses={
        200: {
            "description": "Classificação realizada com sucesso",
            "model": ClassificationResponse
        },
        400: {
            "description": "Erro de validação",
            "model": ErrorResponse,
            "content": {
                "application/json": {
                    "examples": {
                        "sem_conteudo": {
                            "summary": "Sem conteúdo",
                            "value": {"error": "É necessário fornecer um arquivo ou texto"}
                        },
                        "arquivo_invalido": {
                            "summary": "Arquivo inválido",
                            "value": {"error": "Tipo de arquivo não suportado. Use .txt ou .pdf"}
                        },
                        "texto_longo": {
                            "summary": "Texto muito longo",
                            "value": {"error": "Texto muito longo. Máximo 800 caracteres"}
                        }
                    }
                }
            }
        },
        500: {
            "description": "Erro interno do servidor",
            "model": ErrorResponse
        }
    },
    summary="Classificar Email",
    description="""
Classifica um email como **Produtivo** ou **Improdutivo** e gera uma resposta sugerida.

### Formas de envio:

**1. Via JSON (texto direto):**
```json
{
    "text": "Conteúdo do email aqui"
}
```

**2. Via Form Data (upload de arquivo):**
- Campo `file`: Arquivo .txt ou .pdf
- Campo `text` (opcional): Texto alternativo

### Critérios de classificação:

**Produtivo:**
- Solicitações de suporte técnico
- Dúvidas sobre o sistema
- Problemas técnicos
- Solicitações de informação

**Improdutivo:**
- Mensagens de felicitações
- Agradecimentos genéricos
- Spam
- Mensagens sem propósito claro
    """,
    tags=["Classificação"]
)
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


@app.post(
    "/api/classify/text",
    response_model=ClassificationResponse,
    responses={
        200: {"description": "Classificação realizada com sucesso", "model": ClassificationResponse},
        400: {"description": "Erro de validação", "model": ErrorResponse},
        500: {"description": "Erro interno do servidor", "model": ErrorResponse}
    },
    summary="Classificar Email (Texto)",
    description="Classifica um email enviado como texto JSON. Endpoint alternativo com tipagem explícita.",
    tags=["Classificação"]
)
async def classify_email_text(body: TextRequest):
    try:
        result = await classify_email(body.text)
        return result
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"error": f"Erro ao processar: {str(e)}"}
        )


@app.post(
    "/api/classify/file",
    response_model=ClassificationResponse,
    responses={
        200: {"description": "Classificação realizada com sucesso", "model": ClassificationResponse},
        400: {"description": "Erro de validação", "model": ErrorResponse},
        500: {"description": "Erro interno do servidor", "model": ErrorResponse}
    },
    summary="Classificar Email (Arquivo)",
    description="Classifica um email enviado como arquivo (.txt ou .pdf).",
    tags=["Classificação"]
)
async def classify_email_file(
    file: UploadFile = File(..., description="Arquivo .txt ou .pdf contendo o email")
):
    try:
        if not file.filename.endswith(('.txt', '.pdf')):
            return JSONResponse(
                status_code=400,
                content={"error": "Tipo de arquivo não suportado. Use .txt ou .pdf"}
            )
        
        email_content = await parse_file(file)
        result = await classify_email(email_content)
        return result
    except ValueError as e:
        return JSONResponse(
            status_code=400,
            content={"error": str(e)}
        )
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"error": f"Erro ao processar: {str(e)}"}
        )


@app.get(
    "/",
    summary="Raiz",
    description="Endpoint raiz da API. Retorna informações básicas sobre a API.",
    tags=["Status"]
)
async def root():
    return {
        "message": "Classificador de Emails API",
        "version": "1.0.0",
        "status": "running",
        "docs": "/docs"
    }


@app.get(
    "/health",
    summary="Health Check",
    description="Verifica se a API está funcionando corretamente.",
    tags=["Status"]
)
async def health():
    return {"status": "healthy"}