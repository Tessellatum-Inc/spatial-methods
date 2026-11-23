import hashlib
import json
from pathlib import Path
import tempfile
import unittest

from verify_acquisition import verify_manifest


class AcquisitionVerificationTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        self.dataset = self.root / "datasets" / "drone_heig_2019"
        self.dataset.mkdir(parents=True)
        self.file = self.dataset / "image.txt"
        self.file.write_text("source bytes", encoding="utf-8")
        self.manifest = self.root / "acquisition-provenance.json"
        self.write_manifest()

    def tearDown(self):
        self.tmp.cleanup()

    def write_manifest(self, files=None):
        entries = files if files is not None else [{
            "path": "datasets/drone_heig_2019/image.txt",
            "size_bytes": self.file.stat().st_size,
            "sha256": hashlib.sha256(self.file.read_bytes()).hexdigest(),
        }]
        self.manifest.write_text(json.dumps({
            "resolved_revision": "a" * 40,
            "selected_path": "datasets/drone_heig_2019",
            "repository_id": "heig-vd-geo/scop-datasets",
            "file_count": len(entries),
            "files": entries,
        }), encoding="utf-8")

    def test_matching_file_is_verified(self):
        report = verify_manifest(self.manifest)
        self.assertEqual(report["status"], "verified")
        self.assertEqual(report["verified_file_count"], 1)

    def test_modified_file_is_reported_as_mismatch(self):
        self.file.write_text("changed bytes", encoding="utf-8")
        report = verify_manifest(self.manifest)
        self.assertEqual(report["status"], "integrity_error")
        self.assertEqual(report["mismatched_or_invalid_file_count"], 1)

    def test_missing_file_is_reported(self):
        self.file.unlink()
        report = verify_manifest(self.manifest)
        self.assertEqual(report["missing_file_count"], 1)
        self.assertEqual(report["status"], "integrity_error")

    def test_unmanifested_extra_file_is_reported(self):
        (self.dataset / "unexpected.txt").write_text("extra", encoding="utf-8")
        report = verify_manifest(self.manifest)
        self.assertEqual(report["unmanifested_files"], ["datasets/drone_heig_2019/unexpected.txt"])
        self.assertEqual(report["status"], "integrity_error")

    def test_path_traversal_is_rejected(self):
        self.write_manifest([{
            "path": "../../outside.txt", "size_bytes": 0, "sha256": "x"
        }])
        with self.assertRaises(ValueError):
            verify_manifest(self.manifest)

    def test_wrong_dataset_root_is_rejected(self):
        data = json.loads(self.manifest.read_text(encoding="utf-8"))
        data["selected_path"] = "datasets/other"
        self.manifest.write_text(json.dumps(data), encoding="utf-8")
        with self.assertRaises(ValueError):
            verify_manifest(self.manifest)

    def test_wrong_file_count_is_rejected(self):
        data = json.loads(self.manifest.read_text(encoding="utf-8"))
        data["file_count"] = 99
        self.manifest.write_text(json.dumps(data), encoding="utf-8")
        with self.assertRaises(ValueError):
            verify_manifest(self.manifest)



    def test_symlinked_manifest_path_component_is_rejected(self):
        real_dir = self.root / "real"
        real_dir.mkdir()
        target = real_dir / "payload.txt"
        target.write_text("source bytes", encoding="utf-8")
        link_dir = self.dataset / "linked"
        link_dir.symlink_to(real_dir, target_is_directory=True)
        self.write_manifest([{
            "path": "datasets/drone_heig_2019/linked/payload.txt",
            "size_bytes": target.stat().st_size,
            "sha256": hashlib.sha256(target.read_bytes()).hexdigest(),
        }])
        report = verify_manifest(self.manifest)
        self.assertEqual(report["status"], "integrity_error")
        self.assertEqual(report["files"][0]["status"], "invalid")

    def test_unmanifested_symlink_directory_is_reported(self):
        target = self.root / "external"
        target.mkdir()
        (target / "payload.txt").write_text("outside", encoding="utf-8")
        (self.dataset / "linked").symlink_to(target, target_is_directory=True)
        report = verify_manifest(self.manifest)
        self.assertEqual(report["status"], "integrity_error")
        self.assertEqual(report["symbolic_link_paths"], ["datasets/drone_heig_2019/linked"])

if __name__ == "__main__":
    unittest.main()
