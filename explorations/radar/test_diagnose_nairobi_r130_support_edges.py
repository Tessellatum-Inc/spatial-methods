import unittest
import numpy as np
from explorations.radar.diagnose_nairobi_r130_support_edges import support_edge_distance, metrics

class SupportEdgeTests(unittest.TestCase):
    def test_square_interior_distance(self):
        valid=np.ones((9,9),dtype=bool)
        d=support_edge_distance(valid,max_radius=5)
        self.assertEqual(int(d[0,0]),1)
        self.assertEqual(int(d[1,1]),2)
        self.assertEqual(int(d[4,4]),5)

    def test_invalid_hole_creates_internal_edge(self):
        valid=np.ones((9,9),dtype=bool);valid[4,4]=False
        d=support_edge_distance(valid,max_radius=3)
        self.assertEqual(int(d[3,3]),1)
        self.assertEqual(int(d[2,2]),2)

    def test_invalid_pixels_have_zero_distance(self):
        valid=np.ones((5,5),dtype=bool);valid[2,2]=False
        d=support_edge_distance(valid,max_radius=3)
        self.assertEqual(int(d[2,2]),0)

    def test_metrics_preserve_outliers(self):
        x=np.array([0.1,0.2,1.2])
        m=metrics(x)
        self.assertEqual(m["count"],3)
        self.assertAlmostEqual(m["fraction_abs_gt_1_db"],1/3)

if __name__=="__main__":unittest.main()
