"""Offline tests for the Nairobi ASF Sentinel-1 catalogue query client."""
import importlib.util
from pathlib import Path
import unittest

MODULE_PATH = Path(__file__).resolve().parents[1] / "explorations" / "radar" / "query_asf_sentinel1.py"
SPEC = importlib.util.spec_from_file_location("query_asf_sentinel1", MODULE_PATH)
QUERY = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(QUERY)


class ASFQueryTests(unittest.TestCase):
    def test_default_query_is_explicit_and_closed_wkt(self):
        params = QUERY.build_query(
            QUERY.DEFAULT_START, QUERY.DEFAULT_END, "VV+VH", 30
        )
        self.assertEqual(params["dataset"], "SENTINEL-1")
        self.assertEqual(params["beamMode"], "IW")
        self.assertEqual(params["processingLevel"], "GRD_HD")
        self.assertEqual(params["polarization"], "VV+VH")
        self.assertEqual(params["output"], "geojson")
        self.assertEqual(params["maxResults"], "30")
        self.assertTrue(params["intersectsWith"].startswith("polygon(("))
        self.assertTrue(params["intersectsWith"].endswith("))"))
        self.assertEqual(
            params["intersectsWith"].split(",")[0],
            "polygon((36.65 -1.45",
        )

    def test_vv_fallback_is_a_separate_parameter_choice(self):
        params = QUERY.build_query("2026-10-01T00:00:00Z", "2026-11-21T23:59:59Z", "VV", 30)
        self.assertEqual(params["polarization"], "VV")

    def test_rejects_nonpositive_result_limit(self):
        with self.assertRaises(ValueError):
            QUERY.build_query("start", "end", "VV+VH", 0)

    def test_accepts_empty_feature_collection(self):
        payload = QUERY.parse_feature_collection(
            b'{"type":"FeatureCollection","features":[]}'
        )
        self.assertEqual(payload["features"], [])

    def test_accepts_well_formed_feature(self):
        raw = (
            b'{"type":"FeatureCollection","features":['
            b'{"type":"Feature","geometry":{"type":"Point","coordinates":[36.8,-1.3]},'
            b'"properties":{"fileID":"example"}}]}'
        )
        self.assertEqual(len(QUERY.parse_feature_collection(raw)["features"]), 1)

    def test_rejects_api_error_json_as_not_geojson(self):
        with self.assertRaisesRegex(ValueError, "FeatureCollection"):
            QUERY.parse_feature_collection(b'{"error":"bad query"}')

    def test_rejects_malformed_feature(self):
        raw = b'{"type":"FeatureCollection","features":[{"type":"Feature"}]}'
        with self.assertRaisesRegex(ValueError, "lacks properties or geometry"):
            QUERY.parse_feature_collection(raw)


if __name__ == "__main__":
    unittest.main()
