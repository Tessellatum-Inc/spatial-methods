import unittest
import numpy as np
from explorations.radar.spatial_subsampling import spatial_subsampling_mean_interval


class SpatialSubsamplingTests(unittest.TestCase):
    def test_interval_matches_manual_subwindow_inversion(self):
        grid = np.arange(36, dtype=float).reshape(6, 6)
        result = spatial_subsampling_mean_interval(
            np.arange(36), grid.ravel(), grid_rows=6, grid_columns=6,
            subsample_width_blocks=3, min_subwindows=1,
        )
        means = np.array([grid[r:r+3, c:c+3].mean()
                          for r in range(4) for c in range(4)])
        stats = 3 * (means-grid.mean())
        qlo, qhi = np.quantile(stats, [0.025, 0.975])
        self.assertAlmostEqual(result["lower"], grid.mean()-qhi/3)
        self.assertAlmostEqual(result["upper"], grid.mean()-qlo/3)
        self.assertEqual(result["subwindows"], 16)

    def test_irregular_mask_is_not_silently_rescaled(self):
        result = spatial_subsampling_mean_interval(
            [0, 1, 3, 4], [1., 2., 3., 4.], grid_rows=2, grid_columns=3,
            subsample_width_blocks=1,
        )
        self.assertEqual(result["interval_status"], "irregular_mask_unsupported")
        self.assertIsNone(result["lower"])

    def test_constant_grid_returns_zero_width_interval(self):
        result = spatial_subsampling_mean_interval(
            np.arange(25), np.full(25, 2.5), grid_rows=5, grid_columns=5,
            subsample_width_blocks=2, min_subwindows=1,
        )
        self.assertEqual(result["interval_status"], "spatial_subsampling")
        self.assertEqual(result["lower"], 2.5)
        self.assertEqual(result["upper"], 2.5)

    def test_rejects_invalid_grid_and_width(self):
        with self.assertRaises(ValueError):
            spatial_subsampling_mean_interval([0], [1.], grid_rows=0,
                                              grid_columns=1, subsample_width_blocks=1)
        with self.assertRaises(ValueError):
            spatial_subsampling_mean_interval([0], [1.], grid_rows=1,
                                              grid_columns=1, subsample_width_blocks=0)


if __name__ == "__main__":
    unittest.main()
