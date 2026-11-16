import numpy as np
import pytest
from security_game import minimax_patrol_allocation


def test_equal_value_sites_receive_equal_fractional_coverage():
    result = minimax_patrol_allocation([10.,10.,10.], [1.,1.,1.], 1.5)
    np.testing.assert_allclose(result["coverage"], [.5,.5,.5], atol=1e-8)
    np.testing.assert_allclose(result["attacker_payoffs"], [5.,5.,5.], atol=1e-8)
    assert result["resources_used"] == pytest.approx(1.5)


def test_heterogeneous_sites_equalize_attack_payoffs_when_partially_covered():
    result = minimax_patrol_allocation([20.,10.,5.], [1.,1.,1.], 1.5)
    active = (result["coverage"] > 1e-7) & (result["coverage"] < 1-1e-7)
    assert active.sum() >= 2
    assert np.ptp(result["attacker_payoffs"][active]) < 1e-7
    assert result["resources_used"] == pytest.approx(1.5, abs=1e-7)


def test_detection_effectiveness_limits_full_coverage_payoff():
    result = minimax_patrol_allocation([10.,8.], [.5,1.], 2.)
    np.testing.assert_allclose(result["coverage"], [1.,1.])
    np.testing.assert_allclose(result["attacker_payoffs"], [5.,0.])


def test_zero_resources_leave_payoffs_uncovered():
    result = minimax_patrol_allocation([4.,7.], [1.,.5], 0.)
    np.testing.assert_array_equal(result["coverage"], [0.,0.])
    assert result["worst_case_payoff"] == 7.


def test_security_game_validates_inputs():
    with pytest.raises(ValueError, match="matching"):
        minimax_patrol_allocation([1.,2.], [1.], 1.)
    with pytest.raises(ValueError, match="effectiveness"):
        minimax_patrol_allocation([1.], [0.], 1.)
    with pytest.raises(ValueError, match="resources"):
        minimax_patrol_allocation([1.], [1.], 2.)
