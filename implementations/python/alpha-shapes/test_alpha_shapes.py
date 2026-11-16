import math
import pytest
from alpha_shapes import alpha_shape

def area(ring):
    return 0.5 * sum(ring[i][0] * ring[(i+1)%len(ring)][1]
                     - ring[(i+1)%len(ring)][0] * ring[i][1]
                     for i in range(len(ring)))

def test_large_threshold_recovers_square_convex_hull():
    rings = alpha_shape([(0,0),(2,0),(2,2),(0,2),(1,1)], 10)
    assert len(rings) == 1
    assert rings[0] == [(0.0,0.0),(2.0,0.0),(2.0,2.0),(0.0,2.0)]
    assert area(rings[0]) == pytest.approx(4)

def test_threshold_respects_triangle_circumradius():
    points = [(0,0),(2,0),(2,2),(0,2)]
    assert alpha_shape(points, 1.4) == []
    assert len(alpha_shape(points, math.sqrt(2))) == 1

def test_concave_boundary_before_convex_hull():
    points = [(0,0),(4,0),(4,4),(3,4),(3,1),(1,1),(1,4),(0,4)]
    concave, convex = alpha_shape(points, 2), alpha_shape(points, 5)
    assert len(concave) == len(convex) == 1
    assert area(concave[0]) == pytest.approx(9)
    assert area(convex[0]) == pytest.approx(16)
    assert len(concave[0]) > 4

@pytest.mark.parametrize("points", [[],[(0,0)],[(0,0),(1,1)],[(0,0),(1,1),(2,2),(3,3)]])
def test_lower_dimensional_inputs(points):
    assert alpha_shape(points, 10) == []

def test_duplicate_points_are_removed():
    assert alpha_shape([(0,0),(2,0),(2,2),(0,2),(1,1),(1,1)],10) == alpha_shape(
        [(0,0),(2,0),(2,2),(0,2),(1,1)],10)

@pytest.mark.parametrize("alpha", [0,-1,float("nan"),float("inf"),True,"1"])
def test_invalid_alpha(alpha):
    with pytest.raises(ValueError, match="alpha"):
        alpha_shape([(0,0),(1,0),(0,1)], alpha)

@pytest.mark.parametrize("bad", [(float("nan"),0),(0,float("inf")),(0,)])
def test_invalid_coordinates(bad):
    with pytest.raises(ValueError):
        alpha_shape([(0,0),(1,0),(0,1),bad],10)

def test_translation_and_scaling_invariance():
    points = [(0,0),(4,0),(4,4),(3,4),(3,1),(1,1),(1,4),(0,4)]
    original = alpha_shape(points,2)
    transformed = alpha_shape([(3*x+7,3*y-5) for x,y in points],6)
    assert len(original) == len(transformed) == 1
    assert area(transformed[0]) == pytest.approx(9*area(original[0]))
    assert len(original[0]) == len(transformed[0])

def test_outer_boundary_is_counter_clockwise():
    ring = alpha_shape([(0,0),(2,0),(2,2),(0,2),(1,1)],10)[0]
    assert area(ring) > 0
