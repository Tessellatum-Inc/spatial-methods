import numpy as np
import pytest

from spatial_spectral_analysis import (
    canonical_correlation_analysis,
    eof_analysis,
    maximum_covariance_analysis,
    periodogram_2d,
    ssa_decompose,
    welch_coherence,
)


def test_2d_periodogram_identifies_a_known_spatial_frequency():
    rows, cols = np.mgrid[0:16, 0:16]
    field = np.sin(2 * np.pi * 3 * cols / 16)
    result = periodogram_2d(field, window="none")
    peak = np.unravel_index(np.argmax(result["power"]), result["power"].shape)
    assert abs(result["frequency_x"][peak[1]]) == pytest.approx(3 / 16)
    assert result["frequency_y"][peak[0]] == pytest.approx(0)


def test_periodogram_constant_field_has_zero_power_and_physical_frequency_units():
    result = periodogram_2d(np.ones((8, 10)), spacing=(2, 5), window="none")
    assert np.all(result["power"] == 0)
    assert result["frequency_y"][1] - result["frequency_y"][0] == pytest.approx(1 / 16)
    assert result["frequency_x"][1] - result["frequency_x"][0] == pytest.approx(1 / 50)


def test_eof_full_rank_reconstructs_time_by_space_field():
    rng = np.random.default_rng(8)
    field = rng.normal(size=(30, 5)) @ rng.normal(size=(5, 4)) + 2
    result = eof_analysis(field)
    reconstructed = result["pcs"] @ result["eofs"].T + result["mean"]
    np.testing.assert_allclose(reconstructed, field, atol=1e-10)
    assert result["variance_fraction"].sum() == pytest.approx(1)
    np.testing.assert_allclose(result["eofs"].T @ result["eofs"], np.eye(4), atol=1e-10)


def test_eof_reduced_modes_and_standardization():
    rng = np.random.default_rng(12)
    field = rng.normal(size=(20, 3)) * [1, 4, 9]
    result = eof_analysis(field, n_modes=2, standardize=True)
    assert result["eofs"].shape == (3, 2)
    assert result["pcs"].shape == (20, 2)
    assert result["variance_fraction"].shape == (2,)


def test_ssa_all_components_reconstruct_original_series():
    series = np.sin(np.arange(40) / 5) + 0.2 * np.arange(40)
    result = ssa_decompose(series, window_length=12)
    np.testing.assert_allclose(result["reconstruction"], series, atol=1e-10)
    assert result["components"].shape == (12, 40)


def test_ssa_reduced_components_are_finite_and_bounded():
    series = np.sin(np.arange(50) / 4)
    result = ssa_decompose(series, window_length=15, n_components=2)
    assert result["components"].shape == (2, 50)
    assert np.isfinite(result["reconstruction"]).all()


def test_maximum_covariance_analysis_patterns_are_orthonormal():
    rng = np.random.default_rng(4)
    left = rng.normal(size=(40, 5))
    right = left[:, :3] @ rng.normal(size=(3, 4)) + 0.1 * rng.normal(size=(40, 4))
    result = maximum_covariance_analysis(left, right)
    np.testing.assert_allclose(result["left_patterns"].T @ result["left_patterns"], np.eye(4), atol=1e-10)
    np.testing.assert_allclose(result["right_patterns"].T @ result["right_patterns"], np.eye(4), atol=1e-10)
    assert np.all(np.diff(result["singular_values"]) <= 0)
    assert result["covariance_fraction"].sum() == pytest.approx(1)


def test_cca_finds_perfect_linear_relationship_with_regularisation():
    rng = np.random.default_rng(2)
    left = rng.normal(size=(100, 3))
    right = left @ np.array([[2, 0], [0, 3], [1, -1]])
    result = canonical_correlation_analysis(left, right, ridge=1e-10)
    assert result["canonical_correlations"][0] == pytest.approx(1, abs=1e-7)
    assert result["left_variates"].shape == (100, 2)


def test_welch_coherence_is_one_for_identical_signals():
    rng = np.random.default_rng(19)
    signal = rng.normal(size=128)
    result = welch_coherence(signal, signal, sampling_frequency=10, segment_length=32)
    np.testing.assert_allclose(result["coherence"][1:], np.ones(16), atol=1e-12)
    assert result["frequency"][-1] == pytest.approx(5)


@pytest.mark.parametrize("kwargs", [
    {"spacing": (0, 1)}, {"window": "blackman"},
])
def test_periodogram_rejects_invalid_controls(kwargs):
    with pytest.raises(ValueError):
        periodogram_2d(np.ones((4, 4)), **kwargs)


def test_eof_rejects_invalid_data_and_modes():
    with pytest.raises(ValueError):
        eof_analysis([[1, 2], [1, 2]])
    with pytest.raises(ValueError):
        eof_analysis([[1, 2], [2, 3]], n_modes=3)
    with pytest.raises(ValueError):
        eof_analysis([[1, 2], [2, 3]], standardize="yes")


def test_ssa_rejects_invalid_window_and_series():
    with pytest.raises(ValueError):
        ssa_decompose([1, 2, 3], window_length=1)
    with pytest.raises(ValueError):
        ssa_decompose([1, 2, np.nan], window_length=2)


def test_multivariate_methods_reject_misaligned_and_invalid_controls():
    with pytest.raises(ValueError):
        maximum_covariance_analysis(np.ones((5, 2)), np.ones((4, 2)))
    with pytest.raises(ValueError):
        canonical_correlation_analysis(np.ones((5, 2)), np.ones((5, 2)), ridge=-1)
    with pytest.raises(ValueError):
        welch_coherence([1, 2, 3, 4], [1, 2, 3, 4], segment_length=1)
