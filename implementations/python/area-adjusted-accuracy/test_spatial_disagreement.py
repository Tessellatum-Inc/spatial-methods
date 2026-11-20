import unittest
from spatial_disagreement import analyse, haversine_km
W={"a":0.5,"b":0.5}; P={"a":100,"b":100}
def row(i,h,mc,ref,lon=0.0,lat=0.0):
 return {"sample_id":str(i),"sampling_stratum":h,"map_class":mc,"reference_class":ref,"longitude":lon,"latitude":lat,"worldcover_code":10,"source_tile":"fixture.tif"}
class Tests(unittest.TestCase):
 def test_four_outcomes(self):
  rows=[row(1,"a","a","a"),row(2,"a","b","a"),row(3,"a","a","b"),row(4,"a","b","c"),row(5,"b","b","b"),row(6,"b","a","b"),row(7,"b","b","a"),row(8,"b","c","d")]
  report,geo=analyse(rows,W,P)
  self.assertEqual(report["sample_size"],8);self.assertEqual(len(geo["features"]),8)
  for k in ("both_correct","fiji_only_correct","worldcover_only_correct","both_wrong"):self.assertAlmostEqual(report["four_outcome_estimates"][k]["estimate"],.25)
  self.assertAlmostEqual(sum(x["estimate"] for x in report["four_outcome_estimates"].values()),1)
 def test_direct_label_disagreement_distinct_from_four_outcomes(self):
  rows=[row(1,"a","a","a"),row(2,"a","b","a"),row(3,"a","c","d"),row(4,"a","c","d"),row(5,"b","b","b"),row(6,"b","a","b"),row(7,"b","c","d"),row(8,"b","c","d")]
  report,_=analyse(rows,W,P);self.assertEqual(report["direct_map_label_disagreement"]["sample_count"],6)
 def test_antimeridian_haversine(self):
  self.assertLess(haversine_km(row(1,"a","a","a",179.9),row(2,"a","a","a",-179.9)),23)
 def test_invalid_weights_rejected(self):
  rows=[row(1,"a","a","a"),row(2,"a","b","a"),row(3,"b","b","b"),row(4,"b","a","b")]
  with self.assertRaises(ValueError):analyse(rows,{"a":.4,"b":.4},P)
if __name__=="__main__":unittest.main()
