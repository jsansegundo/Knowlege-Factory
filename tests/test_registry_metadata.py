import tempfile
import unittest
from pathlib import Path

import registry


VALID_METADATA = {
    "source_authority": "microsoft_program",
    "program": "Frontier Accelerate",
    "document_role": "Engagement Guide",
    "canonical_status": "canonical",
}


class RegistryMetadataTests(unittest.TestCase):
    def test_valid_metadata_is_accepted(self):
        self.assertTrue(
            registry.validate_document_metadata(VALID_METADATA)
        )

    def test_missing_required_field_is_rejected(self):
        metadata = dict(VALID_METADATA)
        del metadata["source_authority"]

        with self.assertRaisesRegex(
            ValueError,
            "source_authority",
        ):
            registry.validate_document_metadata(metadata)

    def test_invalid_controlled_value_is_rejected(self):
        metadata = dict(VALID_METADATA)
        metadata["canonical_status"] = "unapproved"

        with self.assertRaisesRegex(
            ValueError,
            "canonical_status",
        ):
            registry.validate_document_metadata(metadata)

    def test_metadata_does_not_change_technical_status(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            file_path = Path(temp_dir) / "sample.docx"
            file_path.write_text("content", encoding="utf-8")

            data = {
                "registry_version": "1.0",
                "last_update": None,
                "documents": [],
            }

            file_hash = registry.compute_file_hash(file_path)

            registry.register_document(
                data,
                file_path.name,
                str(file_path),
                ".docx",
                file_hash,
            )

            self.assertEqual(
                data["documents"][0]["status"],
                "pending_index",
            )
            self.assertIsNone(
                data["documents"][0]["metadata"]
            )

            self.assertTrue(
                registry.set_document_metadata(
                    data,
                    file_path.name,
                    VALID_METADATA,
                )
            )

            document = data["documents"][0]

            self.assertEqual(
                document["metadata"],
                VALID_METADATA,
            )
            self.assertEqual(
                document["status"],
                "pending_index",
            )

            registry.mark_document_indexed(
                data,
                file_path.name,
            )

            self.assertEqual(
                document["status"],
                "active",
            )
            self.assertEqual(
                document["metadata"],
                VALID_METADATA,
            )

    def test_unknown_document_returns_false(self):
        data = {
            "registry_version": "1.0",
            "last_update": None,
            "documents": [],
        }

        self.assertFalse(
            registry.set_document_metadata(
                data,
                "missing.docx",
                VALID_METADATA,
            )
        )


if __name__ == "__main__":
    unittest.main()
