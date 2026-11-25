import unittest

import numpy as np

from explorations.radar.spatial_moving_block_bootstrap import (
    moving_spatial_block_bootstrap_interval,
    moving_window_membership,
)


class MovingSpatialBlockBootstrapTests(unittest.TestCase):
    def test_every_block_has_equal_window_membership_at_edges_and_gaps(self):
        ids = np.array([0, 1, 3, 4, 7, 8, 11])
        windows = moving_window_membership(
            ids, grid_columns=4, window_width_blocks=2
        )
        counts = np.zeros(ids.size, dtype=int)
        for window in windows:
            counts[window] += 1
        np.testing.assert_array_equal(counts, np.full(ids.size, 4))
        self.assertGreater(len(windows), 0)

    def test_dense_grid_has_expected_candidate_window_count(self):
        ids = np.arange(16)
        windows = moving_window_membership(
            ids, grid_columns=4, window_width_blocks=2
        )
        # Extended origins create (4+2-1)^2 candidate windows.
        self.assertEqual(len(windows), 25)

    def test_invalid_inputs_are_rejected(self):
        with self.assertRaises(ValueError):
            moving_window_membership([0, 0], grid_columns=4, window_width_blocks=2)
        with self.assertRaises(ValueError):
            moving_window_membership([-1], grid_columns=4, window_width_blocks=2)

    def test_bootstrap_is_reproducible_and_preserves_point_estimate(self):
        ids = np.arange(100)
        values = np.linspace(-1, 1, 100)
        kwargs = dict(
            grid_columns=10, window_width_blocks=2,
            replicates=300, seed=41, min_windows=20,
        )
        first = moving_spatial_block_bootstrap_interval(ids, values, **kwargs)
        second = moving_spatial_block_bootstrap_interval(ids, values, **kwargs)
        self.assertEqual(first, second)
        self.assertAlmostEqual(first["estimate_db"], values.mean())
        self.assertEqual(first["interval_status"], "percentile_moving_spatial_block_bootstrap")
        self.assertEqual(first["windows_per_replicate"], 31)

    def test_irregular_mask_uses_fixed_equal_inclusion_normalization(self):
        ids = np.array([0, 1, 3, 4, 7, 8, 11])
        values = np.array([0.0, 1.0, 9.0, 2.0, 12.0, 3.0, 20.0])
        width = 2
        replicates = 500
        seed = 73
        windows = moving_window_membership(
            ids, grid_columns=4, window_width_blocks=width
        )
        draws_per_replicate = int(np.ceil(len(windows) / width**2))
        window_sums = np.array([values[index].sum() for index in windows])
        rng = np.random.default_rng(seed)
        sampled = rng.integers(
            0, len(windows), size=(replicates, draws_per_replicate)
        )
        expected_draws = (
            window_sums[sampled].sum(axis=1) * len(windows)
            / (draws_per_replicate * width**2 * values.size)
        )
        result = moving_spatial_block_bootstrap_interval(
            ids, values, grid_columns=4, window_width_blocks=width,
            replicates=replicates, seed=seed, min_windows=1, min_blocks=1,
        )
        expected_lower, expected_upper = np.quantile(
            expected_draws, [0.025, 0.975]
        )
        self.assertAlmostEqual(result["lower_95_db"], expected_lower)
        self.assertAlmostEqual(result["upper_95_db"], expected_upper)


    def test_complete_window_average_has_exact_equal_block_normalization(self):
        # This identity catches a missing candidate-window / eligible-block
        # factor, which a zero-mean coverage experiment cannot detect.
        ids = np.array([0, 1, 3, 4, 7, 8, 11])
        values = np.array([2.0, 3.0, 11.0, 4.0, 14.0, 5.0, 22.0])
        width = 2
        windows = moving_window_membership(
            ids, grid_columns=4, window_width_blocks=width
        )
        window_sums = np.array([values[index].sum() for index in windows])
        normalized_complete_average = (
            window_sums.mean() * len(windows) / (width**2 * values.size)
        )
        self.assertAlmostEqual(normalized_complete_average, values.mean(), places=12)

    def test_nonzero_mean_bootstrap_distribution_is_centered_on_point_estimate(self):
        ids = np.array([0, 1, 3, 4, 7, 8, 11])
        values = np.array([2.0, 3.0, 11.0, 4.0, 14.0, 5.0, 22.0])
        result = moving_spatial_block_bootstrap_interval(
            ids, values, grid_columns=4, window_width_blocks=2,
            replicates=50000, seed=91, min_windows=1, min_blocks=1,
        )
        midpoint = (result["lower_95_db"] + result["upper_95_db"]) / 2
        self.assertLess(abs(midpoint - result["estimate_db"]), 1.0)

    def test_insufficient_base_blocks_suppress_interval_even_with_many_windows(self):
        result = moving_spatial_block_bootstrap_interval(
            [0], [1.], grid_columns=1, window_width_blocks=5,
            min_windows=1, min_blocks=2,
        )
        self.assertEqual(result["candidate_windows"], 0)
        self.assertEqual(result["interval_status"], "insufficient_blocks")
        self.assertIsNone(result["lower_95_db"])

    def test_insufficient_windows_suppresses_interval(self):
        result = moving_spatial_block_bootstrap_interval(
            [0, 1], [1., 2.], grid_columns=2,
            window_width_blocks=1, min_windows=20, min_blocks=1,
        )
        self.assertEqual(result["interval_status"], "insufficient_windows")
        self.assertIsNone(result["lower_95_db"])


if __name__ == "__main__":
    unittest.main()
