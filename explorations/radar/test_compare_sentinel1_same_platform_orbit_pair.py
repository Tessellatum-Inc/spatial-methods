from __future__ import annotations
import importlib.util, unittest
from pathlib import Path
import numpy as np
P=Path(__file__).with_name("compare_sentinel1_same_platform_orbit_pair.py")
S=importlib.util.spec_from_file_location("same_platform_compare",P); M=importlib.util.module_from_spec(S); S.loader.exec_module(M)
class TestSharedMaskMetrics(unittest.TestCase):
    def test_relation_metrics_recovers_synthetic_area_relation(self):
        area=np.array([0.8,0.9,1.0,1.1,1.2]*100,dtype=float)
        ell=np.full(area.shape,0.01); delta=-10*np.log10(area)+0.2; rtc=ell*10**(delta/10)
        result=M.summarize_relation(ell,rtc,area,np.ones(area.shape,dtype=bool))
        self.assertAlmostEqual(result["ols_slope"],1.0,places=8)
        self.assertAlmostEqual(result["median_observed_minus_area_factor_db"],0.2,places=8)
        self.assertAlmostEqual(result["ols_intercept_db"],0.2,places=8)
if __name__=="__main__": unittest.main()
