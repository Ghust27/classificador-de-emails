from fastapi import UploadFile
from io import BytesIO
from PyPDF2 import PdfReader

async def parse_file(file: UploadFile) -> str:
    try:
        content = await file.read()

        if file.filename and file.filename.endswith('.txt'):
            return content.decode('utf-8')

        elif file.filename and file.filename.endswith('.pdf'):
            pdf_file = BytesIO(content)
            reader = PdfReader(pdf_file)

            text = ""
            for page in reader.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"

            if not text.strip():
                raise ValueError("PDF não contém texto extraível (pode ser escaneado)")

            return text

        else:
            raise ValueError("Tipo de arquivo não suportado. Use .txt ou .pdf")

    except UnicodeDecodeError as e:
        raise ValueError("Erro ao decodificar arquivo. Certifique-se de usar UTF-8") from e
    except Exception as e:
        raise ValueError(f"Erro ao ler arquivo: {str(e)}") from e
