from __future__ import annotations
import importlib.util, unittest
from pathlib import Path
P=Path(__file__).with_name("discover_sentinel1_intermediate_same_platform_orbits.py")
S=importlib.util.spec_from_file_location("intermediate_orbit_discovery",P); M=importlib.util.module_from_spec(S); S.loader.exec_module(M)
def feature(orbit,stamp,fraction=0.8,platform="sentinel-1a",direction="ASCENDING"):
    return {"id":f"scene-{orbit}-{stamp}","properties":{"platform":platform,"sat:orbit_state":direction,
        "sat:relative_orbit":orbit,"datetime":stamp,"sar:polarizations":["VV","VH"]}}
class TestIntermediateOrbitDiscovery(unittest.TestCase):
    def test_groups_repeated_same_platform_ascending_tracks_and_excludes_existing_tracks(self):
        rows=[feature(57,"2025-01-01T00:00:00Z"),feature(130,"2025-01-02T00:00:00Z")]
        rows += [feature(88,f"2025-01-{day:02d}T00:00:00Z") for day in (1,13,25)]
        rows += [feature(88,"2025-02-06T00:00:00Z")]
        rows += [feature(99,"2025-01-01T00:00:00Z",platform="sentinel-1b") for _ in range(4)]
        result=M.summarize(rows,min_scenes=4,min_fraction=0.7)
        self.assertEqual(len(result["candidates"]),1)
        self.assertEqual(result["candidates"][0]["relative_orbit"],88)
        self.assertEqual(result["candidates"][0]["scene_count"],4)
    def test_excludes_low_overlap_items(self):
        result=M.summarize([feature(88,"2025-01-01T00:00:00Z",0.5)],min_scenes=2,min_fraction=0.7)
        self.assertEqual(result["tracks"],[])
if __name__=="__main__": unittest.main()
