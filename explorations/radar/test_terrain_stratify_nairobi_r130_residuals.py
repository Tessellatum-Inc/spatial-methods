import unittest
import numpy as np
from explorations.radar.terrain_stratify_nairobi_r130_residuals import terrain_derivatives, summarize, strata

class TerrainResidualTests(unittest.TestCase):
    def test_planar_eastward_rise_has_expected_slope(self):
        y,x=np.mgrid[0:9,0:9]
        z=2.0*x
        slope,aspect,valid=terrain_derivatives(z,np.ones_like(z,dtype=bool),30)
        self.assertTrue(valid[4,4])
        self.assertAlmostEqual(float(slope[4,4]),np.degrees(np.arctan(2/30)),places=5)
        self.assertAlmostEqual(float(aspect[4,4]),270.0,places=5)

    def test_flat_surface_has_no_aspect(self):
        z=np.ones((7,7))*100
        slope,aspect,valid=terrain_derivatives(z,np.ones_like(z,dtype=bool),30)
        self.assertTrue(valid[3,3])
        self.assertTrue(np.isnan(aspect[3,3]))
        self.assertAlmostEqual(float(slope[3,3]),0.0,places=6)

    def test_invalid_neighborhood_is_excluded(self):
        z=np.ones((7,7));m=np.ones_like(z,dtype=bool);m[3,4]=False
        slope,aspect,valid=terrain_derivatives(z,m,30)
        self.assertFalse(valid[3,3])

    def test_strata_partition(self):
        values=np.array([.1,.2,.3,.4])
        slope=np.array([.5,2,7,20])
        rows=strata(values,slope,[0,1,5,10,30],["flat","low","mid","steep"])
        self.assertEqual(sum(x["count"] for x in rows),4)
        self.assertEqual(rows[0]["count"],1)
        self.assertEqual(summarize(values)["count"],4)

if __name__=="__main__":unittest.main()
