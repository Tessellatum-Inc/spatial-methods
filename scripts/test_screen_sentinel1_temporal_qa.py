"""Unit tests for local Sentinel-1 temporal QA screening."""
import importlib.util
from pathlib import Path
import unittest
import json
import tempfile
import numpy as np

SCRIPT=Path(__file__).resolve().parents[1]/'explorations/radar/screen_sentinel1_temporal_qa.py'
spec=importlib.util.spec_from_file_location('sentinel1_temporal_qa',SCRIPT)
module=importlib.util.module_from_spec(spec); spec.loader.exec_module(module)

class TemporalQATests(unittest.TestCase):
    def test_identical_tile_has_zero_shift(self):
        rng=np.random.default_rng(12)
        a=np.exp(rng.normal(-2,0.5,(128,128))).astype(np.float32)
        result=module._phase_shift(a,a,np.ones(a.shape,bool))
        self.assertIsNotNone(result)
        self.assertLess(result['shift_magnitude_pixels'],0.01)

    def test_known_translation_is_detected(self):
        rng=np.random.default_rng(21)
        a=np.exp(rng.normal(-2,0.5,(128,128))).astype(np.float32)
        b=np.roll(np.roll(a,2,axis=0),-3,axis=1)
        result=module._phase_shift(a,b,np.ones(a.shape,bool))
        self.assertAlmostEqual(abs(result['shift_x_pixels']),3,delta=0.1)
        self.assertAlmostEqual(abs(result['shift_y_pixels']),2,delta=0.1)

    def test_rejects_low_common_valid_fraction(self):
        rng=np.random.default_rng(2); a=np.exp(rng.normal(size=(128,128))).astype(np.float32)
        mask=np.zeros(a.shape,bool); mask[:20,:]=True
        self.assertIsNone(module._phase_shift(a,a,mask))

    def test_json_report_is_strict_json_with_real_newline(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "report.json"
            module.write_json_report(path, {"analysis_ready": False})
            raw = path.read_text(encoding="utf-8")
            self.assertTrue(raw.endswith("\n"))
            self.assertFalse(raw.endswith("\\\\n"))
            self.assertEqual(json.loads(raw), {"analysis_ready": False})

    def test_radiometric_statistics_are_in_linear_and_db_units(self):
        a=np.full((10,10),0.1,np.float32); mask=np.ones(a.shape,bool)
        stats=module._stats(a,mask)
        self.assertAlmostEqual(stats['median_linear'],0.1,places=6)
        self.assertAlmostEqual(stats['median_db'],-10.0,places=5)

if __name__=='__main__': unittest.main()
