import numpy as np
import pytest
from uncertainty import monte_carlo_propagation, sobol_sensitivity

def test_monte_carlo_recovers_uniform_linear_mean_and_variance():
    r=monte_carlo_propagation(lambda x:2*x[:,0]+3*x[:,1],[[0,1],[0,1]],n_samples=100000,seed=42)
    assert r["mean"]==pytest.approx(2.5,abs=.015)
    assert r["standard_deviation"]==pytest.approx(np.sqrt(13/12),abs=.015)
    assert r["quantiles"].shape==(3,)

def test_monte_carlo_returns_reproducible_samples():
    fn=lambda x:x[:,0]**2
    a=monte_carlo_propagation(fn,[[0,1]],n_samples=50,seed=3,return_samples=True)
    b=monte_carlo_propagation(fn,[[0,1]],n_samples=50,seed=3,return_samples=True)
    np.testing.assert_array_equal(a["input_samples"],b["input_samples"])
    np.testing.assert_array_equal(a["output_samples"],b["output_samples"])

def test_sobol_indices_for_additive_linear_model():
    r=sobol_sensitivity(lambda x:x[:,0]+2*x[:,1],[[0,1],[0,1]],n_samples=30000,seed=8)
    np.testing.assert_allclose(r["first_order"],[.2,.8],atol=.025)
    np.testing.assert_allclose(r["total_order"],[.2,.8],atol=.025)

def test_sobol_total_order_dominates_first_order_with_interaction():
    r=sobol_sensitivity(lambda x:x[:,0]+x[:,1]+2*x[:,0]*x[:,1],[[0,1],[0,1]],n_samples=30000,seed=11)
    assert np.all(r["total_order"]+.02>=r["first_order"])
    assert np.all(r["total_order"]>0)

def test_methods_validate_inputs_and_model_output():
    with pytest.raises(ValueError,match="bounds"): monte_carlo_propagation(lambda x:x,[[1,1]])
    with pytest.raises(ValueError,match="n_samples"): monte_carlo_propagation(lambda x:x[:,0],[[0,1]],n_samples=1)
    with pytest.raises(ValueError,match="finite outputs"): monte_carlo_propagation(lambda x:np.full(len(x),np.nan),[[0,1]])
    with pytest.raises(ValueError,match="positive"): sobol_sensitivity(lambda x:np.ones(len(x)),[[0,1]],n_samples=100)
    with pytest.raises(ValueError,match="scalar"): sobol_sensitivity(lambda x:np.column_stack([x[:,0],x[:,0]]),[[0,1]],n_samples=100)
