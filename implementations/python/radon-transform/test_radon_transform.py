import numpy as np
import pytest
from radon_transform import radon_transform

def test_constant_square_centre_line_integral():
    x=np.ones((9,9))
    s,r,t=radon_transform(x,theta=[0,90])
    i=np.argmin(abs(r))
    assert s[i,0]>0 and s[i,1]>0
    assert abs(s[i,0]-9)<1e-8
    assert abs(s[i,1]-9)<1e-8

def test_impulse_symmetry_and_shape():
    x=np.zeros((9,9)); x[4,4]=1
    s,r,t=radon_transform(x,theta=[0,45,90])
    assert s.shape==(len(r),3)
    assert np.allclose(s[:,0],s[:,2])

def test_validation():
    with pytest.raises(ValueError): radon_transform(np.ones((3,4)),rho_resolution=0)
