import numpy as np
import pytest
from erosion import rusle_ls_factor, rusle_soil_loss, usle_soil_loss


def test_rusle_ls_factor_flat_and_sloping_cases():
    flat = rusle_ls_factor(0, 22.13)
    assert flat == pytest.approx(0.03)
    steep = rusle_ls_factor(15, 100)
    assert steep > 1


def test_rusle_ls_factor_broadcast_and_explicit_m():
    result = rusle_ls_factor([[5], [10]], [22.13, 44.26], m=.5)
    assert result.shape == (2, 2)
    assert np.all(result[:, 1] > result[:, 0])


def test_rusle_soil_loss_factor_product_and_broadcast():
    result = rusle_soil_loss([100, 200], .3, 2, .5, .8)
    np.testing.assert_allclose(result, [24, 48])
    np.testing.assert_allclose(usle_soil_loss(100, .3, 2, .5, .8), 24)


@pytest.mark.parametrize("args", [
    (-1, .2, 1, .5, .5), (1, np.nan, 1, .5, .5),
    (1, .2, 1, -0.1, .5),
])
def test_soil_loss_rejects_invalid_factors(args):
    with pytest.raises(ValueError):
        rusle_soil_loss(*args)


def test_ls_rejects_invalid_slope_length_and_exponent():
    with pytest.raises(ValueError):
        rusle_ls_factor(90, 10)
    with pytest.raises(ValueError):
        rusle_ls_factor(10, 0)
    with pytest.raises(ValueError):
        rusle_ls_factor(10, 20, m=2)
