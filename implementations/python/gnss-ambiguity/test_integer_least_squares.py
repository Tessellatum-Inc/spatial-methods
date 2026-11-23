import itertools
import pytest
from integer_least_squares import integer_least_squares

def test_diagonal_covariance_matches_nearest_integer_solution():
    result=integer_least_squares([2.1, -1.8], [[1,0],[0,1]])
    assert result["best"]==[2,-2]
    assert result["best_objective"]==pytest.approx(0.05)
    assert result["second_best_objective"]>=result["best_objective"]

def test_correlated_case_matches_brute_force_reference():
    a=[0.49,0.49]; q=[[1,0.9],[0.9,1]]
    result=integer_least_squares(a,q)
    def score(z):
        # inverse of [[1,.9],[.9,1]] is 1/.19 * [[1,-.9],[-.9,1]]
        x,y=a[0]-z[0],a[1]-z[1]
        return (x*x-1.8*x*y+y*y)/0.19
    candidates=sorted((score(z),z) for z in itertools.product(range(-2,3),repeat=2))
    assert result["best"]==list(candidates[0][1])
    assert result["best_objective"]==pytest.approx(candidates[0][0])

def test_search_returns_distinct_two_best_integer_candidates():
    result=integer_least_squares([1.2], [[0.25]])
    assert result["best"]!=result["second_best"]
    assert result["second_best_objective"]>=result["best_objective"]

@pytest.mark.parametrize("a,q", [([],[]), ([1,2],[[1]]), ([1],[[0]]), ([1,2],[[1,2],[0,1]])])
def test_rejects_invalid_dimensions_or_covariance(a,q):
    with pytest.raises(ValueError):
        integer_least_squares(a,q)
