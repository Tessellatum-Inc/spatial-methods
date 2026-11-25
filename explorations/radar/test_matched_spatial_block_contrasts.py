import unittest
import numpy as np
from explorations.radar.spatial_block_bootstrap import matched_block_contrasts, bootstrap_interval
class MatchedBlockTests(unittest.TestCase):
 def test_only_shared_strata_contribute_and_equal_weighted(self):
  # Block 1 has shared stratum 10; stratum 20 has only target class and is excluded.
  b=np.array([1,1,1,1,1,1]);c=np.array([6,6,1,1,1,1]);s=np.array([10,10,10,10,20,20]);r=np.array([.1,.2,.3,.4,.5,.6])
  rows=matched_block_contrasts(b,c,s,r)
  self.assertEqual(len(rows),1);self.assertEqual(rows[0]["matched_strata"],1)
  self.assertAlmostEqual(rows[0]["contrast_db"],.2)
 def test_separate_blocks_are_resampling_units(self):
  b=np.array([1,1,2,2]);c=np.array([6,1,6,1]);s=np.array([3,3,3,3]);r=np.array([.1,.3,.2,.6])
  rows=matched_block_contrasts(b,c,s,r)
  self.assertEqual([x["block_id"] for x in rows],[1,2])
  self.assertAlmostEqual(rows[0]["contrast_db"],.2)
  self.assertAlmostEqual(rows[1]["contrast_db"],.4)
 def test_nan_residual_excluded(self):
  rows=matched_block_contrasts(np.array([1,1]),np.array([6,1]),np.array([1,1]),np.array([.1,np.nan]))
  self.assertEqual(rows,[])
 def test_shape_mismatch_rejected(self):
  with self.assertRaises(ValueError):matched_block_contrasts([1],[6,1],[1],[.1])
if __name__=="__main__":unittest.main()
