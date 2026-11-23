import unittest
from explorations.radar.interpolate_surat_r009_incidence import BBOX, HEIGHT, WIDTH

class SuratIncidenceInterpolationConfigTests(unittest.TestCase):
    def test_grid_matches_paired_processing_grid(self):
        self.assertEqual((WIDTH,HEIGHT),(2500,2200))
        self.assertEqual(len(BBOX),4)
        self.assertLess(BBOX[0],BBOX[2])
        self.assertLess(BBOX[1],BBOX[3])

if __name__=="__main__": unittest.main()
