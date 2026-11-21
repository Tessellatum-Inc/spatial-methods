from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from output_inspection import inspect_outputs


class OutputInspectionTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.project = Path(self.tmp.name) / "project"
        self.project.mkdir()
        (self.project / "odm_orthophoto").mkdir()
        (self.project / "odm_orthophoto" / "orthophoto.tif").write_bytes(b"fake raster")

    def tearDown(self):
        self.tmp.cleanup()

    def test_missing_declared_output_blocks_delivery_review(self):
        report = inspect_outputs(self.project, ["odm_dem/dsm.tif"])
        self.assertEqual(report["status"], "blocked")
        self.assertTrue(report["blockers"])

    def test_rasterio_absence_is_transparent_not_silent(self):
        with patch.dict("sys.modules", {"rasterio": None}):
            report = inspect_outputs(self.project)
        self.assertEqual(report["status"], "review_required")
        self.assertEqual(report["rasters"][0]["status"], "not_inspected")
        self.assertTrue(report["warnings"])

    def test_path_traversal_is_rejected(self):
        with self.assertRaises(ValueError):
            inspect_outputs(self.project, ["../outside.tif"])

    def test_inventory_records_project_relative_files(self):
        report = inspect_outputs(self.project)
        self.assertEqual(report["file_inventory"][0]["path"], "odm_orthophoto/orthophoto.tif")
        self.assertEqual(report["file_inventory"][0]["size_bytes"], 11)


if __name__ == "__main__":
    unittest.main()
