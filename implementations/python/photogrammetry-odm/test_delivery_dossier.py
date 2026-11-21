"""Tests for the evidence delivery dossier."""
import json
import tempfile
import unittest
import zipfile
from pathlib import Path

from delivery_dossier import create_delivery_bundle


class DeliveryDossierTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        self.files = {}
        acquisition_payload = {
            "resolved_revision": "a" * 40,
            "selected_path": "datasets/drone_heig_2019",
            "file_count": 1,
            "files": [{"path": "datasets/drone_heig_2019/images/frame.jpg", "size_bytes": 1, "sha256": "b" * 64}],
        }
        acquisition_path = self.root / "acquisition-provenance.json"
        acquisition_path.write_text(json.dumps(acquisition_payload), encoding="utf-8")
        import hashlib
        verification_payload = {
            "status": "verified", "resolved_revision": "a" * 40,
            "selected_path": "datasets/drone_heig_2019",
            "declared_file_count": 1, "verified_file_count": 1,
            "manifest_sha256": hashlib.sha256(acquisition_path.read_bytes()).hexdigest(),
        }
        verification_path = self.root / "acquisition-verification.json"
        verification_path.write_text(json.dumps(verification_payload), encoding="utf-8")
        self.files["acquisition_manifest"] = acquisition_path
        self.files["acquisition_verification"] = verification_path
        payloads = {
            "manifest": {"project_id": "demo"},
            "preflight": {"project_id": "demo", "status": "ready_for_operator_review"},
            "run": {"run_id": "run-001", "status": "succeeded"},
            "outputs": {"status": "inspected"},
            "validation": {
                "project_id": "demo", "processing_run_id": "run-001",
                "evidence_status": "assessable",
                "acceptance": {"decision": "accepted", "reviewer": "Reviewer A", "rationale": "Meets project criteria"},
            },
        }
        for key, value in payloads.items():
            path = self.root / f"{key}.json"
            path.write_text(json.dumps(value), encoding="utf-8")
            self.files[key] = path

    def tearDown(self):
        self.tmp.cleanup()

    def bundle(self, destination):
        return create_delivery_bundle(
            self.files["acquisition_manifest"], self.files["acquisition_verification"],
            self.files["manifest"], self.files["preflight"], self.files["run"],
            self.files["outputs"], self.files["validation"], destination,
        )

    def test_complete_evidence_is_bundled_but_not_release_authorized(self):
        archive_path = self.root / "delivery.zip"
        result = self.bundle(archive_path)
        self.assertEqual(result["dossier"]["status"], "assembled")
        self.assertFalse(result["dossier"]["release_authorized"])
        with zipfile.ZipFile(archive_path) as archive:
            names = set(archive.namelist())
            self.assertIn("delivery-dossier.json", names)
            self.assertIn("evidence/project-manifest.json", names)
            dossier = json.loads(archive.read("delivery-dossier.json"))
            self.assertEqual(dossier["project_id"], "demo")
            self.assertEqual(len(dossier["artifacts"]), 7)
            self.assertEqual(dossier["observed_statuses"]["acquisition_verification"], "verified")
        second_archive = self.root / "delivery-repeat.zip"
        self.bundle(second_archive)
        self.assertEqual(archive_path.read_bytes(), second_archive.read_bytes())

    def test_pending_acceptance_requires_review_not_auto_approval(self):
        self.files["validation"].write_text(json.dumps({
            "project_id": "demo", "processing_run_id": "run-001",
            "evidence_status": "assessable", "acceptance": {"decision": "pending"},
        }), encoding="utf-8")
        result = self.bundle(self.root / "pending.zip")
        self.assertEqual(result["dossier"]["status"], "review_required")
        self.assertIn("Human validation acceptance decision is pending.", result["dossier"]["warnings"])

    def test_run_identity_mismatch_is_inconsistent(self):
        self.files["validation"].write_text(json.dumps({
            "project_id": "demo", "processing_run_id": "wrong",
            "evidence_status": "assessable", "acceptance": {"decision": "accepted"},
        }), encoding="utf-8")
        result = self.bundle(self.root / "mismatch.zip")
        self.assertEqual(result["dossier"]["status"], "inconsistent")
        self.assertTrue(result["dossier"]["consistency_errors"])

    def test_destination_cannot_overwrite_source_evidence(self):
        with self.assertRaisesRegex(ValueError, "must not overwrite"):
            self.bundle(self.files["manifest"])
    def test_missing_required_artifact_is_rejected(self):
        self.files["outputs"].unlink()
        with self.assertRaisesRegex(ValueError, "Required evidence file is missing"):
            self.bundle(self.root / "missing.zip")



    def test_acquisition_manifest_hash_mismatch_is_inconsistent(self):
        self.files["acquisition_manifest"].write_text(
            json.dumps({"resolved_revision": "a" * 40, "selected_path": "datasets/drone_heig_2019", "file_count": 1, "files": []}),
            encoding="utf-8",
        )
        result = self.bundle(self.root / "acquisition-mismatch.zip")
        self.assertEqual(result["dossier"]["status"], "inconsistent")
        self.assertTrue(any("manifest_sha256" in item for item in result["dossier"]["consistency_errors"]))

    def test_unverified_acquisition_requires_review(self):
        verification = json.loads(self.files["acquisition_verification"].read_text())
        verification["status"] = "integrity_error"
        self.files["acquisition_verification"].write_text(json.dumps(verification), encoding="utf-8")
        result = self.bundle(self.root / "unverified-acquisition.zip")
        self.assertEqual(result["dossier"]["status"], "review_required")
        self.assertTrue(any("Acquisition verification status" in item for item in result["dossier"]["warnings"]))

if __name__ == "__main__":
    unittest.main()
