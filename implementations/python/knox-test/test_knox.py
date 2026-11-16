import numpy as np
import pytest
from knox import knox_test

def test_knox_detects_constructed_space_time_clustering():
    xy=np.array([[0,0],[.1,0],[10,0],[10.1,0],[20,0],[20.1,0]],float)
    times=np.array([0,0.1,10,10.1,20,20.1])
    r=knox_test(xy,times,spatial_threshold=.5,temporal_threshold=.5,permutations=999,seed=7)
    assert r["observed_pairs"]==3
    assert r["p_value_upper"]<=.1
    assert r["null_mean"]<r["observed_pairs"]

def test_knox_returns_reproducible_permutation_distribution():
    xy=np.array([[0,0],[1,0],[2,0],[3,0]],float); t=np.array([0,1,2,3.])
    a=knox_test(xy,t,spatial_threshold=1.1,temporal_threshold=1.1,permutations=50,seed=3)
    b=knox_test(xy,t,spatial_threshold=1.1,temporal_threshold=1.1,permutations=50,seed=3)
    np.testing.assert_array_equal(a["permutation_counts"],b["permutation_counts"])

def test_knox_validates_dimensions_thresholds_and_permutations():
    with pytest.raises(ValueError,match="coordinates"):
        knox_test([[0,0],[1,1]],[0,1],spatial_threshold=1,temporal_threshold=1)
    with pytest.raises(ValueError,match="times"):
        knox_test([[0,0],[1,1],[2,2]],[0,1],spatial_threshold=1,temporal_threshold=1)
    with pytest.raises(ValueError,match="positive"):
        knox_test([[0,0],[1,1],[2,2]],[0,1,2],spatial_threshold=0,temporal_threshold=1)
    with pytest.raises(ValueError,match="permutations"):
        knox_test([[0,0],[1,1],[2,2]],[0,1,2],spatial_threshold=1,temporal_threshold=1,permutations=0)
