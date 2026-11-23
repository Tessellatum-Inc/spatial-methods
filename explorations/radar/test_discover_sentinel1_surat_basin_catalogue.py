import unittest
from explorations.radar.discover_sentinel1_surat_basin_catalogue import summarize

TARGETS=[{"name":f"CR {i}","longitude":150.0+i*0.01,"latitude":-26.5} for i in range(10)]
def feature(name,orbit,day,geometry,pols=None,direction="ASCENDING"):
    return {"id":name,"geometry":geometry,"properties":{"platform":"sentinel-1a","sat:orbit_state":direction,
        "sat:relative_orbit":orbit,"datetime":f"2025-01-{day:02d}T00:00:00Z","sar:polarizations":pols or ["VV","VH"]}}
def polygon(west,east):
    return {"type":"Polygon","coordinates":[[[west,-27],[east,-27],[east,-26],[west,-26],[west,-27]]]}

class SuratCatalogueTests(unittest.TestCase):
    def test_identifies_repeated_ascending_track_covering_all_targets(self):
        features=[feature(f"full-{i}",57,i,polygon(149,152)) for i in (1,7,13,19)]
        result=summarize(features,TARGETS)
        self.assertEqual(result["candidate_track_count"],1)
        candidate=result["candidates"][0]
        self.assertTrue(candidate["candidate_for_processing"])
        self.assertEqual(candidate["scenes_with_full_array_coverage"],4)
        self.assertEqual(candidate["qualifying_scene_count"],4)

    def test_partial_scene_does_not_qualify(self):
        features=[feature(f"partial-{i}",57,i,polygon(150.0,150.04)) for i in (1,7,13,19)]
        result=summarize(features,TARGETS)
        self.assertEqual(result["candidate_track_count"],0)

    def test_descending_track_not_selected_for_ascending_oriented_array(self):
        features=[feature(f"desc-{i}",57,i,polygon(149,152),direction="DESCENDING") for i in (1,7,13,19)]
        result=summarize(features,TARGETS)
        self.assertEqual(result["candidate_track_count"],0)

if __name__=="__main__": unittest.main()
