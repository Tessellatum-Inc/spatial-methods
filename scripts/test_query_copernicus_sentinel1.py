"""Offline tests for the Nairobi Copernicus Sentinel-1 OData discovery client."""
import importlib.util
from pathlib import Path
import unittest
from unittest.mock import patch

MODULE_PATH = Path(__file__).resolve().parents[1] / "explorations" / "radar" / "query_copernicus_sentinel1.py"
SPEC = importlib.util.spec_from_file_location("query_copernicus_sentinel1", MODULE_PATH)
QUERY = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(QUERY)


class CopernicusQueryTests(unittest.TestCase):
    def test_default_query_has_collection_product_type_and_closed_aoi(self):
        params = QUERY.build_query(QUERY.DEFAULT_START, QUERY.DEFAULT_END, 100)
        query = params["$filter"]
        self.assertIn("Collection/Name eq 'SENTINEL-1'", query)
        self.assertIn("Value eq 'IW_GRDH_1S'", query)
        self.assertIn("SRID=4326;POLYGON((", query)
        self.assertIn("36.65 -1.45", query)
        self.assertIn("36.65 -1.45))')", query)
        self.assertEqual(params["$top"], "100")
        self.assertEqual(params["$expand"], "Attributes")

    def test_location_query_rejects_empty_product_id(self):
        with self.assertRaisesRegex(ValueError, "non-empty string"):
            QUERY.build_location_query("")

    def test_location_query_expands_locations_for_exact_product(self):
        url = QUERY.build_location_query("abc-123")
        self.assertIn("Id+eq+%27abc-123%27", url)
        self.assertIn("%24expand=Locations", url)

    @patch.object(
        QUERY,
        "retrieve",
        return_value=b'{"value":[{"Id":"abc","Locations":[{"Type":"product"}]}]}',
    )
    def test_attaches_product_locations(self, mock_retrieve):
        products = [{"Id": "abc", "Name": "example"}]
        errors = QUERY.attach_product_locations(products, timeout=10)
        self.assertEqual(errors, [])
        self.assertTrue(products[0]["LocationsRetrieved"])
        self.assertEqual(products[0]["Locations"], [{"Type": "product"}])
        mock_retrieve.assert_called_once()

    @patch.object(QUERY, "retrieve", side_effect=QUERY.URLError("offline"))
    def test_records_location_lookup_failure_without_losing_product(self, mock_retrieve):
        products = [{"Id": "abc", "Name": "example"}]
        errors = QUERY.attach_product_locations(products, timeout=10)
        self.assertEqual(len(errors), 1)
        self.assertFalse(products[0]["LocationsRetrieved"])
        self.assertEqual(products[0]["Id"], "abc")
        self.assertIn("offline", products[0]["LocationsFetchError"])
        mock_retrieve.assert_called_once()


    def test_normalizes_timestamp_to_utc(self):
        params = QUERY.build_query("2026-10-01T03:00:00+03:00", "2026-11-22T03:00:00+03:00", 10)
        self.assertIn("2026-10-01T00:00:00.000Z", params["$filter"])
        self.assertIn("2026-11-22T00:00:00.000Z", params["$filter"])

    def test_rejects_naive_timestamp(self):
        with self.assertRaisesRegex(ValueError, "explicit UTC offset"):
            QUERY.build_query("2026-10-01T00:00:00", QUERY.DEFAULT_END, 10)

    def test_rejects_invalid_window(self):
        with self.assertRaisesRegex(ValueError, "earlier than end"):
            QUERY.build_query(QUERY.DEFAULT_END, QUERY.DEFAULT_START, 10)

    def test_rejects_invalid_limit(self):
        with self.assertRaisesRegex(ValueError, "between 1 and 1000"):
            QUERY.build_query(QUERY.DEFAULT_START, QUERY.DEFAULT_END, 1001)

    def test_accepts_empty_catalogue(self):
        self.assertEqual(QUERY.parse_catalogue_response(b'{"value":[]}')["value"], [])

    def test_accepts_product_with_optional_footprint(self):
        raw = b'{"value":[{"Id":"abc","Name":"S1A_IW_GRDH_1SDV_example","GeoFootprint":null}]}'
        self.assertEqual(len(QUERY.parse_catalogue_response(raw)["value"]), 1)

    def test_rejects_api_error_object(self):
        with self.assertRaisesRegex(ValueError, "no valid 'value' array"):
            QUERY.parse_catalogue_response(b'{"error":{"message":"bad filter"}}')

    def test_rejects_product_without_id(self):
        with self.assertRaisesRegex(ValueError, "no usable Id"):
            QUERY.parse_catalogue_response(b'{"value":[{"Name":"example"}]}')

    def test_rejects_non_object_product(self):
        with self.assertRaisesRegex(ValueError, "not a JSON object"):
            QUERY.parse_catalogue_response(b'{"value":["bad"]}')

    def test_rejects_invalid_footprint_type(self):
        with self.assertRaisesRegex(ValueError, "invalid GeoFootprint"):
            QUERY.parse_catalogue_response(b'{"value":[{"Id":"abc","Name":"x","GeoFootprint":"bad"}]}')


if __name__ == "__main__":
    unittest.main()
