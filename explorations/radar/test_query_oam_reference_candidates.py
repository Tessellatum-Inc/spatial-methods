import unittest
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from shapely.geometry import box, mapping
from query_oam_reference_candidates import (audit, search_items, validate_asset_href,
    fetch_source_metadata, STAC_ROOT)


class OAMReferenceAuditTests(unittest.TestCase):
    def test_https_asset_only(self):
        self.assertTrue(validate_asset_href("https://example.org/image.tif"))
        self.assertFalse(validate_asset_href("http://example.org/image.tif"))
        self.assertFalse(validate_asset_href("file:///tmp/image.tif"))

    def test_geometry_intersection_screen(self):
        item = {
            "id": "inside",
            "geometry": mapping(box(36.7, -1.4, 36.8, -1.3)),
            "properties": {"datetime": "2026-10-13T10:00:00Z", "gsd": 0.04,
                          "license": "CC-BY-4.0", "oam:producer_name": "SDI Kenya",
                          "oam:platform_type": "uav",
                          "oam:acquisition_time_estimated": False},
            "assets": {"visual": {"href": "https://example.org/a.tif"}},
            "license": "PROPRIETARY-OUTER",
        }
        row = audit([item])[0]
        self.assertTrue(row["intersects_r130_bbox"])
        self.assertEqual(row["license"], "CC-BY-4.0")
        self.assertEqual(row["producer_name"], "SDI Kenya")
        self.assertEqual(row["platform_type"], "uav")
        self.assertFalse(row["acquisition_time_estimated"])
        self.assertEqual(row["https_asset_hrefs_available"], 1)
        self.assertEqual(row["geometry"], item["geometry"])
        self.assertEqual(row["assets"]["visual"]["href"], "https://example.org/a.tif")
        self.assertFalse(row["assets"]["visual"]["href_query_redacted"])


    def test_asset_query_string_is_redacted_but_provenance_is_retained(self):
        item = {
            "id": "signed",
            "geometry": mapping(box(36.7, -1.4, 36.8, -1.3)),
            "properties": {},
            "assets": {"metadata": {
                "href": "https://example.org/item.json?token=secret",
                "type": "application/json",
                "roles": ["metadata"],
                "title": "Item metadata",
            }},
        }
        row = audit([item])[0]
        asset = row["assets"]["metadata"]
        self.assertEqual(asset["href"], "https://example.org/item.json")
        self.assertTrue(asset["href_query_redacted"])
        self.assertNotIn("secret", str(row))

    def test_missing_geometry_is_not_overlap(self):
        row = audit([{"id": "unknown", "properties": {}, "assets": {}}])[0]
        self.assertIsNone(row["intersects_r130_bbox"])
        self.assertFalse(row["geometry_present"])



    def test_fetch_source_metadata_from_allowlisted_host(self):
        class Response:
            status_code = 200
            headers = {"Content-Length": "22"}
            def iter_content(self, chunk_size):
                yield b'{"capture":"2026-11-05"}'
        class Session:
            def get(self, href, **kwargs):
                self.href, self.kwargs = href, kwargs
                return Response()
        session = Session()
        result = fetch_source_metadata(
            "https://oin-hotosm-prod.s3.us-east-1.amazonaws.com/item_meta.json",
            session=session)
        self.assertEqual(result["status"], "ok")
        self.assertEqual(result["metadata"]["capture"], "2026-11-05")
        self.assertFalse(session.kwargs["allow_redirects"])

    def test_fetch_source_metadata_blocks_untrusted_host(self):
        class Session:
            def get(self, *args, **kwargs):
                raise AssertionError("untrusted host must not be requested")
        result = fetch_source_metadata("https://example.org/meta.json", session=Session())
        self.assertEqual(result["status"], "blocked_untrusted_metadata_host")

    def test_audit_can_attach_source_metadata(self):
        class Response:
            status_code = 200
            headers = {"Content-Length": "17"}
            def iter_content(self, chunk_size):
                yield b'{"source":"OAM"}'
        class Session:
            def get(self, href, **kwargs):
                return Response()
        item = {"id": "metadata-item", "geometry": None, "properties": {},
                "assets": {"metadata": {"href":
                    "https://oin-hotosm-prod.s3.us-east-1.amazonaws.com/meta.json"}}}
        row = audit([item], fetch_metadata=True, session=Session())[0]
        self.assertEqual(row["source_metadata"]["status"], "ok")
        self.assertEqual(row["source_metadata"]["metadata"]["source"], "OAM")

    def test_post_pagination_link_is_followed(self):
        class Response:
            def __init__(self, payload, url):
                self.payload, self.url = payload, url
            def raise_for_status(self):
                pass
            def json(self):
                return self.payload

        class Session:
            def __init__(self):
                self.calls = []
            def get(self, url, **kwargs):
                self.calls.append(("GET", url, kwargs))
                return Response({
                    "features": [{"id": "first"}],
                    "links": [{"rel": "next", "href": STAC_ROOT + "/search",
                               "method": "POST", "body": {"token": "page-2"}}]
                }, url)
            def post(self, url, **kwargs):
                self.calls.append(("POST", url, kwargs))
                return Response({"features": [{"id": "second"}], "links": []}, url)

        session = Session()
        items, pages = search_items(session=session)
        self.assertEqual([x["id"] for x in items], ["first", "second"])
        self.assertEqual([x[0] for x in session.calls], ["GET", "POST"])
        self.assertEqual(session.calls[1][2]["json"], {"token": "page-2"})
        self.assertEqual(len(pages), 2)

    def test_rejects_external_next_link(self):
        class Response:
            url = STAC_ROOT + "/search"
            def raise_for_status(self):
                pass
            def json(self):
                return {"features": [], "links": [
                    {"rel": "next", "href": "https://attacker.example/collect"}
                ]}
        class Session:
            def get(self, url, **kwargs):
                return Response()
        with self.assertRaises(ValueError):
            search_items(session=Session())


if __name__ == "__main__":
    unittest.main()
