import numpy as np
import pytest
from space_time_scan import space_time_poisson_scan,monte_carlo_space_time_scan


def fixture():
    xy=np.array([[0.,0.],[1.,0.],[10.,0.],[11.,0.]])
    exposure=np.full((4,4),100.)
    cases=np.ones((4,4),dtype=int)
    cases[2:4,0:2]=20
    return xy,cases,exposure


def test_space_time_scan_detects_cylindrical_spatiotemporal_cluster():
    xy,cases,exposure=fixture()
    result=space_time_poisson_scan(xy,cases,exposure,max_exposure_fraction=.5,
                                   min_cases=2,min_time_bins=2,max_time_bins=2)
    assert result["log_likelihood_ratio"]>0
    assert set(result["member_indices"])=={0,1}
    assert (result["time_start"],result["time_end"])==(2,4)
    assert result["cases_inside"]==80
    assert result["expected_cases_inside"]==pytest.approx(23.)


def test_space_time_scan_respects_time_window_bounds_and_exposure_offsets():
    xy,cases,exposure=fixture()
    result=space_time_poisson_scan(xy,cases,exposure,max_exposure_fraction=.5,
                                   min_time_bins=1,max_time_bins=1)
    assert result["time_end"]-result["time_start"]==1
    # A high raw count in a high-exposure cell need not be a high-rate cylinder.
    balanced=np.ones((3,4),dtype=int)
    pop=np.array([[10,10,10,10],[10,10,10,1000],[10,10,10,10]],float)
    balanced[1,3]=20
    scan=space_time_poisson_scan(xy,balanced,pop,max_exposure_fraction=.5)
    assert scan["log_likelihood_ratio"]>=0


def test_space_time_monte_carlo_is_reproducible_and_plus_one_corrected():
    xy,cases,exposure=fixture()
    a=monte_carlo_space_time_scan(xy,cases,exposure,n_simulations=39,rng=17,
                                  max_exposure_fraction=.5,min_time_bins=2,max_time_bins=2)
    b=monte_carlo_space_time_scan(xy,cases,exposure,n_simulations=39,rng=17,
                                  max_exposure_fraction=.5,min_time_bins=2,max_time_bins=2)
    assert a["p_value"]==b["p_value"]
    np.testing.assert_array_equal(a["simulated_maxima"],b["simulated_maxima"])
    assert 1/40<=a["p_value"]<=1


@pytest.mark.parametrize("cases,pop,kwargs",[
    (np.ones((4,4))*1.5,np.ones((4,4)),{}),
    (np.zeros((4,4)),np.ones((4,4)),{}),
    (np.ones((4,3)),np.ones((4,4)),{}),
    (np.ones((4,4)),np.zeros((4,4)),{}),
    (np.ones((4,4)),np.ones((4,4)),{"min_time_bins":0}),
    (np.ones((4,4)),np.ones((4,4)),{"max_time_bins":5}),
    (np.ones((4,4)),np.ones((4,4)),{"max_exposure_fraction":0}),
])
def test_space_time_scan_rejects_invalid_inputs(cases,pop,kwargs):
    with pytest.raises(ValueError):
        space_time_poisson_scan(np.array([[0.,0.],[1.,0.],[2.,0.],[3.,0.]]),cases,pop,**kwargs)


def test_space_time_scan_rejects_invalid_monte_carlo_controls():
    xy,cases,pop=fixture()
    with pytest.raises(ValueError):
        monte_carlo_space_time_scan(xy,cases,pop,n_simulations=0)
