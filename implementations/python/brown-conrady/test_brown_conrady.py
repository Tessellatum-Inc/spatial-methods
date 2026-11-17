import numpy as np
import pytest
from brown_conrady import distort, undistort


def test_zero_coefficients_are_identity():
    p = np.array([[0., 0.], [.1, -.2], [1.2, .7]])
    assert np.allclose(distort(p), p)
    assert np.allclose(undistort(p), p)


def test_radial_and_tangential_round_trip():
    p = np.array([[.1, .2], [-.25, .3], [.45, -.35], [0., 0.]])
    d = distort(p, k1=-.12, k2=.025, p1=.001, p2=-.002, k3=-.003)
    recovered = undistort(d, k1=-.12, k2=.025, p1=.001, p2=-.002, k3=-.003)
    assert np.allclose(recovered, p, atol=1e-10)


def test_arbitrary_leading_dimensions_are_preserved():
    p = np.zeros((2, 3, 2))
    assert distort(p).shape == p.shape
    assert undistort(p).shape == p.shape


@pytest.mark.parametrize("points", [np.array([1., 2., 3.]), np.array([[1., np.nan]])])
def test_invalid_points_are_rejected(points):
    with pytest.raises(ValueError):
        distort(points)


def test_nonfinite_coefficients_and_invalid_iteration_controls_raise():
    with pytest.raises(ValueError):
        distort([[0., 0.]], k1=np.nan)
    with pytest.raises(ValueError):
        undistort([[0., 0.]], max_iter=0)
    with pytest.raises(ValueError):
        undistort([[0., 0.]], tolerance=0)
