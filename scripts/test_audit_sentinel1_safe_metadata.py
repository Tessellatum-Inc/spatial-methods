"""Offline tests for the Sentinel-1 SAFE metadata audit."""
from pathlib import Path
import tempfile
import unittest
import zipfile

from explorations.radar.audit_sentinel1_safe_metadata import audit_archive


ROOT = "S1C_IW_GRDH_1SDV_20261102T031112_20261102T031137_010152_01443B_5D46.SAFE"
MANIFEST = """<?xml version="1.0" encoding="UTF-8"?>
<xfdu xmlns:s1="urn:sentinel">
  <s1:transmitterReceiverPolarisation>VV</s1:transmitterReceiverPolarisation>
  <s1:transmitterReceiverPolarisation>VH</s1:transmitterReceiverPolarisation>
  <s1:mode>IW</s1:mode>
</xfdu>
"""


def members(polarisations=("vv", "vh")):
    files = {f"{ROOT}/manifest.safe": MANIFEST}
    for pol in polarisations:
        base = f"s1c-iw-grd-{pol}-20261102t031112-20261102t031137-010152-01443b-004"
        files[f"{ROOT}/measurement/{base}.tiff"] = "raster-placeholder"
        files[f"{ROOT}/annotation/{base}.xml"] = "<annotation/>"
        files[f"{ROOT}/calibration/calibration-{base}.xml"] = "<calibration/>"
        files[f"{ROOT}/annotation/noise-{base}.xml"] = "<noise/>"
    return files


class SafeMetadataAuditTests(unittest.TestCase):
    def make_archive(self, directory, content):
        path = Path(directory) / "sample.SAFE.zip"
        with zipfile.ZipFile(path, "w", compression=zipfile.ZIP_DEFLATED) as archive:
            for name, value in content.items():
                archive.writestr(name, value)
        return path

    def test_passes_complete_dual_pol_file_set(self):
        with tempfile.TemporaryDirectory() as directory:
            path = self.make_archive(directory, members())
            report = audit_archive(path, ROOT)
            self.assertEqual(report["structural_dual_pol_gate"], "passed")
            self.assertEqual(report["measurement_polarisations"], ["vh", "vv"])
            self.assertTrue(report["checks"]["product_name_matches_expected"])
            self.assertEqual(report["scientific_processing_status"], "not_started")

    def test_fails_when_vh_measurement_is_missing(self):
        with tempfile.TemporaryDirectory() as directory:
            path = self.make_archive(directory, members(("vv",)))
            report = audit_archive(path)
            self.assertEqual(report["structural_dual_pol_gate"], "failed")
            self.assertFalse(report["checks"]["measurement_contains_vv_and_vh"])

    def test_fails_when_calibration_annotation_is_missing_for_one_pol(self):
        content = members()
        del content[f"{ROOT}/calibration/calibration-s1c-iw-grd-vh-20261102t031112-20261102t031137-010152-01443b-004.xml"]
        with tempfile.TemporaryDirectory() as directory:
            path = self.make_archive(directory, content)
            report = audit_archive(path)
            self.assertFalse(report["checks"]["calibration_contains_vv_and_vh"])

    def test_rejects_path_traversal_member(self):
        content = members()
        content[f"{ROOT}/../outside.txt"] = "bad"
        with tempfile.TemporaryDirectory() as directory:
            path = self.make_archive(directory, content)
            with self.assertRaisesRegex(ValueError, "Unsafe path"):
                audit_archive(path)

    def test_rejects_malformed_manifest_xml(self):
        content = members()
        content[f"{ROOT}/manifest.safe"] = "<not-closed>"
        with tempfile.TemporaryDirectory() as directory:
            path = self.make_archive(directory, content)
            with self.assertRaises(Exception):
                audit_archive(path)


if __name__ == "__main__":
    unittest.main()
