from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch
from types import SimpleNamespace

from processing_run import create_run_record


class ProcessingRunTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        self.project = self.root / "project"
        self.images = self.project / "images"
        self.images.mkdir(parents=True)
        (self.images / "frame.jpg").write_bytes(b"synthetic image bytes")
        self.run_dir = self.root / "runs" / "run-001"
        self.image = "opendronemap/odm:3.6.1@sha256:" + "a" * 64

    def tearDown(self):
        self.tmp.cleanup()

    def test_default_is_dry_run_and_records_input_hashes(self):
        with patch("processing_run.docker_image_metadata") as inspect:
            record = create_run_record(self.project, self.image, [], self.run_dir)
        inspect.assert_not_called()
        self.assertEqual(record["status"], "prepared")
        self.assertFalse(record["processing"]["executed"])
        self.assertEqual(record["input_count"], 1)
        self.assertEqual(len(record["input_inventory"][0]["sha256"]), 64)
        self.assertFalse(record["container"]["available"])
        self.assertTrue((self.run_dir / "processing-run.json").is_file())

    def test_run_directory_inside_project_is_rejected(self):
        with self.assertRaises(ValueError):
            create_run_record(self.project, self.image, [], self.project / "runs")

    @patch("processing_run.subprocess.run")
    @patch("processing_run.docker_image_metadata")
    @patch("processing_run.shutil.which", return_value="/usr/bin/docker")
    def test_explicit_execution_records_logs_exit_and_outputs(self, which, inspect, run):
        def execute(command, **kwargs):
            (self.project / "odm_orthophoto").mkdir()
            (self.project / "odm_orthophoto" / "orthophoto.tif").write_bytes(b"synthetic output")
            return SimpleNamespace(returncode=0, stdout="complete", stderr="")
        run.side_effect = execute
        inspect.return_value = {
            "available": True,
            "image_id": "sha256:" + "b" * 64,
            "repo_digests": [self.image],
            "os": "linux",
            "architecture": "amd64",
        }
        record = create_run_record(self.project, self.image, [], self.run_dir, execute=True)
        self.assertEqual(record["status"], "succeeded")
        self.assertTrue(record["processing"]["executed"])
        self.assertEqual(record["exit_code"], 0)
        self.assertEqual(record["logs"]["stdout"], "stdout.log")
        self.assertTrue(any("orthophoto.tif" in item["path"] for item in record["outputs"]))
        self.assertEqual((self.run_dir / "stdout.log").read_text(), "complete")

    @patch("processing_run.subprocess.run")
    @patch("processing_run.docker_image_metadata", return_value={"available": False})
    @patch("processing_run.shutil.which", return_value="/usr/bin/docker")
    def test_failed_execution_is_preserved_in_record(self, which, inspect, run):
        run.return_value = SimpleNamespace(returncode=17, stdout="", stderr="processing failed")
        record = create_run_record(self.project, self.image, [], self.run_dir, execute=True)
        self.assertEqual(record["status"], "failed")
        self.assertEqual(record["exit_code"], 17)
        self.assertIn("processing failed", (self.run_dir / "stderr.log").read_text())


if __name__ == "__main__":
    unittest.main()
