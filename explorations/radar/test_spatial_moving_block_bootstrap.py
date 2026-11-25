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

    def test_insufficient_windows_suppresses_interval(self):
        result = moving_spatial_block_bootstrap_interval(
            [0, 1], [1., 2.], grid_columns=2,
            window_width_blocks=1, min_windows=20,
        )
        self.assertEqual(result["interval_status"], "insufficient_windows")
        self.assertIsNone(result["lower_95_db"])


if __name__ == "__main__":
    unittest.main()
