"Offline tests for the Sentinel-1 stack manifest builder."""
import importlib.util
from pathlib import Path
import tempfile
import unittest

MODULE_PATH = Path(__file__).resolve().parents[1] / "explorations" / "radar" / "build_sentinel1_stack_manifest.py"
SPEC = importlib.util.spec_from_file_location("build_sentinel1_stack_manifest", MODULE_PATH)
BUILDER = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(BUILDER)

HEADER = (
    "product_id,product_name,sensing_start_utc,orbit_direction,relative_orbit,"
    "platform,polarisation_channels,product_composition,slice_number,total_slices,"
    "online,covers_study_aoi,location_formats,download_links\n"
)
ELIGIBLE = (
    "6b4943ac-6e85-4e36-bc25-e271fb5e63a9,"
    "S1C_IW_GRDH_1SDV_20261009T031112.SAFE,2026-10-09T03:11:12Z,"
    "DESCENDING,79,C,VV&VH,Slice,4,11,True,True,Extracted,"
    "https://example.test/product\n"
)
EXCLUDED = (
    "973bc555-cb21-4e26-aa89-a03d21601eb9,"
    "S1D_IW_GRDH_1SDV_20261006T155531.SAFE,2026-10-06T15:55:31Z,"
    "ASCENDING,130,D,VV&VH,Slice,7,11,True,False,Extracted,\n"
)


class StackManifestTests(unittest.TestCase):
    def write_inventory(self, directory, content):
        path = Path(directory) / "inventory.csv"
        path.write_text(HEADER + content, encoding="utf-8")
        return path

    def test_selects_only_matching_full_aoi_candidates(self):
        with tempfile.TemporaryDirectory() as directory:
            path = self.write_inventory(directory, ELIGIBLE + EXCLUDED)
            rows, digest = BUILDER.load_inventory(path)
            manifest = BUILDER.build_manifest(rows, digest)
            self.assertEqual(manifest["inventory_row_count"], 2)
            self.assertEqual(manifest["candidate_count"], 1)
            self.assertEqual(
                manifest["candidates"][0]["product_id"],
                "6b4943ac-6e85-4e36-bc25-e271fb5e63a9",
            )
            self.assertFalse(manifest["analysis_ready"])
            self.assertFalse(manifest["candidates"][0]["analysis_ready"])
            self.assertEqual(len(manifest["excluded_inventory_records"]), 1)
            self.assertIn(
                "catalogue footprint audit does not cover study AOI",
                manifest["excluded_inventory_records"][0]["exclusion_reasons"],
            )

    def test_preserves_slice_context_and_download_links(self):
        with tempfile.TemporaryDirectory() as directory:
            path = self.write_inventory(directory, ELIGIBLE)
            rows, digest = BUILDER.load_inventory(path)
            item = BUILDER.build_manifest(rows, digest)["candidates"][0]
            self.assertEqual(item["slice_number"], 4)
            self.assertEqual(item["total_slices"], 11)
            self.assertEqual(item["download_links"], ["https://example.test/product"])

    def test_rejects_duplicate_product_ids(self):
        with tempfile.TemporaryDirectory() as directory:
            path = self.write_inventory(directory, ELIGIBLE + ELIGIBLE)
            with self.assertRaisesRegex(ValueError, "duplicate product_id"):
                BUILDER.load_inventory(path)

    def test_rejects_naive_acquisition_timestamp(self):
        bad = ELIGIBLE.replace("2026-10-09T03:11:12Z", "2026-10-09T03:11:12")
        with tempfile.TemporaryDirectory() as directory:
            path = self.write_inventory(directory, bad)
            with self.assertRaisesRegex(ValueError, "needs a timezone"):
                BUILDER.load_inventory(path)

    def test_rejects_non_boolean_coverage_flag(self):
        bad = ELIGIBLE.replace(",True,True,Extracted,", ",True,maybe,Extracted,")
        with tempfile.TemporaryDirectory() as directory:
            path = self.write_inventory(directory, bad)
            with self.assertRaisesRegex(ValueError, "covers_study_aoi must be True or False"):
                BUILDER.load_inventory(path)


if __name__ == "__main__":
    unittest.main()
