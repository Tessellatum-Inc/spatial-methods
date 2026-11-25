import unittest
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from shapely.geometry import box, mapping
from query_oam_reference_candidates import audit, search_items, validate_asset_href, STAC_ROOT


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
                          "license": "PROPRIETARY-OUTER", "oam:producer_name": "SDI Kenya",
                          "oam:platform_type": "uav",
                          "oam:acquisition_time_estimated": False},
            "assets": {"visual": {"href": "https://example.org/a.tif"}},
            "license": "CC-BY-4.0",
        }
        row = audit([item])[0]
        self.assertTrue(row["intersects_r130_bbox"])
        self.assertEqual(row["license"], "CC-BY-4.0")
        self.assertEqual(row["producer_name"], "SDI Kenya")
        self.assertEqual(row["platform_type"], "uav")
        self.assertFalse(row["acquisition_time_estimated"])
        self.assertEqual(row["https_asset_hrefs_available"], 1)

    def test_missing_geometry_is_not_overlap(self):
        row = audit([{"id": "unknown", "properties": {}, "assets": {}}])[0]
        self.assertIsNone(row["intersects_r130_bbox"])
        self.assertFalse(row["geometry_present"])


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
