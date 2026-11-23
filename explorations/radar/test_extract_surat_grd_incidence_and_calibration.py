import unittest
from explorations.radar.extract_surat_grd_incidence_and_calibration import BBOX, PRODUCT_IDS

class SuratIncidenceSourceTests(unittest.TestCase):
    def test_four_selected_scenes_are_unique(self):
        self.assertEqual(len(PRODUCT_IDS),4)
        self.assertEqual(len(set(PRODUCT_IDS)),4)

    def test_reflector_aoi_bbox_is_ordered(self):
        west,south,east,north=BBOX
        self.assertLess(west,east)
        self.assertLess(south,north)

if __name__=="__main__": unittest.main()
