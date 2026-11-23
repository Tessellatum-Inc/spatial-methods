import numpy as np
import pytest
from spectral_matched_filter import spectral_matched_filter

def test_target_injection_scores_high():
    rng=np.random.default_rng(14)
    x=rng.normal(size=(30,30,4))
    target=np.array([4.,-3.,2.,5.])
    x[12,12]=target
    out=spectral_matched_filter(x,target)
    assert out["scores"][12,12]>np.percentile(out["scores"],99)

def test_masked_background_and_weight_shape():
    x=np.random.default_rng(3).normal(size=(8,9,3))
    mask=np.ones((8,9),bool); mask[0,:]=False
    out=spectral_matched_filter(x,np.array([2.,1.,3.]),background_mask=mask)
    assert out["weights"].shape==(3,)
    assert out["scores"].shape==(8,9)

def test_reject_target_equal_background():
    x=np.ones((4,5,2))
    with pytest.raises(ValueError):
        spectral_matched_filter(x,np.ones(2))
