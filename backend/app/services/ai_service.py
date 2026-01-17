import os
import json
from typing import Dict, Any


def get_openai_client():
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY não encontrada nas variáveis de ambiente")
    
    try:
        from openai import OpenAI
        
        client = OpenAI(
            api_key=api_key.strip(),
        )
        return client
    except ImportError:
        raise ValueError("Biblioteca openai não está instalada. Execute: pip install openai>=1.40.0")
    except Exception as e:
        raise ValueError(f"Erro ao inicializar cliente OpenAI: {str(e)}")


async def get_ai_classification(text: str) -> Dict[str, Any]:
    try:
        client = get_openai_client()
        
        prompt = f"""Você é um classificador de emails profissional para uma empresa financeira.
Analise o seguinte email e classifique-o como "Produtivo" ou "Improdutivo":
Email: {text}
Critérios:
- Produtivo: Emails que requerem uma ação ou resposta específica (solicitações de suporte técnico, atualização sobre casos, dúvidas sobre o sistema, problemas técnicos, solicitações de informação)
- Improdutivo: Emails que não necessitam de uma ação imediata (mensagens de felicitações, agradecimentos genéricos, spam, mensagens sem propósito claro)
Responda APENAS com JSON válido no formato:
{{"category": "Produtivo" ou "Improdutivo", "confidence": 0.0-1.0}}
Não inclua nenhum texto adicional, apenas o JSON."""
        
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system", 
                    "content": "Você é um classificador de emails especializado. Sempre responda apenas com JSON válido."
                },
                {
                    "role": "user", 
                    "content": prompt
                }
            ],
            temperature=0.3,
            max_tokens=100
        )
        
        response_text = response.choices[0].message.content.strip()
        
        response_text = response_text.replace("```json", "").replace("```", "").strip()
        
        try:
            result = json.loads(response_text)
        except json.JSONDecodeError:
            if "Produtivo" in response_text:
                result = {"category": "Produtivo", "confidence": 0.8}
            elif "Improdutivo" in response_text:
                result = {"category": "Improdutivo", "confidence": 0.8}
            else:
                result = {"category": "Produtivo", "confidence": 0.5}
        
        if result.get("category") not in ["Produtivo", "Improdutivo"]:
            result["category"] = "Produtivo"
        
        if "confidence" not in result or not isinstance(result["confidence"], (int, float)):
            result["confidence"] = 0.8
        
        result["confidence"] = max(0.0, min(1.0, float(result["confidence"])))
        
        return result
        
    except ValueError as e:
        raise Exception(f"Erro de configuração: {str(e)}")
    except Exception as e:
        error_msg = str(e)
        if "proxies" in error_msg.lower() or "proxy" in error_msg.lower():
            raise Exception(
                f"Erro na inicialização do cliente OpenAI. "
                f"Tente reinstalar: pip uninstall openai -y && pip install 'openai>=1.40.0'"
            )
        raise Exception(f"Erro ao classificar com OpenAI: {error_msg}")


async def generate_response(email_content: str, category: str) -> str:
    try:
        client = get_openai_client()
        nome = "Lucas"
        cargo = "CEO"
        empresa = "AutoU"
        
        if category == "Produtivo":
            prompt = f"""Você é um assistente profissional de uma empresa financeira.
Gere uma resposta profissional, curta e adequada para o seguinte email produtivo.
Email recebido:
{email_content}
Requisitos:
- Resposta em português brasileiro
- Profissional mas calorosa
- Indique que a solicitação foi recebida e será analisada
- Seja específico e relevante ao conteúdo do email
- Máximo 150 palavras
- Sempre finalize a resposta com:
  Atenciosamente.
  {nome}
  {cargo}
  {empresa}

Responda APENAS com a resposta sugerida, sem explicações ou formatação adicional."""
        else:
            prompt = f"""Você é um assistente profissional de uma empresa financeira.
Gere uma resposta profissional, curta e adequada para o seguinte email improdutivo (agradecimento, felicitações, etc).
Email recebido:
{email_content}
Requisitos:
- Resposta em português brasileiro
- Profissional mas calorosa
- Agradeça o contato
- Seja breve e cordial
- Máximo 50 palavras
- Sempre finalize a resposta com:
  Atenciosamente.
  {nome}
  {cargo}
  {empresa}

Responda APENAS com a resposta sugerida, sem explicações ou formatação adicional."""
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system", 
                    "content": "Você é um assistente que gera respostas profissionais para emails corporativos. Sempre responda em português brasileiro."
                },
                {
                    "role": "user", 
                    "content": prompt
                }
            ],
            temperature=0.7,
            max_tokens=200
        )
        
        response_text = response.choices[0].message.content.strip()
        
        if response_text.startswith('"') and response_text.endswith('"'):
            response_text = response_text[1:-1]
        if response_text.startswith("'") and response_text.endswith("'"):
            response_text = response_text[1:-1]
        
        nome = "Lucas"
        cargo = "CEO"
        empresa = "AutoU"
        assinatura = f"Atenciosamente.\n{nome}\n{cargo}\n{empresa}"
        
        if nome not in response_text or empresa not in response_text:
            response_text = response_text.rstrip() + f"\n\n{assinatura}"
        
        return response_text
    
    except ValueError as e:
        raise Exception(f"Erro de configuração: {str(e)}")
    except Exception as e:
        error_msg = str(e)
        if "proxies" in error_msg.lower() or "proxy" in error_msg.lower():
            raise Exception(
                f"Erro na inicialização do cliente OpenAI. "
                f"Tente reinstalar: pip uninstall openai -y && pip install 'openai>=1.40.0'"
            )
        nome = "Lucas"
        cargo = "CEO"
        empresa = "AutoU"
        
        if category == "Produtivo":
            return f"Obrigado pelo seu email. Recebemos sua solicitação e nossa equipe está analisando. Retornaremos em breve com uma resposta.\n\nAtenciosamente.\n{nome}\n{cargo}\n{empresa}"
        else:
            return f"Obrigado pelo contato. Sua mensagem foi recebida com muito carinho. Tenha um ótimo dia!\n\nAtenciosamente.\n{nome}\n{cargo}\n{empresa}"