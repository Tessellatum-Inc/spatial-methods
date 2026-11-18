import numpy as np
import pytest
from fourier_filtering import (fft2_image, ifft2_image, radial_filter, filter_frequency,\n                              notch_reject_filter, destripe_periodic)

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


def test_notch_filter_removes_known_periodic_vertical_striping():
    rows, cols = 64, 96
    y, x = np.indices((rows, cols))
    clean = 20.0 + 0.05 * x + 0.02 * y
    stripe = 3.0 * np.cos(2 * np.pi * 7 * x / cols)
    observed = clean + stripe
    restored = destripe_periodic(observed, centers=[(0.0, 7 / cols)], radius=0.008)
    assert np.sqrt(np.mean((restored - clean) ** 2)) < 0.15


def test_notch_filter_is_conjugate_symmetric_and_preserves_dc():
    shape = (32, 48)
    h = notch_reject_filter(shape, [(0.0, 5 / 48)], radius=0.01)
    assert h[shape[0] // 2, shape[1] // 2] == pytest.approx(1.0)
    assert h[shape[0] // 2, shape[1] // 2 + 5] < 1e-12
    assert h[shape[0] // 2, shape[1] // 2 - 5] < 1e-12
    assert np.allclose(h, h[::-1, ::-1], atol=1e-12)


def test_notch_filter_rejects_invalid_parameters():
    with pytest.raises(ValueError): notch_reject_filter((8, 8), [], 0.1)
    with pytest.raises(ValueError): notch_reject_filter((8, 8), [(0.0, 0.1)], 0)
    with pytest.raises(ValueError): notch_reject_filter((8, 8), [(0.0, 0.5)], 0.1)
