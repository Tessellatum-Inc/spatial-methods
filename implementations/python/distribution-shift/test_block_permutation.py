import numpy as np
import pytest
from block_permutation import spatial_block_mmd_test

def make_data(shift=0.0,seed=4):
    rng=np.random.default_rng(seed); X=[]; labels=[]; blocks=[]
    for b in range(12):
        group=0 if b<6 else 1
        X.append(rng.normal(shift*group,.25,size=(5,2)))
        labels.extend([group]*5); blocks.extend([b]*5)
    return np.vstack(X),np.asarray(labels),np.asarray(blocks)

def test_detects_separated_block_distributions():
    X,y,b=make_data(2.5); r=spatial_block_mmd_test(X,y,b,permutations=499,seed=12)
    assert r["mmd2_unbiased"]>0 and r["p_value"]<=.05
    assert r["n_blocks"]==12 and r["permutation_unit"]=="whole spatial block"

def test_permutation_is_reproducible_and_preserves_block_counts():
    X,y,b=make_data(.5); a=spatial_block_mmd_test(X,y,b,permutations=99,seed=3)
    c=spatial_block_mmd_test(X,y,b,permutations=99,seed=3)
    np.testing.assert_array_equal(a["permutation_statistics"],c["permutation_statistics"])
    assert a["p_value"]==c["p_value"] and a["n_blocks_group_0"]==6 and a["n_blocks_group_1"]==6

def test_validation():
    X,y,b=make_data()
    with pytest.raises(ValueError): spatial_block_mmd_test(X,y,b,bandwidth=0)
    with pytest.raises(ValueError): spatial_block_mmd_test(X,y,b,permutations=0)
    with pytest.raises(ValueError): spatial_block_mmd_test(X,y,b,alpha=1)
    with pytest.raises(ValueError): spatial_block_mmd_test(np.ones((4,1)),[0,0,1,1],[1,1,2,2])

def test_each_block_must_have_one_group():
    X,y,b=make_data(); y[0]=1
    with pytest.raises(ValueError,match="exactly one group"): spatial_block_mmd_test(X,y,b)

def test_two_blocks_per_group_required():
    X,y,b=make_data(); keep=np.isin(b,[0,1,2,3])
    with pytest.raises(ValueError): spatial_block_mmd_test(X[keep],y[keep],b[keep])
