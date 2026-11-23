from __future__ import annotations
import importlib.util
import unittest
from pathlib import Path
P=Path(__file__).with_name("process_sentinel1_alternate_orbit.py")
S=importlib.util.spec_from_file_location("alt_orbit",P); M=importlib.util.module_from_spec(S); S.loader.exec_module(M)
def feature(i,orbit,fraction):
    width=0.4*fraction
    coords=[[36.65,-1.45],[36.65+width,-1.45],[36.65+width,-1.15],[36.65,-1.15],[36.65,-1.45]]
    return {"id":i,"geometry":{"type":"Polygon","coordinates":[coords]},"properties":{"datetime":f"2026-10-{i}T15:55:31Z","sat:orbit_state":"ascending","sat:relative_orbit":orbit,"sar:polarizations":["VV","VH"]}}
class TestAlternateOrbitSelection(unittest.TestCase):
    def test_selects_only_repeated_track_items_above_coverage_threshold(self):
        rows=[feature("06",130,0.84),feature("18",130,0.84),feature("30",130,0.84),feature("11",57,0.75)]
        selected=M.select_candidates(rows,"ascending",130,0.8)
        self.assertEqual(len(selected),3)
        self.assertTrue(all(x[2]>=0.8 for x in selected))
    def test_does_not_claim_partial_scene_is_full_coverage(self):
        rows=M.select_candidates([feature("06",130,0.84)],"ascending",130,0.8)
        self.assertFalse(rows[0][1])
if __name__=="__main__": unittest.main()
