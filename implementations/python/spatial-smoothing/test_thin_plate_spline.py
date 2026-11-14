import numpy as np
import pytest
from thin_plate_spline import ThinPlateSpline2D


def test_zero_penalty_interpolates_training_values():
    x = np.array([[0., 0.], [1., 0.], [0., 1.], [1., 1.], [0.4, 0.7]])
    y = np.sin(x[:, 0]) + x[:, 1] ** 2
    fit = ThinPlateSpline2D(smoothing=0.0).fit(x, y)
    np.testing.assert_allclose(fit.predict(x), y, atol=1e-8)


def test_linear_plane_is_unpenalized_for_positive_smoothing():
    rng = np.random.default_rng(5)
    x = rng.uniform(-2, 2, size=(20, 2))
    y = 4.0 + 2.5 * x[:, 0] - 0.75 * x[:, 1]
    fit = ThinPlateSpline2D(smoothing=10.0).fit(x, y)
    np.testing.assert_allclose(fit.predict(x), y, atol=1e-8)


def test_predict_at_new_locations_is_finite():
    x = np.array([[0., 0.], [1., 0.], [0., 1.], [1., 1.]])
    y = x[:, 0] * x[:, 1]
    model = ThinPlateSpline2D(0.2).fit(x, y)
    pred = model.predict(np.array([[0.5, 0.5], [2., 2.]]))
    assert pred.shape == (2,)
    assert np.isfinite(pred).all()


@pytest.mark.parametrize("x,y,smoothing", [
    (np.ones((4, 3)), np.ones(4), 1.0),
    (np.array([[0., 0.], [1., 1.], [2., 2.]]), np.ones(3), 1.0),
    (np.ones((4, 2)), np.ones(3), 1.0),
    (np.ones((4, 2)), np.ones(4), -1.0),
    (np.ones((4, 2)), np.ones(4), np.nan),
])
def test_invalid_inputs(x, y, smoothing):
    with pytest.raises(ValueError):
        ThinPlateSpline2D(smoothing).fit(x, y)


def test_predict_before_fit_raises():
    with pytest.raises(RuntimeError):
        ThinPlateSpline2D().predict(np.array([[0., 0.]]))
