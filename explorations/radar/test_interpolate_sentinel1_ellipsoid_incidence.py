import unittest
import numpy as np
from explorations.radar.interpolate_sentinel1_ellipsoid_incidence import cross_validate, interpolate_to_grid

def points_grid():
    points=[]
    for i,lat in enumerate([0.0,1.0,2.0,3.0,4.0]):
        for j,lon in enumerate([0.0,1.0,2.0,3.0,4.0]):
            points.append({"line":float(i*10),"pixel":float(j*10),"latitude":lat,"longitude":lon,
                "incidenceAngle":30.0+2*lon+3*lat})
    return points

class IncidenceInterpolationTests(unittest.TestCase):
    def test_linear_interpolation_recovers_linear_field(self):
        raster,meta=interpolate_to_grid(points_grid(),width=20,height=20,bbox=(1,1,3,3))
        self.assertEqual(raster.shape,(20,20))
        self.assertAlmostEqual(meta["coverage_fraction"],1.0)
        self.assertAlmostEqual(float(np.nanmedian(raster)),40.0,places=2)

    def test_cross_validation_reports_held_out_errors(self):
        result=cross_validate(points_grid())
        self.assertGreater(result["held_out_points_predicted"],0)
        self.assertLess(result["mae_degrees"],1e-8)

    def test_keeps_outside_hull_pixels_nodata_without_extrapolation(self):
        raster,meta=interpolate_to_grid(points_grid(),width=20,height=20,bbox=(-2,-2,6,6))
        self.assertLess(meta["coverage_fraction"],1.0)
        self.assertEqual(meta["extrapolated_pixels"],0)
        self.assertTrue(np.isnan(raster[0,0]))
        with self.assertRaises(ValueError):
            interpolate_to_grid(points_grid(),width=20,height=20,bbox=(-2,-2,6,6),min_coverage_fraction=0.95)

if __name__=="__main__": unittest.main()
