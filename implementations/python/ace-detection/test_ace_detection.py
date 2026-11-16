import numpy as np
import pytest
from ace_detection import ace_detect

def test_ace_bounded_and_target_response():
    rng=np.random.default_rng(19); x=rng.normal(size=(25,25,4)); target=np.array([3.,-2.,4.,1.])
    x[10,10]=target
    out=ace_detect(x,target)
    assert out["scores"].min()>=0 and out["scores"].max()<=1
    assert out["scores"][10,10]>np.percentile(out["scores"],99)

def test_rejects_degenerate_target():
    with pytest.raises(ValueError): ace_detect(np.ones((4,5,2)),np.ones(2))
