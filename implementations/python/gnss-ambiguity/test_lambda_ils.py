import itertools
import numpy as np
import pytest
from lambda_ils import lambda_integer_least_squares, lambda_reduction

def objective(a,z,q):
    d=a-z
    return float(d@np.linalg.solve(q,d))

def test_reduction_is_integer_unimodular_and_preserves_factorisation():
    a=np.array([1.2,1.8]); q=np.array([[4.0,3.9],[3.9,4.0]])
    r=lambda_reduction(a,q); z=r["transformation"]
    assert np.allclose(z,np.rint(z)) and abs(round(np.linalg.det(z)))==1
    assert np.allclose(r["transformed_covariance"],z.T@q@z)
    assert np.allclose(r["transformed_covariance"],r["L"].T@np.diag(r["D"])@r["L"])

def test_correlated_case_returns_two_best_candidates():
    a=np.array([1.2,1.8]); q=np.array([[4.0,3.9],[3.9,4.0]])
    r=lambda_integer_least_squares(a,q)
    assert r["best"].tolist()==[1,2] and r["second_best"].tolist()==[0,1]
    assert r["best_objective"]==pytest.approx(objective(a,[1,2],q))
    assert r["second_best_objective"]==pytest.approx(objective(a,[0,1],q))

def test_search_matches_exhaustive_small_correlated_problem():
    a=np.array([1.2,-2.4,3.49])
    q=np.array([[1.0,.99,.95],[.99,1.0,.96],[.95,.96,1.0]])
    r=lambda_integer_least_squares(a,q); center=np.floor(a+.5).astype(int); candidates=[]
    for off in itertools.product(range(-4,5),repeat=3):
        z=center+np.asarray(off); candidates.append((objective(a,z,q),tuple(z)))
    candidates.sort()
    assert r["best"].tolist()==list(candidates[0][1])
    assert r["second_best"].tolist()==list(candidates[1][1])
    assert r["best_objective"]==pytest.approx(candidates[0][0])

def test_diagonal_covariance_agrees_with_componentwise_rounding():
    r=lambda_integer_least_squares([2.2,-1.7,.1],np.diag([.4,1.2,2.0]))
    assert r["best"].tolist()==[2,-2,0]

@pytest.mark.parametrize("a,q",[
    ([],[]),([1.0,np.nan],np.eye(2)),([1.0,2.0],[[1.0,2.0],[0.0,1.0]]),
    ([1.0,2.0],[[1.0,2.0],[2.0,1.0]]),([1.0,2.0],[[1.0,0.0],[0.0,0.0]])
])
def test_invalid_inputs_rejected(a,q):
    with pytest.raises(ValueError): lambda_integer_least_squares(a,q)

def test_search_controls_validated():
    with pytest.raises(ValueError): lambda_integer_least_squares([1.0],[[1.0]],candidate_count=1)
    with pytest.raises(ValueError): lambda_integer_least_squares([1.0],[[1.0]],max_nodes=0)
