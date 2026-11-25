import unittest
import numpy as np
from explorations.radar.spatial_block_bootstrap import block_mean_contrast, bootstrap_interval, matched_block_contrasts

class SpatialBlockBootstrapTests(unittest.TestCase):
    def test_matched_strata_are_equal_weighted_within_block(self):
        # Stratum 0: target MAE 5 minus built MAE 2 = 3.
        # Stratum 1: target MAE 4 minus built MAE 2 = 2.
        # The block estimate is the equal-stratum mean: 2.5, not a pixel-weighted mean.
        block = np.array([0, 0, 0, 0, 0, 0])
        classes = np.array([6, 6, 1, 1, 6, 1])
        strata = np.array([0, 0, 0, 0, 1, 1])
        residuals = np.array([1., 3., 4., 6., 2., 4.])
        result = matched_block_contrasts(block, classes, strata, residuals)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]["matched_strata"], 2)
        self.assertAlmostEqual(result[0]["contrast_db"], 2.5)

    def test_unmatched_strata_are_excluded(self):
        block = np.array([0, 0, 0])
        classes = np.array([6, 1, 1])
        strata = np.array([0, 0, 1])
        residuals = np.array([2., 5., 9.])
        result = matched_block_contrasts(block, classes, strata, residuals)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]["matched_strata"], 1)
        self.assertAlmostEqual(result[0]["contrast_db"], 3.0)

    def test_input_shape_mismatch_raises(self):
        with self.assertRaises(ValueError):
            matched_block_contrasts([0, 1], [6], [0, 0], [1., 2.])

    def test_equal_block_weighting(self):
        self.assertAlmostEqual(block_mean_contrast([1,3,5]),3.0)
    def test_nan_values_ignored(self):
        self.assertAlmostEqual(block_mean_contrast([1,np.nan,3]),2.0)
    def test_small_sample_interval_suppressed(self):
        result=bootstrap_interval([.1,.2,.3],min_blocks=20)
        self.assertEqual(result["interval_status"],"insufficient_blocks")
        self.assertIsNone(result["lower_95_db"])
        self.assertEqual(result["replicates"],0)
    def test_bootstrap_is_reproducible_and_bounds_estimate(self):
        x=np.arange(25,dtype=float)/100
        a=bootstrap_interval(x,replicates=500,seed=42,min_blocks=20)
        b=bootstrap_interval(x,replicates=500,seed=42,min_blocks=20)
        self.assertEqual(a,b)
        self.assertLessEqual(a["lower_95_db"],a["estimate_db"])
        self.assertGreaterEqual(a["upper_95_db"],a["estimate_db"])


    def test_rook_morans_i_detects_positive_and_negative_neighbour_patterns(self):
        from explorations.radar.spatial_block_bootstrap import rook_morans_i
        positive = rook_morans_i([0, 1, 2, 3], [1., 2., 2., 3.], grid_columns=2, min_blocks=4)
        negative = rook_morans_i([0, 1, 2, 3], [1., -1., -1., 1.], grid_columns=2, min_blocks=4)
        self.assertEqual(positive["status"], "computed")
        self.assertEqual(negative["status"], "computed")
        self.assertGreater(positive["moran_i"], 0)
        self.assertLess(negative["moran_i"], 0)
        self.assertEqual(positive["neighbor_pairs"], 4)

    def test_rook_morans_i_flags_constant_values_and_disconnected_blocks(self):
        from explorations.radar.spatial_block_bootstrap import rook_morans_i
        constant = rook_morans_i([0, 1, 2, 3], [2., 2., 2., 2.], grid_columns=2, min_blocks=4)
        disconnected = rook_morans_i([0, 3], [1., 2.], grid_columns=2, min_blocks=2)
        self.assertEqual(constant["status"], "no_variation")
        self.assertEqual(disconnected["status"], "no_neighbour_pairs")

    def test_rook_morans_i_suppresses_small_block_sets(self):
        from explorations.radar.spatial_block_bootstrap import rook_morans_i
        result = rook_morans_i([0, 1, 2], [1., 2., 3.], grid_columns=2, min_blocks=4)
        self.assertEqual(result["status"], "insufficient_blocks")
        self.assertIsNone(result["moran_i"])
