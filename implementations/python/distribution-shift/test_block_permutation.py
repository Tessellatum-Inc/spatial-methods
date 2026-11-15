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


def _make_unequal_block_data(shift=0.0, seed=4):
    rng = np.random.default_rng(seed)
    features, labels, block_ids = [], [], []
    for block in range(12):
        group = 0 if block < 6 else 1
        count = 3 + (block % 3)
        features.append(rng.normal(shift * group, .25, size=(count, 2)))
        labels.extend([group] * count)
        block_ids.extend([block] * count)
    return np.vstack(features), np.asarray(labels), np.asarray(block_ids)


def test_block_kernel_mmd_detects_separated_domains_with_unequal_blocks():
    from block_permutation import spatial_block_mmd_test
    x, labels, blocks = _make_unequal_block_data(2.5)
    result = spatial_block_mmd_test(x, labels, blocks, permutations=199, seed=12)
    assert result["mmd2_unbiased"] > 0
    assert result["p_value"] <= .05
    assert result["n_blocks"] == 12
    assert result["permutation_unit"] == "whole spatial block"


def test_block_kernel_mmd_is_reproducible_and_preserves_block_counts():
    from block_permutation import spatial_block_mmd_test
    x, labels, blocks = _make_unequal_block_data(.5)
    first = spatial_block_mmd_test(x, labels, blocks, permutations=99, seed=3)
    second = spatial_block_mmd_test(x, labels, blocks, permutations=99, seed=3)
    np.testing.assert_array_equal(first["permutation_statistics"], second["permutation_statistics"])
    assert first["p_value"] == second["p_value"]
    assert first["n_blocks_group_0"] == 6
    assert first["n_blocks_group_1"] == 6


def test_block_kernel_mmd_rejects_mixed_group_blocks_and_invalid_parameters():
    from block_permutation import spatial_block_mmd_test
    x, labels, blocks = _make_unequal_block_data()
    with pytest.raises(ValueError, match="exactly one group"):
        mixed = labels.copy()
        mixed[0] = 1
        spatial_block_mmd_test(x, mixed, blocks)
    with pytest.raises(ValueError):
        spatial_block_mmd_test(x, labels, blocks, bandwidth=0)
    with pytest.raises(ValueError):
        spatial_block_mmd_test(x, labels, blocks, permutations=0)
    with pytest.raises(ValueError):
        spatial_block_mmd_test(x, labels, blocks, alpha=1)
