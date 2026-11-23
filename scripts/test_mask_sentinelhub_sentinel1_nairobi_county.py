"""Offline tests for Nairobi County Sentinel-1 masking."""
import hashlib
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
            "properties": {"shapeName": "Nairobi", "shapeISO": "KEN-030", "shapeID": "KEN-ADM1-030"},
            "geometry": {
                "type": "Polygon",
                "coordinates": [[[36.70,-1.40],[37.00,-1.40],[37.00,-1.20],
                                 [36.70,-1.20],[36.70,-1.40]]],
            },
        }
        self.features = [self.feature] + [
            {
                "type": "Feature",
                "properties": {"shapeName": f"County {index}"},
                "geometry": self.feature["geometry"],
            }
            for index in range(1, CLIENT.BOUNDARY_FEATURE_COUNT)
        ]
        self.raw = json.dumps({"type": "FeatureCollection", "features": self.features}).encode()
        self.digest = hashlib.sha256(self.raw).hexdigest()

    @mock.patch.object(CLIENT, "urlopen")
    def test_downloads_pinned_dataset_and_selects_one_nairobi_feature(self, mocked):
        mocked.return_value = FakeResponse(self.raw)
        with mock.patch.object(CLIENT, "BOUNDARY_SIZE_BYTES", len(self.raw)), \
             mock.patch.object(CLIENT, "BOUNDARY_LFS_SHA256", self.digest):
            feature, provenance = CLIENT.fetch_nairobi_boundary()
        self.assertEqual(feature["properties"]["shapeName"], "Nairobi")
        self.assertEqual(provenance["boundary_id"], "KEN-ADM1-32016919")
        self.assertEqual(provenance["feature_count"], 47)
        self.assertEqual(provenance["downloaded_file_sha256"], self.digest)
        self.assertIn("media.githubusercontent.com", mocked.call_args.args[0].full_url)

    @mock.patch.object(CLIENT, "urlopen")
    def test_rejects_checksum_mismatch(self, mocked):
        mocked.return_value = FakeResponse(self.raw)
        with mock.patch.object(CLIENT, "BOUNDARY_SIZE_BYTES", len(self.raw)):
            with self.assertRaisesRegex(RuntimeError, "checksum mismatch"):
                CLIENT.fetch_nairobi_boundary()

    @mock.patch.object(CLIENT, "urlopen")
    def test_rejects_wrong_feature_count(self, mocked):
        raw = json.dumps({"type": "FeatureCollection", "features": self.features[:-1]}).encode()
        mocked.return_value = FakeResponse(raw)
        with mock.patch.object(CLIENT, "BOUNDARY_SIZE_BYTES", len(raw)), \
             mock.patch.object(CLIENT, "BOUNDARY_LFS_SHA256", hashlib.sha256(raw).hexdigest()):
            with self.assertRaisesRegex(RuntimeError, "Expected 47"):
                CLIENT.fetch_nairobi_boundary()

    @mock.patch.object(CLIENT, "urlopen")
    def test_rejects_ambiguous_or_missing_nairobi_county(self, mocked):
        duplicate = dict(self.feature, properties={"shapeName": "Nairobi City"})
        duplicate_payload = json.dumps({
            "type": "FeatureCollection", "features": [self.feature, duplicate] + self.features[2:]
        }).encode()
        mocked.return_value = FakeResponse(duplicate_payload)
        with mock.patch.object(CLIENT, "BOUNDARY_SIZE_BYTES", len(duplicate_payload)), \
             mock.patch.object(CLIENT, "BOUNDARY_LFS_SHA256", hashlib.sha256(duplicate_payload).hexdigest()):
            with self.assertRaisesRegex(RuntimeError, "received 2"):
                CLIENT.fetch_nairobi_boundary()

        wrong_features = [dict(item, properties={"shapeName": f"County {index}"})
                          for index, item in enumerate(self.features)]
        wrong_payload = json.dumps({"type": "FeatureCollection", "features": wrong_features}).encode()
        mocked.return_value = FakeResponse(wrong_payload)
        with mock.patch.object(CLIENT, "BOUNDARY_SIZE_BYTES", len(wrong_payload)), \
             mock.patch.object(CLIENT, "BOUNDARY_LFS_SHA256", hashlib.sha256(wrong_payload).hexdigest()):
            with self.assertRaisesRegex(RuntimeError, "received 0"):
                CLIENT.fetch_nairobi_boundary()

    @mock.patch.object(CLIENT, "fetch_nairobi_boundary")
    def test_masks_outside_county_and_reports_county_coverage(self, mocked_fetch):
        mocked_fetch.return_value = (
            self.feature,
            {"provider": "geoBoundaries", "boundary_id": CLIENT.BOUNDARY_ID,
             "download_url": CLIENT.BOUNDARY_URL, "geometry_crs": "EPSG:4326"},
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
            self.assertEqual(report["boundary_provenance"]["provider"], "geoBoundaries")
            with rasterio.open(output) as ds:
                vv = ds.read(1)
                mask = ds.read(3)
                self.assertTrue(np.any(vv == CLIENT.NODATA))
                self.assertTrue(np.any(mask == 0))
                self.assertTrue(np.all(vv[mask == 1] == np.float32(0.2)))
            self.assertEqual(json.loads(report_path.read_text())["quality_status"], "pass")


if __name__ == "__main__":
    unittest.main()
