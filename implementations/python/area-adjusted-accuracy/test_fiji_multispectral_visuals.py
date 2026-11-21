import json
import tempfile
import unittest
from pathlib import Path
import numpy as np
from fiji_multispectral_visuals import build_visual_evidence, write_visual_manifest

class FijiMultispectralVisualTests(unittest.TestCase):
    def _bands(self):
        return {
            "B02":np.full((8,8),0.1,dtype=np.float32),
            "B03":np.full((8,8),0.2,dtype=np.float32),
            "B04":np.full((8,8),0.3,dtype=np.float32),
            "B08":np.full((8,8),0.7,dtype=np.float32),
            "B05":np.full((4,4),0.2,dtype=np.float32),
            "B8A":np.full((4,4),0.6,dtype=np.float32),
            "B11":np.full((4,4),0.25,dtype=np.float32),
            "B12":np.full((4,4),0.35,dtype=np.float32),
            "SCL":np.array([[4,4,8,8],[4,5,9,10],[4,4,4,4],[4,4,4,4]],dtype=np.float32),
        }
    def test_expected_panels_preserve_native_grid_and_hashes(self):
        with tempfile.TemporaryDirectory() as d:
            rows=build_visual_evidence("P1","scene/1","2021-01-01",self._bands(),{},Path(d))
            by={r["panel"]:r for r in rows}
            self.assertEqual(by["true_colour_10m"]["native_grid"],"10m")
            self.assertEqual(by["false_colour_10m"]["native_grid"],"10m")
            self.assertEqual(by["ndvi_10m"]["native_grid"],"10m")
            self.assertEqual(by["ndre_20m_scl_screened"]["native_grid"],"20m")
            self.assertEqual(by["swir_rededge_20m"]["native_grid"],"20m")
            self.assertIn("invalid classes masked",by["ndre_20m_scl_screened"]["mask"])
            self.assertTrue(all((Path(d)/r["filename"]).exists() for r in rows))
            self.assertTrue(all(len(r["sha256"])==64 for r in rows))
    def test_no_cross_resolution_composite(self):
        bands=self._bands(); bands["B11"]=np.full((8,8),0.2,dtype=np.float32)
        with tempfile.TemporaryDirectory() as d:
            rows=build_visual_evidence("P1","scene","2021",bands,{},Path(d))
            self.assertNotIn("swir_rededge_20m",{r["panel"] for r in rows})
    def test_manifest_roundtrip(self):
        with tempfile.TemporaryDirectory() as d:
            rows=build_visual_evidence("P1","scene","2021",self._bands(),{},Path(d)/"visuals")
            p=Path(d)/"manifest.json"; write_visual_manifest(rows,p)
            self.assertEqual(len(json.loads(p.read_text())),len(rows))

if __name__=="__main__": unittest.main()
