import json
import hashlib

from pathlib import Path
from datetime import datetime, UTC


REGISTRY_FILE = "manifests/registry.json"


REQUIRED_METADATA_FIELDS = (
    "source_authority",
    "program",
    "document_role",
    "canonical_status",
)


ALLOWED_METADATA_VALUES = {
    "source_authority": {
        "microsoft_program",
        "microsoft_product",
        "seidor_adaptation",
        "internal_working",
    },
    "program": {
        "Frontier Accelerate",
        "Zero Trust",
        "DSEW",
        "CSEW",
        "MSOEW",
        "TPEW",
        "Incentives",
    },
    "document_role": {
        "Engagement Guide",
        "Master Guide",
        "Module Guide",
        "Deck",
        "FAQ",
        "Workbook",
        "Template",
        "Changelog",
    },
    "canonical_status": {
        "canonical",
        "subordinate",
        "derived",
        "sample",
        "legacy",
        "pending-validation",
    },
}


def load_registry():

    registry_path = Path(
        REGISTRY_FILE
    )

    if not registry_path.exists():

        return {
            "registry_version": "1.0",
            "last_update": None,
            "documents": []
        }

    with open(
        registry_path,
        "r",
        encoding="utf-8"
    ) as f:

        registry = json.load(f)

    # Compatibilidad con documentos registrados
    # antes de incorporar los metadatos.
    for document in registry.get(
        "documents",
        []
    ):
        document.setdefault(
            "metadata",
            None
        )

    return registry


def save_registry(
    registry
):

    with open(
        REGISTRY_FILE,
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            registry,
            f,
            ensure_ascii=False,
            indent=2
        )


def compute_file_hash(
    file_path
):

    sha256 = hashlib.sha256()

    with open(
        file_path,
        "rb"
    ) as f:

        for block in iter(
            lambda: f.read(4096),
            b""
        ):
            sha256.update(block)

    return sha256.hexdigest()


def get_document(
    registry,
    file_name
):

    for document in registry["documents"]:

        if (
            document["file_name"]
            == file_name
        ):
            return document

    return None


def validate_document_metadata(
    metadata
):

    if not isinstance(
        metadata,
        dict
    ):
        raise ValueError(
            "metadata must be a dictionary"
        )

    for field in REQUIRED_METADATA_FIELDS:

        if (
            field not in metadata
            or metadata[field] is None
            or metadata[field] == ""
        ):
            raise ValueError(
                "Missing required metadata "
                f"field: {field}"
            )

        allowed_values = (
            ALLOWED_METADATA_VALUES[field]
        )

        if (
            metadata[field]
            not in allowed_values
        ):
            raise ValueError(
                "Invalid value for metadata "
                f"field {field}: "
                f"{metadata[field]!r}"
            )

    return True


def set_document_metadata(
    registry,
    file_name,
    metadata
):

    document = get_document(
        registry,
        file_name
    )

    if document is None:
        return False

    validate_document_metadata(
        metadata
    )

    # Se almacena una copia para evitar que
    # cambios externos modifiquen el Registry.
    document["metadata"] = dict(
        metadata
    )

    return True


def register_document(
    registry,
    file_name,
    file_path,
    file_type,
    file_hash
):

    detected_at = (
        datetime.now(UTC).isoformat()
    )

    document = {

        "file_name": file_name,

        "file_path": file_path,

        "file_type": file_type,

        "file_hash": file_hash,

        "size_bytes":
            Path(file_path).stat().st_size,

        "last_modified":
            datetime.fromtimestamp(
                Path(file_path).stat().st_mtime
            ).isoformat(),

        "status": "pending_index",

        "detected_at": detected_at,

        "indexed_at": None,

        "metadata": None
    }

    registry["documents"].append(
        document
    )

    registry["last_update"] = detected_at

    return True


def document_exists(
    registry,
    file_hash
):

    for document in registry["documents"]:

        if (
            document["file_hash"]
            == file_hash
        ):
            return True

    return False


def document_status(
    registry,
    file_name,
    file_hash
):

    document = get_document(
        registry,
        file_name
    )

    if document is None:
        return "new"

    if (
        document["file_hash"]
        == file_hash
    ):
        return "existing"

    return "updated"


def update_document(
    registry,
    file_name,
    file_path,
    file_type,
    file_hash
):

    document = get_document(
        registry,
        file_name
    )

    if document is None:
        return False

    detected_at = (
        datetime.now(UTC).isoformat()
    )

    document["file_path"] = file_path
    document["file_type"] = file_type
    document["file_hash"] = file_hash

    document["size_bytes"] = (
        Path(file_path).stat().st_size
    )

    document["last_modified"] = (
        datetime.fromtimestamp(
            Path(file_path).stat().st_mtime
        ).isoformat()
    )

    document["status"] = "pending_index"
    document["indexed_at"] = None
    document["detected_at"] = detected_at

    # Los documentos antiguos pueden no
    # disponer todavía de esta propiedad.
    document.setdefault(
        "metadata",
        None
    )

    registry["last_update"] = detected_at

    return True


def mark_document_indexed(
    registry,
    file_name
):

    document = get_document(
        registry,
        file_name
    )

    if document is None:
        return False

    indexed_at = (
        datetime.now(UTC).isoformat()
    )

    document["status"] = "active"
    document["indexed_at"] = indexed_at

    registry["last_update"] = indexed_at

    return True