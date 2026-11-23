import math
import pytest
from online import bocpd_normal_mean


def test_bocpd_returns_valid_probabilities_and_run_lengths():
    cp, run = bocpd_normal_mean([0, 0.1, -0.1, 3, 3.1, 2.9],
                                observation_variance=0.1, hazard=0.1)
    assert len(cp) == len(run) == 6
    assert all(0 <= p <= 1 for p in cp)
    assert all(r >= 0 for r in run)


def test_bocpd_detects_evidence_for_a_new_mean_regime():
    cp, run = bocpd_normal_mean([0.0] * 20 + [4.0] * 8,
                                observation_variance=0.05, hazard=0.05)
    assert max(cp[20:]) > max(cp[:20])


def test_bocpd_run_length_cap_is_respected():
    cp, run = bocpd_normal_mean([0.0] * 20, observation_variance=1.0,
                                max_run_length=4)
    assert max(run) <= 4


@pytest.mark.parametrize("kwargs", [
    {"observation_variance": 0}, {"observation_variance": 1, "hazard": 1},
    {"observation_variance": 1, "prior_kappa": 0},
    {"observation_variance": 1, "max_run_length": 0},
])
def test_bocpd_rejects_invalid_parameters(kwargs):
    with pytest.raises(ValueError):
        bocpd_normal_mean([1, 2], **kwargs)


def test_bocpd_rejects_nonfinite_observations():
    with pytest.raises(ValueError):
        bocpd_normal_mean([1, float("nan")], observation_variance=1)
