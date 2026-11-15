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
