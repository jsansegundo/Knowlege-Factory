from dotenv import load_dotenv
from openai import OpenAI
from pathlib import Path
import os
import faiss
import json
import numpy as np

from registry import load_registry


METADATA_DISPLAY_FIELDS = (
    ("program", "Program"),
    ("document_role", "Role"),
    ("source_authority", "Authority"),
    ("canonical_status", "Status"),
    ("version", "Version"),
    ("fiscal_year", "Fiscal Year"),
    ("release_date", "Release Date"),
    ("audience", "Audience"),
    ("volatility", "Volatility"),
    ("validation_required", "Validation"),
)


def enrich_chunks_with_registry_metadata(
    chunks,
    registry_data
):
    metadata_by_name = {}
    metadata_by_path = {}

    for doc in registry_data.get(
        "documents",
        []
    ):
        metadata = doc.get("metadata")
        if not isinstance(metadata, dict):
            continue

        file_name = doc.get("file_name")
        file_path = doc.get("file_path")

        if file_name:
            metadata_by_name[file_name] = (
                dict(metadata)
            )
        if file_path:
            metadata_by_path[file_path] = (
                dict(metadata)
            )

    for chunk in chunks:
        if isinstance(
            chunk.get("metadata"),
            dict
        ):
            continue

        doc_name = chunk.get(
            "document_name",
            ""
        )
        doc_basename = Path(doc_name).name

        resolved = (
            metadata_by_path.get(doc_name)
            or metadata_by_name.get(doc_basename)
        )

        chunk["metadata"] = (
            dict(resolved)
            if resolved is not None
            else None
        )

    return chunks


def format_chunk_metadata_lines(
    chunk
):
    metadata = chunk.get("metadata")

    if not isinstance(metadata, dict):
        return []

    lines = []

    for key, label in METADATA_DISPLAY_FIELDS:
        value = metadata.get(key)
        if value:
            lines.append(
                f"{label}: {value}"
            )

    return lines


def format_candidate_block(
    position,
    chunk
):
    lines = [
        f"[CANDIDATE {position}]",
        f"Document: {chunk['document_name']}",
        f"Chunk: {chunk['chunk_number']}",
    ]

    lines.extend(
        format_chunk_metadata_lines(chunk)
    )

    lines.append("Content:")
    lines.append(chunk["content"])

    return "\n".join(lines)


def format_context_block(
    chunk
):
    lines = [
        f"[Document: {chunk['document_name']} | "
        f"Chunk: {chunk['chunk_number']}]"
    ]

    lines.extend(
        format_chunk_metadata_lines(chunk)
    )

    lines.append(chunk["content"])

    return "\n".join(lines)


def format_source_citation(
    chunk
):
    base = (
        f"- {chunk['document_name']} "
        f"(chunk {chunk['chunk_number']})"
    )

    metadata = chunk.get("metadata")

    if not isinstance(metadata, dict):
        return base

    tags = []
    for key in (
        "program",
        "document_role",
        "canonical_status",
        "source_authority",
    ):
        value = metadata.get(key)
        if value:
            tags.append(str(value))

    if not tags:
        return base

    return f"{base} [{' | '.join(tags)}]"


def main():
    load_dotenv()

    client = OpenAI(
        base_url=os.getenv(
            "AZURE_OPENAI_ENDPOINT"
        ),
        api_key=os.getenv(
            "AZURE_OPENAI_API_KEY"
        )
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

    registry_data = load_registry()

    enrich_chunks_with_registry_metadata(
        chunks,
        registry_data
    )

    print(
        f"Chunks cargados: {len(chunks)}"
    )
    print()
    print("Knowledge Chat listo.")
    print(
        "Escribe 'salir' para terminar.\n"
    )

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

        rewrite_response = (
            client.responses.create(
                model=os.getenv(
                    "AZURE_OPENAI_DEPLOYMENT"
                ),
                input=rewrite_prompt
            )
        )

        english_query = (
            rewrite_response
            .output_text
            .strip()
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
            response = (
                client.embeddings.create(
                    model=os.getenv(
                        "AZURE_EMBEDDING_DEPLOYMENT"
                    ),
                    input=search_query
                )
            )

            query_vector = np.array(
                [response.data[0].embedding],
                dtype="float32"
            )

            distances, indices = (
                index.search(
                    query_vector,
                    3
                )
            )

            for chunk_index in indices[0]:
                chunk_index = int(
                    chunk_index
                )

                if (
                    chunk_index >= 0
                    and chunk_index
                    < len(chunks)
                    and chunk_index
                    not in candidate_indices
                ):
                    candidate_indices.append(
                        chunk_index
                    )

        candidate_chunks = [
            chunks[chunk_index]
            for chunk_index
            in candidate_indices
        ]

        candidate_text = "\n\n".join(
            [
                format_candidate_block(
                    position,
                    chunk
                )
                for position, chunk
                in enumerate(
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

        rerank_response = (
            client.responses.create(
                model=os.getenv(
                    "AZURE_OPENAI_DEPLOYMENT"
                ),
                input=rerank_prompt
            )
        )

        rerank_output = (
            rerank_response
            .output_text
            .strip()
        )

        selected_positions = []

        try:
            array_start = (
                rerank_output.find("[")
            )
            array_end = (
                rerank_output.rfind("]")
            )

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
                        isinstance(
                            position,
                            int
                        )
                        and 1 <= position
                        <= len(candidate_chunks)
                        and position
                        not in selected_positions
                    ):
                        selected_positions.append(
                            position
                        )

                    if (
                        len(selected_positions)
                        == 4
                    ):
                        break

        except (
            json.JSONDecodeError,
            TypeError
        ):
            selected_positions = []

        if selected_positions:
            retrieved_chunks = [
                candidate_chunks[position - 1]
                for position
                in selected_positions
            ]
        else:
            retrieved_chunks = (
                candidate_chunks
            )

        context = "\n\n".join(
            [
                format_context_block(chunk)
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
                format_source_citation(chunk)
            )

        print(
            "\n" + "-" * 80 + "\n"
        )


if __name__ == "__main__":

    main()
