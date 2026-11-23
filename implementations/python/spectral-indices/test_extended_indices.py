import numpy as np
import pytest
from spectral_indices import ndre, ndmi, lswi, ndwi, mndwi, ndbi, nbr, ndsi, savi, evi, dnbr


def test_ratio_indices_match_independent_formulas():
    nir, red, green, swir1, swir2, red_edge = 0.6, 0.2, 0.3, 0.1, 0.05, 0.4
    assert ndre(nir, red_edge) == pytest.approx((nir-red_edge)/(nir+red_edge))
    assert ndmi(nir, swir1) == pytest.approx((nir-swir1)/(nir+swir1))
    assert lswi(nir, swir1) == pytest.approx((nir-swir1)/(nir+swir1))
    assert ndwi(green, nir) == pytest.approx((green-nir)/(green+nir))
    assert mndwi(green, swir1) == pytest.approx((green-swir1)/(green+swir1))
    assert ndbi(swir1, nir) == pytest.approx((swir1-nir)/(swir1+nir))
    assert nbr(nir, swir2) == pytest.approx((nir-swir2)/(nir+swir2))
    assert ndsi(green, swir1) == pytest.approx((green-swir1)/(green+swir1))


def test_savi_and_evi_match_published_forms():
    nir, red, blue = np.array([0.6]), np.array([0.2]), np.array([0.1])
    assert savi(nir, red)[0] == pytest.approx(1.5 * (0.4) / 1.3)
    assert evi(nir, red, blue)[0] == pytest.approx(2.5 * 0.4 / (0.6 + 1.2 - 0.75 + 1))


def test_ratio_indices_propagate_zero_denominator_and_mask():
    a = np.array([0.4, 0.2, 0.6, np.nan])
    b = np.array([0.2, -0.2, 0.1, 0.1])
    mask = np.array([True, True, False, True])
    result = ndmi(a, b, valid_mask=mask)
    assert np.isfinite(result[0])
    assert np.isnan(result[1:]).all()


def test_multiband_indices_validate_shapes_and_masks():
    with pytest.raises(ValueError):
        evi(np.ones(2), np.ones(3), np.ones(2))
    with pytest.raises(TypeError):
        savi(np.ones(2), np.ones(2), valid_mask=np.ones(2, dtype=int))
    with pytest.raises(ValueError):
        savi(np.ones(2), np.ones(2), soil_factor=-1)


def test_dnbr_sign_and_nonfinite_propagation():
    pre = np.array([0.8, 0.5, np.nan])
    post = np.array([0.2, 0.6, 0.1])
    np.testing.assert_allclose(dnbr(pre, post)[:2], [0.6, -0.1])
    assert np.isnan(dnbr(pre, post)[2])


def test_awei_variants_match_reference_equations_and_masking():
    from spectral_indices import awei_sh, awei_nsh
    blue, green, nir, swir1, swir2 = 0.1, 0.3, 0.5, 0.2, 0.05
    expected_sh = blue + 2.5*green - 1.5*(nir+swir1) - 0.25*swir2
    expected_nsh = 4*(green-swir1) - (0.25*nir + 2.75*swir2)
    assert awei_sh(blue, green, nir, swir1, swir2) == pytest.approx(expected_sh)
    assert awei_nsh(green, nir, swir1, swir2) == pytest.approx(expected_nsh)
    masked = awei_sh(np.array([blue, blue]), np.array([green, green]),
                     np.array([nir, nir]), np.array([swir1, swir1]),
                     np.array([swir2, swir2]), valid_mask=np.array([True, False]))
    assert np.isfinite(masked[0]) and np.isnan(masked[1])
