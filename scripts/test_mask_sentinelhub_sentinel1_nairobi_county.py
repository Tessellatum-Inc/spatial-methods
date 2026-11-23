"""Offline tests for Nairobi County Sentinel-1 masking."""
import importlib.util
import json
from pathlib import Path
import tempfile
from unittest import mock
import unittest

import numpy as np
import rasterio
from rasterio.transform import from_bounds

ROOT = Path(__file__).resolve().parents[1]
PATH = ROOT / "explorations" / "radar" / "mask_sentinelhub_sentinel1_nairobi_county.py"
SPEC = importlib.util.spec_from_file_location("mask_sentinelhub_sentinel1_nairobi_county", PATH)
CLIENT = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(CLIENT)


class FakeResponse:
    def __init__(self, body):
        self.body = body
    def __enter__(self):
        return self
    def __exit__(self, *_args):
        return False
    def read(self):
        return self.body


class CountyMaskTests(unittest.TestCase):
    def setUp(self):
        self.feature = {
            "type": "Feature",
            "properties": {"county": "Nairobi", "area_km2": 696.1, "objectid": 1},
            "geometry": {
                "type": "Polygon",
                "coordinates": [[[36.70,-1.40],[37.00,-1.40],[37.00,-1.20],
                                 [36.70,-1.20],[36.70,-1.40]]],
            },
        }

    @mock.patch.object(CLIENT, "urlopen")
    def test_fetches_and_validates_one_nairobi_feature(self, mocked):
        payload = {"type": "FeatureCollection", "features": [self.feature]}
        mocked.return_value = FakeResponse(json.dumps(payload).encode())
        feature, provenance = CLIENT.fetch_nairobi_boundary()
        self.assertEqual(feature["properties"]["county"], "Nairobi")
        self.assertEqual(provenance["geometry_crs"], "EPSG:4326")
        request = mocked.call_args.args[0]
        self.assertIn("county%3D%27Nairobi%27", request.full_url)

    @mock.patch.object(CLIENT, "urlopen")
    def test_rejects_ambiguous_or_wrong_county(self, mocked):
        mocked.return_value = FakeResponse(json.dumps({
            "type": "FeatureCollection", "features": [self.feature, self.feature]
        }).encode())
        with self.assertRaisesRegex(RuntimeError, "exactly one"):
            CLIENT.fetch_nairobi_boundary()
        wrong = dict(self.feature, properties={"county": "Kiambu"})
        mocked.return_value = FakeResponse(json.dumps({
            "type": "FeatureCollection", "features": [wrong]
        }).encode())
        with self.assertRaisesRegex(RuntimeError, "did not identify"):
            CLIENT.fetch_nairobi_boundary()

    @mock.patch.object(CLIENT, "fetch_nairobi_boundary")
    def test_masks_outside_county_and_reports_county_coverage(self, mocked_fetch):
        mocked_fetch.return_value = (
            self.feature,
            {"service_layer": CLIENT.LAYER_URL, "geometry_crs": "EPSG:4326"},
        )
        with tempfile.TemporaryDirectory() as tmp:
            source = Path(tmp) / "source.tif"
            out = Path(tmp) / "out"
            width, height = 40, 30
            profile = {
                "driver": "GTiff", "width": width, "height": height, "count": 3,
                "dtype": "float32", "crs": "EPSG:4326",
                "transform": from_bounds(36.65, -1.45, 37.05, -1.15, width, height),
            }
            with rasterio.open(source, "w", **profile) as ds:
                ds.write(np.full((height, width), 0.2, dtype=np.float32), 1)
                ds.write(np.full((height, width), 0.03, dtype=np.float32), 2)
                ds.write(np.ones((height, width), dtype=np.float32), 3)
            output, boundary, report_path, report = CLIENT.mask_raster_to_county(source, out)
            self.assertTrue(output.is_file())
            self.assertTrue(boundary.is_file())
            self.assertTrue(report_path.is_file())
            self.assertGreater(report["county_pixel_coverage"]["valid_percent"], 99)
            with rasterio.open(output) as ds:
                vv = ds.read(1)
                mask = ds.read(3)
                self.assertTrue(np.any(vv == CLIENT.NODATA))
                self.assertTrue(np.any(mask == 0))
                self.assertTrue(np.all(vv[mask == 1] == np.float32(0.2)))
            self.assertEqual(json.loads(report_path.read_text())["quality_status"], "pass")


if __name__ == "__main__":
    unittest.main()
