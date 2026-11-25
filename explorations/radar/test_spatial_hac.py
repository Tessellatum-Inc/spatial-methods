import unittest

import numpy as np

from explorations.radar.spatial_hac import spatial_hac_mean_interval


class SpatialHacTests(unittest.TestCase):
    def test_bandwidth_one_is_diagonal_only(self):
        values = np.array([1.0, 2.0, 4.0, 7.0])
        ids = np.array([0, 1, 4, 5])
        result = spatial_hac_mean_interval(
            ids, values, grid_columns=4, bandwidth_rows=1, min_blocks=2
        )
        expected_se = np.sqrt(np.sum((values-values.mean())**2) / values.size**2)
        self.assertAlmostEqual(result["standard_error"], expected_se, places=12)

    def test_irregular_subset_returns_nonnegative_variance(self):
        ids = np.array([0, 1, 3, 4, 7, 8, 11, 14])
        values = np.array([0.2, 1.1, -0.4, 2.0, 0.7, -1.0, 1.5, 0.3])
        result = spatial_hac_mean_interval(
            ids, values, grid_columns=4, bandwidth_rows=3,
            bandwidth_columns=2, min_blocks=2,
        )
        self.assertEqual(result["interval_status"], "spatial_hac_normal")
        self.assertGreaterEqual(result["standard_error"], 0.0)
        self.assertLess(result["lower"], result["estimate"])
        self.assertGreater(result["upper"], result["estimate"])

    def test_result_is_invariant_to_input_order(self):
        ids = np.array([0, 1, 3, 4, 7, 8, 11, 14])
        values = np.array([0.2, 1.1, -0.4, 2.0, 0.7, -1.0, 1.5, 0.3])
        a = spatial_hac_mean_interval(ids, values, grid_columns=4,
                                      bandwidth_rows=3, min_blocks=2)
        b = spatial_hac_mean_interval(ids[::-1], values[::-1], grid_columns=4,
                                      bandwidth_rows=3, min_blocks=2)
        self.assertAlmostEqual(a["standard_error"], b["standard_error"], places=12)
        self.assertAlmostEqual(a["lower"], b["lower"], places=12)

    def test_constant_values_have_zero_width_interval(self):
        result = spatial_hac_mean_interval(
            np.arange(25), np.full(25, 3.5), grid_columns=5,
            bandwidth_rows=3,
        )
        self.assertEqual(result["interval_status"], "no_variation")
        self.assertEqual(result["lower"], 3.5)
        self.assertEqual(result["upper"], 3.5)

    def test_insufficient_blocks_suppress_interval(self):
        result = spatial_hac_mean_interval(
            [0, 1], [1.0, 2.0], grid_columns=2,
            bandwidth_rows=2, min_blocks=3,
        )
        self.assertEqual(result["interval_status"], "insufficient_blocks")
        self.assertIsNone(result["lower"])

    def test_invalid_inputs_are_rejected(self):
        with self.assertRaises(ValueError):
            spatial_hac_mean_interval([0, 0], [1.0, 2.0], grid_columns=2,
                                      bandwidth_rows=2)
        with self.assertRaises(ValueError):
            spatial_hac_mean_interval([0], [1.0], grid_columns=2,
                                      bandwidth_rows=0)


if __name__ == "__main__":
    unittest.main()
