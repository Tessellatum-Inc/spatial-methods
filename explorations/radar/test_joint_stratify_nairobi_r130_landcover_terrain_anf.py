import unittest
from types import SimpleNamespace
import numpy as np
from affine import Affine
from rasterio.crs import CRS
from explorations.radar.joint_stratify_nairobi_r130_landcover_terrain_anf import (
    report_date, pixel_spacing_metres, terrain, summarize,
)
class JointStratificationTests(unittest.TestCase):
    def test_iso_date_is_preserved_and_compact_rejected(self):
        self.assertEqual(report_date("2026-10-06"),"2026-10-06")
        with self.assertRaises(ValueError): report_date("20261006")
    def test_geographic_pixel_spacing_is_metric(self):
        grid=SimpleNamespace(transform=Affine(0.00027,0,36.8,0,-0.00027,-1.3),
            height=100,width=100,crs=CRS.from_epsg(4326))
        dx,dy=pixel_spacing_metres(grid)
        self.assertGreater(dx,25);self.assertLess(dx,35)
        self.assertGreater(dy,25);self.assertLess(dy,35)
    def test_planar_slope_uses_metric_spacing(self):
        y,x=np.mgrid[0:9,0:9]
        z=2*x
        slope=terrain(z,np.ones_like(z,dtype=bool),30,30)
        self.assertAlmostEqual(float(slope[4,4]),np.degrees(np.arctan(2/30)),places=5)
    def test_summary_reports_no_fake_samples(self):
        self.assertEqual(summarize([np.nan])["count"],0)
        self.assertEqual(summarize([.1,.2])["count"],2)
if __name__=="__main__":unittest.main()
