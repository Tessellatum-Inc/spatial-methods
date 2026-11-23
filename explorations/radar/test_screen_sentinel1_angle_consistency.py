"""Offline tests for local-incidence-angle consistency screening."""
import importlib.util
from pathlib import Path
import tempfile
import unittest

import numpy as np
import rasterio
from rasterio.transform import from_origin

ROOT = Path(__file__).resolve().parents[2]
SCRIPT = ROOT / "explorations" / "radar" / "screen_sentinel1_angle_consistency.py"
SPEC = importlib.util.spec_from_file_location("screen_sentinel1_angle_consistency", SCRIPT)
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


class AngleConsistencyTests(unittest.TestCase):
    def write_raster(self, path, angle, mask=None, transform=None):
        mask = np.ones(angle.shape, dtype=np.float32) if mask is None else mask.astype(np.float32)
        with rasterio.open(path, "w", driver="GTiff", width=angle.shape[1], height=angle.shape[0],
                           count=2, dtype="float32", crs="EPSG:4326",
                           transform=transform or from_origin(36.0, -1.0, 0.01, 0.01)) as ds:
            ds.write(angle.astype(np.float32), 1)
            ds.write(mask, 2)

    def test_reports_pixelwise_angle_differences(self):
        with tempfile.TemporaryDirectory() as tmp:
            a = Path(tmp) / "a.tif"
            b = Path(tmp) / "b.tif"
            self.write_raster(a, np.full((4, 4), 42.0))
            self.write_raster(b, np.full((4, 4), 42.05))
            report = MODULE.compare_angle_rasters([b, a])
            self.assertEqual(report["scene_count"], 2)
            self.assertAlmostEqual(report["comparisons"][0]["absolute_delta_degrees"]["median"], 0.05, places=5)
            self.assertFalse(report["analysis_ready"])

    def test_rejects_single_scene(self):
        with self.assertRaisesRegex(ValueError, "At least two"):
            MODULE.compare_angle_rasters([Path("one.tif")])

    def test_rejects_grid_mismatch(self):
        with tempfile.TemporaryDirectory() as tmp:
            a, b = Path(tmp) / "a.tif", Path(tmp) / "b.tif"
            self.write_raster(a, np.ones((4, 4)))
            self.write_raster(b, np.ones((4, 4)), transform=from_origin(36.1, -1.0, 0.01, 0.01))
            with self.assertRaisesRegex(ValueError, "identical grid"):
                MODULE.compare_angle_rasters([a, b])


if __name__ == "__main__":
    unittest.main()
