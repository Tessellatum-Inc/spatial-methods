import csv
import json
from pathlib import Path
import tempfile
import unittest

from lock_visual_review import lock_review


FIELDS = [
    "point_id", "image_name", "pixel_x", "pixel_y",
    "target_visible", "target_identity_clear", "marker_centred",
    "blur", "occlusion", "ambiguity", "decision", "rationale",
    "reviewer", "reviewed_at",
]


def make_fixture(root: Path, reviewers=("reviewer-a",)):
    summary = root / "visual-review-summary.json"
    summary.write_text(json.dumps({
        "status": "role_blind_visual_review_material_prepared_not_human_approved",
        "source_revision": "a" * 40,
        "selected_dataset_path": "datasets/drone_heig_2019",
        "observation_count": 2,
        "source_observations": [
            {"point_id": "P1", "image_name": "img1.JPG", "pixel_x": 10.0, "pixel_y": 20.0},
            {"point_id": "P2", "image_name": "img2.JPG", "pixel_x": 30.0, "pixel_y": 40.0},
        ],
    }), encoding="utf-8")
    manifest = root / "acquisition-provenance.json"
    manifest.write_text(json.dumps({
        "resolved_revision": "a" * 40,
        "selected_path": "datasets/drone_heig_2019",
    }), encoding="utf-8")
    decisions = root / "review-decisions.csv"
    with decisions.open("w", newline="", encoding="utf-8") as stream:
        writer = csv.DictWriter(stream, fieldnames=FIELDS)
        writer.writeheader()
        for index, values in enumerate([
            ("P1", "img1.JPG", "10.000", "20.000", "accepted", "Target clear and marker centred."),
            ("P2", "img2.JPG", "30.000", "40.000", "questioned", "Target partly obscured."),
        ]):
            point, image, px, py, decision, rationale = values
            writer.writerow({
                "point_id": point, "image_name": image, "pixel_x": px, "pixel_y": py,
                "target_visible": "yes", "target_identity_clear": "yes",
                "marker_centred": "uncertain" if decision == "questioned" else "yes",
                "blur": "none", "occlusion": "moderate" if decision == "questioned" else "none",
                "ambiguity": "low" if decision == "questioned" else "none",
                "decision": decision, "rationale": rationale,
                "reviewer": reviewers[index] if index < len(reviewers) else reviewers[0],
                "reviewed_at": f"2026-11-21T12:0{index}:00+03:00",
            })
    return decisions, summary, manifest


class LockVisualReviewTests(unittest.TestCase):
    def test_locks_complete_single_reviewer_review_without_unblinding(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            decisions, summary, manifest = make_fixture(root)
            report = lock_review(decisions, summary, manifest, root / "locked-review.json")
            self.assertEqual(report["status"], "single_reviewer_adjudication_locked")
            self.assertFalse(report["unblinded"])
            self.assertFalse(report["independent_validation"])
            self.assertEqual(report["observation_count_reviewed"], 2)
            self.assertEqual(report["decision_counts"], {"accepted": 1, "questioned": 1})

    def test_rejects_blank_decision_or_rationale(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            decisions, summary, manifest = make_fixture(root)
            rows = list(csv.DictReader(decisions.open()))
            rows[0]["decision"] = ""
            with decisions.open("w", newline="", encoding="utf-8") as stream:
                writer = csv.DictWriter(stream, fieldnames=FIELDS)
                writer.writeheader()
                writer.writerows(rows)
            with self.assertRaisesRegex(ValueError, "blank required values"):
                lock_review(decisions, summary, manifest, root / "locked.json")

    def test_rejects_changed_source_pixel_coordinates(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            decisions, summary, manifest = make_fixture(root)
            rows = list(csv.DictReader(decisions.open()))
            rows[0]["pixel_x"] = "11"
            with decisions.open("w", newline="", encoding="utf-8") as stream:
                writer = csv.DictWriter(stream, fieldnames=FIELDS)
                writer.writeheader()
                writer.writerows(rows)
            with self.assertRaisesRegex(ValueError, "pixel coordinates were altered"):
                lock_review(decisions, summary, manifest, root / "locked.json")

    def test_rejects_missing_observation_row(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            decisions, summary, manifest = make_fixture(root)
            rows = list(csv.DictReader(decisions.open()))[:1]
            with decisions.open("w", newline="", encoding="utf-8") as stream:
                writer = csv.DictWriter(stream, fieldnames=FIELDS)
                writer.writeheader()
                writer.writerows(rows)
            with self.assertRaisesRegex(ValueError, "Expected 2 observation decisions"):
                lock_review(decisions, summary, manifest, root / "locked.json")

    def test_rejects_naive_review_timestamp(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            decisions, summary, manifest = make_fixture(root)
            rows = list(csv.DictReader(decisions.open()))
            rows[0]["reviewed_at"] = "2026-11-21T12:00:00"
            with decisions.open("w", newline="", encoding="utf-8") as stream:
                writer = csv.DictWriter(stream, fieldnames=FIELDS)
                writer.writeheader()
                writer.writerows(rows)
            with self.assertRaisesRegex(ValueError, "timezone offset"):
                lock_review(decisions, summary, manifest, root / "locked.json")

    def test_rejects_manifest_revision_mismatch(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            decisions, summary, manifest = make_fixture(root)
            manifest.write_text(json.dumps({
                "resolved_revision": "b" * 40,
                "selected_path": "datasets/drone_heig_2019",
            }), encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "source revision"):
                lock_review(decisions, summary, manifest, root / "locked.json")

    def test_multiple_names_do_not_claim_independence(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            decisions, summary, manifest = make_fixture(root, reviewers=("reviewer-a", "reviewer-b"))
            report = lock_review(decisions, summary, manifest, root / "locked-review.json")
            self.assertEqual(report["status"], "multi_reviewer_adjudication_locked_not_independent")
            self.assertFalse(report["independent_validation"])


if __name__ == "__main__":
    unittest.main()
