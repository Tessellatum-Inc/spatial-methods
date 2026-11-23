import math
import pytest
from trajectory_covariance import interpolate_navigation_pose_with_covariance

I=[[1,0,0],[0,1,0],[0,0,1]]
RZ=[[0,-1,0],[1,0,0],[0,0,1]]

def zeros(n=12): return [[0.0]*n for _ in range(n)]

def test_position_covariance_interpolates_endpoint_variances_and_cross_terms():
    c=zeros()
    c[0][0]=4.0;c[6][6]=9.0;c[0][6]=c[6][0]=2.0
    out=interpolate_navigation_pose_with_covariance(
        [0,2],[[0,0,0],[2,0,0]],[I,I],1,c)
    assert out["covariance"][0][0]==pytest.approx(0.25*4+0.25*9+0.5*2)
    assert out["jacobian"][0][0]==pytest.approx(0.5)
    assert out["jacobian"][0][6]==pytest.approx(0.5)

def test_attitude_uncertainty_at_midpoint_of_identical_poses():
    c=zeros();c[3][3]=0.04;c[9][9]=0.09
    out=interpolate_navigation_pose_with_covariance(
        [0,2],[[0,0,0],[0,0,0]],[I,I],1,c)
    assert out["covariance"][3][3]==pytest.approx(0.25*(0.04+0.09),abs=1e-8)
    assert out["jacobian"][3][3]==pytest.approx(0.5,abs=1e-6)
    assert out["jacobian"][3][9]==pytest.approx(0.5,abs=1e-6)

def test_endpoint_epochs_recover_endpoint_covariance_blocks():
    c=zeros();c[0][0]=2.0;c[6][6]=5.0
    first=interpolate_navigation_pose_with_covariance(
        [0,1],[[0,0,0],[1,0,0]],[I,I],0,c)
    last=interpolate_navigation_pose_with_covariance(
        [0,1],[[0,0,0],[1,0,0]],[I,I],1,c)
    assert first["covariance"][0][0]==pytest.approx(2.0,abs=1e-8)
    assert last["covariance"][0][0]==pytest.approx(5.0,abs=1e-8)

def test_rejects_out_of_support_and_asymmetric_covariance():
    c=zeros();c[0][6]=1
    with pytest.raises(ValueError):
        interpolate_navigation_pose_with_covariance([0,1],[[0,0,0],[1,0,0]],[I,I],2,zeros())
    with pytest.raises(ValueError):
        interpolate_navigation_pose_with_covariance([0,1],[[0,0,0],[1,0,0]],[I,I],.5,c)

def test_rotation_covariance_jacobian_is_finite_for_rotating_segment():
    c=zeros()
    for i in (3,4,5,9,10,11): c[i][i]=1e-4
    out=interpolate_navigation_pose_with_covariance(
        [0,2],[[0,0,0],[0,0,0]],[I,RZ],1,c)
    assert all(math.isfinite(x) for row in out["jacobian"] for x in row)
    assert out["covariance"][3][3]>=0
