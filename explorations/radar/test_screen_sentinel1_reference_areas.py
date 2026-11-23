import numpy as np

from screen_sentinel1_reference_areas import distribution, erode_binary


def test_erode_binary_removes_edges_and_preserves_interior():
    mask = np.zeros((9, 9), dtype=bool)
    mask[1:8, 1:8] = True
    result = erode_binary(mask, iterations=2)
    assert result.sum() == 9
    assert result[3:6, 3:6].all()


def test_erode_binary_empty_and_zero_iterations():
    mask = np.zeros((4, 4), dtype=bool)
    assert not erode_binary(mask, iterations=1).any()
    assert np.array_equal(erode_binary(mask, iterations=0), mask)


def test_erode_binary_rejects_invalid_input():
    try:
        erode_binary(np.ones(4), iterations=1)
    except ValueError:
        pass
    else:
        raise AssertionError("Expected a 2D-mask validation error")


def test_distribution_reports_db_quantiles():
    result = distribution(np.array([0.1, 1.0, 10.0], dtype=np.float32))
    assert result["valid_pixels"] == 3
    assert abs(result["median_db"]) < 1e-9
