"""Offline tests for the CDSE Sentinel Hub OAuth and Catalog client."""
import importlib.util
import io
import json
from pathlib import Path
from unittest import mock
import unittest
from urllib.error import HTTPError

MODULE_PATH = Path(__file__).resolve().parents[1] / "explorations" / "radar" / "query_sentinelhub_sentinel1.py"
SPEC = importlib.util.spec_from_file_location("query_sentinelhub_sentinel1", MODULE_PATH)
CLIENT = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(CLIENT)


class FakeResponse:
    def __init__(self, payload):
        self.payload = json.dumps(payload).encode("utf-8")

    def __enter__(self):
        return self

    def __exit__(self, *_args):
        return False

    def read(self):
        return self.payload


class SentinelHubClientTests(unittest.TestCase):
    def test_builds_nairobi_sentinel1_iw_search(self):
        payload = CLIENT.build_search_payload(
            "2026-11-01T00:00:00Z", "2026-11-23T00:00:00Z", 12
        )
        self.assertEqual(payload["collections"], ["sentinel-1-grd"])
        self.assertEqual(payload["bbox"], [36.65, -1.45, 37.05, -1.15])
        self.assertEqual(payload["limit"], 12)
        self.assertIn("IW", payload["filter"])

    def test_rejects_naive_timestamps(self):
        with self.assertRaisesRegex(ValueError, "timezone"):
            CLIENT.build_search_payload("2026-11-01", "2026-11-23")

    def test_rejects_reversed_dates(self):
        with self.assertRaisesRegex(ValueError, "earlier"):
            CLIENT.build_search_payload("2026-11-23T00:00:00Z", "2026-11-01T00:00:00Z")

    def test_rejects_limit_above_catalogue_maximum(self):
        with self.assertRaisesRegex(ValueError, "between 1 and 100"):
            CLIENT.build_search_payload("2026-11-01T00:00:00Z", "2026-11-23T00:00:00Z", 101)

    def test_requires_both_oauth_credentials(self):
        with self.assertRaisesRegex(ValueError, "SENTINEL_HUB_CLIENT_ID"):
            CLIENT.request_access_token("", "secret")

    @mock.patch.object(CLIENT, "urlopen")
    def test_requests_client_credentials_token_without_exposing_secret(self, mocked):
        mocked.return_value = FakeResponse({"access_token": "short-lived-token", "expires_in": 3600})
        token = CLIENT.request_access_token("client-id", "client-secret")
        self.assertEqual(token, "short-lived-token")
        request = mocked.call_args.args[0]
        body = request.data.decode("utf-8")
        self.assertIn("grant_type=client_credentials", body)
        self.assertIn("client_id=client-id", body)
        self.assertNotIn("client-secret", request.headers.values())

    @mock.patch.object(CLIENT, "urlopen")
    def test_token_http_error_does_not_leak_response_body(self, mocked):
        mocked.side_effect = HTTPError(
            CLIENT.TOKEN_URL, 401, "Unauthorized", {},
            io.BytesIO(b'{"error_description":"secret should not appear"}')
        )
        with self.assertRaises(RuntimeError) as raised:
            CLIENT.request_access_token("client-id", "client-secret")
        self.assertIn("HTTP 401", str(raised.exception))
        self.assertNotIn("secret should not appear", str(raised.exception))
        self.assertNotIn("client-secret", str(raised.exception))

    @mock.patch.object(CLIENT, "urlopen")
    def test_search_uses_bearer_token_and_validates_feature_collection(self, mocked):
        mocked.return_value = FakeResponse({
            "type": "FeatureCollection",
            "features": [{"type": "Feature", "id": "S1A_TEST"}],
            "context": {"returned": 1, "limit": 20},
        })
        result = CLIENT.search_catalog(
            "bearer-token",
            CLIENT.build_search_payload("2026-11-01T00:00:00Z", "2026-11-23T00:00:00Z"),
        )
        self.assertEqual(result["features"][0]["id"], "S1A_TEST")
        request = mocked.call_args.args[0]
        self.assertEqual(request.get_header("Authorization"), "Bearer bearer-token")

    def test_rejects_catalog_response_without_features(self):
        with mock.patch.object(CLIENT, "urlopen", return_value=FakeResponse({"type": "FeatureCollection"})):
            with self.assertRaisesRegex(ValueError, "features"):
                CLIENT.search_catalog(
                    "token",
                    CLIENT.build_search_payload("2026-11-01T00:00:00Z", "2026-11-23T00:00:00Z"),
                )


if __name__ == "__main__":
    unittest.main()
