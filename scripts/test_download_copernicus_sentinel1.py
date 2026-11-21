"""Offline tests for the Copernicus Sentinel-1 SAFE download validator."""
import importlib.util
from pathlib import Path
import tempfile
import unittest
import zipfile

MODULE_PATH = Path(__file__).resolve().parents[1] / "explorations" / "radar" / "download_copernicus_sentinel1.py"
SPEC = importlib.util.spec_from_file_location("download_copernicus_sentinel1", MODULE_PATH)
DOWNLOAD = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(DOWNLOAD)


class Sentinel1DownloadValidationTests(unittest.TestCase):
    PRODUCT_ID = "6b4943ac-6e85-4e36-bc25-e271fb5e63a9"

    def test_accepts_canonical_product_uuid(self):
        self.assertEqual(DOWNLOAD.validate_product_id(self.PRODUCT_ID), self.PRODUCT_ID)

    def test_rejects_non_uuid_product_id(self):
        with self.assertRaisesRegex(ValueError, "valid UUID"):
            DOWNLOAD.validate_product_id("../../not-a-uuid")

    def test_requires_canonical_uuid_format(self):
        with self.assertRaisesRegex(ValueError, "canonical UUID"):
            DOWNLOAD.validate_product_id("6b4943ac6e854e36bc25e271fb5e63a9")

    def test_rejects_redirect_to_untrusted_host(self):
        handler = DOWNLOAD.DataspaceRedirectHandler()
        request = DOWNLOAD.Request("https://download.dataspace.copernicus.eu/file")
        with self.assertRaisesRegex(Exception, "untrusted host"):
            handler.redirect_request(
                request, None, 302, "Found", {}, "https://example.com/steal-token"
            )

    def test_accepts_safe_archive_with_required_members_and_crc(self):
        with tempfile.TemporaryDirectory() as directory:
            archive_path = Path(directory) / "candidate.zip"
            with zipfile.ZipFile(archive_path, "w", zipfile.ZIP_DEFLATED) as archive:
                archive.writestr("candidate.SAFE/manifest.safe", "<manifest/>")
                archive.writestr("candidate.SAFE/measurement/s1-vv.tiff", "raster")
                archive.writestr("candidate.SAFE/annotation/s1.xml", "<annotation/>")
            result = DOWNLOAD.validate_safe_archive(archive_path)
            self.assertEqual(result["measurement_file_count"], 1)
            self.assertEqual(result["annotation_file_count"], 1)
            self.assertEqual(result["manifest"], "candidate.safe/manifest.safe")

    def test_rejects_non_zip_download(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "not-a-zip.zip"
            path.write_text("not a zip")
            with self.assertRaisesRegex(ValueError, "not a valid ZIP"):
                DOWNLOAD.validate_safe_archive(path)

    def test_rejects_safe_archive_without_measurement(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "incomplete.zip"
            with zipfile.ZipFile(path, "w") as archive:
                archive.writestr("candidate.SAFE/manifest.safe", "<manifest/>")
                archive.writestr("candidate.SAFE/annotation/s1.xml", "<annotation/>")
            with self.assertRaisesRegex(ValueError, "no measurement GeoTIFF"):
                DOWNLOAD.validate_safe_archive(path)

    def test_requires_credentials_without_network_access(self):
        with self.assertRaisesRegex(ValueError, "CDSE_USERNAME and CDSE_PASSWORD"):
            DOWNLOAD.request_access_token("", "")


if __name__ == "__main__":
    unittest.main()
