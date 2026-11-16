import numpy as np
import pytest
from edge_detection import sobel, canny

def test_sobel_constant_has_zero_gradient():
    gx,gy,m,a=sobel(np.ones((8,9)))
    np.testing.assert_allclose(gx,0); np.testing.assert_allclose(gy,0); np.testing.assert_allclose(m,0)

def test_sobel_ramp_detects_horizontal_change():
    x=np.tile(np.arange(9,dtype=float),(7,1))
    gx,gy,m,_=sobel(x)
    assert np.all(gx[:,2:-2]>0)
    np.testing.assert_allclose(gy,0,atol=1e-12)

def test_canny_detects_step_and_is_boolean():
    x=np.zeros((40,40)); x[:,20:]=1
    e=canny(x,low_threshold=.05,high_threshold=.1,sigma=1)
    assert e.dtype==bool and e.any()
    assert np.abs(np.where(e)[1].mean()-20)<2

def test_canny_threshold_validation():
    with pytest.raises(ValueError): canny(np.zeros((3,3)),low_threshold=2,high_threshold=1)
    with pytest.raises(ValueError): sobel(np.ones((2,2,2)))
