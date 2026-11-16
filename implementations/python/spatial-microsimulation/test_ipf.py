import numpy as np
import pytest
from ipf import iterative_proportional_fit


def test_ipf_matches_known_row_and_column_margins():
    seed = [[10, 20], [30, 40]]
    result = iterative_proportional_fit(seed, {0: [40, 60], 1: [50, 50]})
    fitted = np.asarray(result["fitted"])
    assert result["converged"]
    assert fitted.sum(axis=1) == pytest.approx([40, 60])
    assert fitted.sum(axis=0) == pytest.approx([50, 50])


def test_ipf_preserves_structural_zeros():
    result = iterative_proportional_fit([[1, 0], [2, 3]], {0: [4, 6], 1: [5, 5]})
    assert result["converged"]
    assert result["fitted"][0][1] == 0


def test_ipf_handles_zero_margins():
    result = iterative_proportional_fit([[1, 2], [3, 4]], {0: [0, 7], 1: [3, 4]})
    assert result["converged"]
    assert result["fitted"][0] == pytest.approx([0, 0])
    assert result["fitted"][1] == pytest.approx([3, 4])


def test_ipf_reports_nonconvergence_at_iteration_limit():
    result = iterative_proportional_fit([[1, 2], [3, 4]], {0: [40, 60], 1: [50, 50]},
                                        max_iterations=1, tolerance=1e-15)
    assert result["iterations"] == 1
    assert isinstance(result["converged"], bool)


def test_ipf_zero_grand_total_returns_zero_table():
    result = iterative_proportional_fit([[1, 2], [3, 4]], {0: [0, 0], 1: [0, 0]})
    assert result["converged"] and result["fitted"] == [[0, 0], [0, 0]]


@pytest.mark.parametrize("seed,margins", [
    ([[1, 2]], {0: [2], 1: [1, 2]}),
    ([[1, 0], [0, 1]], {0: [1, 1], 1: [0, 2]}),
])
def test_ipf_rejects_inconsistent_or_unsupported_margins(seed, margins):
    with pytest.raises(ValueError):
        iterative_proportional_fit(seed, margins)


def test_ipf_rejects_invalid_seed_and_controls():
    with pytest.raises(ValueError):
        iterative_proportional_fit([[-1, 2], [3, 4]], {0: [1, 2], 1: [1, 2]})
    with pytest.raises(ValueError):
        iterative_proportional_fit([[1, 2], [3, 4]], {0: [1, 2], 1: [1, 2]}, tolerance=0)
