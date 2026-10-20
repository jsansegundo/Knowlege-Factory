from pathlib import Path

from classify_corpus import apply_catalog_to_registry
from registry import (
    load_registry,
    save_registry,
    compute_file_hash,
    register_document,
    document_status,
    update_document,
)


DOCUMENTS_FOLDER = Path("documents")

SUPPORTED_EXTENSIONS = {
    ".pdf",
    ".docx",
    ".pptx",
}


def process_documents(
    registry,
    documents_folder=DOCUMENTS_FOLDER,
):
    """
    Detecta documentos nuevos, existentes y actualizados.

    Después de procesar su estado técnico, aplica el catálogo
    documental sin alterar el ciclo técnico del Registry.

    No guarda el Registry. El guardado corresponde a main(),
    para que toda la operación se persista una sola vez.
    """

    new_count = 0
    existing_count = 0
    updated_count = 0

    print("\n=== BUILD REGISTRY ===\n")

    for file in sorted(
        documents_folder.iterdir(),
        key=lambda item: item.name.casefold(),
    ):
        if not file.is_file():
            continue

        if file.suffix.lower() not in SUPPORTED_EXTENSIONS:
            print(
                f"Ignorado: {file.name} "
                f"(formato no soportado)"
            )
            continue

        file_hash = compute_file_hash(
            str(file)
        )

        status = document_status(
            registry,
            file.name,
            file_hash,
        )

        if status == "new":
            print(
                f"NUEVO: {file.name}"
            )

            register_document(
                registry=registry,
                file_name=file.name,
                file_path=str(file),
                file_type=file.suffix.lower(),
                file_hash=file_hash,
            )

            new_count += 1

        elif status == "existing":
            print(
                f"SIN CAMBIOS: {file.name}"
            )

            existing_count += 1

        elif status == "updated":
            print(
                f"ACTUALIZADO: {file.name}"
            )

            update_document(
                registry=registry,
                file_name=file.name,
                file_path=str(file),
                file_type=file.suffix.lower(),
                file_hash=file_hash,
            )

            updated_count += 1

        else:
            raise ValueError(
                f"Estado documental no reconocido para "
                f"{file.name}: {status}"
            )

    classification_summary = apply_catalog_to_registry(
        registry
    )

    build_summary = {
        "new": new_count,
        "existing": existing_count,
        "updated": updated_count,
    }

    return build_summary, classification_summary


def print_summary(
    registry,
    build_summary,
    classification_summary,
):
    print("\n=== RESUMEN ===\n")

    print(
        f"Nuevos: {build_summary['new']}"
    )

    print(
        f"Sin cambios: {build_summary['existing']}"
    )

    print(
        f"Actualizados: {build_summary['updated']}"
    )

    print(
        f"Total en registry: "
        f"{len(registry['documents'])}"
    )

    print("\n=== CLASIFICACIÓN DOCUMENTAL ===\n")

    print(
        "Metadatos asignados: "
        f"{len(classification_summary['assigned'])}"
    )

    print(
        "Metadatos sin cambios: "
        f"{len(classification_summary['unchanged'])}"
    )

    print(
        "Documentos sin clasificación: "
        f"{len(classification_summary['unmatched'])}"
    )

    print(
        "Catalogados aún no registrados: "
        f"{len(classification_summary['catalog_not_registered'])}"
    )


def main():
    registry = load_registry()

    build_summary, classification_summary = process_documents(
        registry=registry,
        documents_folder=DOCUMENTS_FOLDER,
    )

    # Guardado único después de completar tanto el ciclo técnico
    # como la clasificación documental.
    save_registry(
        registry
    )

    print_summary(
        registry=registry,
        build_summary=build_summary,
        classification_summary=classification_summary,
    )


if __name__ == "__main__":
    main()