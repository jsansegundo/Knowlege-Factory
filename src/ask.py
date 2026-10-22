from dotenv import load_dotenv
from openai_client import create_openai_client
import os
import faiss
import json
import numpy as np


def build_prompt(context, question):

    return f"""
Responde únicamente utilizando la información disponible en el contexto.

CONTEXTO:

{context}

PREGUNTA:

{question}
"""


def main():

    load_dotenv()

    client = create_openai_client()

    print("Cargando índice...")

    index = faiss.read_index(
        "data/incentives.index"
    )

    with open(
        "data/incentives_chunks.json",
        "r",
        encoding="utf-8"
    ) as f:

        chunks = json.load(f)

    print("Asistente listo.")
    print("Escribe 'salir' para terminar.\n")

    while True:

        question = input("Pregunta: ")

        if question.lower() in ["salir", "exit", "quit"]:
            print("Hasta luego 👋")
            break

        response = client.embeddings.create(
            model=os.getenv("AZURE_EMBEDDING_DEPLOYMENT"),
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

        context = "\n\n".join(
            [chunks[i] for i in indices[0]]
        )

        answer = client.responses.create(
            model=os.getenv("AZURE_OPENAI_DEPLOYMENT"),
            input=build_prompt(context, question)
        )

        print("\nRespuesta:\n")
        print(answer.output_text)
        print("\n" + "-" * 80 + "\n")


if __name__ == "__main__":
    main()
