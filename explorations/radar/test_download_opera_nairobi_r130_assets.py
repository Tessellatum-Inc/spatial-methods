import unittest
from explorations.radar.download_opera_nairobi_r130_assets import select_assets

class DownloadSelectionTests(unittest.TestCase):
    def fixture(self):
        bursts=["T130_279214_IW3","T130_279215_IW3","T130_279216_IW3"]
        rtc=[]
        for date in ["20261006","20261018","20261030","20261111","20261123"]:
            for burst in bursts:
                stem=f"OPERA_L2_RTC-S1_{burst}_{date}T155541Z_S1D_30_v1.0"
                urls=[f"https://datapool.asf.alaska.edu/OPERA-S1/{stem}{suffix}"
                      for suffix in [".h5",".iso.xml","_VV.tif","_VH.tif","_mask.tif"]]
                rtc.append({"burst_id":burst,"file_id":stem,"properties":{"additionalUrls":urls}})
        static=[]
        for burst in bursts:
            stem=f"OPERA_L2_RTC-S1-STATIC_{burst}_S1D_30_v1.0"
            urls=[f"https://datapool.asf.alaska.edu/OPERA-S1/{stem}{suffix}"
                  for suffix in [".iso.xml","_incidence_angle.tif","_local_incidence_angle.tif",
                                 "_mask.tif","_number_of_looks.tif","_rtc_anf_gamma0_to_beta0.tif",
                                 "_rtc_anf_gamma0_to_sigma0.tif"]]
            static.append({"burst_id":burst,"properties":{"additionalUrls":urls}})
        return {"acquisition_groups":[{"burst_ids":bursts}],"features":rtc,
                "static_layer_query":{"features":static}}

    def test_selects_complete_rtc_and_static_asset_sets(self):
        assets=select_assets(self.fixture())
        self.assertEqual(len(assets),15*5+3*7)
        self.assertEqual(sum(x["product_type"]=="rtc" for x in assets),75)
        self.assertEqual(sum(x["product_type"]=="static" for x in assets),21)
        self.assertEqual(len({x["filename"] for x in assets}),len(assets))

    def test_rejects_missing_static_burst(self):
        report=self.fixture()
        report["static_layer_query"]["features"].pop()
        with self.assertRaises(ValueError): select_assets(report)

if __name__=="__main__": unittest.main()
