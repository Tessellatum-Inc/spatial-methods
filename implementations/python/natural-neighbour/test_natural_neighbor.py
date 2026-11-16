import numpy as np
import pytest
from natural_neighbor import natural_neighbor


def test_affine_reproduction():
    p = np.array([[0.,0.],[4.,0.],[4.,3.],[0.,3.],[2.,1.],[1.,2.]])
    z = 2.5*p[:,0] - 1.25*p[:,1] + 7
    q = np.array([[1.2,.8],[2.5,1.7],[.8,1.8]])
    expected = 2.5*q[:,0] - 1.25*q[:,1] + 7
    np.testing.assert_allclose(natural_neighbor(p,z,q), expected, atol=1e-9)


def test_exact_sample_and_constant_reproduction():
    p = np.array([[0.,0.],[3.,0.],[3.,3.],[0.,3.],[1.,1.]])
    np.testing.assert_array_equal(natural_neighbor(p,np.arange(5.),[[3.,0.]]),[1.])
    np.testing.assert_allclose(natural_neighbor(p,np.full(5,8.25),[[1.2,1.4],[2.,1.]]),8.25)


def test_multiple_value_columns():
    p = np.array([[0.,0.],[4.,0.],[4.,4.],[0.,4.],[2.,2.]])
    z = np.column_stack([p[:,0]+p[:,1],3*p[:,0]-p[:,1]])
    np.testing.assert_allclose(natural_neighbor(p,z,[[1.,2.]]),[[3.,1.]],atol=1e-9)


@pytest.mark.parametrize("q", [[-1.,1.],[0.,1.],[5.,5.]])
def test_rejects_outside_or_boundary(q):
    p = np.array([[0.,0.],[4.,0.],[4.,4.],[0.,4.]])
    with pytest.raises(ValueError,match="strictly inside"):
        natural_neighbor(p,np.arange(4.),[q])


def test_rejects_invalid_sites_and_nonfinite_values():
    with pytest.raises(ValueError,match="duplicate"):
        natural_neighbor([[0,0],[1,0],[0,1],[0,0]],[1,2,3,4],[[.2,.2]])
    with pytest.raises(ValueError,match="two-dimensional"):
        natural_neighbor([[0,0],[1,0],[2,0]],[1,2,3],[[.5,0]])
    with pytest.raises(ValueError,match="finite"):
        natural_neighbor([[0,0],[1,0],[0,1]],[1,np.nan,3],[[.2,.2]])
