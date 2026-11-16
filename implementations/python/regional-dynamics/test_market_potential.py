import numpy as np
import pytest
from market_potential import market_potential

def test_inverse_distance_market_potential():
    mass=np.array([10.,20.,30.]); d=np.array([[1.,2.,4.],[2.,1.,2.],[4.,2.,1.]])
    got=market_potential(mass,d)
    assert np.allclose(got,[10+10+7.5,5+20+15,2.5+10+30])

def test_excludes_self_potential():
    mass=np.array([10.,20.]); d=np.array([[1.,2.],[2.,1.]])
    assert np.allclose(market_potential(mass,d,self_potential=False),[10.,5.])

def test_generalized_cost_exponent():
    assert np.isclose(market_potential([4.,8.],[[1.,2.],[2.,1.]],exponent=2)[0],6.)

def test_rejects_invalid_inputs():
    with pytest.raises(ValueError): market_potential([1.,2.],[[0.,0.],[1.,1.]])
    with pytest.raises(ValueError): market_potential([1.,-2.],[[1.,2.],[2.,1.]])
