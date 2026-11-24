import unittest
from explorations.radar.discover_opera_nairobi_r130_products import build_query, build_static_query, identify, parse_collection, summarize

class DiscoveryTests(unittest.TestCase):
    def test_query_is_rtc_for_aoi(self):
        q=build_query("2026-10-01T00:00:00Z","2026-11-24T00:00:00Z")
        self.assertEqual(q["dataset"],"OPERA-S1")
        self.assertEqual(q["processingLevel"],"RTC")
        self.assertIn("36.65",q["intersectsWith"])

    def test_static_query_uses_rtc_static_catalogue(self):
        q=build_static_query()
        self.assertEqual(q["processingLevel"],"RTC-STATIC")
        self.assertEqual(q["start"],"2014-04-03T00:00:00Z")

    def test_rejects_non_utc_and_empty_interval(self):
        with self.assertRaises(ValueError): build_query("2026-10-01T00:00:00","2026-11-24T00:00:00Z")
        with self.assertRaises(ValueError): build_query("2026-11-24T00:00:00Z","2026-11-24T00:00:00Z")

    def test_extracts_relative_orbit_and_timestamp_from_burst_name(self):
        got=identify({"fileName":"OPERA_L2_RTC-S1_T130_279159_IW3_20261110T041200Z_20261110T180000Z_S1A_30_v1.0"})
        self.assertEqual(got["relative_orbit_from_burst"],130)
        self.assertEqual(got["acquisition_datetime_utc"],"2026-11-10T04:12:00Z")

    def test_filters_other_orbits_and_groups_target_bursts(self):
        features=[
          {"properties":{"fileName":"OPERA_T130-019159-IW3_20261110T041200Z","polarization":"VV"},"geometry":{"type":"Polygon","coordinates":[]}},
          {"properties":{"fileName":"OPERA_T130-019159-IW3_20261110T041204Z","polarization":"VH"},"geometry":{"type":"Polygon","coordinates":[]}},
          {"properties":{"fileName":"OPERA_T009-019159-IW3_20261110T041200Z","polarization":"VV"},"geometry":{"type":"Polygon","coordinates":[]}},
        ]
        report=summarize(parse_collection(b'{"type":"FeatureCollection","features":[]}')) if False else summarize({"type":"FeatureCollection","features":features})
        self.assertEqual(report["target_orbit_feature_count"],2)
        self.assertEqual(len(report["acquisition_groups"]),1)
        self.assertEqual(report["acquisition_groups"][0]["polarizations"],["VH","VV"])
        self.assertEqual(len(report["acquisition_groups"][0]["burst_start_times_utc"]),2)

if __name__=="__main__": unittest.main()
