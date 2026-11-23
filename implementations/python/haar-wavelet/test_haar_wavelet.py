import numpy as np
import pytest
from haar_wavelet import haar2d,inverse_haar2d

def test_exact_multilevel_reconstruction():
    x=np.random.default_rng(9).normal(size=(16,24))
    c=haar2d(x,levels=3)
    assert np.allclose(inverse_haar2d(c),x,atol=1e-12)

def test_constant_has_only_approximation():
    x=np.full((8,8),4.)
    c=haar2d(x,levels=2)
    assert np.allclose(c["approximation"],16.)
    for triple in c["details"]:
        for d in triple: assert np.allclose(d,0)

def test_reject_odd_dimensions():
    with pytest.raises(ValueError): haar2d(np.ones((7,8)))
