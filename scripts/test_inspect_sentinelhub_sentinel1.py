"""Tests for Sentinel-1 raster quality inspection."""
import importlib.util
from pathlib import Path
import tempfile
import unittest

import numpy as np
import rasterio
from rasterio.transform import from_bounds

ROOT = Path(__file__).resolve().parents[1]
PATH = ROOT / "explorations" / "radar" / "inspect_sentinelhub_sentinel1.py"
SPEC = importlib.util.spec_from_file_location("inspect_sentinelhub_sentinel1", PATH)
CLIENT = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(CLIENT)


class RasterInspectionTests(unittest.TestCase):
    def _write_test_raster(self, path, mask=None):
        width, height = 20, 10
        if mask is None:
            mask = np.ones((height, width), dtype=np.float32)
        profile = {
            "driver": "GTiff", "width": width, "height": height, "count": 3,
            "dtype": "float32", "crs": "EPSG:4326",
            "transform": from_bounds(36.65, -1.45, 37.05, -1.15, width, height),
        }
        with rasterio.open(path, "w", **profile) as ds:
            ds.write(np.full((height, width), 0.2, dtype=np.float32), 1)
            ds.write(np.full((height, width), 0.03, dtype=np.float32), 2)
            ds.write(mask.astype(np.float32), 3)

    def test_creates_quicklook_and_report_for_full_coverage(self):
        with tempfile.TemporaryDirectory() as tmp:
            source = Path(tmp) / "sample.tif"
            self._write_test_raster(source)
            quicklook, report_path, report = CLIENT.inspect_raster(source, Path(tmp))
            self.assertTrue(quicklook.is_file())
            self.assertTrue(report_path.is_file())
            self.assertEqual(report["quality_status"], "pass")
            self.assertEqual(report["data_mask"]["valid_percent"], 100.0)
            self.assertEqual(report["backscatter"]["VV"]["count"], 200)

    def test_flags_partial_coverage_without_treating_it_as_failure(self):
        with tempfile.TemporaryDirectory() as tmp:
            source = Path(tmp) / "partial.tif"
            mask = np.zeros((10, 20), dtype=np.float32)
            mask[:, :15] = 1
            self._write_test_raster(source, mask)
            _, _, report = CLIENT.inspect_raster(source, Path(tmp))
            self.assertEqual(report["quality_status"], "partial_coverage")
            self.assertEqual(report["data_mask"]["valid_percent"], 75.0)

    def test_rejects_mask_with_nonbinary_values(self):
        with tempfile.TemporaryDirectory() as tmp:
            source = Path(tmp) / "bad-mask.tif"
            mask = np.ones((10, 20), dtype=np.float32)
            mask[0, 0] = 0.5
            self._write_test_raster(source, mask)
            with self.assertRaisesRegex(ValueError, "only 0 and 1"):
                CLIENT.inspect_raster(source, Path(tmp))

    def test_rejects_nonfinite_valid_backscatter(self):
        with tempfile.TemporaryDirectory() as tmp:
            source = Path(tmp) / "bad-values.tif"
            self._write_test_raster(source)
            with rasterio.open(source, "r+") as ds:
                vv = ds.read(1)
                vv[0, 0] = np.nan
                ds.write(vv, 1)
            with self.assertRaisesRegex(ValueError, "non-finite values inside"):
                CLIENT.inspect_raster(source, Path(tmp))

    def test_rejects_no_valid_pixels(self):
        with tempfile.TemporaryDirectory() as tmp:
            source = Path(tmp) / "empty.tif"
            self._write_test_raster(source, np.zeros((10, 20), dtype=np.float32))
            with self.assertRaisesRegex(ValueError, "no valid data"):
                CLIENT.inspect_raster(source, Path(tmp))


if __name__ == "__main__":
    unittest.main()
