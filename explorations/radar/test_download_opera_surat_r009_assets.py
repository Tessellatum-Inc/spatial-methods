import unittest

from explorations.radar.download_opera_surat_r009_assets import select_assets


class OperaAssetSelectionTests(unittest.TestCase):
    def test_selects_rtc_science_assets_and_excludes_browse_and_md5(self):
        rtc_features = []
        for i in range(8):
            base = f"product{i}"
            rtc_features.append({
                "file_id": base,
                "properties": {
                    "s3Urls": [
                        f"s3://asf-cumulus-prod-opera-products/path/{base}.h5",
                        f"s3://asf-cumulus-prod-opera-products/path/{base}.iso.xml",
                        f"s3://asf-cumulus-prod-opera-products/path/{base}_VV.tif",
                        f"s3://asf-cumulus-prod-opera-products/path/{base}_VH.tif",
                        f"s3://asf-cumulus-prod-opera-products/path/{base}_mask.tif",
                        f"s3://asf-cumulus-prod-opera-products/path/{base}_VV.tif.md5",
                        f"s3://asf-cumulus-prod-opera-browse/path/{base}_BROWSE.png",
                    ],
                    "bytes": {},
                },
            })
        static_features = []
        for i in range(2):
            base = f"static{i}"
            static_features.append({
                "file_id": base,
                "properties": {
                    "s3Urls": [
                        f"s3://asf-cumulus-prod-opera-products/path/{base}.iso.xml",
                        f"s3://asf-cumulus-prod-opera-products/path/{base}_incidence_angle.tif",
                        f"s3://asf-cumulus-prod-opera-products/path/{base}_local_incidence_angle.tif",
                        f"s3://asf-cumulus-prod-opera-products/path/{base}_mask.tif",
                        f"s3://asf-cumulus-prod-opera-products/path/{base}_number_of_looks.tif",
                        f"s3://asf-cumulus-prod-opera-products/path/{base}_rtc_anf_gamma0_to_beta0.tif",
                        f"s3://asf-cumulus-prod-opera-products/path/{base}_rtc_anf_gamma0_to_sigma0.tif",
                        f"s3://asf-cumulus-prod-opera-products/path/{base}_mask.tif.md5",
                    ],
                    "bytes": {},
                },
            })
        report = {
            "matched_features": rtc_features,
            "static_layer_query": {"features": static_features},
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
