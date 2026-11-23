import itertools

import numpy as np
import pytest

from mutual_information_sensor_selection import gaussian_sensor_mutual_information


TARGETS = np.array([[0., 0.], [1., 0.], [0., 1.]])
CANDIDATES = np.array([[0., 0.], [1., 1.], [3., 0.], [0., 3.]])


def test_single_target_single_candidate_matches_closed_form():
    result = gaussian_sensor_mutual_information(
        [[0, 0]], [[0, 0], [2, 0]], max_sensors=1, noise_variance=0.5
    )
    assert result["selected_indices"] == (0,)
    assert result["mutual_information"] == pytest.approx(0.5 * np.log(1 + 1 / .5))


def test_greedy_step_matches_independent_exhaustive_marginal_oracle():
    result = gaussian_sensor_mutual_information(
        TARGETS, CANDIDATES, max_sensors=3, length_scale=1.3,
        noise_variance=[.1, .2, .3, .4]
    )
    chosen = []
    previous = 0.0
    for selected, gain in zip(result["selected_indices"], result["marginal_gains"]):
        alternatives = []
        remaining = [candidate for candidate in range(len(CANDIDATES)) if candidate not in chosen]
        for candidate in remaining:
            # Independent subset objective computed directly from Gaussian blocks.
            subset = chosen + [candidate]
            kt = np.exp(-.5 * (np.linalg.norm(TARGETS[:, None]-TARGETS[None, :], axis=2)/1.3)**2)
            kc = np.exp(-.5 * (np.linalg.norm(CANDIDATES[:, None]-CANDIDATES[None, :], axis=2)/1.3)**2)
            kx = np.exp(-.5 * (np.linalg.norm(TARGETS[:, None]-CANDIDATES[None, :], axis=2)/1.3)**2)
            ids = np.asarray(subset)
            conditional = kt - kx[:, ids] @ np.linalg.solve(kc[np.ix_(ids, ids)] + np.diag(np.array([.1,.2,.3,.4])[ids]), kx[:, ids].T)
            sign, logdet = np.linalg.slogdet(conditional)
            assert sign > 0
            sign0, logdet0 = np.linalg.slogdet(kt)
            alternatives.append(.5*(logdet0-logdet)-previous)
        best_position = int(np.argmax(alternatives))
        assert gain == pytest.approx(max(alternatives), abs=1e-10)
        assert selected == remaining[best_position]
        chosen.append(selected)
        previous += gain


def test_selection_is_deterministic_and_gains_are_nonnegative():
    a = gaussian_sensor_mutual_information(TARGETS, CANDIDATES, max_sensors=4, length_scale=2)
    b = gaussian_sensor_mutual_information(TARGETS, CANDIDATES, max_sensors=4, length_scale=2)
    assert a["selected_indices"] == b["selected_indices"]
    assert a["marginal_gains"] == pytest.approx(b["marginal_gains"])
    assert all(gain >= 0 for gain in a["marginal_gains"])
    assert np.all(np.linalg.eigvalsh(a["conditional_covariance"]) > 0)


def test_zero_budget_returns_prior_information_and_covariance():
    result = gaussian_sensor_mutual_information(TARGETS, CANDIDATES, max_sensors=0)
    assert result["selected_indices"] == ()
    assert result["mutual_information"] == 0
    assert result["marginal_gains"] == ()
    assert result["conditional_covariance"] == pytest.approx(
        np.exp(-.5 * np.linalg.norm(TARGETS[:, None]-TARGETS[None, :], axis=2)**2)
    )


@pytest.mark.parametrize("kwargs", [
    {"max_sensors": -1}, {"max_sensors": 5}, {"max_sensors": True},
    {"length_scale": 0}, {"length_scale": float("inf")},
    {"noise_variance": 0}, {"noise_variance": [1, 2]},
    {"kernel": "matern"},
])
def test_invalid_controls_are_rejected(kwargs):
    with pytest.raises(ValueError):
        gaussian_sensor_mutual_information(TARGETS, CANDIDATES, **kwargs)


def test_duplicate_target_locations_are_rejected_as_singular_covariance():
    with pytest.raises(ValueError):
        gaussian_sensor_mutual_information([[0, 0], [0, 0]], CANDIDATES, max_sensors=1)


def test_empty_or_nonfinite_coordinates_are_rejected():
    with pytest.raises(ValueError):
        gaussian_sensor_mutual_information([], CANDIDATES, max_sensors=1)
    with pytest.raises(ValueError):
        gaussian_sensor_mutual_information(TARGETS, [[0, float("nan")]], max_sensors=1)

def test_variance_design_single_target_matches_closed_form():
    from mutual_information_sensor_selection import greedy_kriging_variance_design
    result = greedy_kriging_variance_design([[0, 0]], [[0, 0], [2, 0]],
                                            max_sensors=1, noise_variance=.5)
    assert result["selected_indices"] == (0,)
    assert result["posterior_variance_trace"] == pytest.approx(1 / 3)
    assert result["variance_reductions"] == pytest.approx([2 / 3])


def test_variance_design_greedy_steps_match_independent_trace_oracle():
    from mutual_information_sensor_selection import greedy_kriging_variance_design
    result = greedy_kriging_variance_design(TARGETS, CANDIDATES, max_sensors=3,
                                            length_scale=1.3,
                                            noise_variance=[.1, .2, .3, .4])
    kt = np.exp(-.5 * (np.linalg.norm(TARGETS[:, None]-TARGETS[None, :], axis=2)/1.3)**2)
    kc = np.exp(-.5 * (np.linalg.norm(CANDIDATES[:, None]-CANDIDATES[None, :], axis=2)/1.3)**2)
    kx = np.exp(-.5 * (np.linalg.norm(TARGETS[:, None]-CANDIDATES[None, :], axis=2)/1.3)**2)
    noise = np.array([.1, .2, .3, .4])
    chosen, current = [], float(np.trace(kt))
    for selected, reduction in zip(result["selected_indices"], result["variance_reductions"]):
        remaining, alternatives = [], []
        for candidate in range(len(CANDIDATES)):
            if candidate in chosen:
                continue
            remaining.append(candidate)
            ids = np.asarray(chosen + [candidate])
            conditional = kt - kx[:, ids] @ np.linalg.solve(
                kc[np.ix_(ids, ids)] + np.diag(noise[ids]), kx[:, ids].T
            )
            alternatives.append(current - float(np.trace(conditional)))
        best = int(np.argmax(alternatives))
        assert selected == remaining[best]
        assert reduction == pytest.approx(alternatives[best])
        chosen.append(selected)
        current -= reduction


def test_variance_design_zero_budget_and_invalid_noise():
    from mutual_information_sensor_selection import greedy_kriging_variance_design
    result = greedy_kriging_variance_design(TARGETS, CANDIDATES, max_sensors=0)
    assert result["selected_indices"] == ()
    assert result["posterior_variance_trace"] == pytest.approx(3.0)
    with pytest.raises(ValueError):
        greedy_kriging_variance_design(TARGETS, CANDIDATES, max_sensors=1,
                                       noise_variance=[True, False, True, False])
