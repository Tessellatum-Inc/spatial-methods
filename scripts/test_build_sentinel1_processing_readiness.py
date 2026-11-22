"""Offline tests for the Sentinel-1 processing-readiness reconciler."""
import importlib.util
from pathlib import Path
import unittest

MODULE_PATH = Path(__file__).resolve().parents[1] / "explorations" / "radar" / "build_sentinel1_processing_readiness.py"
SPEC = importlib.util.spec_from_file_location("build_sentinel1_processing_readiness", MODULE_PATH)
BUILDER = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(BUILDER)

PRODUCT_ID = "8ffa5641-c404-4189-b0fb-ed805b077d71"
PRODUCT_NAME = "S1C_IW_GRDH_1SDV_20261102T031112_20261102T031137_010152_01443B_5D46.SAFE"
ARCHIVE = f"sentinel1_{PRODUCT_ID}.SAFE.zip"
DIGEST = "a" * 64


def evidence():
    stack = {
        "manifest_schema": "tessellatum.sentinel1.stack-manifest.v1",
        "source_inventory_sha256": "b" * 64,
        "candidates": [{
            "product_id": PRODUCT_ID,
            "product_name": PRODUCT_NAME,
            "catalogue_selection_status": "candidate",
        }],
    }
    download = {
        "product_id": PRODUCT_ID,
        "archive_file": ARCHIVE,
        "archive_sha256": DIGEST,
        "validation": "passed",
        "downloaded_at_utc": "2026-11-21T00:00:00Z",
    }
    audit = {
        "archive": ARCHIVE,
        "archive_sha256": DIGEST,
        "safe_root_name": PRODUCT_NAME,
        "structural_dual_pol_gate": "passed",
        "checks": {
            "measurement_contains_vv_and_vh": True,
            "annotation_contains_vv_and_vh": True,
            "calibration_contains_vv_and_vh": True,
            "noise_annotation_contains_vv_and_vh": True,
            "manifest_is_well_formed_xml": True,
            "safe_root_name_is_sentinel1_iw_grd": True,
            "manifest_identifies_iw_mode": True,
        },
    }
    return stack, download, audit


class ProcessingReadinessTests(unittest.TestCase):
    def test_reconciles_matching_evidence_but_never_authorizes_processing(self):
        record = BUILDER.build_readiness_record(*evidence())
        self.assertEqual(record["structural_preflight_status"], "passed")
        self.assertEqual(record["structural_preflight_blockers"], [])
        self.assertFalse(record["processing_authorized"])
        self.assertEqual(record["processing_status"], "not_started")
        self.assertTrue(record["processing_blockers"])

    def test_blocks_checksum_mismatch(self):
        stack, download, audit = evidence()
        audit["archive_sha256"] = "c" * 64
        record = BUILDER.build_readiness_record(stack, download, audit)
        self.assertEqual(record["structural_preflight_status"], "blocked")
        self.assertIn("download_and_audit_archive_checksums_do_not_match", record["structural_preflight_blockers"])

    def test_blocks_product_identity_mismatch(self):
        stack, download, audit = evidence()
        audit["safe_root_name"] = "different.SAFE"
        record = BUILDER.build_readiness_record(stack, download, audit)
        self.assertIn("safe_root_name_does_not_match_catalogue_product_name", record["structural_preflight_blockers"])

    def test_blocks_failed_download_or_audit(self):
        stack, download, audit = evidence()
        download["validation"] = "failed"
        audit["structural_dual_pol_gate"] = "failed"
        record = BUILDER.build_readiness_record(stack, download, audit)
        self.assertIn("download_archive_validation_not_passed", record["structural_preflight_blockers"])
        self.assertIn("safe_structural_dual_polarisation_gate_not_passed", record["structural_preflight_blockers"])

    def test_blocks_missing_iw_grd_identity_check(self):
        stack, download, audit = evidence()
        del audit["checks"]["safe_root_name_is_sentinel1_iw_grd"]
        record = BUILDER.build_readiness_record(stack, download, audit)
        self.assertEqual(record["structural_preflight_status"], "blocked")
        self.assertIn("safe_audit_contains_missing_or_failed_checks", record["structural_preflight_blockers"])

    def test_blocks_failed_iw_grd_identity_checks(self):
        for check_name in ("safe_root_name_is_sentinel1_iw_grd", "manifest_identifies_iw_mode"):
            with self.subTest(check_name=check_name):
                stack, download, audit = evidence()
                audit["checks"][check_name] = False
                record = BUILDER.build_readiness_record(stack, download, audit)
                self.assertEqual(record["structural_preflight_status"], "blocked")
                self.assertIn("safe_audit_contains_missing_or_failed_checks", record["structural_preflight_blockers"])

    def test_rejects_unknown_product_id(self):
        stack, download, audit = evidence()
        download["product_id"] = "unknown-product"
        with self.assertRaisesRegex(ValueError, "found 0"):
            BUILDER.build_readiness_record(stack, download, audit)


if __name__ == "__main__":
    unittest.main()
