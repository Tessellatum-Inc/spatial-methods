import unittest
import numpy as np
from explorations.radar.qa_surat_r009_angle_equation import relation_summary, valid_geometry_mask

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

    def test_shadow_and_invalid_incidence_pixels_are_excluded(self):
        ellipsoid=np.ones((2,3),dtype=bool)
        rtc=np.ones((2,3),dtype=bool)
        shadow=np.zeros((2,3),dtype=float)
        angle=np.full((2,3),40.0)
        shadow[0,1]=1.0
        angle[1,2]=np.nan
        mask=valid_geometry_mask(ellipsoid,rtc,shadow,angle)
        self.assertEqual(int(mask.sum()),4)
        self.assertFalse(mask[0,1])
        self.assertFalse(mask[1,2])

    def test_geometry_mask_rejects_misaligned_arrays(self):
        with self.assertRaises(ValueError):
            valid_geometry_mask(np.ones((2,2)),np.ones((2,2)),np.ones((2,2)),np.ones((2,3)))

if __name__=="__main__": unittest.main()
