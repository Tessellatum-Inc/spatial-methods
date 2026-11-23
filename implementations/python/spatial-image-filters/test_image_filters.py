import numpy as np
import pytest
from image_filters import gaussian_filter, laplacian_filter, median_filter, bilateral_filter, anisotropic_diffusion

def test_gaussian_preserves_constant_and_is_symmetric():
    a = np.full((9, 11), 4.25)
    np.testing.assert_allclose(gaussian_filter(a, 1.3), a, atol=1e-12)
    impulse = np.zeros((15, 15)); impulse[7, 7] = 1
    out = gaussian_filter(impulse, 1)
    np.testing.assert_allclose(out, out[::-1, :])
    np.testing.assert_allclose(out, out[:, ::-1])
    assert out[7, 7] > out[7, 8] > out[7, 10]

def test_laplacian_constant_zero_and_quadratic_interior():
    np.testing.assert_allclose(laplacian_filter(np.ones((5, 6))), 0)
    y, x = np.indices((9, 9), dtype=float)
    np.testing.assert_allclose(laplacian_filter(x*x+y*y)[2:-2, 2:-2], 4)

def test_median_removes_impulse_and_matches_independent_oracle():
    a = np.arange(20, dtype=float).reshape(4, 5); a[1, 2] = 1000
    got = median_filter(a, 1)
    p = np.pad(a, 1, mode="reflect")
    expected = np.array([[np.median(p[y:y+3, x:x+3]) for x in range(5)] for y in range(4)])
    np.testing.assert_allclose(got, expected)
    assert got[1, 2] != 1000
    np.testing.assert_array_equal(median_filter(a, 0), a)

def test_bilateral_preserves_constant_and_respects_step_edge():
    a = np.zeros((9, 12)); a[:, 6:] = 10; a[4, 4] = 2
    out = bilateral_filter(a, 2, 1, radius=3)
    assert out[4, 4] < 1
    assert out[4, 6] > 9
    np.testing.assert_allclose(bilateral_filter(np.full((5, 5), 3.), 1, 2), 3)

def test_diffusion_preserves_constant_and_reduces_variance():
    constant = np.full((8, 9), 2.)
    np.testing.assert_allclose(anisotropic_diffusion(constant), constant)
    noisy = np.zeros((15, 15)); noisy[7, 7] = 10
    out = anisotropic_diffusion(noisy, iterations=8, conductance=5, step=.2)
    assert out.var() < noisy.var()
    assert np.isfinite(out).all()

@pytest.mark.parametrize("call", [
    lambda: gaussian_filter([[1]], 0),
    lambda: median_filter([[1]], -1),
    lambda: bilateral_filter([[1]], 1, 0),
    lambda: anisotropic_diffusion([[1]], step=.3),
    lambda: anisotropic_diffusion([[1]], option="bad"),
    lambda: laplacian_filter([[1, 2], [3, np.nan]]),
])
def test_invalid_inputs_raise(call):
    with pytest.raises(ValueError):
        call()
