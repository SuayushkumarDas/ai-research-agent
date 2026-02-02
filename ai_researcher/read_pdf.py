import io
import requests
from PyPDF2 import PdfReader


def read_pdf(url: str) -> str:
    response = requests.get(url)
    response.raise_for_status()

    reader = PdfReader(io.BytesIO(response.content))
    text = ""

    for page in reader.pages:
        text += page.extract_text() or ""

    return text.strip()
