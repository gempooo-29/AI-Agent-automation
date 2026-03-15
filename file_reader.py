import os
import PyPDF2
import docx
from langchain_core.tools import tool


@tool
def read_file(file_name: str, folder_path: str) -> str:
    """
    Read a file (PDF, DOCX, or TXT) from a specific folder and return its content.
    Use this when the user asks to read, open, or summarize a file.

    Args:
        file_name: The name of the file (e.g. 'report.pdf')
        folder_path: The folder where the file is (e.g. 'C:/Users/elkat/Downloads')

    Returns:
        The text content of the file.
    """
    full_path = os.path.join(folder_path, file_name)

    if not os.path.exists(full_path):
        return f"Error: File '{file_name}' not found in '{folder_path}'"

    ext = os.path.splitext(file_name)[1].lower()

    try:
        if ext == ".pdf":
            return _read_pdf(full_path)
        elif ext == ".docx":
            return _read_docx(full_path)
        elif ext == ".txt":
            return _read_txt(full_path)
        else:
            return f"Unsupported file type '{ext}'. Supported: .pdf, .docx, .txt"
    except Exception as e:
        return f"Error reading file: {str(e)}"


def _read_pdf(path: str) -> str:
    text = ""
    with open(path, "rb") as f:
        reader = PyPDF2.PdfReader(f)
        for i, page in enumerate(reader.pages):
            content = page.extract_text()
            if content:
                text += f"\n--- Page {i + 1} ---\n{content}"
    return text.strip() if text else "No text could be extracted from the PDF."


def _read_docx(path: str) -> str:
    doc = docx.Document(path)
    paragraphs = [p.text for p in doc.paragraphs if p.text.strip()]
    return "\n".join(paragraphs) if paragraphs else "No text found in the DOCX file."


def _read_txt(path: str) -> str:
    with open(path, "r", encoding="utf-8") as f:
        return f.read().strip()