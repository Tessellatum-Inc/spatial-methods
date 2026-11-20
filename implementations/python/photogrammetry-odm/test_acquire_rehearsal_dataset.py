import hashlib
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from acquire_rehearsal_dataset import (
    build_manifest,
    revision_snapshot_dir,
    sha256_file,
)


class AcquisitionManifestTests(unittest.TestCase):
    def test_each_revision_uses_an_isolated_snapshot_directory(self):
        with tempfile.TemporaryDirectory() as tmp:
            destination = Path(tmp)
            first = "a" * 40
            second = "b" * 40
            self.assertEqual(
                revision_snapshot_dir(destination, first),
                destination / "snapshots" / first,
            )
            self.assertNotEqual(
                revision_snapshot_dir(destination, first),
                revision_snapshot_dir(destination, second),
            )

    def test_manifest_excludes_files_from_other_revision_snapshots(self):
        with tempfile.TemporaryDirectory() as tmp:
            destination = Path(tmp)
            old_revision = "a" * 40
            new_revision = "b" * 40
            old_dataset = revision_snapshot_dir(destination, old_revision) / "datasets" / "drone_heig_2019"
            new_dataset = revision_snapshot_dir(destination, new_revision) / "datasets" / "drone_heig_2019"
            old_dataset.mkdir(parents=True)
            new_dataset.mkdir(parents=True)
            (old_dataset / "stale.txt").write_text("old revision", encoding="utf-8")
            (new_dataset / "current.txt").write_text("new revision", encoding="utf-8")

            with patch("acquire_rehearsal_dataset.version", return_value="1.2.3"):
                manifest = build_manifest(
                    revision_snapshot_dir(destination, new_revision),
                    new_dataset,
                    new_revision,
                )

            self.assertEqual(manifest["file_count"], 1)
            self.assertEqual(
                [item["path"] for item in manifest["files"]],
                ["datasets/drone_heig_2019/current.txt"],
            )

    def test_invalid_revision_is_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            with self.assertRaises(ValueError):
                revision_snapshot_dir(Path(tmp), "../../stale")

    def test_sha256_file_matches_known_digest(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "sample.bin"
            path.write_bytes(b"spatial methods")
            self.assertEqual(
                sha256_file(path),
                hashlib.sha256(b"spatial methods").hexdigest(),
            )

    def test_manifest_records_sorted_relative_paths_sizes_and_hashes(self):
        with tempfile.TemporaryDirectory() as tmp:
            destination = Path(tmp)
            dataset = destination / "datasets" / "drone_heig_2019"
            dataset.mkdir(parents=True)
            (dataset / "z.txt").write_bytes(b"last")
            (dataset / "a.txt").write_bytes(b"first")

            with patch("acquire_rehearsal_dataset.version", return_value="1.2.3"):
                manifest = build_manifest(destination, dataset, "abc123")

            self.assertEqual(manifest["resolved_revision"], "abc123")
            self.assertEqual(manifest["file_count"], 2)
            self.assertEqual(
                [item["path"] for item in manifest["files"]],
                [
                    "datasets/drone_heig_2019/a.txt",
                    "datasets/drone_heig_2019/z.txt",
                ],
            )
            self.assertEqual(manifest["files"][0]["size_bytes"], 5)
            self.assertEqual(
                manifest["files"][0]["sha256"],
                hashlib.sha256(b"first").hexdigest(),
            )
            self.assertEqual(manifest["huggingface_hub_version"], "1.2.3")
            self.assertTrue(manifest["retrieved_at_utc"].endswith("+00:00"))

    def test_empty_dataset_is_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            destination = Path(tmp)
            dataset = destination / "datasets" / "drone_heig_2019"
            dataset.mkdir(parents=True)
            with self.assertRaises(RuntimeError):
                build_manifest(destination, dataset, "abc123")


if __name__ == "__main__":
    unittest.main()
