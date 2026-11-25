import sys
import tempfile
import unittest
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import numpy as np
import rasterio
from rasterio.transform import from_origin
from audit_oam_candidate_against_r130_residuals import inspect_raster

class CandidateOverlapTests(unittest.TestCase):
    def test_counts_candidate_pixel_centres_and_valid_support(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "2026-11-11_T130-279215-IW3_VV_delta-residual-db.tif"
            data = np.array([[1.0, 2.0], [-9999.0, 4.0]], dtype="float32")
            with rasterio.open(path, "w", driver="GTiff", height=2, width=2,
                               count=1, dtype="float32", crs="EPSG:4326",
                               transform=from_origin(0, 2, 1, 1), nodata=-9999.0) as ds:
                ds.write(data, 1)
            geom = {"type": "Polygon", "coordinates": [[[0, 0], [2, 0], [2, 2], [0, 2], [0, 0]]]}
            row = inspect_raster(path, geom)
            self.assertEqual(row["candidate_footprint_pixel_centres"], 4)
            self.assertEqual(row["candidate_footprint_valid_residual_pixels"], 3)
            self.assertAlmostEqual(row["valid_fraction_within_candidate"], .75)
            self.assertEqual(row["date"], "2026-11-11")
            self.assertEqual(row["burst"], "T130-279215-IW3")
            self.assertEqual(row["polarization"], "VV")

if __name__ == "__main__":
    unittest.main()
