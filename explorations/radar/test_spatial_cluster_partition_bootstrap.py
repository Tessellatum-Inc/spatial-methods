import unittest

import numpy as np

from explorations.radar.spatial_cluster_partition_bootstrap import (
    spatial_cluster_bootstrap_interval,
    spatial_cluster_partition_ids,
)


class SpatialClusterPartitionBootstrapTests(unittest.TestCase):
    def test_zero_phase_groups_adjacent_square_cells(self):
        ids = np.array([0, 1, 4, 5, 8, 9])
        groups = spatial_cluster_partition_ids(
            ids, grid_columns=4, cluster_width_blocks=2
        )
        self.assertEqual(len(np.unique(groups)), 2)
        self.assertEqual(groups[0], groups[1])
        self.assertEqual(groups[0], groups[2])
        self.assertEqual(groups[0], groups[3])

    def test_phase_shift_changes_partition_without_losing_blocks(self):
        ids = np.array([0, 1, 4, 5])
        base = spatial_cluster_partition_ids(
            ids, grid_columns=4, cluster_width_blocks=2
        )
        shifted = spatial_cluster_partition_ids(
            ids, grid_columns=4, cluster_width_blocks=2,
            origin_row_offset=1, origin_col_offset=1,
        )
        self.assertEqual(len(base), len(shifted))
        self.assertEqual(len(np.unique(base)), 1)
        self.assertEqual(len(np.unique(shifted)), 4)

    def test_partition_rejects_invalid_ids_and_offsets(self):
        with self.assertRaises(ValueError):
            spatial_cluster_partition_ids(
                [-1], grid_columns=4, cluster_width_blocks=2
            )
        with self.assertRaises(ValueError):
            spatial_cluster_partition_ids(
                [0], grid_columns=4, cluster_width_blocks=2,
                origin_col_offset=2,
            )

    def test_bootstrap_is_reproducible_and_preserves_base_block_mean(self):
        ids = np.array([0, 1, 4, 5, 8, 9, 12, 13])
        values = np.array([0., 1., 2., 3., 4., 5., 6., 7.])
        kwargs = dict(
            grid_columns=4, cluster_width_blocks=2,
            replicates=500, seed=17, min_clusters=2,
        )
        first = spatial_cluster_bootstrap_interval(ids, values, **kwargs)
        second = spatial_cluster_bootstrap_interval(ids, values, **kwargs)
        self.assertEqual(first, second)
        self.assertAlmostEqual(first["estimate_db"], values.mean())
        self.assertEqual(first["interval_status"], "percentile_spatial_cluster_bootstrap")

    def test_bootstrap_suppresses_insufficient_clusters(self):
        result = spatial_cluster_bootstrap_interval(
            [0, 1, 4, 5], [1., 2., 3., 4.],
            grid_columns=4, cluster_width_blocks=2, min_clusters=2,
        )
        self.assertEqual(result["eligible_clusters"], 1)
        self.assertEqual(result["interval_status"], "insufficient_clusters")
        self.assertIsNone(result["lower_95_db"])


if __name__ == "__main__":
    unittest.main()
