import tempfile
import unittest
from pathlib import Path

from openpyxl import Workbook

from loaders.loader_factory import extract_text


class XlsxLoaderTests(unittest.TestCase):
    def test_extracts_non_empty_cells_per_sheet(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            file_path = Path(temp_dir) / "sample.xlsx"

            workbook = Workbook()
            first = workbook.active
            first.title = "Resumen"
            first.append(["Cliente", None, "Contoso"])
            first.append([None, None, None])
            first.append(["Fase", 2])

            second = workbook.create_sheet("Datos")
            second.append(["Riesgo", "Alto"])
            workbook.save(file_path)

            document = extract_text(str(file_path))

            self.assertEqual(document.source_type, "xlsx")
            self.assertEqual(
                document.content,
                "[Hoja: Resumen]\nCliente | Contoso\nFase | 2\n\n"
                "[Hoja: Datos]\nRiesgo | Alto",
            )


if __name__ == "__main__":
    unittest.main()
