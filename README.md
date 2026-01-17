# Classificador de Emails 📧

Um sistema inteligente de classificação de emails que utiliza IA para categorizar mensagens como **Produtivas** ou **Improdutivas** e gera respostas sugeridas automaticamente.

## 📋 Visão Geral do Projeto

O projeto é composto por dois componentes principais:

- **Frontend**: Interface web moderna construída com React + JavaScript
- **Backend**: API REST desenvolvida com FastAPI + Python

O sistema permite que usuários classifiquem emails através de:
1. **Upload de arquivos** (formatos `.txt` ou `.pdf`)
2. **Entrada de texto** (até 800 caracteres)

## 🏗️ Arquitetura

```
Classificador de Emails
├── Frontend (React + JavaScript + Tailwind)
│   └── Interface para envio e visualização de resultados
└── Backend (FastAPI + OpenAI)
    └── API para classificação e geração de respostas
```

---

## 🖥️ Frontend

### Tecnologias
- **React 19** - Biblioteca JavaScript para interfaces
- **Vite 7** - Build tool
- **Tailwind CSS 4** - Estilização
- **Lucide React** - Ícones

### Estrutura de Pastas

```
frontend/
├── src/
│   ├── App.jsx                 # Componente principal da aplicação
│   ├── main.jsx                # Ponto de entrada
│   ├── index.css               # Estilos globais
│   ├── components/
│   │   ├── ClassificationResult.jsx    # Exibe resultado da classificação
│   │   ├── EmailTextInput.jsx          # Input para texto do email
│   │   ├── EmailUploader.jsx           # Upload de arquivo
│   │   ├── LoadingSpinner.jsx          # Spinner de carregamento
│   │   └── ui/                         # Componentes UI reutilizáveis
│   │       ├── alert.jsx
│   │       ├── badge.jsx
│   │       ├── button.jsx
│   │       ├── card.jsx
│   │       ├── tabs.jsx
│   │       └── textarea.jsx
│   └── lib/
│       ├── api.js              # Funções para chamadas à API
│       └── utils.js            # Utilidades gerais
└── vite.config.js             # Configuração do Vite
```

### Como Funciona o Frontend

1. **Tabs de Navegação**: O usuário escolhe entre "Carregar Arquivo" ou "Inserir Texto"
2. **Envio de Dados**: 
   - Se arquivo: Upload via `FormData`
   - Se texto: Envio via JSON
3. **Estado de Carregamento**: Spinner é exibido enquanto aguarda resposta da API
4. **Exibição de Resultado**: 
   - Categoria (Produtivo/Improdutivo)
   - Resposta sugerida
   - Confiança da classificação
5. **Tratamento de Erros**: Alertas informativos em caso de falha

### Instalação do Frontend

```bash
cd frontend
npm install
```

### Executar Frontend

```bash
npm run dev
```

Acesso em: `http://localhost:5173`

---

## 🔧 Backend

### Tecnologias
- **FastAPI 0.104** - Framework web assíncrono
- **Uvicorn 0.24** - Servidor ASGI
- **OpenAI API** - Modelo GPT-4o-mini para classificação
- **PyPDF2 3.0** - Parser de arquivos PDF
- **Pydantic 2.5** - Validação de dados
- **Python-dotenv** - Gerenciamento de variáveis de ambiente

### Estrutura de Pastas

```
backend/
├── app/
│   ├── main.py                 # Configuração da aplicação FastAPI
│   ├── models/
│   │   └── email.py            # Modelos Pydantic para requisição/resposta
│   ├── routes/
│   │   └── classify.py         # Rotas da API
│   ├── services/
│   │   ├── ai_service.py       # Integração com OpenAI
│   │   └── classifier.py       # Lógica de classificação
│   └── utils/
│       ├── file_parser.py      # Parser para .txt e .pdf
│       └── text_processor.py   # Processamento de texto
├── requirements.txt            # Dependências Python
└── .env                        # Variáveis de ambiente (não incluído)
```

### Como Funciona o Backend

#### 1. **Endpoint Principal: `POST /api/classify`**

Aceita duas formas de entrada:

**A) Arquivo (multipart/form-data)**
```bash
curl -X POST http://localhost:8000/api/classify \
  -F "file=@email.txt"
```

**B) Texto (JSON)**
```bash
curl -X POST http://localhost:8000/api/classify \
  -H "Content-Type: application/json" \
  -d '{"text": "Seu email aqui"}'
```

#### 2. **Fluxo de Processamento**

1. **Recebimento**: O endpoint recebe arquivo ou texto
2. **Validação**: 
   - Arquivo: Verifica extensão (.txt ou .pdf)
   - Texto: Valida tamanho máximo (800 caracteres)
3. **Parsing**: 
   - Converte arquivo em texto usando `parse_file()`
4. **Classificação**:
   - Envia texto para `classify_email()`
   - Utiliza OpenAI para categorizar como "Produtivo" ou "Improdutivo"
5. **Geração de Resposta**:
   - Com base na categoria, gera resposta sugerida
6. **Retorno**: Retorna JSON com categoria, resposta e confiança

#### 3. **Serviço de IA (`ai_service.py`)**

- **`get_ai_classification(text)`**: Utiliza GPT-4o-mini para classificar o email
  - Prompt estruturado com critérios claros
  - Retorna categoria e nível de confiança
  
- **`generate_response(email_content, category)`**: Gera resposta sugerida
  - Respostas diferentes para emails produtivos e improdutivos

#### 4. **Parser de Arquivos (`file_parser.py`)**

- Suporta `.txt` (leitura direta)
- Suporta `.pdf` (usando PyPDF2)
- Retorna conteúdo em texto puro

### Modelo de Resposta

```json
{
  "category": "Produtivo",
  "suggested_response": "Obrigado por sua solicitação. Estamos analisando...",
  "confidence": 0.95
}
```

### Classificação de Categorias

**Produtivo**: Emails que requerem ação ou resposta
- Solicitações de suporte técnico
- Atualização sobre casos
- Dúvidas sobre o sistema
- Problemas técnicos
- Solicitações de informação

**Improdutivo**: Emails sem ação imediata necessária
- Felicitações
- Agradecimentos genéricos
- Spam
- Mensagens sem propósito claro

### Instalação do Backend

```bash
cd backend
python -m venv venv
# Windows
venv\Scripts\activate
# macOS/Linux
source venv/bin/activate

pip install -r requirements.txt
```

### Configuração de Variáveis de Ambiente

Criar arquivo `.env` na pasta `backend/`:

```
OPENAI_API_KEY=sua_chave_openai_aqui
FRONTEND_URL=http://localhost:5173
```

### Executar Backend

```bash
cd backend
uvicorn app.main:app --reload
```

Servidor em: `http://localhost:8000`
Documentação Swagger: `http://localhost:8000/docs`

---

## 🚀 Rodando o Projeto Completo

### Terminal 1 - Backend
```bash
cd backend
venv\Scripts\activate  # Windows
uvicorn app.main:app --reload
```

### Terminal 2 - Frontend
```bash
cd frontend
npm run dev
```

Acesse: `http://localhost:5173`

---

## 📊 Fluxo de Dados

```
Usuário
  ↓
Frontend (React)
  ↓ (requisição HTTP POST)
Backend (FastAPI)
  ↓
Parser (TXT/PDF)
  ↓
Classifier Service
  ↓
OpenAI API
  ↓
Response Generator
  ↓ (JSON Response)
Frontend (React)
  ↓
Resultado Exibido
```

---

## 🔑 Recursos Principais

✅ **Interface Intuitiva**: Duas abas para entrada (arquivo ou texto)  
✅ **Classificação IA**: Usa GPT-4o-mini para análise inteligente  
✅ **Suporte a Múltiplos Formatos**: .txt e .pdf  
✅ **Respostas Sugeridas**: Gera respostas automáticas baseadas na categoria  
✅ **Confiança da Classificação**: Exibe nível de certeza da IA  
✅ **CORS Habilitado**: Frontend e backend se comunicam sem restrições  
✅ **Validações**: Limites de tamanho e tipos de arquivo permitidos  

---

## 🛠️ Troubleshooting

### Erro: "OPENAI_API_KEY não encontrada"
- Verifique se o arquivo `.env` existe na pasta `backend/`
- Verifique se a chave API está correta

### Erro: "CORS policy: No 'Access-Control-Allow-Origin' header"
- Certifique-se de que o backend está rodando
- Verifique se `FRONTEND_URL` está configurada corretamente

### Erro: "Tipo de arquivo não suportado"
- Use apenas arquivos `.txt` ou `.pdf`

### Erro: "Texto muito longo"
- Máximo de 800 caracteres por requisição

---

## 📝 Licença

Projeto desenvolvido para fins educacionais e demonstração.

---

## 👨‍💻 Desenvolvimento

Para contribuições ou melhorias, certifique-se de:
- Manter a estrutura de pastas consistente
- Seguir as convenções de código (PEP 8 para Python, ESLint para JavaScript)
- Adicionar testes quando possível
- Documentar mudanças significativas
