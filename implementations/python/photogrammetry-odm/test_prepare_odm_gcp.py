import hashlib
import json
from pathlib import Path
import tempfile
import unittest

from prepare_odm_gcp import prepare_gcp_list


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def make_fixture(root: Path, status: str = "locked"):
    dataset = root / "dataset"
    (dataset / "images").mkdir(parents=True)
    (dataset / "gcp").mkdir()
    (dataset / "images" / "img1.JPG").write_bytes(b"image-one")
    (dataset / "images" / "img2.JPG").write_bytes(b"image-two")
    (dataset / "README.md").write_text(
        "Original images, 100 × 80 px.\n", encoding="utf-8"
    )
    gcp = dataset / "gcp" / "GCP_MN95.txt"
    gcp.write_text(
        "P1 100.000 200.000 10.000\n"
        "P2 110.000 210.000 11.000\n"
        "P3 120.000 220.000 12.000\n",
        encoding="utf-8",
    )
    observations = dataset / "gcp" / "gcp_obs.csv"
    observations.write_text(
        "P1 img1 10 20\nP1 img2 30 40\n"
        "P2 img1 50 60\nP2 img2 70 70\n"
        "P3 img1 90 10\n",
        encoding="utf-8",
    )
    revision = "a" * 40
    manifest = root / "acquisition-provenance.json"
    manifest.write_text(json.dumps({
        "resolved_revision": revision,
        "selected_path": "datasets/drone_heig_2019",
    }), encoding="utf-8")
    split = root / "split.json"
    split.write_text(json.dumps({
        "status": status,
        "dataset": {
            "resolved_revision": revision,
            "selected_path": "datasets/drone_heig_2019",
            "source_files": {
                "README.md": digest(dataset / "README.md"),
                "gcp/GCP_MN95.txt": digest(gcp),
                "gcp/gcp_obs.csv": digest(observations),
            },
        },
        "selection": {
            "control_points": ["P1", "P2"],
            "checkpoint_points": ["P3"],
            "minimum_image_observations_per_point": 2,
        },
    }), encoding="utf-8")
    return dataset, split, manifest


class PrepareOdmGcpTests(unittest.TestCase):
    def test_exports_only_controls_and_binds_source_hashes(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            dataset, split, manifest = make_fixture(root)
            output = root / "gcp_list.txt"
            report = prepare_gcp_list(dataset, split, manifest, output)
            lines = output.read_text(encoding="utf-8").splitlines()
            self.assertEqual(lines[0], "EPSG:2056")
            self.assertEqual(len(lines) - 1, 4)
            self.assertTrue(all(line.endswith((" P1", " P2")) for line in lines[1:]))
            self.assertNotIn("P3", output.read_text(encoding="utf-8"))
            self.assertEqual(report["control_point_count"], 2)
            self.assertEqual(report["observation_record_count"], 4)
            self.assertEqual(report["vertical_reference"], "LN02")

    def test_proposed_split_requires_explicit_override(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            dataset, split, manifest = make_fixture(root, status="proposed_not_locked")
            with self.assertRaisesRegex(ValueError, "proposed_not_locked"):
                prepare_gcp_list(dataset, split, manifest, root / "gcp_list.txt")
            report = prepare_gcp_list(
                dataset, split, manifest, root / "gcp_list.txt", allow_proposed=True
            )
            self.assertEqual(report["status"], "prepared_provisional")

    def test_rejects_source_hash_mismatch(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            dataset, split, manifest = make_fixture(root)
            with (dataset / "gcp" / "GCP_MN95.txt").open("a", encoding="utf-8") as stream:
                stream.write("P4 130 230 13\n")
            with self.assertRaisesRegex(ValueError, "hash does not match"):
                prepare_gcp_list(dataset, split, manifest, root / "gcp_list.txt")

    def test_rejects_duplicate_control_coordinates(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            dataset, split, manifest = make_fixture(root)
            gcp = dataset / "gcp" / "GCP_MN95.txt"
            gcp.write_text(
                "P1 100 200 10\nP2 100 200 10\nP3 120 220 12\n",
                encoding="utf-8",
            )
            data = json.loads(split.read_text(encoding="utf-8"))
            data["dataset"]["source_files"]["gcp/GCP_MN95.txt"] = digest(gcp)
            split.write_text(json.dumps(data), encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "duplicate coordinates"):
                prepare_gcp_list(dataset, split, manifest, root / "gcp_list.txt")

    def test_rejects_pixel_outside_source_image_dimensions(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            dataset, split, manifest = make_fixture(root)
            obs = dataset / "gcp" / "gcp_obs.csv"
            obs.write_text(
                "P1 img1 10 20\nP1 img2 30 40\n"
                "P2 img1 50 60\nP2 img2 100 80\n",
                encoding="utf-8",
            )
            data = json.loads(split.read_text(encoding="utf-8"))
            data["dataset"]["source_files"]["gcp/gcp_obs.csv"] = digest(obs)
            split.write_text(json.dumps(data), encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "outside"):
                prepare_gcp_list(dataset, split, manifest, root / "gcp_list.txt")


if __name__ == "__main__":
    unittest.main()
