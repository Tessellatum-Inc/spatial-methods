import pytest
from sounding_uncertainty import propagate_sounding_uncertainty

I=[[1,0,0],[0,1,0],[0,0,1]]

def zero_covariance():
    return [[0.0]*18 for _ in range(18)]

def args(c):
    return ([100,200,10],I,[1,0,0],[0,0,1],I,[0,0,5],c)

def test_position_covariance_transfers_directly_to_sounding():
    c=zero_covariance()
    c[0][0]=4;c[1][1]=9;c[2][2]=16
    out=propagate_sounding_uncertainty(*args(c))
    assert out["point_navigation"]==pytest.approx([99,200,16])
    assert [out["covariance"][i][i] for i in range(3)]==pytest.approx([4,9,16])
    assert out["standard_uncertainties"]==pytest.approx([2,3,4])

def test_attitude_uncertainty_maps_through_acoustic_and_lever_arm_geometry():
    c=zero_covariance();c[3][3]=0.01
    out=propagate_sounding_uncertainty(*args(c))
    # A navigation-frame rotation about x moves the 6 m forward vector in z.
    assert out["covariance"][2][2]==pytest.approx(0.36)
    assert out["covariance"][1][1]==pytest.approx(0.0)

def test_shared_position_and_lever_arm_cross_covariance_is_retained():
    c=zero_covariance();c[0][0]=1;c[6][6]=1;c[0][6]=c[6][0]=0.5
    out=propagate_sounding_uncertainty(*args(c))
    # The x lever-arm derivative is -1, so the positive cross term cancels.
    assert out["covariance"][0][0]==pytest.approx(1.0)

def test_rejects_asymmetric_or_wrong_sized_covariance():
    c=zero_covariance();c[0][1]=1
    with pytest.raises(ValueError): propagate_sounding_uncertainty(*args(c))
    with pytest.raises(ValueError):
        propagate_sounding_uncertainty([0,0,0],I,[0,0,0],[0,0,0],I,[0,0,1],[[1]])
