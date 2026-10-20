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

    def test_data_security_module_is_subordinate(self):
        file_name = (
            "DS-01-Module Delivery Guide-Exchange "
            "- v8.5.1.docx"
        )

        metadata = (
            classify_corpus
            .CORPUS_METADATA[file_name]
        )

        self.assertEqual(
            metadata["source_authority"],
            "microsoft_program",
        )

        self.assertEqual(
            metadata["program"],
            "DSEW",
        )

        self.assertEqual(
            metadata["document_role"],
            "Module Guide",
        )

        self.assertEqual(
            metadata["canonical_status"],
            "subordinate",
        )

    def test_simulation_template_is_sample(self):
        file_name = (
            "DS-64-Employee Resignations "
            "Simulation Template - v8.5.xlsx"
        )

        metadata = (
            classify_corpus
            .CORPUS_METADATA[file_name]
        )

        self.assertEqual(
            metadata["document_role"],
            "Template",
        )

        self.assertEqual(
            metadata["canonical_status"],
            "sample",
        )

    def test_design_decision_points_is_workbook(self):
        file_name = (
            "10 - Threat Protection "
            "Envisioning Workshop "
            "- Design Decision Points.xlsx"
        )

        metadata = (
            classify_corpus
            .CORPUS_METADATA[file_name]
        )

        self.assertEqual(
            metadata["program"],
            "TPEW",
        )

        self.assertEqual(
            metadata["document_role"],
            "Workbook",
        )

        self.assertEqual(
            metadata["canonical_status"],
            "subordinate",
        )

    def test_seidor_document_is_derived(self):
        file_name = (
            "EL CAMBIO REAL (FY26 → FY27).docx"
        )

        metadata = (
            classify_corpus
            .CORPUS_METADATA[file_name]
        )

        self.assertEqual(
            metadata["source_authority"],
            "seidor_adaptation",
        )

        self.assertEqual(
            metadata["canonical_status"],
            "derived",
        )

    def test_second_batch_preserves_technical_status(self):
        file_name = (
            "DS-40-Pre-Engagement "
            "and Kickoff deck - v8.5.pptx"
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
            .apply_catalog_to_registry(data)
        )

        self.assertEqual(
            summary["assigned"],
            [file_name],
        )

        self.assertEqual(
            data["documents"][0]["status"],
            "active",
        )

        self.assertEqual(
            data["documents"][0]["indexed_at"],
            "2026-10-20T08:00:00+00:00",
        )


if __name__ == "__main__":
    unittest.main()