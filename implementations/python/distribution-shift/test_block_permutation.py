import numpy as np
import pytest
from block_permutation import block_mmd_permutation_test


def test_block_permutation_is_reproducible_and_detects_separated_domains():
    rng = np.random.default_rng(3)
    a = rng.normal(0, .2, size=(8, 12, 2))
    b = rng.normal(2, .2, size=(8, 12, 2))
    r1 = block_mmd_permutation_test(a, b, bandwidth=1, n_permutations=49, random_state=4)
    r2 = block_mmd_permutation_test(a, b, bandwidth=1, n_permutations=49, random_state=4)
    assert r1["statistic"] > 0
    assert r1["p_value"] == r2["p_value"]
    assert np.array_equal(r1["null_statistics"], r2["null_statistics"])
    assert r1["permutation_unit"] == "whole_block"


def test_block_permutation_uses_whole_equal_sized_blocks():
    a = np.zeros((3, 5, 2))
    b = np.ones((3, 5, 2))
    result = block_mmd_permutation_test(a, b, 1, n_permutations=5)
    assert result["rows_per_block"] == 5
    assert result["n_source_blocks"] == 3


def test_invalid_block_shapes_and_mismatched_sizes_rejected():
    with pytest.raises(ValueError):
        block_mmd_permutation_test(np.zeros((5, 2)), np.zeros((5, 2)), 1)
    with pytest.raises(ValueError):
        block_mmd_permutation_test(np.zeros((3, 4, 2)), np.zeros((3, 5, 2)), 1)
    with pytest.raises(ValueError):
        block_mmd_permutation_test(np.zeros((1, 4, 2)), np.zeros((3, 4, 2)), 1)


def test_invalid_permutation_count_rejected():
    blocks = np.zeros((3, 4, 2))
    with pytest.raises(ValueError):
        block_mmd_permutation_test(blocks, blocks + 1, 1, n_permutations=0)
