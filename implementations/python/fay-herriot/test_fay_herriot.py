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


def test_fay_herriot_parametric_bootstrap_mse_is_seeded_and_finite():
    from fay_herriot import fay_herriot_bootstrap_mse
    y=[10.,12.,8.,15.,9.,13.,7.,16.]
    d=[.4,.5,.6,.3,.7,.4,.5,.6]
    a=fay_herriot_bootstrap_mse(y,d,replicates=30,seed=27)
    b=fay_herriot_bootstrap_mse(y,d,replicates=30,seed=27)
    assert a==b
    assert np.isfinite(a["bootstrap_mse"]).all()
    assert np.isfinite(a["bootstrap_mse_mc_se"]).all()
    assert np.all(np.asarray(a["bootstrap_mse"])>=0)
    assert np.all(np.asarray(a["bootstrap_mse_mc_se"])>=0)
    assert a["replicates"]==30


@pytest.mark.parametrize("kwargs",[
    {"replicates":1},{"replicates":2.5},{"replicates":True},{"seed":True}
])
def test_fay_herriot_bootstrap_rejects_invalid_controls(kwargs):
    from fay_herriot import fay_herriot_bootstrap_mse
    with pytest.raises(ValueError):
        fay_herriot_bootstrap_mse([1,2,3,4],[1,1,1,1],**kwargs)
