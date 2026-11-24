import unittest
import numpy as np
from explorations.radar.diagnose_opera_nairobi_r130_residuals import (
    db, summarize, stratify, quantile_strata, ANGLE_EDGES
)

class NairobiResidualDiagnosticsTests(unittest.TestCase):
    def test_db_power_conversion(self):
        np.testing.assert_allclose(db(np.array([1.0, 0.1])), [0.0, -10.0])

    def test_summary_outlier_fractions(self):
        result=summarize(np.array([0.1, -0.6, 1.2, -2.2]))
        self.assertEqual(result["count"], 4)
        self.assertAlmostEqual(result["mae_db"], 1.025)
        self.assertAlmostEqual(result["fraction_abs_gt_0_5_db"], 0.75)
        self.assertAlmostEqual(result["fraction_abs_gt_1_db"], 0.5)
        self.assertAlmostEqual(result["fraction_abs_gt_2_db"], 0.25)

    def test_angle_strata_partition_finite_values(self):
        values=np.array([0.1,0.2,0.3,0.4,0.5])
        angles=np.array([39.0,41.0,43.0,47.0,61.0])
        result=stratify(values,angles,ANGLE_EDGES,
            [f"{ANGLE_EDGES[i]}-{ANGLE_EDGES[i+1]}" for i in range(len(ANGLE_EDGES)-1)])
        total=sum(x["count"] for x in result["bins"])+result["underflow"]["count"]+result["overflow"]["count"]
        self.assertEqual(total,5)
        self.assertEqual(result["overflow"]["count"],1)

    def test_anF_quartiles_are_scene_local(self):
        values=np.arange(8,dtype=float)
        covariate=np.arange(8,dtype=float)+1
        result=quantile_strata(values,covariate)
        self.assertEqual(len(result["bins"]),4)
        self.assertEqual(result["quantile_edges"][0],1.0)
        self.assertEqual(result["quantile_edges"][-1],8.0)

if __name__=="__main__": unittest.main()
