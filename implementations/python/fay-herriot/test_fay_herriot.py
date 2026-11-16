import numpy as np
import pytest
from fay_herriot import fay_herriot


def test_fay_herriot_returns_finite_predictions_and_uncertainty():
    y = [10., 12., 8., 15., 9., 13.]
    r = fay_herriot(y, [.5] * len(y))
    assert r["random_effect_variance"] >= 0
    assert np.isfinite(r["predictions"]).all()
    assert np.isfinite(r["mse_plugin"]).all()
    assert np.all(np.asarray(r["mse_plugin"]) >= 0)


def test_fay_herriot_shrinkage_factors_are_bounded():
    r = fay_herriot([0., 1., 2., 20., 21., 22.], [.1] * 6)
    g = np.asarray(r["shrinkage_factors"])
    assert np.all(g >= 0) and np.all(g <= 1)


def test_fay_herriot_covariate_regression():
    x = np.arange(8, dtype=float)
    y = 2 + 3*x + np.array([.1, -.1, .05, -.05, .08, -.08, .02, -.02])
    r = fay_herriot(y, np.full(8, .2), np.column_stack([np.ones(8), x]))
    assert r["beta"] == pytest.approx([2, 3], abs=.1)


def test_fay_herriot_zero_variance_boundary():
    r = fay_herriot([5.] * 4, [.2] * 4)
    assert r["random_effect_variance"] == pytest.approx(0, abs=1e-8)
    assert r["predictions"] == pytest.approx([5.] * 4, abs=1e-6)


@pytest.mark.parametrize("y,d", [
    ([1, 2], [1, 1]), ([1, float("nan"), 3], [1, 1, 1]),
    ([1, 2, 3], [1, 0, 1]), ([1, 2, 3], [1, 1]),
])
def test_fay_herriot_rejects_invalid_observations(y, d):
    with pytest.raises(ValueError):
        fay_herriot(y, d)


def test_fay_herriot_rejects_singular_or_misaligned_covariates():
    with pytest.raises(ValueError):
        fay_herriot([1, 2, 3, 4], [1]*4, [[1, 1]]*4)
    with pytest.raises(ValueError):
        fay_herriot([1, 2, 3, 4], [1]*4, [[1], [2]])
