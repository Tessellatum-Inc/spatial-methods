import numpy as np
import pytest
from adaptive_thresholding import adaptive_threshold

def test_uniform_image_with_positive_offset():
    x=np.full((12,13),5.0)
    binary,t=adaptive_threshold(x,5,offset=1)
    assert binary.all()
    assert np.allclose(t,4)

def test_local_bright_feature_detected():
    x=np.zeros((21,21)); x[9:12,9:12]=10
    binary,_=adaptive_threshold(x,7,offset=0)
    assert binary[10,10]
    assert not binary[0,0]

def test_gaussian_shape_and_constant():
    x=np.full((9,11),3.)
    b,t=adaptive_threshold(x,5,method="gaussian")
    assert not b.any() and np.allclose(t,3)

def test_invalid():
    with pytest.raises(ValueError): adaptive_threshold(np.ones((3,3)),4)
    with pytest.raises(ValueError): adaptive_threshold(np.ones((3,3)),5,method="sauvola")
