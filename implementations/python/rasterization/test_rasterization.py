import unittest
from rasterization import bresenham_line, dda_line, scanline_polygon_fill, supercover_line, wu_line

class RasterizationTests(unittest.TestCase):
 def test_bresenham_octants(self):
  for end in [(5,2),(2,5),(-2,5),(-5,2),(-5,-2),(-2,-5),(2,-5),(5,-2)]:
   a=bresenham_line((0,0),end); self.assertEqual((a[0],a[-1]),((0,0),end)); self.assertEqual(set(a),set(bresenham_line(end,(0,0))))
 def test_bresenham_integer_contract(self):
  with self.assertRaises(ValueError): bresenham_line((0.5,0),(3,2))
 def test_dda_degenerate(self):
  self.assertEqual(dda_line((1,1),(1,1)),[(1,1)])
 def test_supercover_corner(self):
  self.assertEqual(set(supercover_line((0,0),(2,2))),{(0,0),(1,0),(0,1),(1,1),(2,1),(1,2),(2,2)})
 def test_wu_bounds(self):
  values=wu_line((0,0),(5,2)); self.assertTrue(values); self.assertTrue(all(0 < v <= 1 for v in values.values()))
 def test_scanline_square(self):
  self.assertEqual(len(scanline_polygon_fill([(0,0),(3,0),(3,3),(0,3)])),9)
 def test_scanline_triangle(self):
  self.assertEqual(len(scanline_polygon_fill([(0,0),(4,0),(0,4)])),6)
 def test_invalid_ring(self):
  with self.assertRaises(ValueError): scanline_polygon_fill([(0,0),(1,1)])

if __name__ == '__main__': unittest.main()


class TriangleCoverageTests(unittest.TestCase):
 def test_right_triangle_exact_cell_fractions(self):
  got=triangle_coverage([(0,0),(2,0),(0,2)],2,2)
  self.assertEqual(got,{(0,0):1.0,(1,0):0.5,(0,1):0.5})
  self.assertAlmostEqual(sum(got.values()),2.0)

 def test_coverage_is_orientation_invariant_and_conserves_area(self):
  tri=[(.2,.1),(2.4,.3),(.7,2.2)]
  a=triangle_coverage(tri,4,4)
  b=triangle_coverage(list(reversed(tri)),4,4)
  self.assertEqual(set(a),set(b))
  for key in a:self.assertAlmostEqual(a[key],b[key],places=12)
  self.assertAlmostEqual(sum(a.values()),_polygon_area([tuple(p) for p in tri]),places=10)

 def test_non_square_cells_and_partial_raster_overlap(self):
  got=triangle_coverage([(-1,0),(2,0),(0,2)],2,2,origin=(0,0),cell_size=(.5,1.0))
  self.assertTrue(got)
  self.assertTrue(all(0 < value <= 1 for value in got.values()))
  self.assertLess(sum(got.values()),3.0)

 def test_degenerate_triangle_and_invalid_grid_are_rejected(self):
  with self.assertRaises(ValueError):triangle_coverage([(0,0),(1,1),(2,2)],3,3)
  with self.assertRaises(ValueError):triangle_coverage([(0,0),(1,0),(0,1)],0,3)
  with self.assertRaises(ValueError):triangle_coverage([(0,0),(1,0),(0,1)],3,3,cell_size=(0,1))
