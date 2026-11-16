import math
import numpy as np
import pytest
from spatial_entropy import (categorical_entropy,permutation_entropy,renyi_entropy,
    sample_entropy,shannon_entropy,spatial_conditional_entropy,
    spatial_mutual_information,tsallis_entropy)


def test_shannon_reference_distributions():
    assert shannon_entropy([1,1,1,1])==pytest.approx(2)
    assert shannon_entropy([10,0,0])==pytest.approx(0)
    assert shannon_entropy([1,1],base=math.e)==pytest.approx(math.log(2))


def test_renyi_and_tsallis_limits_and_orders():
    p=[1,1,1,1]
    assert renyi_entropy(p,order=2)==pytest.approx(2)
    assert renyi_entropy(p,order=1)==pytest.approx(shannon_entropy(p))
    assert tsallis_entropy(p,q=2)==pytest.approx(.75)
    assert tsallis_entropy(p,q=1)==pytest.approx(shannon_entropy(p))


def test_categorical_raster_mask():
    a=np.array([[1,1,2],[2,2,2]])
    assert categorical_entropy(a)==pytest.approx(-(2/6*math.log2(2/6)+4/6*math.log2(4/6)))
    assert categorical_entropy(a,mask=np.array([[True,True,False],[False,False,False]]))==pytest.approx(0)


def test_permutation_entropy_patterns_and_normalization():
    increasing=np.arange(100.)
    assert permutation_entropy(increasing,order=3)==pytest.approx(0)
    rng=np.random.default_rng(2)
    h=permutation_entropy(rng.normal(size=5000),order=3)
    assert .85<h<=1.0


def _brute_sampen(x,m,tol):
    def count(length):
        windows=np.lib.stride_tricks.sliding_window_view(x,length)
        if length==m:
            windows=windows[:-1]
        return sum(np.max(np.abs(windows[i]-windows[j]))<=tol
                   for i in range(len(windows)) for j in range(i+1,len(windows)))
    a,b=count(m+1),count(m)
    return math.inf if a==0 else -math.log(a/b)


def test_sample_entropy_against_independent_pair_counter():
    x=np.array([0.,0.1,0.2,0.1,0.0,0.2,0.3,0.2,0.1])
    tol=.15
    assert sample_entropy(x,m=2,r=tol,normalize_r=False)==pytest.approx(_brute_sampen(x,2,tol))
    assert sample_entropy(np.ones(20),m=2)==pytest.approx(0.0)


def test_spatial_edge_entropy_and_information():
    labels=np.array(["A","A","B","B"])
    w=np.array([[0,1,0,0],[1,0,1,0],[0,1,0,1],[0,0,1,0]],float)
    # Symmetric chain: both endpoint marginals are balanced and endpoints are
    # perfectly determined by each other only on the two central edge pairs.
    hcond=spatial_conditional_entropy(labels,w)
    mi=spatial_mutual_information(labels,w)
    assert 0.0<=hcond<=1.0
    assert 0.0<=mi<=1.0
    assert spatial_conditional_entropy(["A","A"],[[0,1],[1,0]])==pytest.approx(0.0)
    assert spatial_mutual_information(["A","A"],[[0,1],[1,0]])==pytest.approx(0.0)


def test_spatial_entropy_rejects_bad_graphs():
    with pytest.raises(ValueError): spatial_conditional_entropy([1,2],[[0,0],[0,0]])
    with pytest.raises(ValueError): spatial_mutual_information([1,2],[[0,-1],[-1,0]])
    with pytest.raises(ValueError): spatial_conditional_entropy([1,2],[[0,1]])
    

def test_invalid_inputs():
    with pytest.raises(ValueError): shannon_entropy([0,0])
    with pytest.raises(ValueError): renyi_entropy([1,2],order=0)
    with pytest.raises(ValueError): tsallis_entropy([1,2],q=-1)
    with pytest.raises(ValueError): permutation_entropy([1,2],order=3)
    with pytest.raises(ValueError): sample_entropy([1,2,3],m=2)
