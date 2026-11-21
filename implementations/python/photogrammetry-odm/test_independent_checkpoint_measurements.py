import csv
import hashlib
import json
from pathlib import Path
import tempfile
import unittest

from validate_independent_checkpoint_measurements import validate_measurements


FIELDS = [
    "point_id", "image", "measurement_status", "independent_pixel_x",
    "independent_pixel_y", "measurement_method", "reviewer",
    "measured_at_utc", "source_image_sha256", "measurement_notes",
]


class IndependentCheckpointMeasurementValidationTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        self.image = self.root / "frame.JPG"
        self.image.write_bytes(b"original source image bytes")
        self.image_hash = hashlib.sha256(self.image.read_bytes()).hexdigest()
        self.manifest = self.root / "acquisition.json"
        self.manifest.write_text(json.dumps({
            "resolved_revision": "a" * 40,
            "selected_path": "datasets/example",
            "files": [{"path": "datasets/example/images/frame.JPG",
                       "sha256": self.image_hash, "size_bytes": self.image.stat().st_size}],
        }), encoding="utf-8")
        self.split = self.root / "approved-split.json"
        self.split.write_text(json.dumps({
            "status": "approved_locked",
            "dataset": {"resolved_revision": "a" * 40,
                        "selected_path": "datasets/example"},
            "selection": {"control_points": ["C1"], "checkpoint_points": ["P1", "P2"]},
        }), encoding="utf-8")
        self.summary = self.root / "visual-summary.json"
        self.summary.write_text(json.dumps({
            "source_revision": "a" * 40,
            "selected_dataset_path": "datasets/example",
            "source_observations": [
                {"point_id": "P1", "image_name": "frame.JPG"},
                {"point_id": "P2", "image_name": "frame.JPG"},
            ],
        }), encoding="utf-8")
        self.csv = self.root / "measurements.csv"
        self.write_rows([
            self.row("P1", "10.25", "20.5"),
            self.row("P2", "30", "40"),
        ])

    def tearDown(self):
        self.tmp.cleanup()

    def row(self, point, x, y, **overrides):
        row = {
            "point_id": point, "image": "frame.JPG", "measurement_status": "measured",
            "independent_pixel_x": x, "independent_pixel_y": y,
            "measurement_method": "manual sub-pixel target-centre measurement",
            "reviewer": "Reviewer A", "measured_at_utc": "2026-11-21T09:00:00Z",
            "source_image_sha256": self.image_hash, "measurement_notes": "",
        }
        row.update(overrides)
        return row

    def write_rows(self, rows):
        with self.csv.open("w", newline="", encoding="utf-8") as stream:
            writer = csv.DictWriter(stream, fieldnames=FIELDS)
            writer.writeheader()
            writer.writerows(rows)

    def test_validates_structure_and_provenance_without_claiming_independence(self):
        report = validate_measurements(self.csv, self.split, self.manifest, self.summary)
        self.assertEqual(report["status"], "record_structure_and_provenance_validated")
        self.assertEqual(report["measurement_row_count"], 2)
        self.assertFalse(report["independent_measurement_independence_proven"])
        self.assertFalse(report["accuracy_assessment_performed"])

    def test_rejects_proposed_split(self):
        split = json.loads(self.split.read_text())
        split["status"] = "proposed_not_locked"
        self.split.write_text(json.dumps(split))
        with self.assertRaisesRegex(ValueError, "approved/locked"):
            validate_measurements(self.csv, self.split, self.manifest, self.summary)

    def test_rejects_control_point(self):
        self.write_rows([self.row("C1", "10", "20"), self.row("P2", "30", "40")])
        with self.assertRaisesRegex(ValueError, "control point"):
            validate_measurements(self.csv, self.split, self.manifest, self.summary)

    def test_rejects_wrong_image_hash(self):
        self.write_rows([
            self.row("P1", "10", "20", source_image_sha256="0" * 64),
            self.row("P2", "30", "40"),
        ])
        with self.assertRaisesRegex(ValueError, "does not match acquisition manifest"):
            validate_measurements(self.csv, self.split, self.manifest, self.summary)

    def test_rejects_non_utc_timestamp(self):
        self.write_rows([
            self.row("P1", "10", "20", measured_at_utc="2026-11-21T12:00:00+03:00"),
            self.row("P2", "30", "40"),
        ])
        with self.assertRaisesRegex(ValueError, "recorded in UTC"):
            validate_measurements(self.csv, self.split, self.manifest, self.summary)

    def test_rejects_duplicate_point_image(self):
        self.write_rows([self.row("P1", "10", "20"), self.row("P1", "11", "21"),
                         self.row("P2", "30", "40")])
        with self.assertRaisesRegex(ValueError, "duplicate point/image"):
            validate_measurements(self.csv, self.split, self.manifest, self.summary)

    def test_unmeasurable_record_requires_reason_and_blank_coordinates(self):
        self.write_rows([
            self.row("P1", "", "", measurement_status="unmeasurable",
                     measurement_notes="Target fully occluded in this view."),
            self.row("P1", "12", "22"),
            self.row("P2", "30", "40"),
        ])
        report = validate_measurements(self.csv, self.split, self.manifest, self.summary)
        self.assertEqual(report["measurement_status_counts"], {"measured": 2, "unmeasurable": 1})

    def test_requires_at_least_one_measured_view_per_checkpoint(self):
        self.write_rows([
            self.row("P1", "10", "20"),
            self.row("P2", "", "", measurement_status="unmeasurable",
                     measurement_notes="Target not visible."),
        ])
        with self.assertRaisesRegex(ValueError, "Every approved checkpoint"):
            validate_measurements(self.csv, self.split, self.manifest, self.summary)

    def test_rejects_observation_not_in_source_index(self):
        summary = json.loads(self.summary.read_text())
        summary["source_observations"] = [{"point_id": "P1", "image_name": "frame.JPG"}]
        self.summary.write_text(json.dumps(summary))
        with self.assertRaisesRegex(ValueError, "absent from source observation index"):
            validate_measurements(self.csv, self.split, self.manifest, self.summary)

    def test_rejects_split_manifest_hash_mismatch(self):
        split = json.loads(self.split.read_text())
        split["dataset"]["acquisition_manifest_sha256"] = "0" * 64
        self.split.write_text(json.dumps(split))
        with self.assertRaisesRegex(ValueError, "manifest hash"):
            validate_measurements(self.csv, self.split, self.manifest, self.summary)


if __name__ == "__main__":
    unittest.main()
