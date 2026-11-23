import csv
import json
from pathlib import Path
import tempfile
import unittest

from checkpoint_qa import assess_checkpoints, read_checkpoints
from odm_runner import build_command, validate_project


class ODMRunnerTests(unittest.TestCase):
    def test_project_validation_and_command_construction(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            project = root / "demo"
            images = project / "images"
            images.mkdir(parents=True)
            (images / "one.JPG").write_bytes(b"synthetic placeholder")
            (images / "ignore.txt").write_text("not an image")
            parent, name, count = validate_project(project)
            self.assertEqual((parent, name, count), (root, "demo", 1))
            command = build_command(project, "opendronemap/odm:3.6.1")
            self.assertIn("opendronemap/odm:3.6.1", command)
            self.assertEqual(command[-1], "--dsm")
            self.assertIn("demo", command)

    def test_project_validation_rejects_missing_images(self):
        with tempfile.TemporaryDirectory() as tmp:
            project = Path(tmp) / "demo"
            project.mkdir()
            with self.assertRaises(ValueError):
                validate_project(project)

    def test_project_validation_rejects_empty_image_folder(self):
        with tempfile.TemporaryDirectory() as tmp:
            project = Path(tmp) / "demo"
            (project / "images").mkdir(parents=True)
            with self.assertRaises(ValueError):
                validate_project(project)


class CheckpointQATests(unittest.TestCase):
    def test_analytic_residual_statistics(self):
        records = [
            {"point_id": "A", "ref_x": 0, "ref_y": 0, "ref_z": 0, "model_x": 3, "model_y": 4, "model_z": 2},
            {"point_id": "B", "ref_x": 0, "ref_y": 0, "ref_z": 0, "model_x": 0, "model_y": 0, "model_z": -2},
        ]
        result = assess_checkpoints(records)
        self.assertEqual(result["n"], 2)
        self.assertAlmostEqual(result["component_bias"]["x"], 1.5)
        self.assertAlmostEqual(result["component_bias"]["y"], 2.0)
        self.assertAlmostEqual(result["component_bias"]["z"], 0.0)
        self.assertAlmostEqual(result["component_rmse"]["x"], (4.5) ** 0.5)
        self.assertAlmostEqual(result["horizontal_rmse_2d"], (12.5) ** 0.5)
        self.assertAlmostEqual(result["vertical_rmse_1d"], 2.0)
        self.assertAlmostEqual(result["horizontal_radial_error"]["maximum"], 5.0)

    def test_read_csv_and_json_report(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "points.csv"
            with path.open("w", newline="", encoding="utf-8") as stream:
                writer = csv.DictWriter(stream, fieldnames=[
                    "point_id", "ref_x", "ref_y", "ref_z", "model_x", "model_y", "model_z"
                ])
                writer.writeheader()
                writer.writerow(dict(point_id="CP1", ref_x=1, ref_y=2, ref_z=3,
                                     model_x=1.1, model_y=2.2, model_z=3.3))
            rows = read_checkpoints(path)
            report = assess_checkpoints(rows)
            self.assertEqual(report["n"], 1)
            self.assertIn("not automatically CE95", report["interpretation_note"])

    def test_rejects_duplicate_ids_and_nonfinite_values(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "points.csv"
            headers = ["point_id", "ref_x", "ref_y", "ref_z", "model_x", "model_y", "model_z"]
            with path.open("w", newline="", encoding="utf-8") as stream:
                writer = csv.DictWriter(stream, fieldnames=headers)
                writer.writeheader()
                row = dict(point_id="CP1", ref_x=1, ref_y=2, ref_z=3,
                           model_x=1, model_y=2, model_z=3)
                writer.writerow(row)
                writer.writerow(row)
            with self.assertRaises(ValueError):
                read_checkpoints(path)
            with path.open("w", newline="", encoding="utf-8") as stream:
                writer = csv.DictWriter(stream, fieldnames=headers)
                writer.writeheader()
                writer.writerow(dict(point_id="CP1", ref_x="nan", ref_y=2, ref_z=3,
                                     model_x=1, model_y=2, model_z=3))
            with self.assertRaises(ValueError):
                read_checkpoints(path)


if __name__ == "__main__":
    unittest.main()
