import numpy as np
import pytest

from insar_coherence import coherence_change, local_interferometric_coherence


def test_identical_complex_images_have_unit_local_coherence():
    rng = np.random.default_rng(4)
    image = rng.normal(size=(8, 9)) + 1j * rng.normal(size=(8, 9))
    result = local_interferometric_coherence(image, image, window_size=3)
    assert result.shape == (6, 7)
    np.testing.assert_allclose(result, 1.0, atol=1e-12)


def test_constant_phase_offset_preserves_unit_coherence():
    rng = np.random.default_rng(8)
    master = rng.normal(size=(7, 7)) + 1j * rng.normal(size=(7, 7))
    slave = master * np.exp(1j * 1.1)
    np.testing.assert_allclose(local_interferometric_coherence(master, slave, window_size=5), 1.0, atol=1e-12)


def test_incoherent_independent_complex_fields_have_low_mean_coherence():
    rng = np.random.default_rng(19)
    master = rng.normal(size=(100, 100)) + 1j * rng.normal(size=(100, 100))
    slave = rng.normal(size=(100, 100)) + 1j * rng.normal(size=(100, 100))
    result = local_interferometric_coherence(master, slave, window_size=9)
    assert np.nanmean(result) < 0.2


def test_zero_power_windows_are_nan_and_min_power_is_respected():
    master = np.ones((4, 4), dtype=complex)
    slave = np.zeros((4, 4), dtype=complex)
    assert np.isnan(local_interferometric_coherence(master, slave, window_size=3)).all()
    assert np.isnan(local_interferometric_coherence(master, master, window_size=3, min_power=10)).all()


def test_coherence_change_is_signed_after_minus_before():
    before = np.array([[0.9, 0.2]])
    after = np.array([[0.3, 0.8]])
    np.testing.assert_allclose(coherence_change(before, after), [[-0.6, 0.6]])


@pytest.mark.parametrize("kwargs", [
    {"window_size": 2}, {"window_size": 8}, {"min_power": -1},
])
def test_invalid_coherence_controls_are_rejected(kwargs):
    image = np.ones((5, 5), dtype=complex)
    with pytest.raises(ValueError):
        local_interferometric_coherence(image, image, **kwargs)


def test_mismatched_and_nonfinite_images_are_rejected():
    with pytest.raises(ValueError):
        local_interferometric_coherence(np.ones((4, 4)), np.ones((4, 5)))
    bad = np.ones((4, 4), dtype=complex)
    bad[0, 0] = np.nan + 1j
    with pytest.raises(ValueError):
        local_interferometric_coherence(bad, np.ones((4, 4)), window_size=3)


def test_coherence_change_rejects_out_of_range_and_misaligned_inputs():
    with pytest.raises(ValueError):
        coherence_change([[0.2]], [[1.2]])
    with pytest.raises(ValueError):
        coherence_change([[0.2]], [[0.2, 0.3]])
