import math
import pytest
from navigation_trajectory import interpolate_navigation_trajectory

I=[[1,0,0],[0,1,0],[0,0,1]]
RZ=[[0,-1,0],[1,0,0],[0,0,1]]

def test_piecewise_position_and_velocity_across_multiple_segments():
    out=interpolate_navigation_trajectory(
        [0,2,5],[[0,0,0],[2,0,0],[8,3,0]],[I,I,I],[1,3.5])
    assert out[0]["position_navigation"]==pytest.approx([1,0,0])
    assert out[0]["velocity_navigation"]==pytest.approx([1,0,0])
    assert out[0]["segment_index"]==0
    assert out[1]["position_navigation"]==pytest.approx([5,1.5,0])
    assert out[1]["velocity_navigation"]==pytest.approx([2,1,0])
    assert out[1]["segment_index"]==1

def test_attitude_uses_shortest_so3_geodesic():
    out=interpolate_navigation_trajectory([0,2],[[0,0,0],[0,0,0]],[I,RZ],[1])[0]
    r=out["imu_to_navigation_rotation"]
    assert r[0][0]==pytest.approx(math.sqrt(.5))
    assert r[1][0]==pytest.approx(math.sqrt(.5))
    assert out["angular_rate_body"]==pytest.approx([0,0,math.pi/4])

def test_knots_and_final_endpoint_are_supported():
    out=interpolate_navigation_trajectory([0,1,2],[[0,0,0],[1,0,0],[3,0,0]],[I,I,I],[0,1,2])
    assert [x["position_navigation"][0] for x in out]==pytest.approx([0,1,3])
    assert [x["segment_index"] for x in out]==[0,1,1]
    assert [x["interpolation_fraction"] for x in out]==pytest.approx([0,0,1])

def test_rejects_extrapolation_duplicate_times_and_misalignment():
    with pytest.raises(ValueError):
        interpolate_navigation_trajectory([0,1],[[0,0,0],[1,0,0]],[I,I],[-.01])
    with pytest.raises(ValueError):
        interpolate_navigation_trajectory([0,1,1],[[0,0,0]]*3,[I]*3,[.5])
    with pytest.raises(ValueError):
        interpolate_navigation_trajectory([0,1],[[0,0,0]],[I,I],[.5])
