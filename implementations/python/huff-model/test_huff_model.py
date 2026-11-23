import numpy as np
import pytest
from huff_model import huff_expected_visits,huff_market_shares,huff_probabilities

def test_probabilities_sum_to_one_and_respond_to_attraction_and_cost():
    p=huff_probabilities([1,4],[[1,1.5],[.25,1]])
    np.testing.assert_allclose(p.sum(axis=1),[1,1])
    assert p[0,1]>p[0,0] and p[1,0]>p[1,1]

def test_attractiveness_exponent_and_zero_cost_regularization():
    p=huff_probabilities([1,4],[[0,0]],alpha=1,beta=2,minimum_cost=.1)
    assert p[0,1]==pytest.approx(.8) and np.isfinite(p).all()

def test_market_shares_conserve_origin_demand():
    p=huff_probabilities([2,1],[[1,2],[3,1]])
    visits=huff_market_shares(p,[100,50])
    assert visits.sum()==pytest.approx(150)
    np.testing.assert_allclose(visits,huff_expected_visits([2,1],[[1,2],[3,1]],[100,50]))

def test_validation():
    with pytest.raises(ValueError): huff_probabilities([1,0],[[1,2]])
    with pytest.raises(ValueError): huff_probabilities([1,2],[[-1,2]])
    with pytest.raises(ValueError): huff_probabilities([1,2],[[1,2]],beta=-1)
    with pytest.raises(ValueError): huff_market_shares([[.2,.2]],[1])
