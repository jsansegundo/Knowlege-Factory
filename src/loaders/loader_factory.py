from pathlib import Path

from loaders.pdf_loader import extract_text as pdf_extract
from loaders.docx_loader import extract_text as docx_extract
from loaders.pptx_loader import extract_text as pptx_extract
from loaders.xlsx_loader import extract_text as xlsx_extract


def extract_text(file_path):

    extension = Path(file_path).suffix.lower()

    if extension == ".pdf":
        return pdf_extract(file_path)

    elif extension == ".docx":
        return docx_extract(file_path)

    elif extension == ".pptx":
        return pptx_extract(file_path)

    elif extension == ".xlsx":
        return xlsx_extract(file_path)

    else:
        raise ValueError(
            f"Formato no soportado: {extension}"
        )