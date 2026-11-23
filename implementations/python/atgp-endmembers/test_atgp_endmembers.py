import numpy as np
from atgp_endmembers import atgp

def test_extracts_distinct_observed_signatures():
    x=np.random.default_rng(4).random((10,12,5))
    out=atgp(x,4)
    assert out["endmembers"].shape==(5,4)
    assert len(set(out["pixel_indices"]))==4

def test_mask_excludes_rows():
    x=np.random.default_rng(2).random((7,8,4)); mask=np.ones((7,8),bool); mask[:2]=False
    out=atgp(x,3,mask=mask)
    assert np.all(out["pixel_indices"]>=16)
