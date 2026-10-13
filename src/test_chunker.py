from loaders.loader_factory import extract_text

from chunker import chunk_document


document = extract_text(
    "data/test.docx"
)

chunks = chunk_document(
    document
)

print(
    f"Chunks generados: {len(chunks)}"
)

print()

print(
    chunks[0]
)