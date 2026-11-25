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

 def test_vectorized_results_match_reference_aggregation(self):
  rng=np.random.default_rng(17);n=500
  b=rng.integers(0,12,n);c=rng.choice([1,6,2],n);st=rng.integers(0,8,n);r=rng.normal(0,.2,n)
  got=matched_block_contrasts(b,c,st,r)
  expected=[]
  for block in np.unique(b):
   diffs=[];bn=tn=0
   for stratum in np.unique(st[b==block]):
    m=(b==block)&(st==stratum);built=r[m&(c==6)];target=r[m&(c==1)]
    if built.size and target.size:
     bn+=built.size;tn+=target.size;diffs.append(np.abs(target).mean()-np.abs(built).mean())
   if diffs:expected.append((int(block),float(np.mean(diffs)),int(bn),int(tn)))
  actual=[(x["block_id"],x["contrast_db"],x["built_pixels"],x["target_pixels"]) for x in got]
  self.assertEqual([x[0] for x in actual],[x[0] for x in expected])
  for a,e in zip(actual,expected):
   self.assertAlmostEqual(a[1],e[1],places=12);self.assertEqual(a[2:],e[2:])

if __name__=="__main__":unittest.main()
