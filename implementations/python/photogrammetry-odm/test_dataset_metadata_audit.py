from pathlib import Path
import tempfile
import unittest

from dataset_metadata_audit import audit_dataset


def write_fixture(root: Path) -> None:
    images = root / "images"
    gcp = root / "gcp"
    images.mkdir(parents=True)
    gcp.mkdir()
    for name in ("EB-02-00761_0101_0031.JPG", "EB-02-00761_0101_0032.JPG"):
        (images / name).write_bytes(b"not decoded by metadata audit")
    (gcp / "GCP_MN95.txt").write_text(
        "# label E N H\n"
        "100 2540494.457 1181192.243 447.344\n"
        "206 2540494.457 1181192.243 447.344\n",
        encoding="utf-8",
    )
    (gcp / "gcp_obs.csv").write_text(
        "# gcp_label image_label x y\n"
        "206 EB-02-00761_0101_0031 100.0 200.0\n"
        "206 EB-02-00761_0101_0032 300.0 400.0\n",
        encoding="utf-8",
    )
    identity = "1 0 0 0 1 0 0 0 1"
    (root / "opk.txt").write_text(
        "# Cameras (105)\n"
        "# PhotoID X Y Z Omega Phi Kappa r11 r12 r13 r21 r22 r23 r31 r32 r33\n"
        f"0101_0031.JPG 1 2 3 0 0 0 {identity}\n"
        f"0101_0032.JPG 4 5 6 0 0 0 {identity}\n",
        encoding="utf-8",
    )


class DatasetMetadataAuditTests(unittest.TestCase):
    def test_audits_counts_duplicate_coordinates_and_filename_mapping(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            write_fixture(root)
            report = audit_dataset(
                root,
                expected_images=2,
                expected_ground_points=2,
                expected_observations=2,
                expected_observed_points=1,
                expected_orientations=2,
            )
            self.assertTrue(all(report["count_matches"].values()))
            self.assertEqual(report["ground_points_without_image_observations"], ["100"])
            self.assertEqual(report["duplicate_coordinate_groups_within_1e-6_m"], [["100", "206"]])
            self.assertEqual(report["observation_images_missing_from_images_directory"], [])
            self.assertEqual(report["opk_photo_ids_without_matching_image"], [])
            self.assertEqual(report["observation_images_without_matching_opk"], [])
            self.assertAlmostEqual(report["opk_rotation_max_orthogonality_error"], 0.0)
            self.assertAlmostEqual(report["opk_rotation_determinant_range"][0], 1.0)

    def test_count_mismatch_is_reported(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            write_fixture(root)
            report = audit_dataset(root)
            self.assertFalse(report["count_matches"]["images"])
            self.assertFalse(report["count_matches"]["observations"])

    def test_rejects_nonfinite_coordinates(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            write_fixture(root)
            path = root / "gcp" / "GCP_MN95.txt"
            path.write_text("100 nan 2 3\n", encoding="utf-8")
            with self.assertRaises(ValueError):
                audit_dataset(root)

    def test_rejects_malformed_opk_record(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            write_fixture(root)
            (root / "opk.txt").write_text("0101_0031.JPG 1 2 3\n", encoding="utf-8")
            with self.assertRaises(ValueError):
                audit_dataset(root)


if __name__ == "__main__":
    unittest.main()
