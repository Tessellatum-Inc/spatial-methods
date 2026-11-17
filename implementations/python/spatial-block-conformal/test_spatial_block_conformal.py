import numpy as np
import pytest

from spatial_block_conformal import (
    BlockConformalCalibration,
    calibrate_spatial_blocks,
    spatial_block_interval,
)


def test_block_scores_are_maximum_absolute_residuals():
    result = calibrate_spatial_blocks(
        [1, 3, 2, 8, 5, 5],
        [1, 1, 2, 5, 5, 4],
        ["west", "west", "central", "central", "east", "east"],
        alpha=0.25,
    )
    assert result.block_scores == (2.0, 3.0, 1.0)
    assert result.n_blocks == 3
    assert result.n_observations == 6
    assert result.rank == 3
    assert result.quantile == 3.0


def test_finite_sample_rank_can_require_infinite_interval():
    result = calibrate_spatial_blocks(
        [0, 1, 2], [0, 0, 0], [0, 1, 2], alpha=0.1
    )
    assert result.rank == 4
    assert np.isinf(result.quantile)
    lower, upper = spatial_block_interval([10], result)
    assert np.isneginf(lower[0])
    assert np.isposinf(upper[0])


def test_equal_residuals_within_one_block_count_as_one_unit():
    result = calibrate_spatial_blocks(
        [1, 2, 3, 4], [0, 0, 0, 0], ["a", "a", "a", "b"], alpha=0.5
    )
    assert result.n_blocks == 2
    assert result.block_scores == (3.0, 4.0)


def test_scale_normalised_calibration_and_intervals():
    result = calibrate_spatial_blocks(
        [2, 4, 8.5, 12],
        [0, 0, 5, 5],
        ["a", "a", "b", "b"],
        alpha=0.5,
        scale=[2, 4, 2, 4],
    )
    assert result.block_scores == (1.0, 1.75)
    lower, upper = spatial_block_interval([10, 20], result, scale=[2, 4])
    np.testing.assert_allclose(lower, [6.5, 13.0])
    np.testing.assert_allclose(upper, [13.5, 27.0])


def test_alpha_one_half_uses_upper_order_statistic():
    result = calibrate_spatial_blocks(
        [1, 2, 3, 4, 5], [0, 0, 0, 0, 0], list("abcde"), alpha=0.5
    )
    assert result.rank == 3
    assert result.quantile == 3.0


@pytest.mark.parametrize(
    "truth,pred,blocks,alpha,scale",
    [
        ([1], [1, 2], [0], 0.1, None),
        ([1, 2], [1, 2], [0], 0.1, None),
        ([1], [np.nan], [0], 0.1, None),
        ([1], [1], [0], 1.0, None),
        ([1], [1], [0], 0.1, [0]),
        ([1], [1], [None], 0.1, None),
    ],
)
def test_invalid_calibration_inputs_are_rejected(truth, pred, blocks, alpha, scale):
    with pytest.raises(ValueError):
        calibrate_spatial_blocks(
            truth, pred, blocks, alpha=alpha, scale=scale
        )


@pytest.mark.parametrize("scale", [[0], [-1], [np.inf], [np.nan], [1, 2]])
def test_invalid_prediction_scale_is_rejected(scale):
    calibration = BlockConformalCalibration(0.1, 1.0, 1, 1, 1, (1.0,))
    with pytest.raises(ValueError):
        spatial_block_interval([1], calibration, scale=scale)


def test_non_calibration_object_is_rejected():
    with pytest.raises(TypeError):
        spatial_block_interval([1], object())


def test_prediction_shape_and_finiteness_are_checked():
    calibration = BlockConformalCalibration(0.1, 1.0, 1, 1, 1, (1.0,))
    with pytest.raises(ValueError):
        spatial_block_interval([[1]], calibration)
    with pytest.raises(ValueError):
        spatial_block_interval([np.inf], calibration)
