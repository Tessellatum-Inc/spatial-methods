import pytest
from brovey import brovey_pansharpen

def test_brovey_scales_each_band_to_pan_with_n_band_factor():
    result = brovey_pansharpen(
        [[[1, 2]], [[1, 2]], [[2, 2]]],
        [[8, 12]],
    )
    expected = [[[6, 12]], [[6, 12]], [[12, 12]]]
    for actual_band, expected_band in zip(result["bands"], expected):
        assert actual_band[0] == pytest.approx(expected_band[0])
    assert result["valid_mask"] == [[True, True]]

def test_brovey_preserves_per_pixel_spectral_band_ratios():
    result = brovey_pansharpen([[[2]], [[3]], [[5]]], [[7]])
    values = [band[0][0] for band in result["bands"]]
    assert values[0] / values[1] == pytest.approx(2/3)
    assert values[2] / values[1] == pytest.approx(5/3)

def test_nodata_in_any_input_masks_all_output_bands():
    result = brovey_pansharpen(
        [[[1, -9999]], [[2, 2]]],
        [[3, 3]],
        nodata=-9999,
    )
    assert result["bands"][0][0][1] is None
    assert result["bands"][1][0][1] is None
    assert result["valid_mask"] == [[True, False]]

def test_zero_multispectral_sum_is_unresolved():
    result = brovey_pansharpen([[[0]], [[0]]], [[10]])
    assert result["bands"] == [[[None]], [[None]]]
    assert result["valid_mask"] == [[False]]

def test_pan_zero_is_valid_and_produces_zero_output():
    result = brovey_pansharpen([[[1]], [[2]]], [[0]])
    assert result["bands"] == [[[0]], [[0]]]
    assert result["valid_mask"] == [[True]]

@pytest.mark.parametrize("bands,pan", [
    ([], [[1]]),
    ([[[1]]], [[1]]),
    ([[[1, 2]] , [[1]]], [[1]]),
    ([[[1], [2]], [[1]]], [[1]]),
])
def test_invalid_band_counts_and_shapes_are_rejected(bands, pan):
    with pytest.raises(ValueError):
        brovey_pansharpen(bands, pan)

@pytest.mark.parametrize("value", [-1, float("inf"), True, "bad"])
def test_invalid_valid_pixel_values_are_rejected(value):
    with pytest.raises(ValueError):
        brovey_pansharpen([[[value]], [[1]]], [[1]])

def test_ragged_pan_grid_is_rejected():
    with pytest.raises(ValueError):
        brovey_pansharpen([[[1], [2]], [[1], [2]]], [[1, 2], [3]])

def test_nan_is_treated_as_missing_and_masked():
    result = brovey_pansharpen([[[1, float("nan")]], [[2, 3]]], [[4, 4]])
    assert result["valid_mask"] == [[True, False]]
    assert result["bands"][0][0][1] is None
