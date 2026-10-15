from pathlib import Path

from registry import (
    load_registry,
    save_registry,
    compute_file_hash,
    register_document,
    document_status,
    update_document
)


DOCUMENTS_FOLDER = Path("documents")

SUPPORTED_EXTENSIONS = {
    ".pdf",
    ".docx",
    ".pptx"
}


registry = load_registry()

new_count = 0
existing_count = 0
updated_count = 0


print("\n=== BUILD REGISTRY ===\n")


for file in DOCUMENTS_FOLDER.iterdir():

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
        file_hash
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
            file_hash=file_hash
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
            file_hash=file_hash
        )

        updated_count += 1


save_registry(
    registry
)


print("\n=== RESUMEN ===\n")

print(
    f"Nuevos: {new_count}"
)

print(
    f"Sin cambios: {existing_count}"
)

print(
    f"Actualizados: {updated_count}"
)

print(
    f"Total en registry: "
    f"{len(registry['documents'])}"
)