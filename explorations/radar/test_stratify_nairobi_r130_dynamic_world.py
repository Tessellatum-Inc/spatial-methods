import unittest
import numpy as np
from explorations.radar.stratify_nairobi_r130_dynamic_world import summarize, CLASS_NAMES

class DynamicWorldStratificationTests(unittest.TestCase):
    def test_summary_keeps_counts_and_outlier_rates(self):
        result=summarize(np.array([0.1,-0.2,1.1]))
        self.assertEqual(result["count"],3)
        self.assertAlmostEqual(result["mae_db"],1.4/3)
        self.assertAlmostEqual(result["fraction_abs_gt_1_db"],1/3)

    def test_class_schema_has_nine_dynamic_world_classes(self):
        self.assertEqual(len(CLASS_NAMES),9)
        self.assertEqual(CLASS_NAMES[6],"built")
        self.assertEqual(CLASS_NAMES[8],"snow_and_ice")

if __name__=="__main__":unittest.main()
