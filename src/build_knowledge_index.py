from pathlib import Path
from dotenv import load_dotenv
from openai import OpenAI

import os
import json
import numpy as np
import faiss

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

INDEX_FILE = INDEXES_FOLDER / "knowledge.index"


load_dotenv()


client = OpenAI(
    base_url=os.getenv(
        "AZURE_OPENAI_ENDPOINT"
    ),
    api_key=os.getenv(
        "AZURE_OPENAI_API_KEY"
    )
)


print(
    "\n=== BUILD KNOWLEDGE INDEX ===\n"
)


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


registry = load_registry()


pending_documents = [
    document
    for document in registry["documents"]
    if document["status"] == "pending_index"
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

else:

    for document in pending_documents:

        print(
            f"- {document['file_name']}"
        )


    print()
    print(
        "Generando embeddings..."
    )


    embeddings = []


    for i, chunk in enumerate(
        chunks,
        start=1
    ):

        content = chunk.get(
            "content",
            ""
        ).strip()


        if not content:

            raise ValueError(
                "Se encontró un chunk "
                "sin contenido en la posición "
                f"{i - 1}."
            )


        response = client.embeddings.create(
            model=os.getenv(
                "AZURE_EMBEDDING_DEPLOYMENT"
            ),
            input=content
        )


        embeddings.append(
            response.data[0].embedding
        )


        print(
            f"Embedding {i}/{len(chunks)}"
        )


    embeddings_np = np.array(
        embeddings,
        dtype="float32"
    )


    if embeddings_np.ndim!= 2:

        raise ValueError(
            "Los embeddings no tienen "
            "la estructura esperada."
        )


    vector_dimension = (
        embeddings_np.shape[1]
    )


    index = faiss.IndexFlatL2(
        vector_dimension
    )


    index.add(
        embeddings_np
    )


    if index.ntotal!= len(chunks):

        raise RuntimeError(
            "El número de vectores FAISS "
            "no coincide con el número "
            "de chunks."
        )


    INDEXES_FOLDER.mkdir(
        parents=True,
        exist_ok=True
    )


    faiss.write_index(
        index,
        str(INDEX_FILE)
    )


    print()
    print(
        "Índice FAISS guardado."
    )

    print(
        f"Vectores guardados: {index.ntotal}"
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
        "Indexación completada correctamente."
    )