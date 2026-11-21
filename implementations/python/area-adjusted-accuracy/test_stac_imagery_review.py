import unittest
from stac_imagery_review import acquisition, asset_for, item_cloud


class StacReviewTests(unittest.TestCase):
    def test_item_cloud_defaults_to_100(self):
        self.assertEqual(item_cloud({"properties": {}}), 100.0)

    def test_item_cloud_reads_eo_cloud_cover(self):
        self.assertEqual(item_cloud({"properties": {"eo:cloud_cover": 17.5}}), 17.5)

    def test_acquisition_reads_datetime(self):
        item = {"properties": {"datetime": "2021-05-01T00:00:00Z"}}
        self.assertEqual(acquisition(item), "2021-05-01T00:00:00Z")

    def test_rgb_asset_aliases(self):
        item = {"assets": {"B04_10m": {"href": "red.tif"}}}
        self.assertEqual(asset_for(item, "red"), ("B04_10m", "red.tif"))

    def test_missing_asset_is_none(self):
        self.assertIsNone(asset_for({"assets": {}}, "blue"))


if __name__ == "__main__":
    unittest.main()
