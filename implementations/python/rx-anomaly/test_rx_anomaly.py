import numpy as np
import pytest
from rx_anomaly import rx_detector

def test_injected_outlier_scores_high():
    rng=np.random.default_rng(8)
    x=rng.normal(size=(30,30,3))
    x[15,15]=[9,9,9]
    out=rx_detector(x,regularization=1e-5)
    assert out["scores"][15,15]>np.nanpercentile(out["scores"],99)

def test_masked_scores_nan():
    x=np.random.default_rng(2).normal(size=(8,9,2))
    mask=np.ones((8,9),bool); mask[0,0]=False
    result=rx_detector(x,mask=mask)
    assert np.isnan(result["scores"][0,0])
    assert np.isfinite(result["scores"][mask]).all()

def test_reject_indefinite_covariance():
    x=np.random.default_rng(3).normal(size=(5,6,2))
    with pytest.raises(ValueError): rx_detector(x,covariance=np.array([[1,2],[2,1]]))
