import numpy as np
import pytest
from pca_transform import fit_pca, transform_pca, tasseled_cap_transform

def test_projection_matches_covariance_eigenpairs():
    x=np.array([[1.,2.],[2.,1.],[3.,4.],[4.,3.],[5.,6.]])
    m=fit_pca(x)
    cov=np.cov(x,rowvar=False)
    vals=np.linalg.eigvalsh(cov)[::-1]
    np.testing.assert_allclose(m["eigenvalues"], vals, atol=1e-12)
    y=transform_pca(x,m)
    np.testing.assert_allclose(np.cov(y,rowvar=False), np.diag(vals), atol=1e-12)

def test_mask_and_nonfinite_rows_excluded():
    x=np.array([[0.,0.],[1.,2.],[2.,1.],[np.nan,3.],[100.,100.]])
    m=fit_pca(x,mask=np.array([1,1,1,1,0],dtype=bool))
    assert m["valid_rows"].tolist()==[True,True,True,False,False]
    np.testing.assert_allclose(m["mean"],[1.,1.])

def test_standardization_uses_sample_sd():
    x=np.array([[1.,10.],[2.,20.],[3.,30.]])
    m=fit_pca(x,standardize=True)
    np.testing.assert_allclose(m["scale"],np.std(x,axis=0,ddof=1))
    np.testing.assert_allclose(m["eigenvalues"].sum(),2.,atol=1e-12)

@pytest.mark.parametrize("x", [np.ones((4,2)), np.array([[1.,2.]])])
def test_degenerate_or_too_small_data_rejected(x):
    if x.shape[0]==1:
        with pytest.raises(ValueError): fit_pca(x)
    else:
        with pytest.raises(ValueError): fit_pca(x,standardize=True)

def test_invalid_mask_and_component_count():
    x=np.arange(12.).reshape(6,2)
    with pytest.raises(ValueError): fit_pca(x,mask=[True])
    with pytest.raises(ValueError): fit_pca(x,n_components=3)


def test_tasseled_cap_transform_matches_independent_matrix_product():
    data = np.array([[1., 2., 3.], [4., 5., 6.]])
    coefficients = np.array([[1., 0.], [0., 2.], [-1., 1.]])
    offset = np.array([0.5, 1.0, 2.0])
    expected = np.array([[-0.5, 3.0], [-0.5, 12.0]])
    np.testing.assert_allclose(tasseled_cap_transform(data, coefficients, offset=offset), expected)


def test_tasseled_cap_validates_sensor_matrix_and_band_contract():
    with pytest.raises(ValueError):
        tasseled_cap_transform(np.ones((3, 4)), np.ones((3, 2)))
    with pytest.raises(ValueError):
        tasseled_cap_transform(np.ones((3, 2)), np.ones((2, 2)), offset=[0.0])
