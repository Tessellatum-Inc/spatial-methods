import unittest
import numpy as np
from explorations.radar.stratify_nairobi_r130_dynamic_world import summarize, CLASS_NAMES, valid_landcover_support, report_date

class DynamicWorldStratificationTests(unittest.TestCase):
    def test_summary_keeps_counts_and_outlier_rates(self):
        result=summarize(np.array([0.1,-0.2,1.1]))
        self.assertEqual(result["count"],3)
        self.assertAlmostEqual(result["mae_db"],1.4/3)
        self.assertAlmostEqual(result["fraction_abs_gt_1_db"],1/3)


    def test_zero_confidence_pixels_are_not_landcover_observations(self):
        residual=np.array([0.1,0.2,0.3,0.4],dtype=float)
        classes=np.array([0,6,1,2],dtype=np.uint8)
        confidence=np.array([0.0,0.0,0.35,0.8],dtype=float)
        valid=valid_landcover_support(residual,None,classes,confidence)
        np.testing.assert_array_equal(valid,np.array([False,False,True,True]))
    def test_report_date_preserves_iso_date_tokens(self):
        self.assertEqual(report_date("2026-10-06"),"2026-10-06")
        with self.assertRaises(ValueError):
            report_date("20261006")

    def test_class_schema_has_nine_dynamic_world_classes(self):
        self.assertEqual(len(CLASS_NAMES),9)
        self.assertEqual(CLASS_NAMES[6],"built")
        self.assertEqual(CLASS_NAMES[8],"snow_and_ice")

if __name__=="__main__":unittest.main()
