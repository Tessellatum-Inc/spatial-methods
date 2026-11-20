import unittest
from class_error_analysis import analyse
W={"a":0.5,"b":0.5}
def row(i,h,m,ref):return {"sample_id":str(i),"sampling_stratum":h,"map_class":m,"reference_class":ref}
class Tests(unittest.TestCase):
 def test_design_weighted_matrix_and_accuracy(self):
  rows=[row(1,"a","a","a"),row(2,"a","a","b"),row(3,"b","a","b"),row(4,"b","a","a")]
  x=analyse(rows,W)
  self.assertAlmostEqual(x["fiji"]["overall_accuracy_percent"],50)
  self.assertAlmostEqual(x["worldcover"]["overall_accuracy_percent"],50)
  self.assertAlmostEqual(sum(c["estimated_mapped_area_percent"] for c in x["worldcover"]["class_metrics"]),100)
 def test_stratum_weights_are_mandatory_and_sum_one(self):
  rows=[row(1,"a","a","a"),row(2,"a","b","a"),row(3,"b","b","b"),row(4,"b","a","b")]
  with self.assertRaises(ValueError):analyse(rows,{"a":.4,"b":.4})
 def test_strata_must_match(self):
  with self.assertRaises(ValueError):analyse([row(1,"a","a","a"),row(2,"a","a","a")],{"a":0.5,"b":0.5})
 def test_empty_predicted_class_has_undefined_users_accuracy(self):
  rows=[row(1,"a","a","a"),row(2,"a","a","b"),row(3,"b","a","b"),row(4,"b","a","b")]
  x=analyse(rows,W); cls={z["class"]:z for z in x["worldcover"]["class_metrics"]}
  self.assertIsNone(cls["b"]["users_accuracy_percent"])
if __name__=="__main__":unittest.main()
