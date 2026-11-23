import unittest
import numpy as np
from explorations.radar.qa_surat_r009_angle_equation import relation_summary

class SuratAngleEquationTests(unittest.TestCase):
    def test_area_and_ellipsoid_angle_terms_recover_exact_relation(self):
        area=np.array([0.5,0.7,0.9,1.1,1.3,1.5,1.7,1.9,2.1,2.3,2.5,2.7])
        angle=np.linspace(28,48,len(area))
        delta=-10*np.log10(area)-10*np.log10(np.tan(np.deg2rad(angle)))
        result=relation_summary(delta,area,angle)
        self.assertLess(result["area_plus_ellipsoid_angle_residual"]["mae_db"],1e-10)

    def test_invalid_area_and_angle_samples_are_excluded(self):
        area=np.array([0.5,0.7,0.9,1.1,1.3,1.5,1.7,1.9,2.1,2.3,2.5,2.7])
        angle=np.linspace(28,48,len(area))
        delta=-10*np.log10(area)-10*np.log10(np.tan(np.deg2rad(angle)))
        area[0]=0; angle[1]=90
        result=relation_summary(delta,area,angle)
        self.assertEqual(result["sample_count"],10)

if __name__=="__main__": unittest.main()
