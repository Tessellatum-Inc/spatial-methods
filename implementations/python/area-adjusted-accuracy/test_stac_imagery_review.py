import unittest
from unittest.mock import Mock, patch

import requests

from stac_imagery_review import (
    acquisition,
    asset_for,
    item_cloud,
    post_search,
    search_catalogue,
)


def response(payload):
    result = Mock()
    result.json.return_value = payload
    result.raise_for_status.return_value = None
    return result


class StacReviewTests(unittest.TestCase):
    def test_item_cloud_defaults_to_100(self):
        self.assertEqual(item_cloud({"properties": {}}), 100.0)

    def test_item_cloud_reads_eo_cloud_cover(self):
        self.assertEqual(item_cloud({"properties": {"eo:cloud_cover": 17.5}}), 17.5)

    def test_invalid_cloud_cover_is_conservative(self):
        self.assertEqual(item_cloud({"properties": {"eo:cloud_cover": 140}}), 100.0)
        self.assertEqual(item_cloud({"properties": {"eo:cloud_cover": "unknown"}}), 100.0)

    def test_acquisition_reads_datetime(self):
        item = {"properties": {"datetime": "2021-05-01T00:00:00Z"}}
        self.assertEqual(acquisition(item), "2021-05-01T00:00:00Z")

    def test_rgb_asset_prefers_explicit_10m_band(self):
        item = {"assets": {
            "B04": {"href": "generic.tif"},
            "B04_10m": {"href": "red-10m.tif"},
        }}
        self.assertEqual(asset_for(item, "red"), ("B04_10m", "red-10m.tif"))

    def test_rgb_asset_supports_earth_search_alias(self):
        item = {"assets": {"blue": {"href": "blue.tif"}}}
        self.assertEqual(asset_for(item, "blue"), ("blue", "blue.tif"))

    def test_missing_asset_is_none(self):
        self.assertIsNone(asset_for({"assets": {}}, "blue"))

    def test_unknown_band_is_rejected(self):
        with self.assertRaises(ValueError):
            asset_for({"assets": {}}, "nir")

    @patch("stac_imagery_review.requests.get")
    @patch("stac_imagery_review.requests.post")
    def test_search_follows_next_link_and_deduplicates(self, post, get):
        post.return_value = response({
            "features": [{"id": "one"}],
            "links": [{"rel": "next", "href": "https://catalogue.test/search?page=2"}],
        })
        get.return_value = response({"features": [{"id": "one"}, {"id": "two"}]})

        items = post_search("https://catalogue.test/search", "sentinel", 179.9, -18.1)

        self.assertEqual([item["id"] for item in items], ["one", "two"])
        body = post.call_args.kwargs["json"]
        self.assertNotIn("sortby", body)
        self.assertEqual(body["intersects"]["coordinates"], [179.9, -18.1])
        get.assert_called_once()

    @patch("stac_imagery_review.post_search")
    def test_catalogue_preserves_partial_collection_failure(self, search):
        search.side_effect = [
            [{"id": "valid", "collection": "good"}],
            requests.HTTPError("collection unavailable"),
        ]
        items, errors = search_catalogue(
            "https://catalogue.test/search", ("good", "bad"), 179.9, -18.1
        )
        self.assertEqual([item["id"] for item in items], ["valid"])
        self.assertEqual(len(errors), 1)
        self.assertIn("collection unavailable", errors[0])

    def test_search_page_limit_must_be_positive(self):
        with self.assertRaises(ValueError):
            post_search("https://catalogue.test/search", "sentinel", 0, 0, max_pages=0)


if __name__ == "__main__":
    unittest.main()
