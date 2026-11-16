import numpy as np
import pytest
from gravity_flows import (attraction_constrained_gravity, doubly_constrained_gravity,
    entropy_maximizing_gravity, production_constrained_gravity, unconstrained_gravity)

def _example():
    return np.array([10.,20.]),np.array([5.,15.,10.]),np.array([[1.,2.,1.],[2.,1.,3.]])

def test_unconstrained_gravity_is_mass_times_impedance():
    o,d,f=_example()
    np.testing.assert_allclose(unconstrained_gravity(o,d,f),o[:,None]*d[None,:]*f)

def test_production_constrained_gravity_matches_origin_totals():
    o,d,f=_example(); flows=production_constrained_gravity(o,d,f)
    np.testing.assert_allclose(flows.sum(axis=1),o); assert np.all(flows>=0)

def test_attraction_constrained_gravity_matches_destination_totals():
    o,d,f=_example(); flows=attraction_constrained_gravity(o,d,f)
    np.testing.assert_allclose(flows.sum(axis=0),d); assert np.all(flows>=0)

def test_doubly_constrained_ipf_matches_both_margins():
    o,d,f=_example(); result=doubly_constrained_gravity(o,d,f)
    assert result.converged
    np.testing.assert_allclose(result.flows.sum(axis=1),o,atol=1e-8)
    np.testing.assert_allclose(result.flows.sum(axis=0),d,atol=1e-8)
    assert result.row_error<=1e-10 and result.column_error<=1e-10 and result.iterations>0

def test_entropy_maximizing_exponential_cost_deterrence():
    margins=[10.,10.]; cost=np.array([[0.,10.],[10.,0.]])
    result=entropy_maximizing_gravity(margins,margins,cost,beta=.5)
    assert result.converged and result.flows[0,0]>result.flows[0,1] and result.flows[1,1]>result.flows[1,0]
    np.testing.assert_allclose(result.flows.sum(axis=1),margins,atol=1e-8)
    np.testing.assert_allclose(result.flows.sum(axis=0),margins,atol=1e-8)

def test_zero_margins_and_structural_zeros_are_preserved():
    result=doubly_constrained_gravity([0,10],[5,5],[[0,0],[1,1]])
    assert result.converged and result.flows[0].sum()==0
    np.testing.assert_allclose(result.flows.sum(axis=0),[5,5],atol=1e-8)

def test_infeasible_margins_and_support_are_rejected():
    with pytest.raises(ValueError,match="total origin"):
        doubly_constrained_gravity([2,3],[4,4],np.ones((2,2)))
    with pytest.raises(ValueError,match="no feasible destination"):
        doubly_constrained_gravity([5,5],[5,5],[[1,0],[0,0]])

def test_singly_constrained_support_is_checked():
    with pytest.raises(ValueError,match="no reachable"):
        production_constrained_gravity([1,1],[1,1],[[0,0],[1,1]])
    with pytest.raises(ValueError,match="no reachable"):
        attraction_constrained_gravity([1,1],[1,1],[[0,1],[0,0]])

def test_validation_and_nonconvergence_diagnostics():
    with pytest.raises(ValueError,match="non-negative"): unconstrained_gravity([1],[1],[[-1]])
    with pytest.raises(ValueError,match="beta"): entropy_maximizing_gravity([1],[1],[[1]],beta=-1)
    result=doubly_constrained_gravity([10,20],[5,15,10],_example()[2],max_iter=1)
    assert not result.converged
