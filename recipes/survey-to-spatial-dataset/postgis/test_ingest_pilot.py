import csv
import json
import shutil
import tempfile
import unittest
from pathlib import Path

from ingest_pilot import IngestionError, load_package

FIXTURE = Path(__file__).parent / "input"


class IngestionPackageTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.input_dir = Path(self.temp.name) / "input"
        shutil.copytree(FIXTURE, self.input_dir)

    def tearDown(self):
        self.temp.cleanup()

    def test_committed_fixture_passes_preflight(self):
        manifest, stops, assets = load_package(self.input_dir)
        self.assertEqual(manifest["dataset_status"], "synthetic")
        self.assertEqual(len(stops), 3)
        self.assertEqual(len(assets), 4)

    def test_unknown_stop_foreign_key_fails(self):
        path = self.input_dir / "assets.csv"
        rows = list(csv.DictReader(path.open(encoding="utf-8", newline="")))
        rows[0]["stop_id"] = "NO-SUCH-STOP"
        with path.open("w", encoding="utf-8", newline="") as handle:
            writer = csv.DictWriter(handle, fieldnames=rows[0].keys())
            writer.writeheader()
            writer.writerows(rows)
        with self.assertRaisesRegex(IngestionError, "unknown stop_id"):
            load_package(self.input_dir)

    def test_duplicate_stop_identifier_fails(self):
        path = self.input_dir / "stops.csv"
        rows = list(csv.DictReader(path.open(encoding="utf-8", newline="")))
        rows[1]["stop_id"] = rows[0]["stop_id"]
        with path.open("w", encoding="utf-8", newline="") as handle:
            writer = csv.DictWriter(handle, fieldnames=rows[0].keys())
            writer.writeheader()
            writer.writerows(rows)
        with self.assertRaisesRegex(IngestionError, "duplicate stop_id"):
            load_package(self.input_dir)

    def test_non_synthetic_manifest_fails(self):
        path = self.input_dir / "manifest.json"
        manifest = json.loads(path.read_text(encoding="utf-8"))
        manifest["dataset_status"] = "observed"
        path.write_text(json.dumps(manifest), encoding="utf-8")
        with self.assertRaisesRegex(IngestionError, "only fixtures"):
            load_package(self.input_dir)

    def test_out_of_range_coordinate_fails(self):
        path = self.input_dir / "stops.csv"
        rows = list(csv.DictReader(path.open(encoding="utf-8", newline="")))
        rows[0]["longitude"] = "181"
        with path.open("w", encoding="utf-8", newline="") as handle:
            writer = csv.DictWriter(handle, fieldnames=rows[0].keys())
            writer.writeheader()
            writer.writerows(rows)
        with self.assertRaisesRegex(IngestionError, "longitude"):
            load_package(self.input_dir)


if __name__ == "__main__":
    unittest.main()
