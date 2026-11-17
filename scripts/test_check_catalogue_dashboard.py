import unittest

from check_catalogue_dashboard import cells, dashboard_rows, source_entry_counts


class CatalogueDashboardTests(unittest.TestCase):
    def test_cells_respects_escaped_pipes(self):
        self.assertEqual(cells(r"| A | B\|C |"), ["A", "B|C"])

    def test_source_entry_counts_classifies_all_non_intake_rows_as_partial(self):
        markdown = """| Source entry | Kind | Page | Verification status |
|---|---|---:|---|
| A | Algorithm | 1 | Partial — record exists |
| B | Model | 2 | Not checked — intake only |
| C | Method | 3 | Tested implementation linked |
| D | Model | 4 | Fully verified |
| E | Model | 5 | [Canonical record](record.md) |

| Other inventory | Kind | Page | Not counted |
"""
        self.assertEqual(source_entry_counts(markdown), (5, 3, 1, 1))

    def test_missing_source_table_rejected(self):
        with self.assertRaises(ValueError):
            source_entry_counts("| Name | Status |\n|---|---|")

    def test_empty_status_rejected(self):
        markdown = """| Source entry | Kind | Page | Verification status |
|---|---|---:|---|
| A | Algorithm | 1 | |
"""
        with self.assertRaises(ValueError):
            source_entry_counts(markdown)

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
