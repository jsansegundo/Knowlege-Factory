from dotenv import load_dotenv
from openai import OpenAI
import os
import faiss
import json
import numpy as np

load_dotenv()

client = OpenAI(
    base_url=os.getenv("AZURE_OPENAI_ENDPOINT"),
    api_key=os.getenv("AZURE_OPENAI_API_KEY")
)

print("Cargando Knowledge Base...\n")

index = faiss.read_index(
    "indexes/knowledge.index"
)

with open(
    "manifests/all_chunks.json",
    "r",
    encoding="utf-8"
) as f:

    chunks = json.load(f)

print(f"Chunks cargados: {len(chunks)}")
print()
print("Knowledge Chat listo.")
print("Escribe 'salir' para terminar.\n")

while True:

    question = input("Pregunta: ")

    if question.lower() in [
        "salir",
        "exit",
        "quit"
    ]:
        break

    response = client.embeddings.create(
        model=os.getenv(
            "AZURE_EMBEDDING_DEPLOYMENT"
        ),
        input=question
    )

    query_vector = np.array(
        [response.data[0].embedding],
        dtype="float32"
    )

    distances, indices = index.search(
        query_vector,
        5
    )

    retrieved_chunks = [
        chunks[i]
        for i in indices[0]
    ]

    context = "\n\n".join(
        [
            chunk["content"]
            for chunk in retrieved_chunks
        ]
    )

    prompt = f"""
Responde únicamente usando la información proporcionada.

CONTEXTO:

{context}

PREGUNTA:

{question}
"""

    answer = client.responses.create(
        model=os.getenv(
            "AZURE_OPENAI_DEPLOYMENT"
        ),
        input=prompt
    )

    print("\nRespuesta:\n")
    print(answer.output_text)

    print("\nFuentes utilizadas:\n")

    for chunk in retrieved_chunks:

        print(
            f"- {chunk['document_name']} "
            f"(chunk {chunk['chunk_number']})"
        )

    print(
        "\n" + "-" * 80 + "\n"
    )