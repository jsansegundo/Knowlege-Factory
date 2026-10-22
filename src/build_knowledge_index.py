from pathlib import Path
from dotenv import load_dotenv

import os
import json
import numpy as np
import faiss

from openai_client import create_openai_client
from registry import (
    load_registry,
    save_registry,
    mark_document_indexed
)


CHUNKS_FILE = Path(
    "manifests/all_chunks.json"
)

INDEXES_FOLDER = Path(
    "indexes"
)

INDEX_FILE = (
    INDEXES_FOLDER
    / "knowledge.index"
)

EMBEDDINGS_CACHE_FILE = (
    INDEXES_FOLDER
    / "knowledge_embeddings.npz"
)


def load_chunks():

    if not CHUNKS_FILE.exists():

        raise FileNotFoundError(
            "No se encuentra "
            "manifests/all_chunks.json"
        )

    with open(
        CHUNKS_FILE,
        "r",
        encoding="utf-8"
    ) as f:

        chunks = json.load(f)

    if not chunks:

        raise ValueError(
            "all_chunks.json no contiene chunks."
        )

    validate_chunks(
        chunks
    )

    return chunks


def validate_chunks(
    chunks
):

    chunk_ids = set()

    for position, chunk in enumerate(
        chunks
    ):

        chunk_id = chunk.get(
            "chunk_id",
            ""
        ).strip()

        content = chunk.get(
            "content",
            ""
        ).strip()

        if not chunk_id:

            raise ValueError(
                "Se encontró un chunk "
                "sin chunk_id en la posición "
                f"{position}."
            )

        if not content:

            raise ValueError(
                "Se encontró un chunk "
                "sin contenido en la posición "
                f"{position}."
            )

        if chunk_id in chunk_ids:

            raise ValueError(
                "Se encontró un chunk_id "
                "duplicado: "
                f"{chunk_id}"
            )

        chunk_ids.add(
            chunk_id
        )


def load_embedding_cache(
    deployment_name
):

    if not EMBEDDINGS_CACHE_FILE.exists():

        return (
            [],
            np.empty(
                (0, 0),
                dtype="float32"
            )
        )

    try:

        with np.load(
            EMBEDDINGS_CACHE_FILE,
            allow_pickle=False
        ) as cache:

            cached_chunk_ids = (
                cache["chunk_ids"]
                .astype(str)
                .tolist()
            )

            cached_embeddings = np.asarray(
                cache["embeddings"],
                dtype="float32"
            )

            cached_deployment = str(
                cache["deployment"][0]
            )

    except (
        KeyError,
        ValueError,
        OSError
    ) as exc:

        raise ValueError(
            "La caché de embeddings "
            "no tiene un formato válido."
        ) from exc

    if cached_deployment!= deployment_name:

        print(
            "El deployment de embeddings "
            "ha cambiado."
        )

        print(
            "La caché anterior no se reutilizará."
        )

        return (
            [],
            np.empty(
                (0, 0),
                dtype="float32"
            )
        )

    if cached_embeddings.ndim!= 2:

        raise ValueError(
            "Los embeddings de la caché "
            "no tienen la estructura esperada."
        )

    if (
        len(cached_chunk_ids)
        != cached_embeddings.shape[0]
    ):

        raise ValueError(
            "El número de IDs de la caché "
            "no coincide con el número "
            "de embeddings."
        )

    if (
        len(cached_chunk_ids)
        != len(set(cached_chunk_ids))
    ):

        raise ValueError(
            "La caché contiene "
            "chunk_id duplicados."
        )

    return (
        cached_chunk_ids,
        cached_embeddings
    )


def create_embedding(
    client,
    deployment_name,
    content
):

    response = client.embeddings.create(
        model=deployment_name,
        input=content
    )

    vector = np.asarray(
        response.data[0].embedding,
        dtype="float32"
    )

    if (
        vector.ndim!= 1
        or vector.size == 0
    ):

        raise ValueError(
            "El servicio devolvió "
            "un embedding no válido."
        )

    return vector


def resolve_embeddings(
    chunks,
    cached_chunk_ids,
    cached_embeddings,
    embedding_function
):

    if (
        len(cached_chunk_ids)
        != len(cached_embeddings)
    ):

        raise ValueError(
            "La caché de embeddings "
            "es inconsistente."
        )

    cached_vectors = {
        chunk_id: vector
        for chunk_id, vector in zip(
            cached_chunk_ids,
            cached_embeddings
        )
    }

    resolved_embeddings = []

    reused_count = 0
    generated_count = 0

    expected_dimension = None

    total_chunks = len(
        chunks
    )

    for position, chunk in enumerate(
        chunks,
        start=1
    ):

        chunk_id = chunk["chunk_id"]

        if chunk_id in cached_vectors:

            vector = np.asarray(
                cached_vectors[chunk_id],
                dtype="float32"
            )

            reused_count += 1

            action = "reutilizado"

        else:

            vector = np.asarray(
                embedding_function(
                    chunk["content"].strip()
                ),
                dtype="float32"
            )

            generated_count += 1

            action = "generado"

        if (
            vector.ndim!= 1
            or vector.size == 0
        ):

            raise ValueError(
                "Embedding no válido "
                "para el chunk: "
                f"{chunk_id}"
            )

        if expected_dimension is None:

            expected_dimension = (
                vector.size
            )

        elif (
            vector.size
            != expected_dimension
        ):

            raise ValueError(
                "Los embeddings no tienen "
                "una dimensión uniforme."
            )

        resolved_embeddings.append(
            vector
        )

        print(
            f"Embedding {position}/"
            f"{total_chunks}: {action}"
        )

    embeddings_np = np.vstack(
        resolved_embeddings
    ).astype(
        "float32"
    )

    return (
        embeddings_np,
        reused_count,
        generated_count
    )


def save_embedding_cache(
    chunks,
    embeddings,
    deployment_name
):

    chunk_ids = np.asarray(
        [
            chunk["chunk_id"]
            for chunk in chunks
        ],
        dtype=str
    )

    np.savez_compressed(
        EMBEDDINGS_CACHE_FILE,
        chunk_ids=chunk_ids,
        embeddings=embeddings,
        deployment=np.asarray(
            [deployment_name],
            dtype=str
        )
    )


def build_faiss_index(
    embeddings
):

    if embeddings.ndim!= 2:

        raise ValueError(
            "Los embeddings no tienen "
            "la estructura esperada."
        )

    vector_dimension = (
        embeddings.shape[1]
    )

    index = faiss.IndexFlatL2(
        vector_dimension
    )

    index.add(
        embeddings
    )

    if index.ntotal!= embeddings.shape[0]:

        raise RuntimeError(
            "El número de vectores FAISS "
            "no coincide con el número "
            "de embeddings."
        )

    return index


def main():

    load_dotenv()

    deployment_name = os.getenv(
        "AZURE_EMBEDDING_DEPLOYMENT"
    )

    if not deployment_name:

        raise ValueError(
            "No se ha definido "
            "AZURE_EMBEDDING_DEPLOYMENT."
        )

    print(
        "\n=== BUILD KNOWLEDGE INDEX ===\n"
    )

    chunks = load_chunks()

    registry = load_registry()

    pending_documents = [
        document
        for document
        in registry["documents"]
        if (
            document["status"]
            == "pending_index"
        )
    ]

    print(
        f"Chunks encontrados: {len(chunks)}"
    )

    print(
        "Documentos pendientes: "
        f"{len(pending_documents)}"
    )

    if not pending_documents:

        print()
        print(
            "No hay documentos pendientes "
            "de indexación."
        )

        return

    for document in pending_documents:

        print(
            f"- {document['file_name']}"
        )

    INDEXES_FOLDER.mkdir(
        parents=True,
        exist_ok=True
    )

    (
        cached_chunk_ids,
        cached_embeddings
    ) = load_embedding_cache(
        deployment_name
    )

    print()
    print(
        "Embeddings disponibles "
        "en caché: "
        f"{len(cached_chunk_ids)}"
    )

    client = create_openai_client()

    print()
    print(
        "Resolviendo embeddings..."
    )

    (
        embeddings_np,
        reused_count,
        generated_count
    ) = resolve_embeddings(
        chunks,
        cached_chunk_ids,
        cached_embeddings,
        lambda content: create_embedding(
            client,
            deployment_name,
            content
        )
    )

    index = build_faiss_index(
        embeddings_np
    )

    faiss.write_index(
        index,
        str(INDEX_FILE)
    )

    save_embedding_cache(
        chunks,
        embeddings_np,
        deployment_name
    )

    if index.ntotal!= len(chunks):

        raise RuntimeError(
            "El número de vectores FAISS "
            "no coincide con el número "
            "de chunks."
        )

    print()
    print(
        "Índice FAISS guardado."
    )

    print(
        "Caché de embeddings guardada."
    )

    print(
        f"Vectores reutilizados: "
        f"{reused_count}"
    )

    print(
        f"Vectores generados: "
        f"{generated_count}"
    )

    print(
        f"Vectores totales: "
        f"{index.ntotal}"
    )

    for document in pending_documents:

        result = mark_document_indexed(
            registry,
            document["file_name"]
        )

        if not result:

            raise RuntimeError(
                "No se pudo actualizar "
                "el estado del documento: "
                f"{document['file_name']}"
            )

    save_registry(
        registry
    )

    print()
    print(
        "Documentos marcados como active:"
    )

    for document in pending_documents:

        print(
            f"- {document['file_name']}"
        )

    print()
    print(
        "Indexación incremental "
        "completada correctamente."
    )


if __name__ == "__main__":

    main()
