import numpy as np
import pytest
from ppml import ppml

def test_ppml_recovers_coefficients_with_zero_outcomes():
    rng=np.random.default_rng(44); z=rng.normal(size=5000); x=np.column_stack([np.ones(z.size),z]); beta=np.array([0.45,-0.55])
    y=rng.poisson(np.exp(x@beta)); fit=ppml(y,x)
    assert fit.converged and np.allclose(fit.coefficients,beta,atol=0.07)
    assert np.all(fit.fitted_mean>0) and np.all(fit.standard_errors>=0)

def test_ppml_offset():
    rng=np.random.default_rng(8); z=rng.normal(size=3000); off=np.log(rng.uniform(.5,2,z.size)); x=np.column_stack([np.ones(z.size),z]); beta=np.array([-.2,.35])
    y=rng.poisson(np.exp(off+x@beta)); fit=ppml(y,x,offset=off)
    assert np.allclose(fit.coefficients,beta,atol=.09)

@pytest.mark.parametrize('y,x', [([-1,0,1],[[1],[1],[1]]),([1,2],[[1]]),([1,2,3],[[1,0],[1,0],[1,0]])])
def test_invalid_data(y,x):
    with pytest.raises(ValueError): ppml(np.asarray(y),np.asarray(x))
