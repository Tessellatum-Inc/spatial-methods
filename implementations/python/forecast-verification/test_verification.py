import pytest
from verification import contingency_scores, brier_score, roc_auc, fractions_skill_score

def test_contingency_scores_known_counts():
    result = contingency_scores([1, 1, 0, 0], [1, 0, 1, 0], 0.5)
    assert (result["hits"], result["misses"], result["false_alarms"], result["correct_negatives"]) == (1, 1, 1, 1)
    assert result["pod"] == pytest.approx(0.5)
    assert result["far"] == pytest.approx(0.5)
    assert result["csi"] == pytest.approx(1/3)
    assert result["ets"] == pytest.approx(0.0)

def test_brier_score_and_validation():
    assert brier_score([0.1, 0.8], [0, 1]) == pytest.approx(0.025)
    with pytest.raises(ValueError):
        brier_score([1.2], [1])

def test_auc_handles_ties_and_perfect_ordering():
    assert roc_auc([0.1, 0.4, 0.35, 0.8], [0, 0, 1, 1]) == pytest.approx(0.75)
    assert roc_auc([0.2, 0.2, 0.2, 0.2], [0, 1, 0, 1]) == pytest.approx(0.5)
    with pytest.raises(ValueError):
        roc_auc([1, 2], [1, 1])

def test_fss_perfect_and_displaced_fields():
    observed = [[0, 1, 0], [0, 1, 0], [0, 0, 0]]
    assert fractions_skill_score(observed, observed, 0.5, radius=1) == pytest.approx(1.0)
    displaced = [[0, 0, 1], [0, 0, 1], [0, 0, 0]]
    assert fractions_skill_score(displaced, observed, 0.5, radius=1) < 1.0
    assert fractions_skill_score(observed, observed, 0.5, radius=0) == pytest.approx(1.0)

def test_fss_validation_and_empty_event_convention():
    with pytest.raises(ValueError):
        fractions_skill_score([[1]], [[1, 2]], 0.5)
    assert fractions_skill_score([[0, 0]], [[0, 0]], 0.5) == 1.0

from verification import crps_ensemble, rank_histogram

def test_crps_ensemble_matches_absolute_error_for_single_member():
    assert crps_ensemble([2.0], 5.0) == pytest.approx(3.0)

def test_crps_ensemble_perfect_symmetric_ensemble():
    assert crps_ensemble([0.0, 2.0], 1.0) == pytest.approx(0.5)

def test_rank_histogram_ties_share_mass_across_spanned_ranks():
    counts = rank_histogram([[1, 2, 3], [2, 2, 4]], [0, 2])
    assert counts == pytest.approx([4/3, 1/3, 1/3, 0.0])
    assert sum(counts) == pytest.approx(2.0)

def test_rank_histogram_requires_equal_ensemble_sizes():
    with pytest.raises(ValueError):
        rank_histogram([[1, 2], [1]], [1, 2])
