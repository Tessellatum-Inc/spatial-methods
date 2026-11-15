import numpy as np
import pytest
from thin_plate_regression_spline import ThinPlateRegressionSpline2D
from thin_plate_spline import ThinPlateSpline2D


def test_full_rank_reduction_matches_full_knot_smoothing_spline():
    rng = np.random.default_rng(23)
    x = rng.uniform(-2, 2, size=(18, 2))
    y = np.sin(x[:, 0]) + 0.3 * x[:, 1] ** 2 + rng.normal(0, 0.05, size=18)
    smoothing = 0.4
    full = ThinPlateSpline2D(smoothing=smoothing).fit(x, y)
    reduced = ThinPlateRegressionSpline2D(k=len(x) - 3, smoothing=smoothing).fit(x, y)
    np.testing.assert_allclose(reduced.predict(x), full.predict(x), rtol=1e-8, atol=1e-8)
    assert reduced.basis_dimension_ == len(x)


def test_affine_plane_remains_unpenalized_at_low_rank():
    rng = np.random.default_rng(7)
    x = rng.uniform(-3, 3, size=(30, 2))
    y = 2.0 + 1.5 * x[:, 0] - 0.7 * x[:, 1]
    model = ThinPlateRegressionSpline2D(k=4, smoothing=20.0).fit(x, y)
    np.testing.assert_allclose(model.predict(x), y, atol=1e-8)


def test_low_rank_model_has_requested_basis_dimension_and_predicts():
    rng = np.random.default_rng(12)
    x = rng.uniform(-2, 2, size=(40, 2))
    y = np.sin(x[:, 0]) + x[:, 1] ** 2
    model = ThinPlateRegressionSpline2D(k=6, smoothing=1.0).fit(x, y)
    pred = model.predict(np.array([[0.0, 0.0], [1.0, -1.0]]))
    assert model.basis_rank_ == 6
    assert model.basis_dimension_ == 9
    assert pred.shape == (2,)
    assert np.isfinite(pred).all()


def test_zero_penalty_full_rank_interpolates():
    x = np.array([[0., 0.], [1., 0.], [0., 1.], [1., 1.], [.4, .7], [.2, .3]])
    y = np.sin(x[:, 0]) + x[:, 1] ** 2
    model = ThinPlateRegressionSpline2D(k=len(x) - 3, smoothing=0.0).fit(x, y)
    np.testing.assert_allclose(model.predict(x), y, atol=1e-8)


@pytest.mark.parametrize("k,smoothing", [(0, 1.0), (-1, 1.0), (True, 1.0), (3, -1.0), (3, np.nan)])
def test_invalid_constructor_inputs(k, smoothing):
    with pytest.raises(ValueError):
        ThinPlateRegressionSpline2D(k=k, smoothing=smoothing)


def test_invalid_data_and_rank_inputs():
    x = np.array([[0., 0.], [1., 0.], [0., 1.], [1., 1.]])
    with pytest.raises(ValueError):
        ThinPlateRegressionSpline2D(k=2).fit(x, np.ones(3))
    with pytest.raises(ValueError):
        ThinPlateRegressionSpline2D(k=2).fit(np.vstack((x, x[0])), np.ones(5))
    with pytest.raises(ValueError):
        ThinPlateRegressionSpline2D(k=2).fit(x, np.ones(4))
    with pytest.raises(ValueError):
        ThinPlateRegressionSpline2D(k=2).fit(x, np.array([1., 2., np.nan, 4.]))


def test_predict_before_fit_raises():
    with pytest.raises(RuntimeError):
        ThinPlateRegressionSpline2D(k=2).predict(np.array([[0., 0.]]))
