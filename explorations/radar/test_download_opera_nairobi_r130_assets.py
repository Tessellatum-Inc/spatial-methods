import unittest
from explorations.radar.download_opera_nairobi_r130_assets import select_assets

class DownloadSelectionTests(unittest.TestCase):
    def test_requires_complete_rtc_and_static_burst_sets(self):
        report={"acquisition_groups":[{"burst_ids":["T130_279214_IW3","T130_279215_IW3","T130_279216_IW3"]}],
          "features":[{"properties":{"additionalUrls":["https://datapool.asf.alaska.edu/OPERA-S1/OPERA_L2_RTC-S1_T130_279214_IW3_20261006T155541Z_S1D_30_v1.0_VV.tif"]},
             "burst_id":"T130_279214_IW3"} for _ in range(15)],
          "static_layer_query":{"features":[{"burst_id":x,"properties":{"url":f"https://datapool.asf.alaska.edu/OPERA-S1/OPERA_L2_RTC-S1-STATIC_{x}.h5"}} for x in ["T130_279214_IW3","T130_279215_IW3","T130_279216_IW3"]]}}
        # Duplicate filenames are rejected after exact product asset selection.
        with self.assertRaises(ValueError): select_assets(report)

if __name__=="__main__": unittest.main()
