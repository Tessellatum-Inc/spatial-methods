"""Offline tests for paired ellipsoid/RTC comparison."""
import importlib.util
from pathlib import Path
import tempfile
import unittest

import numpy as np
import rasterio
from rasterio.transform import from_origin

ROOT = Path(__file__).resolve().parents[2]
SCRIPT = ROOT / "explorations" / "radar" / "compare_sentinel1_ellipsoid_vs_terrain.py"
SPEC = importlib.util.spec_from_file_location("compare_sentinel1_ellipsoid_vs_terrain", SCRIPT)
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


class PairedComparisonTests(unittest.TestCase):
    def test_compares_only_common_valid_positive_pixels(self):
        with tempfile.TemporaryDirectory() as tmp:
            base = np.ones((3, 2, 2), dtype=np.float32)
            base[0] = 0.1
            base[1] = 0.01
            base[2, 1, 1] = 0
            rtc = np.ones((6, 2, 2), dtype=np.float32)
            rtc[0] = 0.2
            rtc[1] = 0.02
            rtc[3] = 40  # Exercise the 40–45° local-incidence-angle stratum.
            rtc[4] = 0
            rtc[5] = 1
            rtc[5, 0, 1] = 0
            transform = from_origin(0, 2, 1, 1)
            epath, rpath = Path(tmp) / "ell.tif", Path(tmp) / "rtc.tif"
            for path, array in ((epath, base), (rpath, rtc)):
                with rasterio.open(path, "w", driver="GTiff", width=2, height=2,
                                   count=array.shape[0], dtype="float32",
                                   crs="EPSG:4326", transform=transform) as dst:
                    dst.write(array)
            report = MODULE.compare_pair(epath, rpath)
            self.assertEqual(report["common_valid_pixels"], 2)
            strata = report["polarizations"]["VV"]["stratified_differences"]
            area_bin = next(x for x in strata["scattering_area"] if x["stratum"] == "1.0–1.1")
            angle_bin = next(x for x in strata["local_incidence_angle_degrees"] if x["stratum"] == "40–45°")
            self.assertEqual(area_bin["pixels"], 2)
            self.assertEqual(angle_bin["pixels"], 2)
            self.assertAlmostEqual(
                report["polarizations"]["VV"]["rtc_minus_ellipsoid_db"]["median"],
                10 * np.log10(2), places=5
            )

    def test_scattering_area_factor_relation_reports_residuals(self):
        area = np.array([0.5, 1.0, 2.0], dtype=np.float64)
        expected = -10.0 * np.log10(area)
        observed = expected + np.array([0.1, -0.2, 0.05])
        report = MODULE._area_factor_relation(observed, area)
        self.assertEqual(report["pixels"], 3)
        self.assertAlmostEqual(report["median_absolute_residual_db"], 0.1, places=6)
        self.assertAlmostEqual(report["median_observed_minus_predicted_db"], 0.05, places=6)
        self.assertAlmostEqual(report["median_absolute_centered_residual_db"], 0.05, places=6)
        self.assertAlmostEqual(report["p95_absolute_centered_residual_db"], 0.23, places=2)
        self.assertGreater(report["observed_predicted_pearson_r"], 0.99)

    def test_rejects_mismatched_grids(self):
        with tempfile.TemporaryDirectory() as tmp:
            base = np.ones((3, 2, 2), dtype=np.float32)
            rtc = np.ones((6, 2, 2), dtype=np.float32)
            for name, array, x in (("ell.tif", base, 0), ("rtc.tif", rtc, 1)):
                with rasterio.open(Path(tmp) / name, "w", driver="GTiff", width=2, height=2,
                                   count=array.shape[0], dtype="float32",
                                   crs="EPSG:4326", transform=from_origin(x, 2, 1, 1)) as dst:
                    dst.write(array)
            with self.assertRaisesRegex(ValueError, "identical grids"):
                MODULE.compare_pair(Path(tmp) / "ell.tif", Path(tmp) / "rtc.tif")


if __name__ == "__main__":
    unittest.main()
