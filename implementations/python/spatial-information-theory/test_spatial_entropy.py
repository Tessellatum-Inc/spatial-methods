import math
import numpy as np
import pytest
from spatial_entropy import categorical_entropy,permutation_entropy,renyi_entropy,shannon_entropy,tsallis_entropy

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

def test_invalid_inputs():
    with pytest.raises(ValueError): shannon_entropy([0,0])
    with pytest.raises(ValueError): renyi_entropy([1,2],order=0)
    with pytest.raises(ValueError): tsallis_entropy([1,2],q=-1)
    with pytest.raises(ValueError): permutation_entropy([1,2],order=3)
