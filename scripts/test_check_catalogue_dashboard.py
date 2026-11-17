import unittest

from check_catalogue_dashboard import cells, dashboard_rows


class CatalogueDashboardTests(unittest.TestCase):
    def test_cells(self):
        self.assertEqual(cells("| A | B |"), ["A", "B"])

    def test_dashboard_rows(self):
        markdown = """| Section | Source entries | Partial | Intake only |
|---:|---:|---:|---:|
| 1 — Core GIS | 3 | 2 | 1 |
| 2 — Statistics | 4 | 1 | 3 |
| **Total** | **7** | **3** | **4** |
"""
        self.assertEqual(
            dashboard_rows(markdown),
            {1: (3, 2, 1), 2: (4, 1, 3)},
        )

    def test_duplicate_section_rejected(self):
        markdown = """| Section | Source entries | Partial | Intake only |
|---:|---:|---:|---:|
| 1 — Core GIS | 3 | 2 | 1 |
| 1 — Duplicate | 3 | 2 | 1 |
| **Total** | **6** | **4** | **2** |
"""
        with self.assertRaises(ValueError):
            dashboard_rows(markdown)


if __name__ == "__main__":
    unittest.main()
