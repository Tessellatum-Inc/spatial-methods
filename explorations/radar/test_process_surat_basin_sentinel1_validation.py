import unittest
from explorations.radar.process_surat_basin_sentinel1_validation import BBOX, HEIGHT, TARGETS, WIDTH

class SuratProcessingConfigurationTests(unittest.TestCase):
    def test_target_subset_is_inside_processing_bbox(self):
        west,south,east,north=BBOX
        for target in TARGETS:
            self.assertGreaterEqual(target["longitude"],west)
            self.assertLessEqual(target["longitude"],east)
            self.assertGreaterEqual(target["latitude"],south)
            self.assertLessEqual(target["latitude"],north)

    def test_output_spacing_is_approximately_ten_metres(self):
        lon_m=(east:=BBOX[2]-BBOX[0])*100000*0.89
        lat_m=(north:=BBOX[3]-BBOX[1])*111000
        self.assertLess(lon_m/WIDTH,12)
        self.assertLess(lat_m/HEIGHT,12)

    def test_four_same_track_acquisitions_are_configured(self):
        from explorations.radar.process_surat_basin_sentinel1_validation import PRODUCTS
        self.assertEqual(len(PRODUCTS),4)
        self.assertEqual(len({p[1] for p in PRODUCTS}),4)

if __name__=="__main__": unittest.main()
