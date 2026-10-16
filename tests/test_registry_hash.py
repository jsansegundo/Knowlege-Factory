import tempfile
import unittest
from pathlib import Path

import registry


class RegistryHashTests(unittest.TestCase):
	def test_hash_is_stable_and_changes_with_content(self):
		with tempfile.TemporaryDirectory() as temp_dir:
			file_path = Path(temp_dir) / "document.txt"
			file_path.write_text("version 1", encoding="utf-8")
			first_hash = registry.compute_file_hash(file_path)
			second_hash = registry.compute_file_hash(file_path)
			self.assertEqual(first_hash, second_hash)

			file_path.write_text("version 2", encoding="utf-8")
			updated_hash = registry.compute_file_hash(file_path)
			self.assertNotEqual(first_hash, updated_hash)


if __name__ == "__main__":
	unittest.main()
