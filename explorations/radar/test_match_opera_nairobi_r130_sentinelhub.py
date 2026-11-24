import unittest
from explorations.radar.match_opera_nairobi_r130_sentinelhub import candidate_matches

class CandidateMatchTests(unittest.TestCase):
    def test_requires_orbit_direction_platform_and_close_time(self):
        opera={"acquisition_groups":[{"acquisition_date_utc":"2026-11-23","burst_ids":["T130_279214_IW3"],
            "burst_start_times_utc":["2026-11-23T15:55:41Z","2026-11-23T15:55:46Z"],
            "products":[{"platform":"Sentinel-1D"}]}]}
        features=[
          {"id":"good","properties":{"datetime":"2026-11-23T15:55:43Z","platform":"sentinel-1d","sat:relative_orbit":130,"sat:orbit_state":"ascending","sar:polarizations":["VV","VH"]}},
          {"id":"wrong-orbit","properties":{"datetime":"2026-11-23T15:55:43Z","platform":"sentinel-1d","sat:relative_orbit":9,"sat:orbit_state":"ascending","sar:polarizations":["VV","VH"]}},
          {"id":"wrong-platform","properties":{"datetime":"2026-11-23T15:55:43Z","platform":"sentinel-1a","sat:relative_orbit":130,"sat:orbit_state":"ascending","sar:polarizations":["VV","VH"]}},
          {"id":"wrong-time","properties":{"datetime":"2026-11-23T16:10:00Z","platform":"sentinel-1d","sat:relative_orbit":130,"sat:orbit_state":"ascending","sar:polarizations":["VV","VH"]}},
        ]
        report=candidate_matches(opera,features)
        group=report["acquisition_date_matches"][0]
        self.assertEqual(group["qualified_candidate_count"],1)
        self.assertEqual(group["qualified_candidates"][0]["catalog_item_id"],"good")

if __name__=="__main__": unittest.main()
