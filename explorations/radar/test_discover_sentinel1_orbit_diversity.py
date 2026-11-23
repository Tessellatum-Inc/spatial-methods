from __future__ import annotations
import importlib.util
import unittest
from pathlib import Path
P=Path(__file__).with_name("discover_sentinel1_orbit_diversity.py")
S=importlib.util.spec_from_file_location("orbit_screen",P); M=importlib.util.module_from_spec(S); S.loader.exec_module(M)
def feature(i,d,o,date,partial=False):
    x=37.05 if not partial else 36.85
    coords=[[36.65,-1.45],[x,-1.45],[x,-1.15],[36.65,-1.15],[36.65,-1.45]]
    return {"id":i,"geometry":{"type":"Polygon","coordinates":[coords]},"properties":{"datetime":date,"sat:orbit_state":d,"sat:relative_orbit":o,"platform":"sentinel-1c","sar:polarizations":["VV","VH"]}}
class TestOrbitDiversity(unittest.TestCase):
    def test_identifies_repeated_independent_track(self):
        rows=[feature("b1","descending",79,"2026-10-09T03:11:12Z"),feature("a1","ascending",57,"2026-10-13T15:47:34Z"),feature("a2","ascending",57,"2026-10-25T15:47:34Z")]
        r=M.summarize(rows)
        self.assertEqual(r["status"],"candidate_tracks_found")
        self.assertEqual([(x["orbit_direction"],x["relative_orbit"]) for x in r["independent_full_coverage_candidates"]],[("ASCENDING",57)])
    def test_partial_footprints_do_not_qualify(self):
        r=M.summarize([feature("p1","ascending",57,"2026-10-13T15:47:34Z",True),feature("p2","ascending",57,"2026-10-25T15:47:34Z",True)])
        self.assertEqual(r["independent_full_coverage_candidates"],[])
    def test_missing_orbit_metadata_is_not_inferred(self):
        f=feature("x","ascending",57,"2026-10-13T15:47:34Z"); del f["properties"]["sat:relative_orbit"]
        r=M.summarize([f])
        self.assertEqual(r["features_missing_orbit_metadata"],1)
        self.assertEqual(r["tracks"],[])
if __name__=="__main__": unittest.main()
