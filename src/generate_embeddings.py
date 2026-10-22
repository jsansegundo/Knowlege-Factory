from dotenv import load_dotenv
from openai_client import create_openai_client
from pypdf import PdfReader
import numpy as np
import faiss
import os
import json

load_dotenv()

client = create_openai_client()

reader = PdfReader("data/incentives.pdf")

text = ""

for page in reader.pages:
    page_text = page.extract_text()

    if page_text:
        text += page_text + "\n"

chunk_size = 1000

chunks = [
    text[i:i + chunk_size]
    for i in range(0, len(text), chunk_size)
]

print(f"Chunks: {len(chunks)}")

embeddings = []

for i, chunk in enumerate(chunks):

    response = client.embeddings.create(
        model=os.getenv("AZURE_EMBEDDING_DEPLOYMENT"),
        input=chunk
    )

    vector = response.data[0].embedding

    embeddings.append(vector)

    print(f"Embedding {i+1}/{len(chunks)}")

embeddings_np = np.array(
    embeddings,
    dtype="float32"
)

index = faiss.IndexFlatL2(
    len(embeddings[0])
)

index.add(embeddings_np)

faiss.write_index(
    index,
    "data/incentives.index"
)

with open(
    "data/incentives_chunks.json",
    "w",
    encoding="utf-8"
) as f:

    json.dump(
        chunks,
        f,
        ensure_ascii=False,
        indent=2
    )

print("Índice generado correctamente")
