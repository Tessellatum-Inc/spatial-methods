import numpy as np
import pytest
from hawkes import simulate_exponential_hawkes, exponential_hawkes_log_likelihood

def test_simulator_is_reproducible_sorted_and_within_window():
    a=simulate_exponential_hawkes(.8,.3,1.2,100,seed=4)
    b=simulate_exponential_hawkes(.8,.3,1.2,100,seed=4)
    np.testing.assert_array_equal(a,b)
    assert np.all(np.diff(a)>=0)
    assert np.all((a>=0)&(a<=100))

def test_log_likelihood_matches_poisson_when_excitation_is_zero():
    events=np.array([1.,2.,4.])
    ll=exponential_hawkes_log_likelihood(events,2.,0.,1.,5.)
    assert ll==pytest.approx(3*np.log(2)-10)

def test_likelihood_increases_for_a_close_pair_under_excitation():
    events=np.array([1.,1.05,4.])
    base=exponential_hawkes_log_likelihood(events,1.,0.,1.,5.)
    excited=exponential_hawkes_log_likelihood(events,1.,.7,1.,5.)
    assert excited>base

def test_simulation_mean_rate_exceeds_baseline_with_excitation():
    events=simulate_exponential_hawkes(1.,.5,1.,3000,seed=9)
    rate=len(events)/3000
    assert rate==pytest.approx(1/(1-.5),rel=.18)

def test_hawkes_methods_reject_unstable_or_invalid_inputs():
    with pytest.raises(ValueError,match="decay"):
        simulate_exponential_hawkes(1.,1.,.5,10)
    with pytest.raises(ValueError,match="nondecreasing"):
        exponential_hawkes_log_likelihood([2.,1.],1.,.2,1.,3.)
    with pytest.raises(ValueError,match="contain"):
        exponential_hawkes_log_likelihood([4.],1.,.2,1.,3.)
