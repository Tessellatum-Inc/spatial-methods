import numpy as np
import pytest
from reserve_selection import reserve_objective, marxan_style_select


def test_reserve_objective_matches_direct_cost_shortfall_and_boundary_oracle():
    features = np.array([[1.,0.],[0.,1.],[1.,1.]])
    selected = np.array([True, False, True])
    result = reserve_objective(selected, features, [2.,3.,4.], [2.,2.],
                               adjacency_edges=np.array([[0,1],[1,2]]),
                               boundary_lengths=[5.,7.],
                               boundary_modifier=2., shortfall_penalty=10.)
    assert result["acquisition_cost"] == 6.
    assert result["coverage"].tolist() == [2.,1.]
    assert result["shortfall"].tolist() == [0.,1.]
    assert result["boundary_length"] == 12.
    assert result["objective"] == 6.+24.+10.


def test_annealing_finds_low_cost_target_cover_and_is_reproducible():
    features = np.array([[1.,0.],[0.,1.],[1.,1.],[.5,.5]])
    costs = np.array([1.,1.,4.,1.5])
    result = marxan_style_select(features, costs, [1.,1.],
                                 shortfall_penalty=100.,
                                 iterations=12000, seed=7)
    assert result["met_all_targets"]
    assert result["acquisition_cost"] <= 3.0
    other = marxan_style_select(features, costs, [1.,1.],
                                shortfall_penalty=100.,
                                iterations=12000, seed=7)
    np.testing.assert_array_equal(result["selected"], other["selected"])


def test_infeasible_targets_are_reported_as_shortfall_not_hidden():
    result = marxan_style_select([[1.],[2.]], [1.,2.], [10.],
                                 iterations=100, seed=2)
    assert not result["met_all_targets"]
    assert result["shortfall"][0] == pytest.approx(7.)


def test_reserve_selection_validates_inputs_and_edges():
    with pytest.raises(ValueError, match="non-empty"):
        marxan_style_select(np.empty((0,2)), [], [1.,1.])
    with pytest.raises(ValueError, match="edges"):
        reserve_objective([True,False], [[1.],[1.]], [1.,1.], [1.],
                          adjacency_edges=[[0,1]], boundary_lengths=[])
