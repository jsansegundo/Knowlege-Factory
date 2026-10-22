import json
import os

import numpy as np

from knowledge_chat import (
    format_candidate_block,
    format_context_block,
    format_source_citation,
)

TRAINER_ROLE = (
    "Actúas como formador de un workshop de seguridad para el cliente. "
    "Explica con claridad, paso a paso, y di qué acciones debe tomar el equipo. "
    "Responde únicamente usando la información proporcionada. "
    "Si la información no basta, dilo y sugiere qué habría que revisar."
)


def _search(client, index, chunks, query, top_k=3):
    response = client.embeddings.create(
        model=os.getenv("AZURE_EMBEDDING_DEPLOYMENT"),
        input=query,
    )
    vector = np.array([response.data[0].embedding], dtype="float32")
    _, indices = index.search(vector, top_k)
    return [int(i) for i in indices[0] if 0 <= int(i) < len(chunks)]


def _rerank(client, question, candidates):
    candidate_text = "\n\n".join(
        format_candidate_block(position, chunk)
        for position, chunk in enumerate(candidates, start=1)
    )
    prompt = f"""
Select every candidate that contains information useful
for answering the user's question.

Prioritize complete coverage. Keep multiple relevant candidates when
they provide distinct facts, actions, requirements or examples.
Reject candidates that only share isolated words.
Select no more than 4 candidates.

Return only a JSON array containing their candidate numbers,
ordered from most relevant to least relevant.

USER QUESTION:
{question}

CANDIDATES:
{candidate_text}
"""
    output = client.responses.create(
        model=os.getenv("AZURE_OPENAI_DEPLOYMENT"),
        input=prompt,
    ).output_text.strip()

    try:
        start, end = output.find("["), output.rfind("]")
        positions = json.loads(output[start:end + 1]) if start >= 0 and end > start else []
    except (json.JSONDecodeError, TypeError):
        positions = []

    selected = []
    for position in positions:
        if isinstance(position, int) and 1 <= position <= len(candidates) and position not in selected:
            selected.append(position)
        if len(selected) == 4:
            break

    return [candidates[p - 1] for p in selected] if selected else candidates[:4]


def retrieve(client, index, chunks, question):
    """Recupera los fragmentos del RAG para una pregunta (mismo flujo que knowledge_chat.py)."""
    rewrite = client.responses.create(
        model=os.getenv("AZURE_OPENAI_DEPLOYMENT"),
        input=(
            "Convert the following question into one concise English search query "
            "for semantic retrieval. Preserve names, identifiers, dates and numbers. "
            "Return only the English search query.\n\nQUESTION:\n" + question
        ),
    ).output_text.strip()

    queries = [question]
    if rewrite and rewrite.casefold() != question.casefold():
        queries.append(rewrite)

    candidate_indices = []
    for query in queries:
        for chunk_index in _search(client, index, chunks, query):
            if chunk_index not in candidate_indices:
                candidate_indices.append(chunk_index)

    candidates = [chunks[i] for i in candidate_indices]
    return _rerank(client, question, candidates)


def ask_knowledge(client, index, chunks, question):
    """Devuelve (respuesta, lista de fuentes), con el mismo flujo que knowledge_chat.py."""
    selected = retrieve(client, index, chunks, question)

    context = "\n\n".join(format_context_block(chunk) for chunk in selected)
    prompt = (
        f"{TRAINER_ROLE}\n\nCONTEXTO:\n\n{context}\n\nPREGUNTA:\n\n{question}\n"
    )
    answer = client.responses.create(
        model=os.getenv("AZURE_OPENAI_DEPLOYMENT"),
        input=prompt,
    ).output_text

    sources = [format_source_citation(chunk) for chunk in selected]
    return answer, sources
