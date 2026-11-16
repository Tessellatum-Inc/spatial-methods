import numpy as np
import pytest
from spectral_similarity import spectral_angle,spectral_information_divergence,spectral_angle_map,sid_map

def test_sam_known_angles():
    assert np.isclose(spectral_angle([1,0],[0,1]),np.pi/2)
    assert np.isclose(spectral_angle([1,1],[2,2]),0)

def test_sid_symmetry_and_identity():
    p=np.array([.2,.3,.5]); q=np.array([.1,.4,.5])
    assert np.isclose(spectral_information_divergence(p,p),0)
    assert np.isclose(spectral_information_divergence(p,q),spectral_information_divergence(q,p))

def test_maps_and_zero_policy():
    cube=np.array([[[1.,0.],[0.,1.]]])
    assert spectral_angle_map(cube,np.array([1.,0.])).shape==(1,2)
    assert np.isnan(spectral_angle([0,0],[1,0]))
    assert spectral_angle([0,0],[1,0],zero_policy="zero")==0
    assert sid_map(cube,np.array([1.,0.])).shape==(1,2)

def test_invalid_negative_sid():
    with pytest.raises(ValueError): spectral_information_divergence([-1,2],[1,1])
