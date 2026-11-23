import unittest

from explorations.radar.download_opera_surat_r009_assets import select_assets


class OperaAssetSelectionTests(unittest.TestCase):
    def test_selects_rtc_science_assets_and_excludes_browse_and_md5(self):
        report = {
            "matched_features": [{
                "file_id": "rtc-product",
                "properties": {
                    "s3Urls": [
                        "s3://asf-cumulus-prod-opera-products/path/product.h5",
                        "s3://asf-cumulus-prod-opera-products/path/product.iso.xml",
                        "s3://asf-cumulus-prod-opera-products/path/product_VV.tif",
                        "s3://asf-cumulus-prod-opera-products/path/product_VH.tif",
                        "s3://asf-cumulus-prod-opera-products/path/product_mask.tif",
                        "s3://asf-cumulus-prod-opera-products/path/product_VV.tif.md5",
                        "s3://asf-cumulus-prod-opera-browse/path/product_BROWSE.png",
                    ],
                    "bytes": {},
                },
            } for _ in range(8)],
            "static_layer_query": {
                "features": [{
                    "file_id": "static-product",
                    "properties": {
                        "s3Urls": [
                            "s3://asf-cumulus-prod-opera-products/path/static.iso.xml",
                            "s3://asf-cumulus-prod-opera-products/path/static_incidence_angle.tif",
                            "s3://asf-cumulus-prod-opera-products/path/static_local_incidence_angle.tif",
                            "s3://asf-cumulus-prod-opera-products/path/static_mask.tif",
                            "s3://asf-cumulus-prod-opera-products/path/static_number_of_looks.tif",
                            "s3://asf-cumulus-prod-opera-products/path/static_rtc_anf_gamma0_to_beta0.tif",
                            "s3://asf-cumulus-prod-opera-products/path/static_rtc_anf_gamma0_to_sigma0.tif",
                            "s3://asf-cumulus-prod-opera-products/path/static_mask.tif.md5",
                        ],
                        "bytes": {},
                    },
                } for _ in range(2)],
            },
        }
        assets = select_assets(report)
        rtc = [x for x in assets if x["product_type"] == "rtc"]
        static = [x for x in assets if x["product_type"] == "static"]
        self.assertEqual(len(rtc), 40)
        self.assertEqual(len(static), 12)
        self.assertFalse(any(x["filename"].endswith(".md5") for x in assets))
        self.assertFalse(any("BROWSE" in x["filename"] for x in assets))
        self.assertTrue(any(x["filename"].endswith("_incidence_angle.tif") for x in static))
        self.assertTrue(any(x["filename"].endswith("_rtc_anf_gamma0_to_beta0.tif") for x in static))

    def test_rejects_incomplete_scene_set(self):
        with self.assertRaises(ValueError):
            select_assets({"matched_features": [], "static_layer_query": {"features": []}})


if __name__ == "__main__":
    unittest.main()
