import unittest

from check_catalogue_dashboard import cells, classify_status, is_separator, source_rows


class CatalogueDashboardParserTests(unittest.TestCase):
    def test_cells(self):
        self.assertEqual(cells("| A | B |"), ["A", "B"])

    def test_separator(self):
        self.assertTrue(is_separator("|---|:---:|---:|"))
        self.assertFalse(is_separator("| data | row |"))

    def test_only_source_entry_tables_are_counted(self):
        markdown = """| Source entry | Provisional kind | Source page | Verification status |
|---|---|---:|---|
| Moran's I | statistic | 1 | Partial — related record exists |
| Another item | method | 1 | Not checked — intake only |

| Area | Tool | Page |
|---|---|---:|
| Raster | GDAL | 2 |
"""
        self.assertEqual(len(source_rows(markdown)), 2)

    def test_status_classification(self):
        self.assertEqual(
            classify_status("| A | kind | 1 | Partial — related record exists |", "fixture"),
            "partial",
        )
        self.assertEqual(
            classify_status("| B | kind | 1 | Not checked — intake only |", "fixture"),
            "intake",
        )

    def test_unknown_status_is_rejected(self):
        with self.assertRaises(ValueError):
            classify_status("| C | kind | 1 | Captured |", "fixture")


if __name__ == "__main__":
    unittest.main()
