import numpy as np
import pytest
from otsu_threshold import otsu_threshold, otsu_binarize


def oracle(x):
    levels = np.unique(x)
    if len(levels) == 1:
        return float(levels[0])
    best_score, best_t = -1.0, None
    for a, b in zip(levels[:-1], levels[1:]):
        left, right = x[x <= a], x[x >= b]
        score = len(left) / len(x) * len(right) / len(x) * (left.mean() - right.mean()) ** 2
        if score > best_score:
            best_score, best_t = score, (a + b) / 2
    return float(best_t)


def test_bimodal_and_binary_output():
    x = np.array([[0, 0, 1, 1], [8, 9, 9, 10]], dtype=float)
    t, out = otsu_binarize(x)
    assert 1 < t < 8
    np.testing.assert_array_equal(out, x > t)


def test_seeded_random_against_exhaustive_oracle():
    rng = np.random.default_rng(9127)
    for _ in range(100):
        x = rng.integers(-5, 12, size=(4, 7)).astype(float)
        assert otsu_threshold(x) == pytest.approx(oracle(x))


def test_mask_and_nonfinite_exclusion():
    x = np.array([[0., 1., 10.], [11., np.nan, 1e9]])
    mask = np.array([[True, True, True], [True, True, False]])
    t, out = otsu_binarize(x, mask=mask)
    assert t < 10
    assert not out[1, 1] and not out[1, 2]


def test_constant_and_invalid_inputs():
    assert otsu_threshold(np.full((3, 4), 7.5)) == 7.5
    assert not otsu_binarize(np.full((3, 4), 7.5))[1].any()
    with pytest.raises(ValueError): otsu_threshold(np.array([]))
    with pytest.raises(ValueError): otsu_threshold(np.array([np.nan]))
    with pytest.raises(ValueError): otsu_threshold(np.ones((2, 2)), mask=np.ones((3, 3), bool))
    with pytest.raises(TypeError): otsu_threshold(np.ones((2, 2)), mask=np.ones((2, 2), int))


def test_translation_and_scale_invariance():
    x = np.array([0, 0, 2, 3, 12, 13, 13.], dtype=float)
    t = otsu_threshold(x)
    assert otsu_threshold(x + 100) == pytest.approx(t + 100)
    assert otsu_threshold(x * 4) == pytest.approx(t * 4)
