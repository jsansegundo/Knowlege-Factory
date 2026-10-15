from pathlib import Path
import json

from loaders.loader_factory import extract_text
from chunker import chunk_document
from registry import load_registry


ALL_CHUNKS_FILE = Path(
    "manifests/all_chunks.json"
)

MANIFEST_FILE = Path(
    "manifests/manifest.json"
)

SUPPORTED_EXTENSIONS = {
    ".pdf",
    ".docx",
    ".pptx"
}


def load_json_file(
    file_path,
    default_value
):

    if not file_path.exists():
        return default_value

    with open(
        file_path,
        "r",
        encoding="utf-8"
    ) as f:

        return json.load(f)


registry = load_registry()

pending_documents = [
    document
    for document in registry["documents"]
    if document["status"] == "pending_index"
]


print("\n=== INDEX DOCUMENTS V2 ===\n")


if not pending_documents:

    print(
        "No hay documentos pendientes."
    )

else:

    print(
        "Documentos pendientes: "
        f"{len(pending_documents)}"
    )

    for document in pending_documents:

        print(
            f"- {document['file_name']}"
        )


    existing_chunks = load_json_file(
        ALL_CHUNKS_FILE,
        []
    )

    existing_manifest = load_json_file(
        MANIFEST_FILE,
        []
    )


    pending_file_names = {
        document["file_name"]
        for document in pending_documents
    }

    pending_file_paths = {
        document["file_path"]
        for document in pending_documents
    }


    preserved_chunks = []

    for chunk in existing_chunks:

        document_name = chunk.get(
            "document_name",
            ""
        )

        document_basename = Path(
            document_name
        ).name

        if (
            document_name in pending_file_paths
            or
            document_basename in pending_file_names
        ):
            continue

        preserved_chunks.append(
            chunk
        )


    preserved_manifest = []

    for item in existing_manifest:

        manifest_file = item.get(
            "file",
            ""
        )

        manifest_basename = Path(
            manifest_file
        ).name

        if (
            manifest_file in pending_file_paths
            or
            manifest_basename in pending_file_names
        ):
            continue

        preserved_manifest.append(
            item
        )


    new_chunks = []

    new_manifest_entries = []


    for registry_document in pending_documents:

        file_path = Path(
            registry_document["file_path"]
        )

        if not file_path.exists():

            raise FileNotFoundError(
                "No se encuentra el documento: "
                f"{file_path}"
            )

        if (
            file_path.suffix.lower()
            not in SUPPORTED_EXTENSIONS
        ):

            raise ValueError(
                "Formato no soportado: "
                f"{file_path.name}"
            )


        print()
        print(
            f"Procesando: {file_path.name}"
        )


        document = extract_text(
            str(file_path)
        )

        chunks = chunk_document(
            document
        )


        new_manifest_entries.append(
            {
                "file": file_path.name,
                "type": document.source_type,
                "characters": len(
                    document.content
                ),
                "chunks": len(chunks)
            }
        )


        for chunk in chunks:

            new_chunks.append(
                {
                    "document_name":
                        chunk.document_name,

                    "document_type":
                        chunk.document_type,

                    "document_hash":
                        registry_document[
                            "file_hash"
                        ],

                    "chunk_number":
                        chunk.chunk_number,

                    "chunk_id":
                        (
                            f"{registry_document['file_hash']}:"
                            f"{chunk.chunk_number}"
                        ),

                    "content":
                        chunk.content
                }
            )


        print(
            f"Chunks generados: {len(chunks)}"
        )


    final_chunks = (
        preserved_chunks
        + new_chunks
    )

    final_manifest = (
        preserved_manifest
        + new_manifest_entries
    )


    with open(
        ALL_CHUNKS_FILE,
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            final_chunks,
            f,
            ensure_ascii=False,
            indent=2
        )


    with open(
        MANIFEST_FILE,
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            final_manifest,
            f,
            ensure_ascii=False,
            indent=2
        )


    print()
    print(
        "Chunks conservados: "
        f"{len(preserved_chunks)}"
    )

    print(
        "Chunks nuevos: "
        f"{len(new_chunks)}"
    )

    print(
        "Chunks totales: "
        f"{len(final_chunks)}"
    )

    print()
    print(
        "all_chunks.json actualizado"
    )

    print(
        "manifest.json actualizado"
    )

    print()
    print(
        "Estado del Registry sin cambios: "
        "los documentos continúan "
        "como pending_index."
    )