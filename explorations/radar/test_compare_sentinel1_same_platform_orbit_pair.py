from __future__ import annotations
import importlib.util, unittest
from pathlib import Path
import numpy as np
P=Path(__file__).with_name("compare_sentinel1_same_platform_orbit_pair.py")
S=importlib.util.spec_from_file_location("same_platform_compare",P); M=importlib.util.module_from_spec(S); S.loader.exec_module(M)
class TestSharedMaskMetrics(unittest.TestCase):
    def test_direct_rtc_ellipsoid_difference_is_reported_separately(self):
        area=np.ones(200,dtype=float); ell=np.full(area.shape,0.01)
        rtc=ell*10**(0.03/10); angle=np.linspace(30.0,60.0,len(area))
        result=M.summarize_relation(ell,rtc,area,angle,np.ones(area.shape,dtype=bool))
        self.assertAlmostEqual(result["median_direct_rtc_minus_ellipsoid_db"],0.03,places=8)
        self.assertAlmostEqual(result["mean_absolute_direct_rtc_minus_ellipsoid_db"],0.03,places=8)
    def test_local_angle_geometry_term_removes_synthetic_residual(self):
        area=np.array([0.8,0.9,1.0,1.1,1.2]*100,dtype=float)
        angle=np.linspace(30.0,60.0,len(area)); ell=np.full(area.shape,0.01)
        delta=-10*np.log10(area)-10*np.log10(np.tan(np.deg2rad(angle)))+0.1
        rtc=ell*10**(delta/10)
        result=M.summarize_relation(ell,rtc,area,angle,np.ones(area.shape,dtype=bool))
        self.assertAlmostEqual(result["median_local_angle_proxy_adjusted_residual_db"],0.1,places=8)
        self.assertAlmostEqual(result["mean_absolute_local_angle_proxy_adjusted_residual_db"],0.1,places=8)
    def test_ellipsoid_and_local_angles_jointly_remove_synthetic_geometry_term(self):
        area=np.array([0.8,0.9,1.0,1.1,1.2]*100,dtype=float)
        local=np.linspace(30.0,60.0,len(area)); ellipsoid_angle=np.full(area.shape,39.2)
        geometry=-10*np.log10(np.tan(np.deg2rad(local)))+10*np.log10(np.tan(np.deg2rad(ellipsoid_angle)))
        delta=-10*np.log10(area)+geometry+0.15
        ell=np.full(area.shape,0.01); rtc=ell*10**(delta/10)
        result=M.summarize_relation(ell,rtc,area,local,np.ones(area.shape,dtype=bool),ellipsoid_angle)
        self.assertAlmostEqual(result["median_area_and_geometry_adjusted_residual_db"],0.15,places=8)
        self.assertAlmostEqual(result["mean_absolute_area_and_geometry_adjusted_residual_db"],0.15,places=8)
        self.assertAlmostEqual(result["median_ellipsoid_incidence_angle_degrees"],39.2,places=8)
    def test_ellipsoid_reference_area_term_removes_synthetic_residual(self):
        area=np.array([0.8,0.9,1.0,1.1,1.2]*100,dtype=float)
        ellipsoid_angle=np.linspace(30.0,50.0,len(area)); local=np.linspace(35.0,55.0,len(area))
        reference_term=-10*np.log10(np.tan(np.deg2rad(ellipsoid_angle)))
        delta=-10*np.log10(area)+reference_term+0.12
        ell=np.full(area.shape,0.01); rtc=ell*10**(delta/10)
        result=M.summarize_relation(ell,rtc,area,local,np.ones(area.shape,dtype=bool),ellipsoid_angle)
        self.assertAlmostEqual(result["median_area_and_ellipsoid_angle_adjusted_residual_db"],0.12,places=8)
        self.assertAlmostEqual(result["mean_absolute_area_and_ellipsoid_angle_adjusted_residual_db"],0.12,places=8)
    def test_relation_metrics_recovers_synthetic_area_relation(self):
        area=np.array([0.8,0.9,1.0,1.1,1.2]*100,dtype=float)
        ell=np.full(area.shape,0.01); delta=-10*np.log10(area)+0.2; rtc=ell*10**(delta/10)
        angle=np.linspace(30.0,60.0,len(area))
        result=M.summarize_relation(ell,rtc,area,angle,np.ones(area.shape,dtype=bool))
        self.assertAlmostEqual(result["ols_slope"],1.0,places=8)
        self.assertAlmostEqual(result["median_observed_minus_area_factor_db"],0.2,places=8)
        self.assertAlmostEqual(result["ols_intercept_db"],0.2,places=8)
if __name__=="__main__": unittest.main()
