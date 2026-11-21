import json
from pathlib import Path
import tempfile
import unittest

from project_manifest import validate_manifest


class ProjectManifestTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        self.project = self.root / "demo"
        (self.project / "images").mkdir(parents=True)
        (self.project / "images" / "one.JPG").write_bytes(b"synthetic")
        self.manifest = {
            "schema_version": "1.0",
            "project_id": "DEMO-001",
            "title": "Synthetic rehearsal",
            "intended_use": "Test manifest preflight",
            "dataset": {"project_directory": "demo", "expected_image_count": 1},
            "data_sources": [],
            "processing": {"container_image": "opendronemap/odm:3.6.1@sha256:" + "a" * 64, "arguments": []},
            "validation": {
                "horizontal_crs": "EPSG:32632",
                "vertical_reference": "Local test datum",
                "coordinate_units": "metres",
                "independent_checkpoints": True,
                "acceptance_criteria": "Synthetic test only",
                "reference_uncertainty": "Synthetic exact values",
            },
            "deliverables": ["orthophoto"],
        }

    def tearDown(self):
        self.tmp.cleanup()

    def test_ready_for_operator_review(self):
        report = validate_manifest(self.manifest, self.root / "project.json")
        self.assertEqual(report["status"], "ready_for_operator_review")
        self.assertEqual(report["image_count"], 1)
        self.assertEqual(report["blockers"], [])
        self.assertEqual(report["warnings"], [])

    def test_missing_images_is_blocker(self):
        (self.project / "images" / "one.JPG").unlink()
        report = validate_manifest(self.manifest, self.root / "project.json")
        self.assertEqual(report["status"], "blocked")
        self.assertTrue(report["blockers"])

    def test_relative_project_path_resolves_from_manifest(self):
        report = validate_manifest(self.manifest, self.root / "project.json")
        self.assertEqual(Path(report["project_directory"]), self.project.resolve())

    def test_missing_reference_details_are_warnings(self):
        self.manifest["validation"]["vertical_reference"] = ""
        report = validate_manifest(self.manifest, self.root / "project.json")
        self.assertEqual(report["status"], "review_required")
        self.assertTrue(any("vertical_reference" in item for item in report["warnings"]))

    def test_latest_image_tag_is_flagged(self):
        self.manifest["processing"]["container_image"] = "opendronemap/odm:latest"
        report = validate_manifest(self.manifest, self.root / "project.json")
        self.assertTrue(any("not appear explicitly pinned" in item for item in report["warnings"]))

    def test_rejects_unknown_schema(self):
        self.manifest["schema_version"] = "2.0"
        with self.assertRaises(ValueError):
            validate_manifest(self.manifest, self.root / "project.json")


if __name__ == "__main__":
    unittest.main()
