""""Offline tests for the parallel Sentinel-1 gamma0 terrain branch."""
import importlib.util
from pathlib import Path
import unittest
from http.client import IncompleteRead
from unittest.mock import patch

import numpy as np

ROOT = Path(__file__).resolve().parents[2]
SCRIPT = ROOT / "explorations" / "radar" / "process_sentinel1_gamma0_terrain.py"
SPEC = importlib.util.spec_from_file_location("process_sentinel1_gamma0_terrain", SCRIPT)
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


class Gamma0TerrainTests(unittest.TestCase):
    def feature(self):
        return {"properties": {"datetime": "2026-11-14T03:11:11Z"}}

    def test_payload_requests_terrain_correction_and_auxiliary_bands(self):
        payload = MODULE.build_rtc_payload(self.feature())
        processing = payload["input"]["data"][0]["processing"]
        self.assertEqual(processing["backCoeff"], "GAMMA0_TERRAIN")
        self.assertTrue(processing["orthorectify"])
        self.assertEqual(processing["demInstance"], "COPERNICUS_30")
        self.assertEqual(processing["radiometricTerrainOversampling"], 2)
        for band in ("VV", "VH", "scatteringArea", "localIncidenceAngle", "shadowMask", "dataMask"):
            self.assertIn(band, payload["evalscript"])

    def test_rejects_unsupported_dem_and_oversampling(self):
        with self.assertRaisesRegex(ValueError, "DEM"):
            MODULE.build_rtc_payload(self.feature(), dem_instance="SRTM")
        with self.assertRaisesRegex(ValueError, "oversampling"):
            MODULE.build_rtc_payload(self.feature(), oversampling=5)

    def test_summarizes_six_band_rtc_stack(self):
        # Band order: VV, VH, scatteringArea, localIncidenceAngle, shadowMask, dataMask.
        # Initialize shadow-free pixels and fully valid data, then flag one shadow pixel.
        a = np.ones((6, 3, 3), dtype=np.float32)
        a[0] *= 0.1
        a[1] *= 0.01
        a[2] *= 0.8
        a[3] *= 40
        a[4] = 0
        a[4, 0, 0] = 1
        report = MODULE.summarize_rtc(a)
        self.assertEqual(report["valid_pixels"], 9)
        self.assertAlmostEqual(report["shadow_mask_fraction_of_valid_pixels"], 1 / 9)
        self.assertAlmostEqual(report["vv_median_db"], -10.0, places=6)


    def test_process_api_retries_incomplete_chunked_response(self):
        class Response:
            headers = {"Content-Type": "image/tiff"}
            def __enter__(self):
                return self
            def __exit__(self, *args):
                return False
            def read(self):
                return bytes.fromhex("49492a00") + bytes(8)

        with patch.object(MODULE._PROCESS, "urlopen",
                          side_effect=[IncompleteRead(b"", 12), Response()]) as mocked, \
             patch.object(MODULE._PROCESS.time, "sleep") as sleep:
            body = MODULE._PROCESS.request_geotiff("token", {"test": True}, timeout=1)
        self.assertEqual(body[:4], bytes.fromhex("49492a00"))
        self.assertEqual(mocked.call_count, 2)
        sleep.assert_called_once_with(2)

    def test_rejects_invalid_angle(self):
        a = np.ones((6, 2, 2), dtype=np.float32)
        a[3, 0, 0] = 181
        with self.assertRaisesRegex(ValueError, "incidence angle"):
            MODULE.summarize_rtc(a)

    def test_rejects_invalid_band_count(self):
        with self.assertRaisesRegex(ValueError, "six bands"):
            MODULE.summarize_rtc(np.ones((5, 2, 2), dtype=np.float32))


if __name__ == "__main__":
    unittest.main()
