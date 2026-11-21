from pathlib import Path
import tempfile
import unittest
from unittest.mock import MagicMock, patch
from types import SimpleNamespace

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

    def test_las_without_laspy_is_reported_as_uninspected(self):
        (self.project / "odm_georeferencing").mkdir()
        (self.project / "odm_georeferencing" / "cloud.laz").write_bytes(b"synthetic point cloud")
        with patch.dict("sys.modules", {"laspy": None}):
            report = inspect_outputs(self.project)
        self.assertEqual(report["point_clouds"][0]["status"], "not_inspected")
        self.assertTrue(any("Point-cloud header not inspected" in item for item in report["warnings"]))

    def test_las_header_metadata_is_recorded_when_laspy_is_available(self):
        (self.project / "cloud.las").write_bytes(b"synthetic point cloud")
        header = SimpleNamespace(
            mins=[1.0, 2.0, 3.0],
            maxs=[4.0, 5.0, 6.0],
            point_count=123,
            point_format=SimpleNamespace(id=6),
            version="1.4",
            scales=[0.001, 0.001, 0.001],
            offsets=[0.0, 0.0, 0.0],
            parse_crs=lambda: None,
        )
        reader = MagicMock()
        reader.__enter__.return_value.header = header
        fake_laspy = SimpleNamespace(open=lambda path: reader)
        with patch.dict("sys.modules", {"laspy": fake_laspy}):
            report = inspect_outputs(self.project)
        point_cloud = report["point_clouds"][0]
        self.assertEqual(point_cloud["status"], "readable")
        self.assertEqual(point_cloud["point_count"], 123)
        self.assertEqual(point_cloud["mins"], [1.0, 2.0, 3.0])

    def test_empty_point_cloud_is_not_reported_as_readable(self):
        (self.project / "empty.las").write_bytes(b"synthetic empty point cloud")
        header = SimpleNamespace(
            mins=[0.0, 0.0, 0.0], maxs=[0.0, 0.0, 0.0], point_count=0,
            point_format=SimpleNamespace(id=6), version="1.4",
            scales=[0.001, 0.001, 0.001], offsets=[0.0, 0.0, 0.0],
            parse_crs=lambda: None,
        )
        reader = MagicMock()
        reader.__enter__.return_value.header = header
        with patch.dict("sys.modules", {"laspy": SimpleNamespace(open=lambda path: reader)}):
            report = inspect_outputs(self.project)
        self.assertEqual(report["point_clouds"][0]["status"], "invalid")
        self.assertTrue(any("Point cloud could not be read" in item for item in report["blockers"]))

    def test_missing_laz_backend_is_not_misreported_as_corrupt_data(self):
        (self.project / "cloud.laz").write_bytes(b"synthetic compressed point cloud")
        fake_laspy = SimpleNamespace(
            open=lambda path: (_ for _ in ()).throw(RuntimeError("No LazBackend selected; install lazrs"))
        )
        with patch.dict("sys.modules", {"laspy": fake_laspy}):
            report = inspect_outputs(self.project)
        self.assertEqual(report["point_clouds"][0]["status"], "not_inspected")
        self.assertIn("backend unavailable", report["point_clouds"][0]["reason"])

    def test_inventory_records_project_relative_files(self):
        report = inspect_outputs(self.project)
        self.assertEqual(report["file_inventory"][0]["path"], "odm_orthophoto/orthophoto.tif")
        self.assertEqual(report["file_inventory"][0]["size_bytes"], 11)


if __name__ == "__main__":
    unittest.main()
