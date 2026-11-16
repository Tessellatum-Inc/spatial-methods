import numpy as np
import pytest
from sar import radiometric_calibrate, multilook_intensity


def test_sigma0_calibration_matches_complex_intensity_and_noise_subtraction():
    dn = np.array([[1+1j, 2+0j]])
    result = radiometric_calibrate(dn, 2., noise_power=1.)
    np.testing.assert_allclose(result, [[2.,6.]])


def test_beta0_and_gamma0_use_declared_incidence_geometry():
    sigma = radiometric_calibrate(np.array([[2.]]), 3.)
    angle = np.array([[np.pi/4]])
    beta = radiometric_calibrate(np.array([[2.]]), 3., output="beta0", incidence_angle=angle)
    gamma = radiometric_calibrate(np.array([[2.]]), 3., output="gamma0", incidence_angle=angle)
    assert beta[0,0] == pytest.approx(sigma[0,0]/np.sin(np.pi/4))
    assert gamma[0,0] == pytest.approx(sigma[0,0]/np.cos(np.pi/4))


def test_multilooking_matches_direct_block_means_and_crops_edges():
    image = np.arange(1., 21.).reshape(4,5)
    result = multilook_intensity(image, looks=(2,2))
    np.testing.assert_allclose(result["intensity"], [[4.,6.],[14.,16.]])
    assert result["cropped_shape"] == (4,4)
    np.testing.assert_array_equal(result["valid_looks"], 4)


def test_multilooking_nodata_policies_are_explicit():
    image = np.array([[1.,np.nan],[3.,4.]])
    omit = multilook_intensity(image, looks=(2,2), nodata_policy="omit")
    propagate = multilook_intensity(image, looks=(2,2), nodata_policy="propagate")
    assert omit["intensity"][0,0] == pytest.approx(8/3)
    assert np.isnan(propagate["intensity"][0,0])


def test_sar_methods_validate_controls():
    with pytest.raises(ValueError, match="incidence_angle"):
        radiometric_calibrate([[1.]], 1., output="beta0")
    with pytest.raises(ValueError, match="positive"):
        radiometric_calibrate([[1.]], 0.)
    with pytest.raises(ValueError, match="looks"):
        multilook_intensity(np.ones((2,2)), looks=(0,2))
