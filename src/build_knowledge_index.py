from dotenv import load_dotenv
from openai import OpenAI
import os
import json
import numpy as np
import faiss

load_dotenv()

client = OpenAI(
    base_url=os.getenv("AZURE_OPENAI_ENDPOINT"),
    api_key=os.getenv("AZURE_OPENAI_API_KEY")
)

with open(
    "manifests/all_chunks.json",
    "r",
    encoding="utf-8"
) as f:
    chunks = json.load(f)

print(f"Chunks encontrados: {len(chunks)}")

embeddings = []

for i, chunk in enumerate(chunks):

    response = client.embeddings.create(
        model=os.getenv("AZURE_EMBEDDING_DEPLOYMENT"),
        input=chunk["content"]
    )

    embeddings.append(
        response.data[0].embedding
    )

    print(
        f"Embedding {i+1}/{len(chunks)}"
    )

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
    "indexes/knowledge.index"
)

print()
print("knowledge.index generado correctamente")