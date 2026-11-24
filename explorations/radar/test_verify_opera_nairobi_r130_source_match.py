import unittest
from explorations.radar.verify_opera_nairobi_r130_source_match import parse_product, verify

class SourceMatchTests(unittest.TestCase):
    def test_parse_slc_and_grd_product_names(self):
        slc=parse_product("S1D_IW_SLC__1SDV_20261123T155530_20261123T155557_005596_00AB9A_69B1.zip")
        grd=parse_product("S1D_IW_GRDH_1SDV_20261123T155530_20261123T155555_005596_00AB9A_AA88_COG.SAFE")
        self.assertEqual(slc["absolute_orbit"],grd["absolute_orbit"])
        self.assertEqual(slc["datatake_id"],grd["datatake_id"])
        self.assertEqual(slc["start_time"],grd["start_time"])
    def test_allows_one_second_start_time_difference(self):
        self.assertEqual(parse_product("S1D_IW_SLC__1SDV_20261030T155530_20261030T155557_005246_009F7F_2D96.zip")["datatake_id"],
                         parse_product("S1D_IW_GRDH_1SDV_20261030T155531_20261030T155556_005246_009F7F_498E_COG.SAFE")["datatake_id"])
        audit={"hdf5":[{"file":f"burst{i}.h5","metadata":{"burst_id":f"t130_{i}_iw3","absolute_orbit":5246,"platform":"Sentinel-1D","source_start":"2026-10-30T15:55:41Z","source_slc_granules":["S1D_IW_SLC__1SDV_20261030T155530_20261030T155557_005246_009F7F_2D96.zip"]}} for i in range(3)]}
        catalogue={"acquisition_date_matches":[{"acquisition_date_utc":"2026-10-30","qualified_candidates":[{"catalog_item_id":"S1D_IW_GRDH_1SDV_20261030T155531_20261030T155556_005246_009F7F_498E_COG.SAFE"}]}]}
        result=verify(audit,catalogue)
        self.assertTrue(result["date_matches"][0]["datatake_match_passed"])
        self.assertEqual(result["date_matches"][0]["maximum_source_start_difference_seconds"],1.0)

    def test_requires_three_burst_links_for_each_date(self):
        audit={"hdf5":[{"file":f"burst{i}.h5","metadata":{"burst_id":f"t130_{i}_iw3","absolute_orbit":5596,"platform":"Sentinel-1D","source_start":"2026-11-23T15:55:41Z","source_slc_granules":["S1D_IW_SLC__1SDV_20261123T155530_20261123T155557_005596_00AB9A_69B1.zip"]}} for i in range(3)]}
        catalogue={"acquisition_date_matches":[{"acquisition_date_utc":"2026-11-23","qualified_candidates":[{"catalog_item_id":"S1D_IW_GRDH_1SDV_20261123T155530_20261123T155555_005596_00AB9A_AA88_COG.SAFE"}]}]}
        report=verify(audit,catalogue)
        self.assertTrue(report["checks"]["all_five_dates_link_all_three_opera_bursts"] is False)
        self.assertEqual(report["date_matches"][0]["linked_opera_burst_count"],3)
        self.assertTrue(report["date_matches"][0]["datatake_match_passed"])

if __name__=="__main__": unittest.main()
