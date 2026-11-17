import math
import pytest
from uncertainty_propagation import monte_carlo_uniform, positional_rmse, sobol_first_total


def test_positional_rmse_bias_and_axis_values():
    result = positional_rmse([(0,0),(1,1)], [(3,4),(4,5)])
    assert result["bias"] == [3,4]
    assert result["axis_rmse"] == [3,4]
    assert result["pooled_rmse"] == pytest.approx(math.sqrt(12.5))


def test_positional_rmse_rejects_bad_shapes():
    with pytest.raises(ValueError): positional_rmse([], [])
    with pytest.raises(ValueError): positional_rmse([(0,0)], [(1,)])
    with pytest.raises(ValueError): positional_rmse([(0,float("nan"))], [(1,2)])


def test_monte_carlo_is_reproducible_and_summarizes():
    a = monte_carlo_uniform(lambda x: x[0]**2, [(0,1)], 10000, seed=4)
    b = monte_carlo_uniform(lambda x: x[0]**2, [(0,1)], 10000, seed=4)
    assert a == b
    assert a["mean"] == pytest.approx(1/3, abs=0.015)
    assert a["variance"] == pytest.approx(4/45, abs=0.015)
    assert a["quantiles"]["0.5"] == pytest.approx(0.25, abs=0.02)


def test_sobol_indices_for_additive_linear_model():
    result = sobol_first_total(lambda x: x[0]+2*x[1], [(0,1),(0,1)], 30000, seed=7)
    assert result["first_order"][0] == pytest.approx(0.2, abs=0.025)
    assert result["first_order"][1] == pytest.approx(0.8, abs=0.025)
    assert result["total_order"][0] == pytest.approx(0.2, abs=0.025)
    assert result["total_order"][1] == pytest.approx(0.8, abs=0.025)


def test_sobol_rejects_constant_output():
    with pytest.raises(ValueError):
        sobol_first_total(lambda x: 5, [(0,1)], 100, seed=1)


def test_invalid_monte_carlo_inputs_and_nonfinite_model():
    with pytest.raises(ValueError): monte_carlo_uniform(lambda x:x[0], [], 10)
    with pytest.raises(ValueError): monte_carlo_uniform(lambda x:x[0], [(1,1)], 10)
    with pytest.raises(ValueError): monte_carlo_uniform(lambda x:x[0], [(0,1)], 1)
    with pytest.raises(ValueError): monte_carlo_uniform(lambda x:float("nan"), [(0,1)], 10)
