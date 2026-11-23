import unittest
from datetime import timedelta

from explorations.radar.discover_opera_surat_r009_products import (
    ACQUISITIONS,
    TIME_TOLERANCE_SECONDS,
    acquisition_datetime,
    build_query,
    build_static_query,
    parse_collection,
    summarize,
)


class OperaSuratDiscoveryTests(unittest.TestCase):
    def test_query_targets_opera_rtc_and_exact_aoi(self):
        params = build_query("2025-12-19T08:36:12Z", "2025-12-19T08:46:12Z")
        self.assertEqual(params["dataset"], "OPERA-S1")
        self.assertEqual(params["processingLevel"], "RTC")
        self.assertIn("150.244625", params["intersectsWith"])
        self.assertEqual(params["output"], "geojson")

    def test_query_rejects_naive_or_reversed_times(self):
        with self.assertRaises(ValueError):
            build_query("2025-12-19T08:36:12", "2025-12-19T08:46:12Z")
        with self.assertRaises(ValueError):
            build_query("2025-12-19T08:46:12Z", "2025-12-19T08:36:12Z")

    def test_query_rejects_zero_result_limit(self):
        with self.assertRaises(ValueError):
            build_query("2025-12-19T08:36:12Z", "2025-12-19T08:46:12Z", 0)

    def test_acquisition_time_from_start_time(self):
        result = acquisition_datetime({"startTime": "2025-12-19T08:41:12Z"})
        self.assertEqual(result.isoformat(), "2025-12-19T08:41:12+00:00")

    def test_acquisition_time_from_product_identifier(self):
        result = acquisition_datetime({
            "fileID": "OPERA_L2_RTC-S1_T124-264306-IW2_20251219T084112Z_20251219T184651Z_S1A_30_v1.0"
        })
        self.assertEqual(result.strftime("%Y-%m-%dT%H:%M:%S"), "2025-12-19T08:41:12")

    def test_summary_marks_only_expected_acquisition_time(self):
        collection = {
            "type": "FeatureCollection",
            "features": [{
                "type": "Feature",
                "geometry": {"type": "Polygon", "coordinates": [[[150, -27], [151, -27], [151, -26], [150, -26], [150, -27]]]},
                "properties": {
                    "startTime": ACQUISITIONS["2025-12-19"],
                    "fileID": "opera-test",
                    "operaBurstID": "T124-264306-IW2",
                    "polarization": "VV",
                },
            }],
        }
        report = summarize(parse_collection(__import__("json").dumps(collection).encode()))
        self.assertEqual(report["time_matched_feature_count"], 1)
        self.assertTrue(report["matched_features"][0]["within_source_time_tolerance"])

    def test_static_query_uses_documented_archive_date_and_aoi(self):
        params = build_static_query()
        self.assertEqual(params["processingLevel"], "RTC-STATIC")
        self.assertEqual(params["start"], "2014-04-03T00:00:00Z")
        self.assertEqual(params["end"], "2014-04-04T00:00:00Z")
        self.assertIn("intersectsWith", params)

    def test_invalid_geojson_is_rejected(self):
        with self.assertRaises(ValueError):
            parse_collection(b'{"type":"FeatureCollection","features":[{"type":"Feature"}]}')


if __name__ == "__main__":
    unittest.main()
