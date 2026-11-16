import numpy as np
import pytest
from glcm_texture import quantize, glcm, glcm_features

def test_quantization_clips_and_respects_mask():
    a=np.array([[-1.,0.,5.],[10.,np.nan,20.]])
    q,v=quantize(a,levels=4,value_range=(0,10))
    assert q.tolist()==[[0,0,2],[3,0,3]]
    assert v.tolist()==[[True,True,True],[True,False,True]]

def test_horizontal_glcm_counts_and_symmetry():
    a=np.array([[0,1,1]])
    m=glcm(a,levels=2,offsets=((0,1),))[0]
    np.testing.assert_allclose(m,[[0,1/4],[1/4,1/2]])
    np.testing.assert_allclose(m,m.T)

def test_mask_prevents_pairs_crossing_invalid_cells():
    a=np.array([[0,1,0]])
    mask=np.array([[True,False,True]])
    m=glcm(a,levels=2,offsets=((0,1),),mask=mask)[0]
    assert m.sum()==0

def test_features_match_hand_computed_distribution():
    p=np.array([[0.,.5],[.5,0.]])
    f=glcm_features(p)
    assert f["contrast"]==pytest.approx(1.)
    assert f["dissimilarity"]==pytest.approx(1.)
    assert f["homogeneity"]==pytest.approx(.5)
    assert f["ASM"]==pytest.approx(.5)
    assert f["energy"]==pytest.approx(np.sqrt(.5))
    assert f["correlation"]==pytest.approx(-1.)

def test_empty_and_bad_inputs():
    with pytest.raises(ValueError): glcm(np.ones((2,2)),offsets=((0,0),))
    with pytest.raises(ValueError): glcm_features(np.zeros((2,2)))
    with pytest.raises(ValueError): quantize(np.ones((2,2)),levels=1)
