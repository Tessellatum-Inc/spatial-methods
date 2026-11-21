import csv
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import numpy as np

from fiji_multispectral_pilot import _index_summaries, run_pilot


class FijiMultispectralPilotTests(unittest.TestCase):
    def test_only_same_native_grid_indices_are_summarized(self):
        bands = {
            "B04": np.full((8, 8), 0.2, dtype=np.float32),
            "B08": np.full((8, 8), 0.6, dtype=np.float32),
            "B03": np.full((8, 8), 0.3, dtype=np.float32),
            "B11": np.full((4, 4), 0.1, dtype=np.float32),
            "B05": np.full((4, 4), 0.2, dtype=np.float32),
            "B8A": np.full((4, 4), 0.5, dtype=np.float32),
        }
        result = _index_summaries(bands)
        self.assertIn("NDVI_10m", result)
        self.assertIn("NDRE_20m_unmasked", result)
        self.assertNotIn("NDRE_20m_scl_valid", result)
        self.assertIn("NDVI_10m_unmasked", result)
        self.assertNotIn("MNDWI", result)
        self.assertNotIn("NDBI", result)

    def test_ndre_exposes_unmasked_and_native_scl_screened_summaries(self):
        bands = {
            "B05": np.full((4, 4), 0.2, dtype=np.float32),
            "B8A": np.full((4, 4), 0.5, dtype=np.float32),
            "SCL": np.array([
                [4, 4, 8, 8],
                [4, 5, 9, 10],
                [4, 4, 4, 4],
                [4, 4, 4, 4],
            ], dtype=np.float32),
        }
        result = _index_summaries(bands)
        self.assertEqual(result["NDRE_20m_unmasked"]["valid_pixel_count"], 16)
        self.assertEqual(result["NDRE_20m_scl_valid"]["valid_pixel_count"], 12)

    def test_runner_reads_first_five_rows_and_writes_blind_report(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            source = root / "points.csv"
            with source.open("w", newline="", encoding="utf-8") as stream:
                writer = csv.DictWriter(
                    stream, fieldnames=["sample_id", "longitude", "latitude"]
                )
                writer.writeheader()
                for i in range(7):
                    writer.writerow({
                        "sample_id": f"P{i}", "longitude": 179.0,
                        "latitude": -18.0,
                    })

            fake_item = {
                "id": "scene-1", "collection": "sentinel-2-c1-l2a",
                "properties": {"datetime": "2021-06-01T00:00:00Z",
                               "eo:cloud_cover": 2.0},
            }
            fake_result = {
                "item_id": "scene-1", "collection": "sentinel-2-c1-l2a",
                "datetime": "2021-06-01T00:00:00Z",
                "bands": {
                    "B02": np.full((4, 4), 0.1),
                    "B03": np.full((4, 4), 0.2),
                    "B04": np.full((4, 4), 0.2),
                    "B08": np.full((4, 4), 0.6),
                },
                "band_metadata": {
                    "B02": {"href": "https://example.test/blue.tif", "crs": "EPSG:32760"},
                    "B03": {"href": "https://example.test/green.tif", "crs": "EPSG:32760"},
                    "B04": {"href": "https://example.test/red.tif", "crs": "EPSG:32760"},
                    "B08": {"href": "https://example.test/nir.tif", "crs": "EPSG:32760"},
                },
                "missing_bands": ["B05", "B06", "B07", "B8A", "B11", "B12", "SCL"],
                "native_grids": ["10m"],
            }
            with patch("fiji_multispectral_pilot.search_catalogue",
                       return_value=([fake_item], [])), patch(
                "fiji_multispectral_pilot.read_multispectral_windows",
                return_value=fake_result,
            ):
                result = run_pilot(source, root / "out", point_limit=5, item_limit=1)

            self.assertEqual(result["points_requested"], 5)
            self.assertEqual(result["candidate_rows"], 5)
            with (root / "out" / "fiji-multispectral-pilot.csv").open(
                newline="", encoding="utf-8"
            ) as stream:
                rows = list(csv.DictReader(stream))
            self.assertEqual(len(rows), 5)
            self.assertEqual(rows[0]["status"], "core_bands_read")
            self.assertNotIn("label", ",".join(rows[0].keys()).lower())
            self.assertNotIn("transition", ",".join(rows[0].keys()).lower())


if __name__ == "__main__":
    unittest.main()
