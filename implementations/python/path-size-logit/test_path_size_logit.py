import numpy as np
import pytest
from path_size_logit import path_size_factors,path_size_log_likelihood,path_size_logit_probabilities

def test_disjoint_paths_have_unit_size():
    np.testing.assert_allclose(path_size_factors([["a","b"],["c"]]),[1,1])
def test_shared_edges_and_length_weighting():
    np.testing.assert_allclose(path_size_factors([["s","a"],["s","b"]],{"s":2,"a":1,"b":1}),[2/3,2/3])
def test_probabilities_penalize_overlap_and_are_stable():
    paths=[["s","a"],["s","b"],["c","d"]];p=path_size_logit_probabilities([0,0,0],paths)
    assert p.sum()==pytest.approx(1) and p[2]>p[0]
    assert np.all(path_size_logit_probabilities([10000,9999,9998],paths)>0)
def test_zero_correction_is_multinomial_logit():
    paths=[["a"],["a","b"],["c"]];p=path_size_logit_probabilities([1,2,3],paths,overlap_coefficient=0)
    expected=np.exp(np.array([1,2,3])-3);expected/=expected.sum();np.testing.assert_allclose(p,expected)
def test_likelihood_and_validation():
    paths=[["a"],["b"]];assert path_size_log_likelihood([0,0],paths,0)==pytest.approx(-np.log(2))
    with pytest.raises(ValueError): path_size_factors([[],["a"]])
    with pytest.raises(ValueError): path_size_factors([["a","a"]])
    with pytest.raises(ValueError): path_size_factors([["a"]],{"a":0})
    with pytest.raises(ValueError): path_size_logit_probabilities([0],paths)
