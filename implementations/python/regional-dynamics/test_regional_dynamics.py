import numpy as np
import pytest
from regional_dynamics import markov_transitions, spatial_markov_transitions, lisa_transition_matrix, sigma_convergence

def panel():
    return np.array([[1,2,3,4],[2,2,4,3],[3,1,4,2]],float)
def weights():
    return np.array([[0,1,0,0],[1,0,1,0],[0,1,0,1],[0,0,1,0]],float)

def test_markov_counts_and_probabilities():
    r=markov_transitions(panel(),2)
    assert r["counts"].sum()==8
    nz=r["counts"].sum(axis=1)>0
    np.testing.assert_allclose(r["probabilities"][nz].sum(axis=1),1)

def test_spatial_markov_conditioning():
    r=spatial_markov_transitions(panel(),weights(),2)
    assert r["counts"].shape==(2,2,2)
    assert r["counts"].sum()==8
    nz=r["counts"].sum(axis=2)>0
    np.testing.assert_allclose(r["probabilities"].sum(axis=2)[nz],1)

def test_lisa_quadrants_and_transitions():
    x=np.array([[1,2,8,9],[2,1,9,8],[1,3,7,9]],float)
    r=lisa_transition_matrix(x,weights())
    assert r["labels"]==("HH","HL","LH","LL")
    assert r["counts"].sum()==8
    assert set(np.unique(r["states"])).issubset({0,1,2,3})

def test_sigma_convergence():
    x=np.array([[1,2,3],[2,2,2],[1,3,5]],float)
    np.testing.assert_allclose(sigma_convergence(x),[np.std([1,2,3]),0,np.std([1,3,5])])

@pytest.mark.parametrize("bad",[np.array([[1,2],[3,np.nan]]),np.ones((1,3)),np.ones(3)])
def test_invalid_panel(bad):
    with pytest.raises(ValueError): markov_transitions(bad)

def test_invalid_weights_and_constant_lisa_period():
    with pytest.raises(ValueError): spatial_markov_transitions(panel(),np.zeros((4,4)))
    x=np.array([[1,1,1],[1,2,3]],float)
    w=np.array([[0,1,1],[1,0,1],[1,1,0]],float)
    with pytest.raises(ValueError): lisa_transition_matrix(x,w)
