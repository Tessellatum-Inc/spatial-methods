import math
import pytest
from spatial_centers import mean_center, median_center, standard_distance, standard_deviational_ellipse

def test_mean_center_and_weighted_mean_center():
    pts=[(0,0),(2,0),(0,2)]
    assert mean_center(pts)==pytest.approx((2/3,2/3))
    assert mean_center(pts,[1,2,1])==pytest.approx((1.0,0.5))

def test_geometric_median_minimizes_distance_and_resists_outlier():
    pts=[(0,0),(1,0),(0,1),(100,100)]
    m=median_center(pts)
    mean=mean_center(pts)
    objective=lambda q: sum(math.dist(q,p) for p in pts)
    assert objective(m) <= objective((0.25,0.25)) + 1e-8
    assert math.dist(m,(0,0)) < math.dist(mean,(0,0))

def test_weighted_geometric_median_and_modified_coincident_update():
    pts=[(0,0),(10,0),(-1,0)]
    assert median_center(pts,[1,1,10]) == pytest.approx((-1,0),abs=2e-8)

def test_dominant_weight_point_is_geometric_median():
    assert median_center([(0,0),(10,0),(0,10)],[5,1,1]) == pytest.approx((0,0),abs=1e-8)

def test_standard_distance_for_square():
    assert standard_distance([(-1,-1),(-1,1),(1,-1),(1,1)]) == pytest.approx(math.sqrt(2))

def test_ellipse_axes_and_orientation_for_rotated_line():
    r=standard_deviational_ellipse([(-1,-1),(1,1)])
    assert r["center"] == pytest.approx((0,0))
    assert r["major_axis_sd"] == pytest.approx(math.sqrt(2))
    assert r["minor_axis_sd"] == pytest.approx(0)
    assert r["orientation_degrees_ccw_from_x"] == pytest.approx(45)

def test_ellipse_isotropic_case_has_zero_orientation():
    r=standard_deviational_ellipse([(-1,0),(1,0),(0,-1),(0,1)])
    assert r["major_axis_sd"] == pytest.approx(1/math.sqrt(2))
    assert r["minor_axis_sd"] == pytest.approx(1/math.sqrt(2))
    assert r["orientation_degrees_ccw_from_x"] == 0

def test_ellipse_scale_multiplies_principal_axes():
    pts=[(-1,0),(1,0),(0,-1),(0,1)]
    a=standard_deviational_ellipse(pts)
    b=standard_deviational_ellipse(pts,scale=math.sqrt(2))
    assert b["major_axis_sd"] == pytest.approx(math.sqrt(2)*a["major_axis_sd"])

def test_weighted_standard_distance_and_ellipse():
    pts=[(0,0),(10,0),(0,10)]
    sd=standard_distance(pts,[10,1,1])
    r=standard_deviational_ellipse(pts,[10,1,1])
    assert r["center"] == pytest.approx(mean_center(pts,[10,1,1]))
    assert sd > 0

@pytest.mark.parametrize("pts,w",[
    ([],None), ([(0,0,1)],None), ([(0,float("nan"))],None),
    ([(0,0),(1,1)],[1]), ([(0,0),(1,1)],[-1,1]),
    ([(0,0),(1,1)],[0,0]), ([(0,0),(1,1)],[1,float("inf")])
])
def test_invalid_points_or_weights_rejected(pts,w):
    with pytest.raises(ValueError):
        mean_center(pts,w)

def test_median_center_rejects_invalid_iteration_controls():
    with pytest.raises(ValueError): median_center([(0,0)],tolerance=0)
    with pytest.raises(ValueError): median_center([(0,0)],max_iterations=0)
    with pytest.raises(ValueError): median_center([(0,0)],tolerance=True)

def test_ellipse_rejects_invalid_scale():
    with pytest.raises(ValueError): standard_deviational_ellipse([(0,0)],scale=0)
    with pytest.raises(ValueError): standard_deviational_ellipse([(0,0)],scale=True)
