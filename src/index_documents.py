from pathlib import Path

from loaders.loader_factory import extract_text

DATA_FOLDER = Path("data")

SUPPORTED_EXTENSIONS = [
    ".pdf",
    ".docx",
    ".pptx"
]

documents = []

for file in DATA_FOLDER.iterdir():

    if file.suffix.lower() in SUPPORTED_EXTENSIONS:

        documents.append(file)

print()
print(f"Documentos encontrados: {len(documents)}")
print()

loaded_documents = []

for file in documents:

    print(f"Procesando: {file.name}")

    document = extract_text(
        str(file)
    )

    loaded_documents.append(
        document
    )

    print(
        f"Tipo: {document.source_type}"
    )

    print(
        f"Caracteres: {len(document.content)}"
    )

    print()