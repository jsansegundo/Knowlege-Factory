from pathlib import Path
import json

from loaders.loader_factory import extract_text
from chunker import chunk_document


DATA_FOLDER = Path("documents")

SUPPORTED_EXTENSIONS = [
    ".pdf",
    ".docx",
    ".pptx"
]

all_chunks = []

manifest = []

for file in DATA_FOLDER.iterdir():

    if file.suffix.lower() not in SUPPORTED_EXTENSIONS:
        continue

    print(f"Procesando {file.name}")

    document = extract_text(
        str(file)
    )

    chunks = chunk_document(
        document
    )

    manifest.append(
    {
        "file": file.name,
        "type": document.source_type,
        "characters": len(document.content),
        "chunks": len(chunks)
    }
)

    for chunk in chunks:

        all_chunks.append(
            {
                "document_name": chunk.document_name,
                "document_type": chunk.document_type,
                "chunk_number": chunk.chunk_number,
                "content": chunk.content
            }
        )

print()
print(f"Chunks totales: {len(all_chunks)}")

with open(
    "manifests/all_chunks.json",
    "w",
    encoding="utf-8"
) as f:

    json.dump(
        all_chunks,
        f,
        ensure_ascii=False,
        indent=2
    )

print()
print("all_chunks.json generado")

with open(
    "manifests/manifest.json",
    "w",
    encoding="utf-8"
) as f:

    json.dump(
        manifest,
        f,
        ensure_ascii=False,
        indent=2
    )

print("manifest.json generado")