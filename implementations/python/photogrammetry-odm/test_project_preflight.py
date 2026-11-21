import base64
from pathlib import Path
import tempfile
import unittest

from project_preflight import build_preflight


PNG_1X1 = base64.b64decode(
    "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mP8/x8AAwMCAO+/"
    "l0sAAAAASUVORK5CYII="
)


class IntegratedProjectPreflightTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        self.project = self.root / "demo"
        (self.project / "images").mkdir(parents=True)
        (self.project / "images" / "one.png").write_bytes(PNG_1X1)
        self.manifest_path = self.root / "project.json"
        self.manifest = {
            "schema_version": "1.0",
            "project_id": "DEMO-001",
            "title": "Synthetic preflight",
            "intended_use": "Test the integrated read-only handoff",
            "dataset": {"project_directory": "demo", "expected_image_count": 1},
            "data_sources": [],
            "processing": {
                "engine": "OpenDroneMap",
                "container_image": "opendronemap/odm:3.6.1@sha256:" + "a" * 64,
                "arguments": ["--dsm"],
            },
            "validation": {
                "horizontal_crs": "EPSG:32632",
                "vertical_reference": "Synthetic local datum",
                "coordinate_units": "metres",
                "independent_checkpoints": True,
                "reference_uncertainty": "Synthetic exact values",
                "acceptance_criteria": "Synthetic test only",
            },
            "deliverables": ["orthophoto"],
        }

    def tearDown(self):
        self.tmp.cleanup()

    def test_builds_review_only_processing_handoff(self):
        report = build_preflight(self.manifest, self.manifest_path)
        self.assertIn(report["status"], {"ready_for_operator_review", "review_required"})
        self.assertEqual(report["project"]["image_count"], 1)
        self.assertIsNotNone(report["processing_handoff"]["command"])
        self.assertFalse(report["processing_handoff"]["executed"])
        self.assertIn("docker", report["processing_handoff"]["command"][0])

    def test_missing_images_is_reported_as_blocked_not_exception(self):
        (self.project / "images" / "one.png").unlink()
        report = build_preflight(self.manifest, self.manifest_path)
        self.assertEqual(report["status"], "blocked")
        self.assertIsNone(report["processing_handoff"]["command"])
        self.assertTrue(report["blockers"])

    def test_expected_count_mismatch_requires_review(self):
        self.manifest["dataset"]["expected_image_count"] = 2
        report = build_preflight(self.manifest, self.manifest_path)
        self.assertEqual(report["status"], "review_required")
        self.assertTrue(any("Expected 2 images" in item for item in report["warnings"]))

    def test_processing_command_is_not_executed(self):
        report = build_preflight(self.manifest, self.manifest_path)
        self.assertFalse(report["processing_handoff"]["executed"])
        self.assertIn("Docker was not invoked", report["processing_handoff"]["note"])


if __name__ == "__main__":
    unittest.main()
