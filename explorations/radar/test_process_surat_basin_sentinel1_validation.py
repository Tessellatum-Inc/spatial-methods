import unittest
from explorations.radar.process_surat_basin_sentinel1_validation import BBOX, HEIGHT, TARGETS, WIDTH
from explorations.radar.process_sentinelhub_sentinel1 import build_process_payload
from explorations.radar.process_sentinel1_gamma0_terrain import build_rtc_payload

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

    def test_ellipsoid_and_rtc_payloads_use_same_custom_bbox(self):
        feature={"properties":{"datetime":"2025-12-19T08:41:12Z"}}
        ellipsoid=build_process_payload(feature,width=WIDTH,height=HEIGHT,bbox=BBOX)
        rtc=build_rtc_payload(feature,width=WIDTH,height=HEIGHT,bbox=BBOX)
        self.assertEqual(ellipsoid["input"]["bounds"]["bbox"],BBOX)
        self.assertEqual(rtc["input"]["bounds"]["bbox"],BBOX)
        self.assertEqual(ellipsoid["output"]["width"],WIDTH)
        self.assertEqual(rtc["output"]["height"],HEIGHT)
        self.assertEqual(ellipsoid["input"]["data"][0]["processing"]["backCoeff"],"GAMMA0_ELLIPSOID")
        self.assertEqual(rtc["input"]["data"][0]["processing"]["backCoeff"],"GAMMA0_TERRAIN")

    def test_four_same_track_acquisitions_are_configured(self):
        from explorations.radar.process_surat_basin_sentinel1_validation import PRODUCTS
        self.assertEqual(len(PRODUCTS),4)
        self.assertEqual(len({p[1] for p in PRODUCTS}),4)

if __name__=="__main__": unittest.main()
