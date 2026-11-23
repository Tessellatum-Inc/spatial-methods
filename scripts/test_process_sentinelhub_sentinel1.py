"""Offline tests for the Sentinel Hub Sentinel-1 Process API client."""
import importlib.util
import io
import json
from pathlib import Path
from unittest import mock
import unittest
from urllib.error import HTTPError

ROOT = Path(__file__).resolve().parents[1]
PATH = ROOT / "explorations" / "radar" / "process_sentinelhub_sentinel1.py"
SPEC = importlib.util.spec_from_file_location("process_sentinelhub_sentinel1", PATH)
CLIENT = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(CLIENT)


class FakeResponse:
    def __init__(self, body, content_type="image/tiff"):
        self.body = body
        self.headers = {"Content-Type": content_type}

    def __enter__(self):
        return self

    def __exit__(self, *_args):
        return False

    def read(self):
        return self.body


class ProcessClientTests(unittest.TestCase):
    def setUp(self):
        self.feature = {
            "type": "Feature",
            "id": "S1A_TEST_SCENE",
            "properties": {"datetime": "2026-11-20T03:42:11Z"},
            "geometry": {"type": "Polygon", "coordinates": [[[36.60,-1.50],[37.10,-1.50],[37.10,-1.10],[36.60,-1.10],[36.60,-1.50]]]},
        }

    def test_selects_latest_full_coverage_scene_over_newer_partial_scene(self):
        newer_partial = {
            "id": "newer-partial",
            "properties": {"datetime": "2026-11-22T00:00:00Z"},
            "geometry": {"type": "Polygon", "coordinates": [[[36.65,-1.45],[36.85,-1.45],[36.85,-1.15],[36.65,-1.15],[36.65,-1.45]]]},
        }
        self.assertEqual(
            CLIENT.select_latest_feature({"features": [newer_partial, self.feature]})["id"],
            "S1A_TEST_SCENE",
        )

    def test_requires_explicit_opt_in_for_partial_scene(self):
        partial = {
            "id": "partial",
            "properties": {"datetime": "2026-11-22T00:00:00Z"},
            "geometry": {"type": "Polygon", "coordinates": [[[36.65,-1.45],[36.85,-1.45],[36.85,-1.15],[36.65,-1.15],[36.65,-1.45]]]},
        }
        with self.assertRaisesRegex(ValueError, "No catalogue footprint fully covers"):
            CLIENT.select_latest_feature({"features": [partial]})
        self.assertEqual(
            CLIENT.select_latest_feature({"features": [partial]}, allow_partial=True)["id"],
            "partial",
        )

    def test_reports_full_coverage_fraction(self):
        covers, fraction = CLIENT.feature_coverage(self.feature)
        self.assertTrue(covers)
        self.assertAlmostEqual(fraction, 1.0)

    def test_rejects_empty_catalogue(self):
        with self.assertRaisesRegex(ValueError, "No Sentinel-1"):
            CLIENT.select_latest_feature({"features": []})

    def test_process_request_is_single_acquisition_vv_vh_float32(self):
        payload = CLIENT.build_process_payload(self.feature)
        data = payload["input"]["data"][0]
        self.assertEqual(data["type"], "sentinel-1-grd")
        self.assertEqual(data["processing"]["backCoeff"], "GAMMA0_ELLIPSOID")
        self.assertEqual(payload["output"]["width"], 2048)
        self.assertEqual(payload["output"]["height"], 1536)
        self.assertIn('"VV"', payload["evalscript"])
        self.assertIn('"VH"', payload["evalscript"])
        self.assertIn("FLOAT32", payload["evalscript"])
        self.assertLess(
            data["dataFilter"]["timeRange"]["from"],
            data["dataFilter"]["timeRange"]["to"],
        )

    def test_rejects_oversized_output(self):
        with self.assertRaisesRegex(ValueError, "between 1 and 2500"):
            CLIENT.build_process_payload(self.feature, width=2501)

    @mock.patch.object(CLIENT, "urlopen")
    def test_accepts_geotiff_and_sends_bearer_token(self, mocked):
        tiff = b"II*\x00" + b"\x00" * 64
        mocked.return_value = FakeResponse(tiff)
        result = CLIENT.request_geotiff("token", {"test": True})
        self.assertEqual(result, tiff)
        request = mocked.call_args.args[0]
        self.assertEqual(request.get_header("Authorization"), "Bearer token")
        self.assertEqual(request.full_url, CLIENT.PROCESS_URL)

    @mock.patch.object(CLIENT.time, "sleep")
    @mock.patch.object(CLIENT, "urlopen")
    def test_retries_transient_gateway_error(self, mocked, mocked_sleep):
        tiff = b"II*\\x00" + b"\\x00" * 64
        mocked.side_effect = [
            HTTPError(CLIENT.PROCESS_URL, 502, "Bad Gateway", {}, io.BytesIO(b"")),
            FakeResponse(tiff),
        ]
        self.assertEqual(CLIENT.request_geotiff("token", {}), tiff)
        self.assertEqual(mocked.call_count, 2)
        mocked_sleep.assert_called_once_with(2)

    @mock.patch.object(CLIENT, "urlopen")
    def test_rejects_non_tiff_response(self, mocked):
        mocked.return_value = FakeResponse(b'{"error":"not an image"}', "application/json")
        with self.assertRaisesRegex(RuntimeError, "did not return a GeoTIFF"):
            CLIENT.request_geotiff("token", {})

    @mock.patch.object(CLIENT, "urlopen")
    def test_http_error_does_not_leak_body(self, mocked):
        mocked.side_effect = HTTPError(
            CLIENT.PROCESS_URL, 400, "Bad Request", {},
            io.BytesIO(b'{"detail":"private provider response"}')
        )
        with self.assertRaises(RuntimeError) as raised:
            CLIENT.request_geotiff("token", {})
        self.assertIn("HTTP 400", str(raised.exception))
        self.assertNotIn("private provider response", str(raised.exception))
        self.assertNotIn("token", str(raised.exception))


    @mock.patch.object(CLIENT.time, "sleep")
    @mock.patch.object(CLIENT, "urlopen")
    def test_does_not_retry_non_transient_http_error(self, mocked, mocked_sleep):
        mocked.side_effect = HTTPError(
            CLIENT.PROCESS_URL, 400, "Bad Request", {}, io.BytesIO(b"")
        )
        with self.assertRaisesRegex(RuntimeError, "HTTP 400"):
            CLIENT.request_geotiff("token", {})
        mocked.assert_called_once()
        mocked_sleep.assert_not_called()


if __name__ == "__main__":
    unittest.main()
