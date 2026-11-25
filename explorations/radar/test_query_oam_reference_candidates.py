import unittest
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from shapely.geometry import box, mapping
from query_oam_reference_candidates import audit, validate_asset_href


class OAMReferenceAuditTests(unittest.TestCase):
    def test_https_asset_only(self):
        self.assertTrue(validate_asset_href("https://example.org/image.tif"))
        self.assertFalse(validate_asset_href("http://example.org/image.tif"))
        self.assertFalse(validate_asset_href("file:///tmp/image.tif"))

    def test_intersection_fraction_screen(self):
        item = {
            "id": "inside",
            "geometry": mapping(box(36.7, -1.4, 36.8, -1.3)),
            "properties": {"datetime": "2026-10-13T10:00:00Z", "gsd": 0.04},
            "assets": {"visual": {"href": "https://example.org/a.tif"}},
            "license": "CC-BY-4.0",
        }
        row = audit([item])[0]
        self.assertGreater(row["r130_bbox_intersection_fraction"], 0)
        self.assertEqual(row["license"], "CC-BY-4.0")
        self.assertEqual(row["https_asset_hrefs_available"], 1)

    def test_missing_geometry_is_not_overlap(self):
        row = audit([{"id": "unknown", "properties": {}, "assets": {}}])[0]
        self.assertIsNone(row["r130_bbox_intersection_fraction"])
        self.assertFalse(row["geometry_present"])


if __name__ == "__main__":
    unittest.main()
