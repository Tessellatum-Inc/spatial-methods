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
        self.assertTrue(any("Point-cloud records not inspected" in item for item in report["warnings"]))

    def test_las_header_metadata_is_recorded_when_laspy_is_available(self):
        (self.project / "cloud.las").write_bytes(b"synthetic point cloud")
        header = SimpleNamespace(
            mins=[1.0, 2.0, 3.0],
            maxs=[4.0, 5.0, 7.0],
            point_count=2,
            point_format=SimpleNamespace(id=6),
            version="1.4",
            scales=[0.001, 0.001, 0.001],
            offsets=[0.0, 0.0, 0.0],
            parse_crs=lambda: None,
        )
        reader = MagicMock()
        reader.__enter__.return_value.header = header
        reader.__enter__.return_value.chunk_iterator.return_value = [SimpleNamespace(
            x=[1.5, 2.5], y=[3.5, 4.5], z=[5.5, 6.5],
            classification=[2, 5], intensity=[100, 250],
        )]
        fake_laspy = SimpleNamespace(open=lambda path: reader)
        with patch.dict("sys.modules", {"laspy": fake_laspy}):
            report = inspect_outputs(self.project)
        point_cloud = report["point_clouds"][0]
        self.assertEqual(point_cloud["status"], "readable")
        self.assertEqual(point_cloud["observed_point_count"], 2)
        self.assertEqual(point_cloud["classification_counts"], {"2": 1, "5": 1})
        self.assertEqual(point_cloud["intensity_range"], [100, 250])
        self.assertEqual(point_cloud["header_mins"], [1.0, 2.0, 3.0])

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
        reader.__enter__.return_value.chunk_iterator.return_value = []
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



    def test_obj_mesh_reports_vertices_faces_and_valid_indices(self):
        (self.project / "model.obj").write_text("v 0 0 0\nv 1 0 0\nv 0 1 0\nf 1 2 3\n", encoding="utf-8")
        mesh = inspect_outputs(self.project)["meshes"][0]
        self.assertEqual(mesh["status"], "readable")
        self.assertEqual(mesh["vertex_count"], 3)
        self.assertEqual(mesh["face_count"], 1)

    def test_obj_mesh_rejects_out_of_range_and_zero_indices(self):
        (self.project / "bad.obj").write_text("v 0 0 0\nv 1 0 0\nv 0 1 0\nf 1 2 4\nf 0 2 3\n", encoding="utf-8")
        mesh = inspect_outputs(self.project)["meshes"][0]
        self.assertEqual(mesh["status"], "invalid")
        self.assertEqual(mesh["invalid_line_count"], 2)

    def test_obj_mesh_supports_negative_relative_indices(self):
        (self.project / "relative.obj").write_text("v 0 0 0\nv 1 0 0\nv 0 1 0\nf -3 -2 -1\n", encoding="utf-8")
        self.assertEqual(inspect_outputs(self.project)["meshes"][0]["status"], "readable")

    def test_obj_mesh_rejects_degenerate_face_and_non_finite_vertex(self):
        (self.project / "bad.obj").write_text("v 0 0 0\nv 1 0 0\nv nan 1 0\nf 1 1 2\n", encoding="utf-8")
        mesh = inspect_outputs(self.project)["meshes"][0]
        self.assertEqual(mesh["status"], "invalid")
        self.assertEqual(mesh["degenerate_face_count"], 1)


    def test_point_cloud_flags_points_outside_declared_header_bounds(self):
        (self.project / "outside.las").write_bytes(b"synthetic point cloud")
        header = SimpleNamespace(
            mins=[1.0, 2.0, 3.0], maxs=[4.0, 5.0, 6.0], point_count=1,
            point_format=SimpleNamespace(id=6), version="1.4",
            scales=[0.001, 0.001, 0.001], offsets=[0.0, 0.0, 0.0],
            parse_crs=lambda: None,
        )
        reader = MagicMock()
        reader.__enter__.return_value.header = header
        reader.__enter__.return_value.chunk_iterator.return_value = [SimpleNamespace(
            x=[2.0], y=[3.0], z=[9.0], classification=[2], intensity=[100],
        )]
        with patch.dict("sys.modules", {"laspy": SimpleNamespace(open=lambda path: reader)}):
            report = inspect_outputs(self.project)
        cloud = report["point_clouds"][0]
        self.assertEqual(cloud["status"], "invalid")
        self.assertEqual(cloud["points_outside_header_bounds"], 1)

    def test_point_cloud_flags_header_point_count_mismatch(self):
        (self.project / "mismatch.las").write_bytes(b"synthetic point cloud")
        header = SimpleNamespace(
            mins=[0.0, 0.0, 0.0], maxs=[2.0, 2.0, 2.0], point_count=2,
            point_format=SimpleNamespace(id=6), version="1.4",
            scales=[0.001, 0.001, 0.001], offsets=[0.0, 0.0, 0.0],
            parse_crs=lambda: None,
        )
        reader = MagicMock()
        reader.__enter__.return_value.header = header
        reader.__enter__.return_value.chunk_iterator.return_value = [SimpleNamespace(
            x=[1.0], y=[1.0], z=[1.0], classification=[2], intensity=[100],
        )]
        with patch.dict("sys.modules", {"laspy": SimpleNamespace(open=lambda path: reader)}):
            report = inspect_outputs(self.project)
        cloud = report["point_clouds"][0]
        self.assertFalse(cloud["point_count_matches_header"])
        self.assertEqual(cloud["status"], "invalid")



    def test_mesh_only_deliverable_does_not_require_a_geotiff(self):
        (self.project / "odm_orthophoto" / "orthophoto.tif").unlink()
        (self.project / "model.obj").write_text(
            "v 0 0 0\nv 1 0 0\nv 0 1 0\nf 1 2 3\n", encoding="utf-8"
        )
        report = inspect_outputs(self.project, ["model.obj"])
        self.assertEqual(report["status"], "inspected")
        self.assertFalse(any("No GeoTIFF outputs" in item for item in report["warnings"]))

    def test_declared_raster_deliverable_without_geotiff_is_flagged(self):
        (self.project / "odm_orthophoto" / "orthophoto.tif").unlink()
        report = inspect_outputs(self.project, ["orthophoto.tif"])
        self.assertEqual(report["status"], "blocked")
        self.assertTrue(any("Declared output is missing" in item for item in report["blockers"]))
        self.assertTrue(any("No GeoTIFF outputs" in item for item in report["warnings"]))



    def test_obj_rejects_invalid_texture_coordinate_reference(self):
        (self.project / "bad-texture.obj").write_text(
            "v 0 0 0\\nv 1 0 0\\nv 0 1 0\\nvt 0 0\\nf 1/2 2/1 3/1\\n",
            encoding="utf-8",
        )
        report = inspect_outputs(self.project, ["bad-texture.obj"])
        self.assertEqual(report["meshes"][0]["status"], "invalid")
        self.assertEqual(report["meshes"][0]["invalid_line_count"], 1)

    def test_obj_rejects_collinear_zero_area_face(self):
        (self.project / "collinear.obj").write_text(
            "v 0 0 0\\nv 1 0 0\\nv 2 0 0\\nf 1 2 3\\n",
            encoding="utf-8",
        )
        report = inspect_outputs(self.project, ["collinear.obj"])
        self.assertEqual(report["meshes"][0]["status"], "invalid")
        self.assertEqual(report["meshes"][0]["zero_area_face_count"], 1)

    def test_obj_accepts_negative_relative_indices(self):
        (self.project / "negative.obj").write_text(
            "v 0 0 0\\nv 1 0 0\\nv 0 1 0\\nf -3 -2 -1\\n",
            encoding="utf-8",
        )
        report = inspect_outputs(self.project, ["negative.obj"])
        self.assertEqual(report["meshes"][0]["status"], "readable")

if __name__ == "__main__":
    unittest.main()
