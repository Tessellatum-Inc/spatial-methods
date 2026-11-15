import math
import pytest
from geometry_metrics import directed_hausdorff_distance, hausdorff_distance, discrete_frechet_distance, smallest_enclosing_circle

def test_hausdorff_is_symmetric_and_known_value():
    a=[(0,0),(2,0)]; b=[(0,0),(1,0),(2,0)]
    assert hausdorff_distance(a,b)==1.0
    assert hausdorff_distance(a,b)==hausdorff_distance(b,a)
    assert directed_hausdorff_distance(b,a)==1.0
    assert directed_hausdorff_distance(a,b)==0.0

def test_hausdorff_identical_and_singleton_sets():
    assert hausdorff_distance([(1,2)],[(1,2)])==0.0
    assert hausdorff_distance([(0,0)],[(3,4)])==5.0

def test_discrete_frechet_known_and_order_sensitive():
    a=[(0,0),(1,0),(2,0)]; b=[(0,0),(2,0)]
    assert discrete_frechet_distance(a,b)==1.0
    assert discrete_frechet_distance(a,a)==0.0
    assert discrete_frechet_distance([(0,0),(1,0)],[(1,0),(0,0)])==1.0

def test_discrete_frechet_singleton():
    assert discrete_frechet_distance([(0,0)],[(3,4)])==5.0

def test_smallest_circle_two_and_three_points():
    assert smallest_enclosing_circle([(0,0),(2,0)])==(1.0,0.0,1.0)
    assert smallest_enclosing_circle([(0,0),(2,0),(1,1)])==pytest.approx((1.0,0.0,1.0))

def test_smallest_circle_collinear_and_empty():
    assert smallest_enclosing_circle([]) is None
    assert smallest_enclosing_circle([(0,0),(1,0),(3,0)])==pytest.approx((1.5,0.0,1.5))

def test_smallest_circle_contains_every_point_and_is_reproducible():
    pts=[(0,0),(4,0),(1,2),(2,1),(3,3)]
    c=smallest_enclosing_circle(pts,seed=17)
    assert c==smallest_enclosing_circle(pts,seed=17)
    x,y,r=c
    assert all(math.hypot(px-x,py-y)<=r+1e-9 for px,py in pts)

@pytest.mark.parametrize("fn,args",[
    (hausdorff_distance,([],[(0,0)])),
    (directed_hausdorff_distance,([(0,0)],[])),
    (discrete_frechet_distance,([],[(0,0)])),
])
def test_empty_inputs_rejected(fn,args):
    with pytest.raises(ValueError): fn(*args)

def test_nonfinite_coordinates_rejected():
    with pytest.raises(ValueError):
        hausdorff_distance([(0,float("nan"))],[(0,0)])


def test_rotating_calipers_diameter_square_and_rectangle():
    from geometry_metrics import convex_polygon_diameter
    a, b, d = convex_polygon_diameter([(0,0),(2,0),(2,2),(0,2)])
    assert d == pytest.approx(2 * math.sqrt(2))
    assert {a, b} in ({(0.0,0.0),(2.0,2.0)}, {(2.0,0.0),(0.0,2.0)})
    assert convex_polygon_diameter([(0,0),(4,0),(4,1),(0,1)])[2] == pytest.approx(math.sqrt(17))


def test_rotating_calipers_degenerate_and_duplicate_points():
    from geometry_metrics import convex_polygon_diameter
    assert convex_polygon_diameter([]) is None
    assert convex_polygon_diameter([(2,3),(2,3)]) == ((2.0,3.0),(2.0,3.0),0.0)
    assert convex_polygon_diameter([(0,0),(1,0),(3,0),(1,0)])[2] == 3.0


def test_rotating_calipers_matches_brute_force_on_seeded_clouds():
    from geometry_metrics import convex_polygon_diameter
    import random
    rng = random.Random(42)
    for _ in range(30):
        pts = [(rng.uniform(-10,10), rng.uniform(-10,10)) for _ in range(20)]
        expected = max(math.dist(a,b) for i,a in enumerate(pts) for b in pts[i+1:])
        assert convex_polygon_diameter(pts)[2] == pytest.approx(expected)


def test_polylabel_square_center_and_radius():
    from geometry_metrics import polylabel
    x,y,r,_=polylabel([(0,0),(10,0),(10,10),(0,10)],precision=0.01)
    assert (x,y,r)==pytest.approx((5,5,5),abs=0.01)


def test_polylabel_rectangle_center():
    from geometry_metrics import polylabel
    x,y,r,_=polylabel([(0,0),(12,0),(12,4),(0,4)],precision=0.01)
    assert (x,y,r)==pytest.approx((6,2,2),abs=0.01)


def test_polylabel_respects_hole():
    from geometry_metrics import polylabel
    outer=[(0,0),(10,0),(10,10),(0,10)]
    hole=[(4,4),(6,4),(6,6),(4,6)]
    x,y,r,_=polylabel(outer,holes=[hole],precision=0.02)
    assert not (4<x<6 and 4<y<6)
    assert r>2.0


def test_polylabel_rejects_invalid_parameters_and_degenerate_polygon():
    from geometry_metrics import polylabel
    with pytest.raises(ValueError): polylabel([(0,0),(1,0),(2,0)],precision=0.1)
    with pytest.raises(ValueError): polylabel([(0,0),(1,0),(1,1)],precision=0)
    with pytest.raises(ValueError): polylabel([(0,0),(1,0),(1,1)],max_cells=0)


def test_minimum_area_rectangle_axis_aligned_and_rotated():
    from geometry_metrics import minimum_area_bounding_rectangle
    result = minimum_area_bounding_rectangle([(0,0),(4,0),(4,2),(0,2),(2,1)])
    assert result["area"] == pytest.approx(8.0)
    theta = math.pi/4
    points = [(x*math.cos(theta)-y*math.sin(theta), x*math.sin(theta)+y*math.cos(theta))
              for x,y in [(0,0),(4,0),(4,2),(0,2)]]
    assert minimum_area_bounding_rectangle(points)["area"] == pytest.approx(8.0)


def test_minimum_area_rectangle_degenerate_and_empty():
    from geometry_metrics import minimum_area_bounding_rectangle
    assert minimum_area_bounding_rectangle([]) is None
    assert minimum_area_bounding_rectangle([(2,3)])["area"] == 0.0
    assert minimum_area_bounding_rectangle([(0,0),(3,0),(1,0)])["area"] == 0.0


def test_minimum_area_rectangle_contains_all_points():
    from geometry_metrics import minimum_area_bounding_rectangle
    pts=[(0,0),(5,1),(4,4),(1,3),(2,2)]
    c=minimum_area_bounding_rectangle(pts)["corners"]
    for point in pts:
        crosses=[(b[0]-a[0])*(point[1]-a[1])-(b[1]-a[1])*(point[0]-a[0])
                 for a,b in zip(c,c[1:]+c[:1])]
        assert all(v>=-1e-8 for v in crosses) or all(v<=1e-8 for v in crosses)


def test_polylabel_guards_initial_grid_size():
    from geometry_metrics import polylabel
    with pytest.raises(RuntimeError):
        polylabel([(0,0),(100,0),(100,1),(0,1)], precision=0.1, max_cells=10)
