import unittest

import classify_corpus
import registry


class CorpusClassificationTests(
    unittest.TestCase
):
    def test_all_catalog_metadata_is_valid(
        self
    ):
        for (
            file_name,
            metadata,
        ) in (
            classify_corpus
            .CORPUS_METADATA
            .items()
        ):
            with self.subTest(
                file_name=file_name
            ):
                self.assertTrue(
                    registry
                    .validate_document_metadata(
                        metadata
                    )
                )

    def test_assigns_known_document(
        self
    ):
        file_name = (
            "DS-00-MasterDeliveryGuide "
            "- v8.5.docx"
        )

        data = {
            "registry_version": "1.0",
            "last_update": None,
            "documents": [
                {
                    "file_name": file_name,
                    "status": "active",
                    "indexed_at":
                        "2026-10-20T08:00:00+00:00",
                    "metadata": None,
                }
            ],
        }

        summary = (
            classify_corpus
            .apply_catalog_to_registry(
                data
            )
        )

        document = data["documents"][0]

        self.assertEqual(
            summary["assigned"],
            [file_name],
        )

        self.assertEqual(
            document["metadata"],
            classify_corpus
            .CORPUS_METADATA[file_name],
        )

        self.assertEqual(
            document["status"],
            "active",
        )

        self.assertEqual(
            document["indexed_at"],
            "2026-10-20T08:00:00+00:00",
        )

    def test_unknown_document_is_reported(
        self
    ):
        data = {
            "registry_version": "1.0",
            "last_update": None,
            "documents": [
                {
                    "file_name": "unknown.docx",
                    "status": "active",
                    "metadata": None,
                }
            ],
        }

        summary = (
            classify_corpus
            .apply_catalog_to_registry(
                data
            )
        )

        self.assertEqual(
            summary["assigned"],
            [],
        )

        self.assertEqual(
            summary["unmatched"],
            ["unknown.docx"],
        )

        self.assertIsNone(
            data["documents"][0][
                "metadata"
            ]
        )

    def test_second_application_is_idempotent(
        self
    ):
        file_name = (
            "00 - Cloud Security "
            "Envisioning Workshop "
            "- Delivery Guide.docx"
        )

        metadata = (
            classify_corpus
            .CORPUS_METADATA[file_name]
        )

        data = {
            "registry_version": "1.0",
            "last_update": None,
            "documents": [
                {
                    "file_name": file_name,
                    "status": "active",
                    "metadata": dict(
                        metadata
                    ),
                }
            ],
        }

        summary = (
            classify_corpus
            .apply_catalog_to_registry(
                data
            )
        )

        self.assertEqual(
            summary["assigned"],
            [],
        )

        self.assertEqual(
            summary["unchanged"],
            [file_name],
        )


if __name__ == "__main__":
    unittest.main()