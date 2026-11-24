import unittest
from explorations.radar.process_nairobi_r130_sentinel1_validation import PRODUCTS, BBOX, WIDTH, HEIGHT

class NairobiR130ProcessTests(unittest.TestCase):
    def test_five_verified_datatakes_are_declared(self):
        self.assertEqual(len(PRODUCTS),5)
        self.assertEqual([x["absolute_orbit"] for x in PRODUCTS],[4896,5071,5246,5421,5596])
        self.assertEqual([x["datatake_id"] for x in PRODUCTS],["009371","009986","009F7F","00A58B","00AB9A"])
    def test_process_grid_within_provider_limits(self):
        self.assertEqual(BBOX,[36.65,-1.45,37.05,-1.15])
        self.assertLessEqual(WIDTH,2500);self.assertLessEqual(HEIGHT,2500)

if __name__=="__main__": unittest.main()
