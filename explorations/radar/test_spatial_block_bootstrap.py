import unittest
import numpy as np
from explorations.radar.spatial_block_bootstrap import block_mean_contrast, bootstrap_interval

class SpatialBlockBootstrapTests(unittest.TestCase):
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
