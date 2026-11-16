import numpy as np
import pytest
from insar import remove_orbital_ramp, sbas_network_inversion


def test_orbital_plane_is_removed_from_unwrapped_phase():
    rows, cols = 12, 15
    y, x = np.indices((rows, cols), dtype=float)
    phase = 2. + .4*x - .7*y
    result = remove_orbital_ramp(phase, order=1)
    np.testing.assert_allclose(result["corrected"], 0., atol=1e-12)
    np.testing.assert_allclose(result["ramp"], phase, atol=1e-12)


def test_quadratic_ramp_and_masked_pixels():
    rows, cols = 10, 11
    y, x = np.indices((rows, cols), dtype=float)
    xn, yn = 2*x/(cols-1)-1, 2*y/(rows-1)-1
    phase = 1. + xn + 2*yn + .3*xn**2 + .2*xn*yn - .1*yn**2
    mask = np.ones(phase.shape, dtype=bool)
    mask[:2,:2] = False
    result = remove_orbital_ramp(phase, valid_mask=mask, order=2)
    np.testing.assert_allclose(result["corrected"][mask], 0., atol=1e-12)
    assert np.isnan(result["corrected"][~mask]).all()


def test_sbas_network_inversion_recovers_relative_acquisition_displacements():
    displacement = np.array([0., 2., 5., 4.])
    pairs = np.array([[0,1],[1,2],[2,3],[0,2],[1,3]], dtype=int)
    interferograms = displacement[pairs[:,1]] - displacement[pairs[:,0]]
    result = sbas_network_inversion(interferograms[:,None,None], pairs,
                                    n_dates=4, reference_date=0)
    np.testing.assert_allclose(result["displacement"][:,0,0], displacement, atol=1e-12)
    assert result["rmse"][0,0] == pytest.approx(0.)


def test_sbas_weighted_inversion_and_rank_deficient_network():
    displacement = np.array([0., 1., 3.])
    pairs = np.array([[0,1],[1,2],[0,2]], dtype=int)
    ifgs = displacement[pairs[:,1]] - displacement[pairs[:,0]]
    result = sbas_network_inversion(ifgs, pairs, n_dates=3,
                                    weights=[1.,2.,1.])
    np.testing.assert_allclose(result["displacement"], displacement, atol=1e-12)
    bad = sbas_network_inversion([1.,2.], [[0,1],[2,3]], n_dates=4)
    assert np.isnan(bad["displacement"][1:]).all()
    assert bad["design_rank"] == 2


def test_insar_methods_validate_pairs_masks_and_shapes():
    with pytest.raises(ValueError, match="not enough"):
        remove_orbital_ramp(np.ones((2,2)), order=2)
    with pytest.raises(ValueError, match="pairs"):
        sbas_network_inversion(np.ones((2,2)), [[0,1]], n_dates=2)
    with pytest.raises(ValueError, match="weights"):
        sbas_network_inversion([1.,2.], [[0,1],[1,2]], n_dates=3, weights=[1.,-1.])
