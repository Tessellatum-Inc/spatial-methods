"""Tests for project-level checkpoint evidence records."""
import json
import tempfile
import unittest
from pathlib import Path

from validation_evidence import build_validation_record


class ValidationEvidenceTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        self.csv = self.root / "checkpoints.csv"
        self.csv.write_text(
            "point_id,ref_x,ref_y,ref_z,model_x,model_y,model_z
"
            "A,0,0,0,1,2,3
B,10,10,10,11,12,13
",
            encoding="utf-8",
        )
        self.context = {
            "project_id": "demo",
            "processing_run_id": "run-001",
            "horizontal_crs": "EPSG:32637",
            "vertical_reference": "declared local datum",
            "coordinate_units": "metres",
            "reference_uncertainty": "RTK survey; operator-stated +/- 0.03 m",
            "sample_design": "Independent spatially distributed checkpoints",
            "checkpoint_independence": True,
        }

    def tearDown(self):
        self.tmp.cleanup()

    def test_statistics_and_pending_decision_are_separate(self):
        report = build_validation_record(self.csv, self.context)
        self.assertEqual(report["evidence_status"], "assessable")
        self.assertEqual(report["residual_statistics"]["n"], 2)
        self.assertEqual(report["acceptance"]["decision"], "pending")
        self.assertFalse(report["acceptance"]["automatic_threshold_decision"])

    def test_missing_reference_metadata_is_not_assessable(self):
        context = dict(self.context)
        context["reference_uncertainty"] = ""
        report = build_validation_record(self.csv, context)
        self.assertEqual(report["evidence_status"], "not_assessable")
        self.assertIn("reference_uncertainty", report["missing_evidence"])

    def test_non_independent_points_are_not_assessable(self):
        context = dict(self.context, checkpoint_independence=False)
        report = build_validation_record(self.csv, context)
        self.assertEqual(report["evidence_status"], "not_assessable")

    def test_acceptance_is_blocked_when_required_evidence_is_missing(self):
        context = dict(self.context, reference_uncertainty="", acceptance_decision="accepted",
                       reviewer="Reviewer A", acceptance_rationale="Looks good")
        with self.assertRaisesRegex(ValueError, "evidence is missing"):
            build_validation_record(self.csv, context)

    def test_human_decision_requires_reviewer_and_rationale(self):
        context = dict(self.context, acceptance_decision="accepted")
        with self.assertRaisesRegex(ValueError, "acceptance_rationale"):
            build_validation_record(self.csv, context)

    def test_linked_run_record_is_hashed_and_id_checked(self):
        run = self.root / "run.json"
        run.write_text(json.dumps({"run_id": "run-001"}), encoding="utf-8")
        report = build_validation_record(self.csv, self.context, run_record=run)
        self.assertEqual(report["linked_evidence"]["processing_run"]["sha256"], __import__("hashlib").sha256(run.read_bytes()).hexdigest())
        with self.assertRaisesRegex(ValueError, "does not match"):
            build_validation_record(self.csv, dict(self.context, processing_run_id="wrong"), run_record=run)


if __name__ == "__main__":
    unittest.main()
