import json
import hashlib

from pathlib import Path
from datetime import datetime, UTC


REGISTRY_FILE = "manifests/registry.json"


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

        return json.load(f)


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

        "indexed_at": None
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
    document["detected_at"] = detected_at

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