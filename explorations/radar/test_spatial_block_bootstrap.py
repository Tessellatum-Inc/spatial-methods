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
