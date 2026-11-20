import json
from pathlib import Path
import tempfile
import unittest

from dataset_audit import inspect_images, sha256_file


class DatasetAuditTests(unittest.TestCase):
    def test_manifest_hash_and_expected_count(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            image = root / "nested" / "frame01.JPG"
            image.parent.mkdir()
            image.write_bytes(b"fixture bytes")
            report = inspect_images(root, expected_count=1)
            self.assertEqual(report["image_count"], 1)
            self.assertTrue(report["image_count_matches_expectation"])
            self.assertEqual(report["images"][0]["sha256"], sha256_file(image))
            self.assertEqual(report["images"][0]["path"], "nested/frame01.JPG")

    def test_count_mismatch_is_reported_not_silently_accepted(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "one.jpg").write_bytes(b"one")
            report = inspect_images(root, expected_count=32)
            self.assertFalse(report["image_count_matches_expectation"])

    def test_valid_image_metadata_when_pillow_is_available(self):
        try:
            from PIL import Image
        except ImportError:
            self.skipTest("Pillow is optional")
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            Image.new("RGB", (7, 5)).save(root / "frame.jpg", format="JPEG")
            report = inspect_images(root, expected_count=1)
            self.assertEqual(report["valid_images"], 1)
            self.assertEqual(report["images"][0]["width_px"], 7)
            self.assertEqual(report["images"][0]["height_px"], 5)

    def test_empty_dataset_is_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            with self.assertRaises(ValueError):
                inspect_images(Path(tmp))


if __name__ == "__main__":
    unittest.main()
