import numpy as np
import pytest
from gabor_filters import gabor_kernel, gabor_response, gabor_bank

def test_kernel_zero_mean_and_unit_norm():
    k=gabor_kernel(frequency=.2,theta=.4,sigma=2)
    assert abs(k.mean())<1e-12
    assert np.linalg.norm(k)==pytest.approx(1.)

def test_constant_image_has_near_zero_response():
    k=gabor_kernel(frequency=.2)
    r=gabor_response(np.ones((20,20)),k)
    np.testing.assert_allclose(r,0,atol=1e-10)

def test_bank_shape_and_validation():
    b=gabor_bank(np.zeros((12,12)),frequencies=[.1,.2],orientations=[0,np.pi/2])
    assert b.shape==(2,2,12,12)
    with pytest.raises(ValueError): gabor_kernel(frequency=0)
