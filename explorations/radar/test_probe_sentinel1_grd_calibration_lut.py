import unittest
import numpy as np
from explorations.radar.probe_sentinel1_grd_calibration_lut import parse_calibration_lut, compare_calibration_to_annotation

class CalibrationLUTIncidenceTests(unittest.TestCase):
    def test_recovers_angle_from_beta_sigma_and_gamma_sigma_ratios(self):
        angles=np.array([25.0,35.0,45.0])
        k=np.array([100.0,120.0,140.0])
        sigma=np.sqrt(k/np.sin(np.deg2rad(angles)))
        beta=np.sqrt(k)
        gamma=np.sqrt(k/np.tan(np.deg2rad(angles)))
        xml=(f"<root><calibrationVector><line>0</line><pixel>10 20 30</pixel>"
             f"<sigmaNought>{' '.join(map(str,sigma))}</sigmaNought>"
             f"<betaNought>{' '.join(map(str,beta))}</betaNought>"
             f"<gamma>{' '.join(map(str,gamma))}</gamma></calibrationVector></root>").encode()
        result=parse_calibration_lut(xml)
        self.assertEqual(result["vector_count"],1)
        self.assertEqual(result["sample_count"],3)
        self.assertTrue(np.allclose(result["vectors"][0]["incidence_angle_degrees"],angles,atol=1e-8))
        self.assertLess(result["max_beta_sigma_vs_gamma_sigma_identity_difference_degrees"],1e-8)

    def test_calibration_angle_interpolation_matches_annotation_grid(self):
        lines=[0.0,10.0,20.0,30.0,40.0]
        pixels=[0.0,10.0,20.0,30.0,40.0]
        vectors=[]
        for line in lines:
            vectors.append({"line":line,"pixels":pixels,
                "incidence_angle_degrees":[30.0+0.01*line+0.02*pixel for pixel in pixels]})
        annotation={"points":[
            {"line":5.0,"pixel":5.0,"incidenceAngle":30.15},
            {"line":15.0,"pixel":25.0,"incidenceAngle":30.65},
            {"line":35.0,"pixel":15.0,"incidenceAngle":30.65}]}
        result=compare_calibration_to_annotation({"vectors":vectors},annotation)
        self.assertEqual(result["matched_tie_points"],3)
        self.assertEqual(result["annotation_tie_point_coverage_fraction"],1.0)
        self.assertLess(result["mae_degrees"],1e-8)

    def test_rejects_nonphysical_lut_ratios(self):
        xml=b"<root><calibrationVector><line>0</line><pixel>10</pixel><sigmaNought>1</sigmaNought><betaNought>2</betaNought><gamma>0.5</gamma></calibrationVector></root>"
        with self.assertRaises(ValueError): parse_calibration_lut(xml)

if __name__=="__main__": unittest.main()
