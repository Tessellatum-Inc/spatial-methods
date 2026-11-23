import csv
import hashlib
import json
from pathlib import Path
import tempfile
import unittest

from approve_control_checkpoint_split import approve_split


class SplitApprovalTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        self.proposed = self.root / "proposed.json"
        self.decisions = self.root / "decisions.csv"
        self.lock = self.root / "locked-review.json"
        self.approval = self.root / "approval.json"
        self.output = self.root / "approved.json"
        self.proposed.write_text(json.dumps({
            "status": "proposed_not_locked",
            "dataset": {"resolved_revision": "a" * 40, "selected_path": "datasets/example",
                        "acquisition_manifest_sha256": "b" * 64},
            "selection": {"control_points": ["C1"], "checkpoint_points": ["P1"],
                          "excluded_low_observation_points": {"X1": 2}},
        }))
        with self.decisions.open("w", newline="", encoding="utf-8") as f:
            w = csv.DictWriter(f, fieldnames=["point_id", "image_name", "decision"])
            w.writeheader()
            w.writerows([
                {"point_id": "C1", "image_name": "c.jpg", "decision": "accepted"},
                {"point_id": "P1", "image_name": "p1.jpg", "decision": "accepted"},
                {"point_id": "P1", "image_name": "p2.jpg", "decision": "accepted"},
                {"point_id": "X1", "image_name": "x.jpg", "decision": "questioned"},
            ])
        self.decisions_hash = hashlib.sha256(self.decisions.read_bytes()).hexdigest()
        self.lock.write_text(json.dumps({
            "status": "single_reviewer_adjudication_locked", "unblinded": False,
            "source_revision": "a" * 40, "selected_dataset_path": "datasets/example",
            "acquisition_manifest_sha256": "b" * 64,
            "review_decisions_sha256": self.decisions_hash,
            "observation_count_expected": 4, "observation_count_reviewed": 4,
        }))
        self.lock_hash = hashlib.sha256(self.lock.read_bytes()).hexdigest()
        self.approval.write_text(json.dumps({
            "decision": "approve", "approver": "Human Reviewer",
            "approved_at_utc": "2026-11-21T12:00:00Z",
            "review_lock_sha256": self.lock_hash,
            "review_decisions_sha256": self.decisions_hash,
            "geometry_assessment": "acceptable", "coverage_assessment": "acceptable",
            "control_checkpoint_separation_confirmed": True,
            "checkpoint_withholding_confirmed": True,
            "coordinate_reference_review_status":
                "horizontal_and_vertical_semantics_documented_pending_processing_verification",
            "approval_rationale": "Reviewed geometry and observation coverage.",
        }))

    def tearDown(self):
        self.tmp.cleanup()

    def approve(self):
        return approve_split(self.proposed, self.decisions, self.lock, self.approval, self.output)

    def test_creates_approved_locked_split_only_with_human_signoff(self):
        result = self.approve()
        self.assertEqual(result["status"], "approved_locked")
        self.assertEqual(result["approval"]["approver"], "Human Reviewer")
        self.assertTrue(self.output.exists())

    def test_rejects_unlocked_or_unblinded_review(self):
        lock = json.loads(self.lock.read_text())
        lock["unblinded"] = True
        self.lock.write_text(json.dumps(lock))
        self.refresh_lock_hash()
        with self.assertRaisesRegex(ValueError, "unblinded:false"):
            self.approve()

    def refresh_lock_hash(self):
        lock_hash = hashlib.sha256(self.lock.read_bytes()).hexdigest()
        approval = json.loads(self.approval.read_text())
        approval["review_lock_sha256"] = lock_hash
        self.approval.write_text(json.dumps(approval))

    def test_rejects_questioned_selected_point(self):
        rows = list(csv.DictReader(self.decisions.open()))
        rows[1]["decision"] = "questioned"
        self.write_decisions(rows)
        self.refresh_decision_hashes()
        with self.assertRaisesRegex(ValueError, "questioned/rejected"):
            self.approve()

    def write_decisions(self, rows):
        with self.decisions.open("w", newline="", encoding="utf-8") as f:
            w = csv.DictWriter(f, fieldnames=["point_id", "image_name", "decision"])
            w.writeheader()
            w.writerows(rows)

    def refresh_decision_hashes(self):
        digest = hashlib.sha256(self.decisions.read_bytes()).hexdigest()
        lock = json.loads(self.lock.read_text())
        lock["review_decisions_sha256"] = digest
        self.lock.write_text(json.dumps(lock))
        self.refresh_lock_hash()
        approval = json.loads(self.approval.read_text())
        approval["review_decisions_sha256"] = digest
        approval["review_lock_sha256"] = hashlib.sha256(self.lock.read_bytes()).hexdigest()
        self.approval.write_text(json.dumps(approval))

    def test_rejects_pending_human_approval(self):
        approval = json.loads(self.approval.read_text())
        approval["decision"] = "pending"
        self.approval.write_text(json.dumps(approval))
        with self.assertRaisesRegex(ValueError, "explicitly be 'approve'"):
            self.approve()

    def test_rejects_mismatched_approval_hash(self):
        approval = json.loads(self.approval.read_text())
        approval["review_lock_sha256"] = "0" * 64
        self.approval.write_text(json.dumps(approval))
        with self.assertRaisesRegex(ValueError, "different review lock"):
            self.approve()


if __name__ == "__main__":
    unittest.main()
