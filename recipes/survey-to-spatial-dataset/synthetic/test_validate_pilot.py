import csv
import shutil
import tempfile
import unittest
from pathlib import Path
from validate_pilot import validate

FIXTURE = Path(__file__).parent / "input"

class PilotValidatorTests(unittest.TestCase):
    def copy_fixture(self, target: Path) -> None:
        for source in FIXTURE.glob("*.csv"):
            shutil.copy(source, target / source.name)

    def test_committed_fixture_passes(self):
        report, errors = validate(FIXTURE)
        self.assertEqual(report["validation_status"], "PASS")
        self.assertEqual(report["record_counts"], {"stops": 4, "assets": 6, "observations": 4, "quality_checks": 4})
        self.assertEqual(errors, [])

    def test_unknown_stop_foreign_key_fails(self):
        with tempfile.TemporaryDirectory() as directory:
            target = Path(directory)
            self.copy_fixture(target)
            path = target / "assets.csv"
            with path.open(newline="", encoding="utf-8") as stream:
                rows = list(csv.DictReader(stream))
            rows[0]["stop_id"] = "STOP-NOT-IN-FIXTURE"
            with path.open("w", newline="", encoding="utf-8") as stream:
                writer = csv.DictWriter(stream, fieldnames=rows[0].keys())
                writer.writeheader()
                writer.writerows(rows)
            report, errors = validate(target)
            self.assertEqual(report["validation_status"], "FAIL")
            self.assertTrue(any("unknown stop_id" in error for error in errors))

    def test_duplicate_stop_id_fails(self):
        with tempfile.TemporaryDirectory() as directory:
            target = Path(directory)
            self.copy_fixture(target)
            path = target / "stops.csv"
            with path.open(newline="", encoding="utf-8") as stream:
                rows = list(csv.DictReader(stream))
            rows[1]["stop_id"] = rows[0]["stop_id"]
            with path.open("w", newline="", encoding="utf-8") as stream:
                writer = csv.DictWriter(stream, fieldnames=rows[0].keys())
                writer.writeheader()
                writer.writerows(rows)
            report, errors = validate(target)
            self.assertEqual(report["validation_status"], "FAIL")
            self.assertTrue(any("duplicate or blank stop_id" in error for error in errors))

if __name__ == "__main__":
    unittest.main()
