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
        area = np.array([0.25, 0.5, 1.0, 2.0], dtype=np.float64)
        expected = -10.0 * np.log10(area)
        observed = 2.0 * expected + 0.25
        angle = np.array([30.0, 37.0, 42.0, 47.0], dtype=np.float64)
        report = MODULE._area_factor_relation(observed, area, angle)
        self.assertEqual(report["pixels"], 4)
        self.assertAlmostEqual(report["median_absolute_residual_db"], float(np.median(np.abs(expected + 0.25))), places=12)
        self.assertAlmostEqual(report["median_observed_minus_predicted_db"], float(np.median(expected + 0.25)), places=12)
        centered_expected = expected - np.median(expected)
        self.assertAlmostEqual(
            report["median_absolute_centered_residual_db"],
            float(np.median(np.abs(centered_expected))), places=12
        )
        self.assertAlmostEqual(
            report["p95_absolute_centered_residual_db"],
            float(np.percentile(np.abs(centered_expected), 95)), places=12
        )
        self.assertAlmostEqual(report["observed_predicted_pearson_r"], 1.0, places=12)
        self.assertAlmostEqual(report["observed_on_predicted_ols_slope"], 2.0, places=12)
        self.assertAlmostEqual(report["observed_on_predicted_ols_intercept_db"], 0.25, places=12)
        self.assertAlmostEqual(report["observed_on_predicted_ols_r_squared"], 1.0, places=12)
        angle_bins = report["centered_residual_by_local_incidence_angle_degrees"]
        self.assertEqual([item["pixels"] for item in angle_bins], [1, 1, 1, 1, 0])
        area_bins = report["centered_residual_by_scattering_area"]
        self.assertEqual([item["pixels"] for item in area_bins], [2, 0, 1, 0, 1])


    def test_spatial_holdout_detects_incremental_angle_dependence(self):
        height = width = 1024
        rows, cols = np.indices((height, width))
        rows, cols = rows.ravel(), cols.ravel()
        factor = -2.0 + 4.0 * cols / (width - 1)
        area = 10.0 ** (-factor / 10.0)
        angle = 35.0 + 15.0 * rows / (height - 1)
        angle_scaled = (angle - 45.0) / 10.0
        rng = np.random.default_rng(42)
        delta = 0.4 + 0.8 * factor + 0.18 * angle_scaled + 0.12 * factor * angle_scaled
        delta += rng.normal(0.0, 0.03, size=delta.shape)

        report = MODULE._spatial_holdout_residual_model(
            delta, area, angle, rows, cols, height, width,
            tile_size=256, buffer_pixels=16,
        )
        self.assertEqual(report["status"], "screening_only")
        self.assertGreater(report["train_pixels"], 1000)
        self.assertGreater(report["test_pixels"], 1000)
        self.assertGreater(report["test_rmse_reduction_fraction"], 0.2)
        self.assertLess(
            report["area_plus_angle_test_metrics"]["rmse_db"],
            report["area_only_test_metrics"]["rmse_db"],
        )


    def test_leave_one_acquisition_out_model_transfers_across_dates(self):
        rng = np.random.default_rng(7)
        scenes = []
        for index in range(4):
            area_factor = rng.uniform(-2.0, 2.0, 12000)
            area = 10.0 ** (-area_factor / 10.0)
            angle = rng.uniform(35.0, 55.0, 12000)
            angle_scaled = (angle - 45.0) / 10.0
            delta = 0.35 + 0.9 * area_factor + 0.2 * angle_scaled
            delta += 0.1 * area_factor * angle_scaled
            delta += rng.normal(0.0, 0.025, size=delta.shape)
            scenes.append({
                "file": f"scene-{index}.tif",
                "polarizations": {
                    "VV": {
                        "delta_db": delta.astype(np.float32),
                        "scattering_area": area.astype(np.float32),
                        "local_incidence_angle_degrees": angle.astype(np.float32),
                    }
                },
            })

        report = MODULE._temporal_holdout_residual_model(scenes, "VV")
        self.assertEqual(report["status"], "screening_only")
        self.assertEqual(report["validation"], "leave_one_acquisition_out")
        self.assertEqual(len(report["folds"]), 4)
        for fold in report["folds"]:
            self.assertEqual(fold["test_pixels"], 12000)
            self.assertGreater(fold["test_rmse_reduction_fraction"], 0.2)
            self.assertLess(
                fold["area_plus_angle_test_metrics"]["rmse_db"],
                fold["area_only_test_metrics"]["rmse_db"],
            )

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
