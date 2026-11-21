import tempfile
import unittest
from pathlib import Path
from unittest.mock import Mock, patch

import numpy as np
import rasterio
import requests
from rasterio.transform import from_origin
from rasterio.warp import transform as transform_coordinates

from stac_imagery_review import (
    acquisition,
    asset_for,
    item_cloud,
    post_search,
    search_catalogue,
    write_provenance,
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


    def test_provenance_writer_handles_mixed_discovery_and_chip_rows(self):
        with tempfile.TemporaryDirectory() as folder:
            output = Path(folder) / "provenance.csv"
            rows = [
                {"sample_id": "p1", "status": "no_items", "notes": "none"},
                {"sample_id": "p2", "status": "chip_created", "assets": '{"red": "B04_10m"}',
                 "source_grid": "{}", "read_method": "window"},
            ]
            write_provenance(output, rows)
            import csv
            with open(output, newline="", encoding="utf-8") as stream:
                records = list(csv.DictReader(stream))
            self.assertEqual(len(records), 2)
            self.assertEqual(records[0]["assets"], "")
            self.assertEqual(records[1]["assets"], '{"red": "B04_10m"}')
            self.assertEqual(records[1]["read_method"], "window")

    def test_provenance_writer_removes_stale_output_for_empty_run(self):
        with tempfile.TemporaryDirectory() as folder:
            output = Path(folder) / "provenance.csv"
            output.write_text("stale", encoding="utf-8")
            write_provenance(output, [])
            self.assertFalse(output.exists())

    def _write_rgb_assets(self, folder, lon, lat, misalign_blue=False):
        x, y = transform_coordinates("EPSG:4326", "EPSG:32760", [lon], [lat])
        transform = from_origin(x[0] - 2560, y[0] + 2560, 10, 10)
        assets = {}
        for band, value in (("B04_10m", 3000), ("B03_10m", 2000), ("B02_10m", 1000)):
            band_transform = transform
            if misalign_blue and band == "B02_10m":
                band_transform = from_origin(x[0] - 2550, y[0] + 2560, 10, 10)
            path = Path(folder) / f"{band}.tif"
            with rasterio.open(
                path, "w", driver="GTiff", width=512, height=512, count=1,
                dtype="uint16", crs="EPSG:32760", transform=band_transform,
            ) as dataset:
                dataset.write(np.full((512, 512), value, dtype=np.uint16), 1)
            assets[band] = {"href": str(path)}
        return {"assets": assets, "properties": {"datetime": "2021-06-01T00:00:00Z"}}

    def test_chip_reprojects_wgs84_point_to_raster_crs(self):
        from stac_imagery_review import render_chip
        lon, lat = 179.9, -18.1
        with tempfile.TemporaryDirectory() as folder:
            item = self._write_rgb_assets(folder, lon, lat)
            with patch("stac_imagery_review.rasterio_source",
                       side_effect=lambda href: (href, rasterio.Env())):
                result = render_chip(item, lon, lat, Path(folder) / "chip.png", 64)
        self.assertEqual(result["chip_width"], 64)
        self.assertEqual(result["chip_height"], 64)
        self.assertEqual(result["assets"], '{"blue": "B02_10m", "green": "B03_10m", "red": "B04_10m"}')

    def test_chip_rejects_misaligned_rgb_assets(self):
        from stac_imagery_review import render_chip
        lon, lat = 179.9, -18.1
        with tempfile.TemporaryDirectory() as folder:
            item = self._write_rgb_assets(folder, lon, lat, misalign_blue=True)
            with patch("stac_imagery_review.rasterio_source",
                       side_effect=lambda href: (href, rasterio.Env())):
                with self.assertRaisesRegex(RuntimeError, "not on the same grid"):
                    render_chip(item, lon, lat, Path(folder) / "chip.png", 64)


if __name__ == "__main__":
    unittest.main()
