import unittest

from explorations.radar.download_opera_surat_r009_assets import select_assets


class OperaAssetSelectionTests(unittest.TestCase):
    def test_selects_rtc_science_assets_and_excludes_browse_and_checksums(self):
        rtc_features = []
        for i in range(8):
            base = f"product{i}"
            rtc_features.append({
                "file_id": base,
                "properties": {
                    "url": f"https://cumulus.asf.earthdatacloud.nasa.gov/path/{base}.h5",
                    "additionalUrls": [
                        f"https://cumulus.asf.earthdatacloud.nasa.gov/path/{base}.iso.xml",
                        f"https://cumulus.asf.earthdatacloud.nasa.gov/path/{base}_VV.tif",
                        f"https://cumulus.asf.earthdatacloud.nasa.gov/path/{base}_VH.tif",
                        f"https://cumulus.asf.earthdatacloud.nasa.gov/path/{base}_mask.tif",
                        f"https://cumulus.asf.earthdatacloud.nasa.gov/path/{base}_VV.tif.md5",
                        f"https://cumulus.asf.earthdatacloud.nasa.gov/path/{base}_BROWSE.png",
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
                    "url": f"https://datapool.asf.alaska.edu/path/{base}_incidence_angle.tif",
                    "additionalUrls": [
                        f"https://datapool.asf.alaska.edu/path/{base}.iso.xml",
                        f"https://datapool.asf.alaska.edu/path/{base}_local_incidence_angle.tif",
                        f"https://datapool.asf.alaska.edu/path/{base}_mask.tif",
                        f"https://datapool.asf.alaska.edu/path/{base}_number_of_looks.tif",
                        f"https://datapool.asf.alaska.edu/path/{base}_rtc_anf_gamma0_to_beta0.tif",
                        f"https://datapool.asf.alaska.edu/path/{base}_rtc_anf_gamma0_to_sigma0.tif",
                        f"https://datapool.asf.alaska.edu/path/{base}_mask.tif.md5",
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
        self.assertEqual(len(static), 14)
        self.assertFalse(any(x["filename"].endswith(".md5") for x in assets))
        self.assertFalse(any("BROWSE" in x["filename"] for x in assets))
        self.assertTrue(any(x["filename"].endswith("_incidence_angle.tif") for x in static))
        self.assertTrue(any(x["filename"].endswith("_local_incidence_angle.tif") for x in static))
        self.assertTrue(any(x["filename"].endswith("_rtc_anf_gamma0_to_beta0.tif") for x in static))

    def test_rejects_incomplete_scene_set(self):
        with self.assertRaises(ValueError):
            select_assets({"matched_features": [], "static_layer_query": {"features": []}})

    def test_rejects_untrusted_hosts(self):
        report = {
            "matched_features": [{
                "file_id": "x",
                "properties": {
                    "url": "https://example.com/x.h5",
                    "additionalUrls": ["https://example.com/x_VV.tif"],
                    "bytes": {},
                },
            } for _ in range(8)],
            "static_layer_query": {"features": [{
                "file_id": "s",
                "properties": {
                    "additionalUrls": ["https://example.com/s_rtc_anf_gamma0_to_beta0.tif"],
                    "bytes": {},
                },
            } for _ in range(2)]},
        }
        with self.assertRaises(ValueError):
            select_assets(report)


if __name__ == "__main__":
    unittest.main()
