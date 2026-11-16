import math
import pytest
from geometry_metrics import directed_hausdorff_distance, hausdorff_distance, discrete_frechet_distance, smallest_enclosing_circle, minimum_area_bounding_rectangle

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


def test_continuous_frechet_handles_different_sampling_of_same_curve():
    from geometry_metrics import continuous_frechet_distance, continuous_frechet_decision
    coarse=[(0,0),(2,0)]
    dense=[(0,0),(0.5,0),(1,0),(1.5,0),(2,0)]
    assert continuous_frechet_decision(coarse,dense,0.0)
    assert continuous_frechet_distance(coarse,dense,tolerance=1e-8)==pytest.approx(0.0,abs=1e-8)
    assert discrete_frechet_distance(coarse,dense)==pytest.approx(1.0)


def test_continuous_frechet_parallel_lines_and_threshold_decision():
    from geometry_metrics import continuous_frechet_distance, continuous_frechet_decision
    a=[(0,0),(1,0),(2,0)]
    b=[(0,1),(1,1),(2,1)]
    assert continuous_frechet_decision(a,b,1.0)
    assert not continuous_frechet_decision(a,b,0.99)
    assert continuous_frechet_distance(a,b,tolerance=1e-7)==pytest.approx(1.0,abs=1e-7)


def test_continuous_frechet_is_symmetric_and_respects_endpoints():
    from geometry_metrics import continuous_frechet_distance
    a=[(0,0),(1,1),(2,0)]
    b=[(0,0),(1,0),(2,0)]
    forward=continuous_frechet_distance(a,b,tolerance=1e-7)
    reverse=continuous_frechet_distance(b,a,tolerance=1e-7)
    assert forward==pytest.approx(reverse,abs=1e-7)
    assert continuous_frechet_distance([(0,0),(1,0)],[(3,0),(4,0)])==pytest.approx(3.0,abs=1e-6)


def test_continuous_frechet_singleton_and_validation():
    from geometry_metrics import continuous_frechet_distance, continuous_frechet_decision
    assert continuous_frechet_distance([(0,0)],[(1,0),(2,0)])==pytest.approx(2.0)
    assert continuous_frechet_decision([(0,0)],[(1,0),(2,0)],2.0)
    with pytest.raises(ValueError):
        continuous_frechet_decision([(0,0)],[(1,0)],-1)
    with pytest.raises(ValueError):
        continuous_frechet_distance([(0,0),(1,0)],[(0,0),(1,0)],tolerance=0)


def test_largest_empty_circle_square_sites():
    from geometry_metrics import largest_empty_circle
    x,y,radius,_=largest_empty_circle(
        [(0,0),(10,0),(10,10),(0,10)],precision=0.01
    )
    assert (x,y,radius)==pytest.approx((5,5,math.sqrt(50)),abs=0.02)


def test_largest_empty_circle_is_inside_hull_and_clearance_is_nearest_site():
    from geometry_metrics import largest_empty_circle, convex_hull
    sites=[(0,0),(12,0),(10,8),(2,10),(5,4)]
    x,y,radius,_=largest_empty_circle(sites,precision=0.02)
    hull=convex_hull(sites)
    crosses=[(b[0]-a[0])*(y-a[1])-(b[1]-a[1])*(x-a[0])
             for a,b in zip(hull,hull[1:]+hull[:1])]
    assert all(v>=-1e-8 for v in crosses) or all(v<=1e-8 for v in crosses)
    assert radius==pytest.approx(min(math.dist((x,y),p) for p in sites))


def test_largest_empty_circle_rejects_degenerate_sites_and_invalid_options():
    from geometry_metrics import largest_empty_circle
    with pytest.raises(ValueError):
        largest_empty_circle([(0,0),(1,0),(2,0)],precision=0.1)
    with pytest.raises(ValueError):
        largest_empty_circle([(0,0),(1,0),(0,1)],precision=0)
    with pytest.raises(ValueError):
        largest_empty_circle([(0,0),(1,0),(0,1)],max_cells=0)


def test_largest_empty_circle_respects_cell_budget():
    from geometry_metrics import largest_empty_circle
    sites=[(0,0),(12,0),(10,8),(2,10),(5,4)]
    with pytest.raises(RuntimeError,match="max_cells"):
        largest_empty_circle(sites,precision=0.001,max_cells=1)


def test_linear_calipers_rectangle_matches_quadratic_baseline_on_seeded_clouds():
    import random
    from geometry_metrics import minimum_area_bounding_rectangle_calipers
    rng=random.Random(2026)
    for _ in range(100):
        points=[(rng.uniform(-20,20),rng.uniform(-20,20)) for _ in range(rng.randint(3,35))]
        expected=minimum_area_bounding_rectangle(points)["area"]
        actual=minimum_area_bounding_rectangle_calipers(points)["area"]
        assert actual==pytest.approx(expected,rel=1e-10,abs=1e-9)


def test_linear_calipers_rectangle_degenerate_and_rotated_cases():
    from geometry_metrics import minimum_area_bounding_rectangle_calipers
    assert minimum_area_bounding_rectangle_calipers([]) is None
    assert minimum_area_bounding_rectangle_calipers([(2,3)])["area"]==0
    assert minimum_area_bounding_rectangle_calipers([(0,0),(3,0),(1,0)])["area"]==0
    angle=math.pi/5
    points=[(x*math.cos(angle)-y*math.sin(angle),x*math.sin(angle)+y*math.cos(angle))
            for x,y in [(0,0),(8,0),(8,2),(0,2)]]
    assert minimum_area_bounding_rectangle_calipers(points)["area"]==pytest.approx(16.0)



def _brute_minimum_circle(points):
    """Independent O(n^4) candidate-enumeration oracle for small fixtures."""
    candidates = []
    for point in points:
        candidates.append((point[0], point[1], 0.0))
    for i, a in enumerate(points):
        for b in points[i + 1:]:
            candidates.append(((a[0] + b[0]) / 2, (a[1] + b[1]) / 2,
                               math.dist(a, b) / 2))
    for i, a in enumerate(points):
        for j in range(i + 1, len(points)):
            b = points[j]
            for c in points[j + 1:]:
                ax, ay = a
                bx, by = b
                cx, cy = c
                determinant = 2 * (ax * (by-cy) + bx * (cy-ay) + cx * (ay-by))
                if abs(determinant) < 1e-12:
                    continue
                aa, bb, cc = ax*ax+ay*ay, bx*bx+by*by, cx*cx+cy*cy
                ux = (aa*(by-cy) + bb*(cy-ay) + cc*(ay-by)) / determinant
                uy = (aa*(cx-bx) + bb*(ax-cx) + cc*(bx-ax)) / determinant
                candidates.append((ux, uy, math.dist((ux, uy), a)))
    feasible = [
        circle for circle in candidates
        if all(math.dist((circle[0], circle[1]), point) <= circle[2] + 1e-8
               for point in points)
    ]
    return min(feasible, key=lambda circle: circle[2])


def test_smallest_circle_matches_independent_candidate_oracle_on_seeded_clouds():
    import random
    rng = random.Random(20261115)
    for _ in range(250):
        points = list(dict.fromkeys(
            (rng.uniform(-20, 20), rng.uniform(-20, 20))
            for _ in range(rng.randint(1, 10))
        ))
        expected = _brute_minimum_circle(points)
        actual = smallest_enclosing_circle(points, seed=rng.randrange(1_000_000))
        assert actual == pytest.approx(expected, rel=1e-9, abs=1e-8)


def test_smallest_circle_iterative_construction_handles_large_point_sets():
    import random
    rng = random.Random(90210)
    points = [(rng.uniform(-1, 1), rng.uniform(-1, 1)) for _ in range(5000)]
    circle = smallest_enclosing_circle(points, seed=77)
    assert circle is not None
    x, y, radius = circle
    assert all(math.dist((x, y), point) <= radius + 1e-8 for point in points)


@pytest.mark.parametrize("origin,scale", [
    ((1e9, -1e9), 1.0),
    ((0.0, 0.0), 1e-9),
    ((-3e6, 8e6), 1e-3),
])
def test_smallest_circle_is_translation_and_scale_stable(origin, scale):
    ox, oy = origin
    height = math.sqrt(3.0) * scale
    points = [(ox, oy), (ox + 2.0 * scale, oy), (ox + scale, oy + height)]
    x, y, radius = smallest_enclosing_circle(points, seed=19)
    assert x == pytest.approx(ox + scale, abs=max(scale * 1e-9, 8 * math.ulp(max(abs(ox), abs(oy), 1.0))))
    assert y == pytest.approx(oy + height / 3.0, abs=max(scale * 1e-9, 8 * math.ulp(max(abs(ox), abs(oy), 1.0))))
    assert radius == pytest.approx(2.0 * scale / math.sqrt(3.0), rel=1e-6, abs=1e-15)
    assert all(math.dist((x, y), point) <= radius + 8 * math.ulp(max(abs(x), abs(y), 1.0))
               for point in points)


def _brute_minimum_width(points):
    from geometry_metrics import convex_hull
    hull = convex_hull(points)
    if len(hull) < 3:
        return 0.0
    widths = []
    for a, b in zip(hull, hull[1:] + hull[:1]):
        dx, dy = b[0]-a[0], b[1]-a[1]
        length = math.hypot(dx, dy)
        widths.append(max(abs(dx*(p[1]-a[1])-dy*(p[0]-a[0]))
                          for p in hull) / length)
    return min(widths)


def test_rotating_calipers_minimum_width_known_shapes():
    from geometry_metrics import convex_polygon_minimum_width
    assert convex_polygon_minimum_width([(0,0),(4,0),(4,2),(0,2)]) == pytest.approx(2.0)
    assert convex_polygon_minimum_width([(0,0),(2,0),(2,2),(0,2)]) == pytest.approx(2.0)
    assert convex_polygon_minimum_width([(0,0),(3,0),(1,0)]) == 0.0
    assert convex_polygon_minimum_width([]) == 0.0


def test_rotating_calipers_minimum_width_matches_edge_scan_oracle():
    import random
    from geometry_metrics import convex_polygon_minimum_width
    rng = random.Random(20261119)
    for size in range(3, 151):
        for _ in range(5):
            points = [(rng.uniform(-100,100), rng.uniform(-100,100))
                      for _ in range(size)]
            actual = convex_polygon_minimum_width(points)
            expected = _brute_minimum_width(points)
            assert actual == pytest.approx(expected, rel=1e-10, abs=1e-9)


def test_rotating_calipers_minimum_width_is_translation_and_rotation_invariant():
    from geometry_metrics import convex_polygon_minimum_width
    points = [(0,0),(5,0),(6,2),(3,5),(-1,3)]
    base = convex_polygon_minimum_width(points)
    angle = 0.731
    rotated = [(x*math.cos(angle)-y*math.sin(angle)+17,
                x*math.sin(angle)+y*math.cos(angle)-9) for x,y in points]
    assert convex_polygon_minimum_width(rotated) == pytest.approx(base, rel=1e-10, abs=1e-9)


def test_rotating_calipers_minimum_width_handles_integer_ties_and_duplicates():
    import random
    from geometry_metrics import convex_polygon_minimum_width
    rng = random.Random(20261120)
    for _ in range(500):
        points = list(dict.fromkeys(
            (rng.randrange(-12, 13), rng.randrange(-12, 13))
            for _ in range(rng.randrange(3, 45))
        ))
        assert convex_polygon_minimum_width(points) == pytest.approx(
            _brute_minimum_width(points), rel=1e-11, abs=1e-10
        )


def test_rotating_calipers_minimum_width_thin_and_axis_aligned_shapes():
    from geometry_metrics import convex_polygon_minimum_width
    assert convex_polygon_minimum_width([(0,0),(1000,0),(1000,1e-5),(0,1e-5)]) == pytest.approx(1e-5)
    assert convex_polygon_minimum_width([(0,0),(8,0),(8,3),(0,3)]) == pytest.approx(3.0)
    assert convex_polygon_minimum_width([(0,0),(4,0),(2,0),(3,0)]) == 0.0


def test_continuous_frechet_rolling_rows_are_symmetric_for_unequal_curve_sizes():
    import random
    from geometry_metrics import continuous_frechet_decision, continuous_frechet_distance

    rng = random.Random(20261120)
    for size_a, size_b in ((2, 17), (4, 23), (19, 3), (31, 7)):
        a = [(rng.uniform(-5, 5), rng.uniform(-5, 5)) for _ in range(size_a)]
        b = [(rng.uniform(-5, 5), rng.uniform(-5, 5)) for _ in range(size_b)]
        distance = continuous_frechet_distance(a, b, tolerance=1e-7)
        assert continuous_frechet_decision(a, b, distance + 1e-6)
        assert continuous_frechet_decision(b, a, distance + 1e-6)
        if distance > 2e-6:
            assert not continuous_frechet_decision(a, b, distance - 2e-6)
            assert not continuous_frechet_decision(b, a, distance - 2e-6)


def test_discrete_frechet_is_symmetric_with_unequal_sequence_lengths():
    import random
    rng = random.Random(20261121)
    for size_a, size_b in ((2, 40), (5, 31), (29, 3), (45, 8)):
        a = [(rng.uniform(-5, 5), rng.uniform(-5, 5)) for _ in range(size_a)]
        b = [(rng.uniform(-5, 5), rng.uniform(-5, 5)) for _ in range(size_b)]
        assert discrete_frechet_distance(a, b) == pytest.approx(
            discrete_frechet_distance(b, a), abs=1e-12
        )



def test_rotating_calipers_diameter_is_scale_invariant_for_tiny_and_large_shapes():
    from geometry_metrics import convex_polygon_diameter

    for scale in (1e-12, 1e-9, 1e-3, 1.0, 1e6):
        points = [(0, 0), (2*scale, 0), (2*scale, scale), (0, scale)]
        assert convex_polygon_diameter(points)[2] == pytest.approx(
            math.sqrt(5) * scale, rel=1e-12, abs=scale * 1e-12
        )


def test_rotating_calipers_diameter_matches_pairwise_oracle_on_integer_degeneracies():
    import random
    from geometry_metrics import convex_polygon_diameter

    rng = random.Random(20261122)
    for _ in range(600):
        points = list(dict.fromkeys(
            (rng.randrange(-30, 31), rng.randrange(-30, 31))
            for _ in range(rng.randrange(0, 55))
        ))
        actual = convex_polygon_diameter(points)
        if not points:
            assert actual is None
            continue
        expected = max(
            (math.dist(a, b) for a in points for b in points),
            default=0.0,
        )
        assert actual[2] == pytest.approx(expected, rel=1e-12, abs=1e-12)


def test_rotating_calipers_diameter_is_translation_and_rotation_invariant():
    from geometry_metrics import convex_polygon_diameter

    points = [(-3, 0), (-1, -2), (2, -1), (4, 2), (0, 5), (-2, 3)]
    expected = convex_polygon_diameter(points)[2]
    angle = 0.817
    transformed = [
        (1e6 + x*math.cos(angle) - y*math.sin(angle),
         -2e6 + x*math.sin(angle) + y*math.cos(angle))
        for x, y in points
    ]
    assert convex_polygon_diameter(transformed)[2] == pytest.approx(
        expected, rel=1e-9, abs=1e-8
    )



def test_linear_rectangle_calipers_is_scale_invariant():
    from geometry_metrics import minimum_area_bounding_rectangle_calipers

    for scale in (1e-12, 1e-9, 1e-3, 1.0, 1e6):
        points = [(0, 0), (4*scale, 0), (4*scale, 2*scale), (0, 2*scale)]
        result = minimum_area_bounding_rectangle_calipers(points)
        assert result["area"] == pytest.approx(8 * scale * scale, rel=1e-11,
                                               abs=scale * scale * 1e-12)


def test_linear_rectangle_calipers_matches_quadratic_oracle_on_integer_clouds():
    import random
    from geometry_metrics import (
        minimum_area_bounding_rectangle,
        minimum_area_bounding_rectangle_calipers,
    )

    rng = random.Random(20261123)
    for _ in range(500):
        points = list(dict.fromkeys(
            (rng.randrange(-25, 26), rng.randrange(-25, 26))
            for _ in range(rng.randrange(3, 50))
        ))
        expected = minimum_area_bounding_rectangle(points)
        actual = minimum_area_bounding_rectangle_calipers(points)
        assert actual["area"] == pytest.approx(expected["area"], rel=1e-10,
                                                abs=1e-10)



@pytest.mark.parametrize("origin,scale", [
    ((1e9, -1e9), 1.0),
    ((1e12, -1e12), 10.0),
    ((-1e8, 2e8), 1e-2),
])
def test_linear_rectangle_calipers_is_stable_under_large_translation(origin, scale):
    from geometry_metrics import minimum_area_bounding_rectangle_calipers

    ox, oy = origin
    points = [(ox, oy), (ox+4*scale, oy),
              (ox+4*scale, oy+2*scale), (ox, oy+2*scale)]
    result = minimum_area_bounding_rectangle_calipers(points)
    assert result["area"] == pytest.approx(8*scale*scale, rel=1e-6,
                                           abs=scale*scale*1e-8)
    for px, py in points:
        assert min(math.dist((px, py), corner) for corner in result["corners"]) <= (
            math.hypot(4*scale, 2*scale) + 1e-5*max(scale, 1e-8)
        )



def test_translated_rectangle_corners_enclose_every_input_point():
    from geometry_metrics import minimum_area_bounding_rectangle_calipers

    ox, oy, scale = 1e12, -1e12, 10.0
    points = [(ox, oy), (ox+4*scale, oy),
              (ox+4*scale, oy+2*scale), (ox, oy+2*scale),
              (ox+scale, oy+0.5*scale)]
    result = minimum_area_bounding_rectangle_calipers(points)
    c0, c1, _, c3 = result["corners"]
    ux, uy = math.cos(result["angle_radians"]), math.sin(result["angle_radians"])
    vx, vy = -uy, ux
    width = (c1[0]-c0[0])*ux + (c1[1]-c0[1])*uy
    height = (c3[0]-c0[0])*vx + (c3[1]-c0[1])*vy
    tolerance = 1e-3
    for px, py in points:
        dx, dy = px-c0[0], py-c0[1]
        along_u = dx*ux + dy*uy
        along_v = dx*vx + dy*vy
        assert -tolerance <= along_u <= width+tolerance
        assert -tolerance <= along_v <= height+tolerance


def test_caliper_rectangle_matches_orientation_scan_oracle_on_seeded_clouds():
    import random
    from geometry_metrics import minimum_area_bounding_rectangle, minimum_area_bounding_rectangle_calipers
    rng = random.Random(20261116)
    for _ in range(100):
        points = [(rng.uniform(-100, 100), rng.uniform(-100, 100)) for _ in range(35)]
        expected = minimum_area_bounding_rectangle(points)
        actual = minimum_area_bounding_rectangle_calipers(points)
        assert actual["area"] == pytest.approx(expected["area"], rel=1e-10, abs=1e-9)
        assert actual["width"] >= 0 and actual["height"] >= 0


def test_caliper_rectangle_rotated_rectangle_and_degenerate_inputs():
    from geometry_metrics import minimum_area_bounding_rectangle_calipers
    theta = 0.37
    c, s = math.cos(theta), math.sin(theta)
    points = [(x*c-y*s, x*s+y*c) for x,y in [(0,0),(8,0),(8,3),(0,3),(2,1)]]
    result = minimum_area_bounding_rectangle_calipers(points)
    assert result["area"] == pytest.approx(24.0, abs=1e-9)
    assert sorted((result["width"], result["height"])) == pytest.approx([3.0, 8.0])
    assert minimum_area_bounding_rectangle_calipers([]) is None
    assert minimum_area_bounding_rectangle_calipers([(2,3)])["area"] == 0.0
    assert minimum_area_bounding_rectangle_calipers([(0,0),(3,4)])["area"] == 0.0


def test_minimum_width_matches_brute_force_edge_orientation_oracle():
    import random
    from geometry_metrics import convex_hull, convex_polygon_minimum_width
    rng = random.Random(917)
    for _ in range(60):
        points = [(rng.uniform(-20,20), rng.uniform(-20,20)) for _ in range(25)]
        hull = convex_hull(points)
        expected = float("inf")
        for a,b in zip(hull, hull[1:]+hull[:1]):
            dx,dy=b[0]-a[0],b[1]-a[1]
            length=math.hypot(dx,dy)
            if length == 0: continue
            nx,ny=-dy/length,dx/length
            projections=[x*nx+y*ny for x,y in hull]
            expected=min(expected,max(projections)-min(projections))
        assert convex_polygon_minimum_width(points) == pytest.approx(expected, rel=1e-10, abs=1e-9)
