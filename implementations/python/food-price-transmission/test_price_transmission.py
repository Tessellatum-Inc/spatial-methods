import numpy as np
import pytest
from price_transmission import fit_error_correction_model


def test_error_correction_recovers_long_run_relation_and_adjustment():
    rng = np.random.default_rng(14)
    n = 2500
    source = np.cumsum(rng.normal(0., .5, n)) + 100.
    noise = np.zeros(n)
    innovations = rng.normal(0., .25, n)
    for i in range(1, n):
        noise[i] = .55*noise[i-1] + innovations[i]
    target = 4. + 1.4*source + noise
    model = fit_error_correction_model(source, target)
    assert model["long_run_elasticity"] == pytest.approx(1.4, abs=.02)
    assert model["error_correction_speed"] == pytest.approx(-.45, abs=.06)
    assert model["source_price_change_effect"] == pytest.approx(1.4, abs=.08)
    assert model["error_correction_speed"] < 0
    assert model["short_run_r_squared"] > .5


def test_error_correction_returns_inference_and_residuals():
    rng = np.random.default_rng(3)
    source = np.cumsum(rng.normal(size=100)) + 50.
    noise = np.zeros(100)
    for i in range(1,100):
        noise[i] = .4*noise[i-1] + rng.normal(scale=.3)
    target = 2. + .8*source + noise
    result = fit_error_correction_model(source, target)
    assert result["long_run_residuals"].shape == (100,)
    assert result["standard_errors"].shape == (3,)
    assert result["p_values"].shape == (3,)
    assert result["degrees_of_freedom"] == 96


@pytest.mark.parametrize("source,target", [
    ([1,2,3], [1,2,3]),
    ([1]*12, list(range(12))),
    (list(range(12)), [1]*11+[np.nan]),
])
def test_price_model_rejects_insufficient_or_invalid_series(source,target):
    with pytest.raises(ValueError):
        fit_error_correction_model(source,target)
