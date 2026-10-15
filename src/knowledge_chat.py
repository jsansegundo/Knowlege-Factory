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

    rewrite_prompt = f"""
Convert the following question into one concise English
search query for semantic retrieval.

Preserve names, product names, identifiers, dates,
numbers and quoted expressions exactly.

Return only the English search query.

QUESTION:
{question}
"""

    rewrite_response = client.responses.create(
        model=os.getenv(
            "AZURE_OPENAI_DEPLOYMENT"
        ),
        input=rewrite_prompt
    )

    english_query = (
        rewrite_response.output_text.strip()
    )

    search_queries = [
        question
    ]

    if (
        english_query
        and english_query.casefold()
        != question.casefold()
    ):
        search_queries.append(
            english_query
        )

    candidate_indices = []

    for search_query in search_queries:
        response = client.embeddings.create(
            model=os.getenv(
                "AZURE_EMBEDDING_DEPLOYMENT"
            ),
            input=search_query
        )

        query_vector = np.array(
            [response.data[0].embedding],
            dtype="float32"
        )

        distances, indices = index.search(
            query_vector,
            3
        )

        for chunk_index in indices[0]:
            chunk_index = int(chunk_index)

            if (
                chunk_index >= 0
                and chunk_index < len(chunks)
                and chunk_index
                not in candidate_indices
            ):
                candidate_indices.append(
                    chunk_index
                )

    candidate_chunks = [
        chunks[chunk_index]
        for chunk_index in candidate_indices
    ]

    candidate_text = "\n\n".join(
        [
            (
                f"[CANDIDATE {position}]\n"
                f"Document: "
                f"{chunk['document_name']}\n"
                f"Chunk: "
                f"{chunk['chunk_number']}\n"
                f"Content:\n"
                f"{chunk['content']}"
            )
            for position, chunk in enumerate(
                candidate_chunks,
                start=1
            )
        ]
    )

    rerank_prompt = f"""
Select every candidate that contains information useful
for answering the user's question.

Prioritize complete coverage, not the smallest possible
set of candidates. Keep multiple relevant candidates when
they provide distinct facts, actions, requirements,
examples or complementary details.

If adjacent chunks from the same document contribute
different relevant information, keep all of them.

Reject candidates that only share isolated words but do
not address the meaning of the question.

Select no more than 4 candidates. Do not omit a relevant
candidate merely because another candidate gives a
partial answer.

Return only a JSON array containing their candidate
numbers, ordered from most relevant to least relevant.

Example:
[2, 4, 1]

USER QUESTION:
{question}

CANDIDATES:
{candidate_text}
"""

    rerank_response = client.responses.create(
        model=os.getenv(
            "AZURE_OPENAI_DEPLOYMENT"
        ),
        input=rerank_prompt
    )

    rerank_output = (
        rerank_response.output_text.strip()
    )

    selected_positions = []

    try:
        array_start = rerank_output.find("[")
        array_end = rerank_output.rfind("]")

        if (
            array_start >= 0
            and array_end > array_start
        ):
            parsed_positions = json.loads(
                rerank_output[
                    array_start:array_end + 1
                ]
            )

            for position in parsed_positions:
                if (
                    isinstance(position, int)
                    and 1 <= position
                    <= len(candidate_chunks)
                    and position
                    not in selected_positions
                ):
                    selected_positions.append(
                        position
                    )

                if len(selected_positions) == 4:
                    break

    except (
        json.JSONDecodeError,
        TypeError
    ):
        selected_positions = []

    if selected_positions:
        retrieved_chunks = [
            candidate_chunks[position - 1]
            for position in selected_positions
        ]
    else:
        retrieved_chunks = candidate_chunks

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