import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import numpy as np
import rasterio
from rasterio.transform import from_origin
from rasterio.warp import transform as transform_coordinates

from multispectral_raster import asset_for_band, read_multispectral_windows


class MultispectralRasterTests(unittest.TestCase):
    def test_asset_selector_prefers_explicit_native_band_alias(self):
        item = {"assets": {
            "B04": {"href": "https://example.test/generic.tif"},
            "B04_10m": {"href": "s3://bucket/native.tif"},
            "B04_10m-jp2": {"href": "https://example.test/native.jp2"},
        }}
        key, asset = asset_for_band(item, "B04")
        self.assertEqual(key, "B04_10m-jp2")
        self.assertEqual(asset["href"], "https://example.test/native.jp2")

    def test_asset_selector_prefers_https_within_same_alias(self):
        item = {"assets": {
            "B11": {"href": "s3://bucket/b11.tif"},
            "B11_20m": {"href": "https://example.test/b11.tif"},
        }}
        key, _ = asset_for_band(item, "B11")
        self.assertEqual(key, "B11_20m")

    def test_unknown_band_is_rejected(self):
        with self.assertRaises(ValueError):
            asset_for_band({"assets": {}}, "B09")

    def _write_asset(self, folder, name, lon, lat, value, resolution):
        x, y = transform_coordinates("EPSG:4326", "EPSG:32760", [lon], [lat])
        transform = from_origin(
            x[0] - 256 * resolution, y[0] + 256 * resolution,
            resolution, resolution
        )
        path = Path(folder) / f"{name}.tif"
        with rasterio.open(
            path, "w", driver="GTiff", width=512, height=512, count=1,
            dtype="uint16", crs="EPSG:32760", transform=transform, nodata=0,
        ) as dataset:
            dataset.write(np.full((512, 512), value, dtype=np.uint16), 1)
        return str(path)

    def test_reads_10m_and_20m_windows_without_resampling(self):
        lon, lat = 179.9, -18.1
        with tempfile.TemporaryDirectory() as folder:
            b04 = self._write_asset(folder, "b04", lon, lat, 4000, 10)
            b08 = self._write_asset(folder, "b08", lon, lat, 6000, 10)
            b11 = self._write_asset(folder, "b11", lon, lat, 2000, 20)
            scl = self._write_asset(folder, "scl", lon, lat, 4, 20)
            item = {"id": "test-scene", "assets": {
                "B04_10m": {"href": b04, "raster:bands": [{"scale": 0.0001, "unit": "reflectance"}]},
                "B08_10m": {"href": b08, "raster:bands": [{"scale": 0.0001, "unit": "reflectance"}]},
                "B11_20m": {"href": b11},
                "SCL_20m": {"href": scl},
            }}
            with patch("multispectral_raster.rasterio_source",
                       side_effect=lambda href: (href, rasterio.Env())):
                result = read_multispectral_windows(
                    item, lon, lat, bands=("B04", "B08", "B11", "SCL"),
                    window_pixels=16,
                )
        self.assertEqual(result["native_grids"], ["10m", "20m"])
        self.assertEqual(result["bands"]["B04"].shape, (32, 32))
        self.assertEqual(result["bands"]["B08"].shape, (32, 32))
        self.assertEqual(result["bands"]["B11"].shape, (16, 16))
        self.assertEqual(result["bands"]["SCL"].shape, (16, 16))
        np.testing.assert_allclose(
            result["band_metadata"]["B04"]["window_bounds"],
            result["band_metadata"]["SCL"]["window_bounds"],
        )
        self.assertAlmostEqual(float(np.nanmean(result["bands"]["B04"])), 0.4, places=5)
        self.assertAlmostEqual(float(np.nanmean(result["bands"]["B08"])), 0.6, places=5)
        self.assertEqual(float(np.nanmean(result["bands"]["B11"])), 2000.0)
        self.assertEqual(float(np.nanmean(result["bands"]["SCL"])), 4.0)

    def test_rejects_misaligned_bands_within_same_native_grid(self):
        lon, lat = 179.9, -18.1
        with tempfile.TemporaryDirectory() as folder:
            b04 = self._write_asset(folder, "b04", lon, lat, 4000, 10)
            b08 = self._write_asset(folder, "b08", lon, lat, 6000, 10)
            x, y = transform_coordinates("EPSG:4326", "EPSG:32760", [lon], [lat])
            shifted = from_origin(x[0] - 255 * 10, y[0] + 256 * 10, 10, 10)
            with rasterio.open(
                b08, "w", driver="GTiff", width=512, height=512, count=1,
                dtype="uint16", crs="EPSG:32760", transform=shifted, nodata=0,
            ) as dataset:
                dataset.write(np.full((512, 512), 6000, dtype=np.uint16), 1)
            item = {"assets": {
                "B04_10m": {"href": b04}, "B08_10m": {"href": b08},
            }}
            with patch("multispectral_raster.rasterio_source",
                       side_effect=lambda href: (href, rasterio.Env())):
                with self.assertRaisesRegex(RuntimeError, "not on the same native grid"):
                    read_multispectral_windows(
                        item, lon, lat, bands=("B04", "B08"), window_pixels=16
                    )

    def test_missing_bands_are_reported_not_fabricated(self):
        result = read_multispectral_windows(
            {"assets": {}}, 179.9, -18.1, bands=("B02", "B11")
        )
        self.assertEqual(result["missing_bands"], ["B02", "B11"])
        self.assertEqual(result["bands"], {})


if __name__ == "__main__":
    unittest.main()
