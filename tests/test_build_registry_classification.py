import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from build_registry import process_documents


KNOWN_FILE = "incentives.pdf"
UNKNOWN_FILE = "unknown.pdf"

KNOWN_METADATA = {
    "source_authority": "microsoft_program",
    "program": "Incentives",
    "document_role": "Engagement Guide",
    "canonical_status": "canonical",
}


def empty_registry():
    return {
        "documents": {},
    }


def register_document_side_effect(
    registry,
    file_name,
    file_path,
    file_type,
    file_hash,
):
    registry["documents"][file_name] = {
        "file_name": file_name,
        "file_path": file_path,
        "file_type": file_type,
        "file_hash": file_hash,
        "status": "pending_index",
        "indexed_at": None,
        "metadata": None,
    }


def update_document_side_effect(
    registry,
    file_name,
    file_path,
    file_type,
    file_hash,
):
    document = registry["documents"][file_name]

    document["file_path"] = file_path
    document["file_type"] = file_type
    document["file_hash"] = file_hash
    document["status"] = "pending_index"


def classify_known_document(registry):
    assigned = []
    unchanged = []
    unmatched = []

    for file_name, document in registry["documents"].items():
        if file_name == KNOWN_FILE:
            if document.get("metadata") == KNOWN_METADATA:
                unchanged.append(file_name)
            else:
                document["metadata"] = dict(
                    KNOWN_METADATA
                )
                assigned.append(file_name)
        else:
            unmatched.append(file_name)

    return {
        "assigned": assigned,
        "unchanged": unchanged,
        "unmatched": unmatched,
        "catalog_not_registered": [],
    }


class BuildRegistryClassificationTests(
    unittest.TestCase
):
    def create_document(
        self,
        folder,
        file_name,
        content=b"document-content",
    ):
        file_path = folder / file_name
        file_path.write_bytes(content)
        return file_path

    @patch(
        "build_registry.apply_catalog_to_registry",
        side_effect=classify_known_document,
    )
    @patch(
        "build_registry.register_document",
        side_effect=register_document_side_effect,
    )
    @patch(
        "build_registry.document_status",
        return_value="new",
    )
    @patch(
        "build_registry.compute_file_hash",
        return_value="new-hash",
    )
    def test_new_known_document_receives_metadata(
        self,
        mock_compute_hash,
        mock_document_status,
        mock_register_document,
        mock_apply_catalog,
    ):
        registry = empty_registry()

        with tempfile.TemporaryDirectory() as temp_dir:
            documents_folder = Path(temp_dir)

            self.create_document(
                documents_folder,
                KNOWN_FILE,
            )

            build_summary, classification_summary = (
                process_documents(
                    registry=registry,
                    documents_folder=documents_folder,
                )
            )

        document = registry["documents"][KNOWN_FILE]

        self.assertEqual(
            KNOWN_METADATA,
            document["metadata"],
        )

        self.assertEqual(
            "pending_index",
            document["status"],
        )

        self.assertIsNone(
            document["indexed_at"]
        )

        self.assertEqual(
            1,
            build_summary["new"],
        )

        self.assertEqual(
            [KNOWN_FILE],
            classification_summary["assigned"],
        )

        mock_apply_catalog.assert_called_once_with(
            registry
        )

    @patch(
        "build_registry.apply_catalog_to_registry",
        side_effect=classify_known_document,
    )
    @patch(
        "build_registry.register_document",
        side_effect=register_document_side_effect,
    )
    @patch(
        "build_registry.document_status",
        return_value="new",
    )
    @patch(
        "build_registry.compute_file_hash",
        return_value="unknown-hash",
    )
    def test_unknown_document_remains_unclassified(
        self,
        mock_compute_hash,
        mock_document_status,
        mock_register_document,
        mock_apply_catalog,
    ):
        registry = empty_registry()

        with tempfile.TemporaryDirectory() as temp_dir:
            documents_folder = Path(temp_dir)

            self.create_document(
                documents_folder,
                UNKNOWN_FILE,
            )

            _, classification_summary = (
                process_documents(
                    registry=registry,
                    documents_folder=documents_folder,
                )
            )

        document = registry["documents"][UNKNOWN_FILE]

        self.assertIsNone(
            document["metadata"]
        )

        self.assertEqual(
            "pending_index",
            document["status"],
        )

        self.assertEqual(
            [UNKNOWN_FILE],
            classification_summary["unmatched"],
        )

    @patch(
        "build_registry.apply_catalog_to_registry",
        side_effect=classify_known_document,
    )
    @patch(
        "build_registry.update_document",
        side_effect=update_document_side_effect,
    )
    @patch(
        "build_registry.document_status",
        return_value="updated",
    )
    @patch(
        "build_registry.compute_file_hash",
        return_value="updated-hash",
    )
    def test_updated_known_document_is_reclassified(
        self,
        mock_compute_hash,
        mock_document_status,
        mock_update_document,
        mock_apply_catalog,
    ):
        registry = {
            "documents": {
                KNOWN_FILE: {
                    "file_name": KNOWN_FILE,
                    "file_path": "old-path",
                    "file_type": ".pdf",
                    "file_hash": "old-hash",
                    "status": "active",
                    "indexed_at": "2026-10-19T10:00:00Z",
                    "metadata": {
                        "source_authority": "internal_working",
                        "program": "Incentives",
                        "document_role": "Template",
                        "canonical_status": "pending-validation",
                    },
                },
            },
        }

        with tempfile.TemporaryDirectory() as temp_dir:
            documents_folder = Path(temp_dir)

            self.create_document(
                documents_folder,
                KNOWN_FILE,
                content=b"updated-content",
            )

            build_summary, classification_summary = (
                process_documents(
                    registry=registry,
                    documents_folder=documents_folder,
                )
            )

        document = registry["documents"][KNOWN_FILE]

        self.assertEqual(
            "updated-hash",
            document["file_hash"],
        )

        self.assertEqual(
            "pending_index",
            document["status"],
        )

        self.assertEqual(
            "2026-10-19T10:00:00Z",
            document["indexed_at"],
        )

        self.assertEqual(
            KNOWN_METADATA,
            document["metadata"],
        )

        self.assertEqual(
            1,
            build_summary["updated"],
        )

        self.assertEqual(
            [KNOWN_FILE],
            classification_summary["assigned"],
        )

    @patch(
        "build_registry.apply_catalog_to_registry",
        side_effect=classify_known_document,
    )
    @patch(
        "build_registry.update_document",
    )
    @patch(
        "build_registry.register_document",
    )
    @patch(
        "build_registry.document_status",
        return_value="existing",
    )
    @patch(
        "build_registry.compute_file_hash",
        return_value="stable-hash",
    )
    def test_second_execution_is_idempotent(
        self,
        mock_compute_hash,
        mock_document_status,
        mock_register_document,
        mock_update_document,
        mock_apply_catalog,
    ):
        registry = {
            "documents": {
                KNOWN_FILE: {
                    "file_name": KNOWN_FILE,
                    "file_path": "documents/incentives.pdf",
                    "file_type": ".pdf",
                    "file_hash": "stable-hash",
                    "status": "active",
                    "indexed_at": "2026-10-19T10:00:00Z",
                    "metadata": dict(
                        KNOWN_METADATA
                    ),
                },
            },
        }

        with tempfile.TemporaryDirectory() as temp_dir:
            documents_folder = Path(temp_dir)

            self.create_document(
                documents_folder,
                KNOWN_FILE,
            )

            build_summary, classification_summary = (
                process_documents(
                    registry=registry,
                    documents_folder=documents_folder,
                )
            )

        mock_register_document.assert_not_called()
        mock_update_document.assert_not_called()

        self.assertEqual(
            1,
            build_summary["existing"],
        )

        self.assertEqual(
            [],
            classification_summary["assigned"],
        )

        self.assertEqual(
            [KNOWN_FILE],
            classification_summary["unchanged"],
        )

        document = registry["documents"][KNOWN_FILE]

        self.assertEqual(
            "active",
            document["status"],
        )

        self.assertEqual(
            "2026-10-19T10:00:00Z",
            document["indexed_at"],
        )

    @patch(
        "build_registry.apply_catalog_to_registry",
    )
    @patch(
        "build_registry.document_status",
        return_value="unexpected-status",
    )
    @patch(
        "build_registry.compute_file_hash",
        return_value="hash",
    )
    def test_unknown_technical_status_raises_error(
        self,
        mock_compute_hash,
        mock_document_status,
        mock_apply_catalog,
    ):
        registry = empty_registry()

        with tempfile.TemporaryDirectory() as temp_dir:
            documents_folder = Path(temp_dir)

            self.create_document(
                documents_folder,
                UNKNOWN_FILE,
            )

            with self.assertRaisesRegex(
                ValueError,
                "Estado documental no reconocido",
            ):
                process_documents(
                    registry=registry,
                    documents_folder=documents_folder,
                )

        mock_apply_catalog.assert_not_called()


if __name__ == "__main__":
    unittest.main()