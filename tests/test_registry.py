import tempfile
import unittest
from pathlib import Path
import registry

class RegistryTests(unittest.TestCase):
	def test_load_missing_registry_returns_empty_registry(self):
		with tempfile.TemporaryDirectory() as temp_dir:
			original_file = registry.REGISTRY_FILE
			registry.REGISTRY_FILE = str(Path(temp_dir) / "registry.json")
			try:
				result = registry.load_registry()
			finally:
				registry.REGISTRY_FILE = original_file

			self.assertEqual(result["registry_version"], "1.0")
			self.assertIsNone(result["last_update"])
			self.assertEqual(result["documents"], [])

if __name__ == "__main__":
	unittest.main()
