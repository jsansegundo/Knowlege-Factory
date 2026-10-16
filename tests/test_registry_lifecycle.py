import tempfile
import unittest
from pathlib import Path

import registry


class RegistryLifecycleTests(unittest.TestCase):
	def test_document_lifecycle(self):
		with tempfile.TemporaryDirectory() as temp_dir:
			file_path = Path(temp_dir) / "sample.docx"
			file_path.write_text("version 1", encoding="utf-8")
			data = {"registry_version": "1.0", "last_update": None, "documents": []}
			first_hash = registry.compute_file_hash(file_path)

			self.assertEqual(registry.document_status(data, file_path.name, first_hash), "new")
			self.assertTrue(registry.register_document(data, file_path.name, str(file_path), ".docx", first_hash))
			self.assertEqual(registry.document_status(data, file_path.name, first_hash), "existing")
			self.assertEqual(data["documents"][0]["status"], "pending_index")

			file_path.write_text("version 2", encoding="utf-8")
			updated_hash = registry.compute_file_hash(file_path)
			self.assertEqual(registry.document_status(data, file_path.name, updated_hash), "updated")
			self.assertTrue(registry.update_document(data, file_path.name, str(file_path), ".docx", updated_hash))
			self.assertEqual(data["documents"][0]["status"], "pending_index")

			self.assertTrue(registry.mark_document_indexed(data, file_path.name))
			self.assertEqual(data["documents"][0]["status"], "active")
			self.assertIsNotNone(data["documents"][0]["indexed_at"])
