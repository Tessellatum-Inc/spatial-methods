import unittest
import numpy as np
from explorations.radar.compare_opera_nairobi_r130_processors import db, metrics, SUPPORT_THRESHOLD, MIN_COMMON_PIXELS

class NairobiComparisonTests(unittest.TestCase):
    def test_gamma0_reconstruction_delta_identity(self):
        terrain=np.array([0.2,0.5,0.9],dtype=float)
        anf=np.array([1.1,1.3,1.5],dtype=float)
        theta=np.deg2rad(np.array([30.,40.,50.]))
        reconstructed=terrain*anf*np.tan(theta)
        delta=db(terrain)-db(reconstructed)
        expected=-10*np.log10(anf)-10*np.log10(np.tan(theta))
        np.testing.assert_allclose(delta,expected,rtol=1e-12,atol=1e-12)
    def test_residual_metrics(self):
        m=metrics(np.array([-0.1,0.0,0.1]))
        self.assertAlmostEqual(m["bias_mean_db"],0.0)
        self.assertAlmostEqual(m["mae_db"],0.06666666666666667)
        self.assertEqual(m["count"],3)
    def test_declared_support_gates(self):
        self.assertEqual(SUPPORT_THRESHOLD,0.95)
        self.assertEqual(MIN_COMMON_PIXELS,1000)

if __name__=="__main__":unittest.main()
