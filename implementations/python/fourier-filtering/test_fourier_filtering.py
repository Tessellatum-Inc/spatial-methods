import numpy as np
import pytest
from fourier_filtering import fft2_image, ifft2_image, radial_filter, filter_frequency

def test_round_trip():
    x=np.random.default_rng(4).normal(size=(13,17))
    assert np.allclose(ifft2_image(fft2_image(x)),x,atol=1e-12)

def test_dc_and_filtering():
    x=np.ones((16,16))*7
    h=radial_filter(x.shape,.15,kind="gaussian")
    assert np.allclose(filter_frequency(x,h),x,atol=1e-12)
    hp=radial_filter(x.shape,.15,kind="gaussian",highpass=True)
    assert np.max(np.abs(filter_frequency(x,hp)))<1e-12

def test_ideal_lowpass_attenuates_checkerboard():
    y,x=np.indices((32,32)); a=(-1.0)**(x+y)
    h=radial_filter(a.shape,.1,kind="ideal")
    assert np.max(np.abs(filter_frequency(a,h)))<1e-12

def test_invalid():
    with pytest.raises(ValueError): fft2_image(np.ones(3))
    with pytest.raises(ValueError): radial_filter((5,5),0)
