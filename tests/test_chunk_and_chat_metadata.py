import unittest

from models.chunk import Chunk
from index_documents_v2 import build_chunk_records
from knowledge_chat import (
    enrich_chunks_with_registry_metadata,
    format_candidate_block,
    format_context_block,
    format_source_citation,
)


SAMPLE_METADATA = {
    "source_authority": "microsoft_program",
    "program": "DSEW",
    "document_role": "Master Guide",
    "canonical_status": "canonical",
    "version": "v8.5",
}


class ChunkAndChatMetadataTests(unittest.TestCase):
    def test_build_chunk_records_includes_document_metadata(self):
        registry_document = {
            "file_name": "DS-00-MasterDeliveryGuide - v8.5.docx",
            "file_path": "documents/DS-00-MasterDeliveryGuide - v8.5.docx",
            "file_hash": "abc123",
            "metadata": dict(SAMPLE_METADATA),
        }

        chunks = [
            Chunk(
                document_name="documents/DS-00-MasterDeliveryGuide - v8.5.docx",
                document_type="docx",
                chunk_number=1,
                content="Contenido del chunk 1",
            )
        ]

        records = build_chunk_records(
            registry_document,
            chunks,
        )

        self.assertEqual(len(records), 1)
        self.assertEqual(
            records[0]["metadata"],
            SAMPLE_METADATA,
        )
        self.assertIsNot(
            records[0]["metadata"],
            registry_document["metadata"],
        )

    def test_build_chunk_records_handles_none_metadata(self):
        registry_document = {
            "file_name": "unclassified.docx",
            "file_path": "documents/unclassified.docx",
            "file_hash": "def456",
            "metadata": None,
        }

        chunks = [
            Chunk(
                document_name="documents/unclassified.docx",
                document_type="docx",
                chunk_number=1,
                content="Texto sin clasificar",
            )
        ]

        records = build_chunk_records(
            registry_document,
            chunks,
        )

        self.assertIsNone(records[0]["metadata"])

    def test_enrich_chunks_fills_missing_metadata_from_registry(self):
        chunks = [
            {
                "document_name": "documents/DS-00-MasterDeliveryGuide - v8.5.docx",
                "chunk_number": 1,
                "content": "Texto",
            },
            {
                "document_name": "documents/unknown.docx",
                "chunk_number": 1,
                "content": "Otro texto",
            },
        ]

        registry_data = {
            "documents": [
                {
                    "file_name": "DS-00-MasterDeliveryGuide - v8.5.docx",
                    "file_path": "documents/DS-00-MasterDeliveryGuide - v8.5.docx",
                    "metadata": dict(SAMPLE_METADATA),
                }
            ]
        }

        enrich_chunks_with_registry_metadata(
            chunks,
            registry_data,
        )

        self.assertEqual(
            chunks[0]["metadata"],
            SAMPLE_METADATA,
        )
        self.assertIsNone(chunks[1]["metadata"])

    def test_formatting_includes_metadata_and_citations(self):
        chunk = {
            "document_name": "documents/DS-00-MasterDeliveryGuide - v8.5.docx",
            "chunk_number": 2,
            "content": "Guía maestra de Data Security.",
            "metadata": dict(SAMPLE_METADATA),
        }

        candidate_block = format_candidate_block(1, chunk)
        context_block = format_context_block(chunk)
        citation = format_source_citation(chunk)

        self.assertIn("Program: DSEW", candidate_block)
        self.assertIn("Role: Master Guide", candidate_block)
        self.assertIn("Status: canonical", context_block)
        self.assertIn(
            "[DSEW | Master Guide | canonical | microsoft_program]",
            citation,
        )


if __name__ == "__main__":
    unittest.main()
