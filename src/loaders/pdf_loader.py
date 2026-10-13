from pypdf import PdfReader
from models.document import Document


def extract_text(pdf_path):

    reader = PdfReader(pdf_path)

    text = ""

    for page in reader.pages:

        page_text = page.extract_text()

        if page_text:
            text += page_text + "\n"

    return Document(
        source_file=pdf_path,
        source_type="pdf",
        content=text
    )