import numpy as np
import pytest
from cem_detection import cem_detect

def test_unit_response_and_target_pixel():
    rng=np.random.default_rng(12); x=rng.normal(size=(20,20,3)); target=np.array([2.,-1.,3.])
    x[4,5]=target
    out=cem_detect(x,target)
    assert np.isclose(target@out["weights"],1.)
    assert out["scores"][4,5]>np.percentile(out["scores"],99)

def test_rejects_indefinite_matrix():
    x=np.ones((3,3,2))
    with pytest.raises(ValueError): cem_detect(x,np.array([1.,0.]),correlation=np.array([[1.,2.],[2.,1.]]))
