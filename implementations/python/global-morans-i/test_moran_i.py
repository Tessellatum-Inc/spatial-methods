import pytest

from moran_i import morans_i, row_standardize


CHAIN_WEIGHTS = [
    [0, 1, 0, 0],
    [1, 0, 1, 0],
    [0, 1, 0, 1],
    [0, 0, 1, 0],
]


def test_similar_neighbours_produce_positive_moran_i():
    assert morans_i([1, 2, 3, 4], CHAIN_WEIGHTS) == pytest.approx(1 / 3)


def test_alternating_neighbours_produce_negative_moran_i():
    assert morans_i([1, 4, 1, 4], CHAIN_WEIGHTS) == pytest.approx(-1.0)


def test_row_standardisation_changes_the_statistic():
    weights = row_standardize(CHAIN_WEIGHTS)
    assert morans_i([1, 2, 3, 4], weights) == pytest.approx(0.4)


def test_statistic_is_invariant_to_affine_changes_in_values():
    assert morans_i([1, 2, 3, 4], CHAIN_WEIGHTS) == pytest.approx(
        morans_i([11, 12, 13, 14], CHAIN_WEIGHTS)
    )
    assert morans_i([1, 2, 3, 4], CHAIN_WEIGHTS) == pytest.approx(
        morans_i([2, 4, 6, 8], CHAIN_WEIGHTS)
    )


def test_statistic_is_invariant_to_positive_weight_scaling():
    scaled = [[10 * value for value in row] for row in CHAIN_WEIGHTS]
    assert morans_i([1, 2, 3, 4], CHAIN_WEIGHTS) == pytest.approx(
        morans_i([1, 2, 3, 4], scaled)
    )


def test_row_standardisation_keeps_island_rows_zero():
    weights = [
        [0, 1, 0],
        [1, 0, 0],
        [0, 0, 0],
    ]
    assert row_standardize(weights)[2] == [0.0, 0.0, 0.0]


def test_constant_values_are_undefined():
    with pytest.raises(ValueError, match="constant"):
        morans_i([4, 4, 4, 4], CHAIN_WEIGHTS)


def test_zero_weights_are_rejected():
    with pytest.raises(ValueError, match="positive weight"):
        morans_i([1, 2, 3, 4], [[0] * 4 for _ in range(4)])


def test_misaligned_weights_are_rejected():
    with pytest.raises(ValueError, match="one row"):
        morans_i([1, 2, 3], CHAIN_WEIGHTS)


def test_non_square_weights_are_rejected():
    with pytest.raises(ValueError, match="square"):
        morans_i([1, 2, 3], [[0, 1, 0], [1, 0], [0, 1, 0]])


def test_nonzero_self_weights_are_rejected():
    weights = [row[:] for row in CHAIN_WEIGHTS]
    weights[0][0] = 1
    with pytest.raises(ValueError, match="self-weights"):
        morans_i([1, 2, 3, 4], weights)


def test_negative_weights_are_rejected():
    weights = [row[:] for row in CHAIN_WEIGHTS]
    weights[0][1] = -1
    with pytest.raises(ValueError, match="non-negative"):
        morans_i([1, 2, 3, 4], weights)


def test_non_finite_values_are_rejected():
    with pytest.raises(ValueError, match="finite"):
        morans_i([1, 2, float("nan"), 4], CHAIN_WEIGHTS)



def test_permutation_inference_is_seeded_and_uses_plus_one_correction():
    from moran_i import morans_i_permutation
    first=morans_i_permutation([1,2,3,4],CHAIN_WEIGHTS,permutations=99,seed=7)
    second=morans_i_permutation([1,2,3,4],CHAIN_WEIGHTS,permutations=99,seed=7)
    assert first==second
    assert first["statistic"]==pytest.approx(1/3)
    assert first["expected"]==pytest.approx(-1/3)
    assert 1/100<=first["p_value"]<=1


def test_permutation_alternatives_and_invalid_controls():
    from moran_i import morans_i_permutation
    assert morans_i_permutation([1,2,3,4],CHAIN_WEIGHTS,permutations=20,
                                alternative="greater",seed=2)["p_value"]>0
    assert morans_i_permutation([1,2,3,4],CHAIN_WEIGHTS,permutations=20,
                                alternative="less",seed=2)["p_value"]>0
    with pytest.raises(ValueError): morans_i_permutation([1,2,3,4],CHAIN_WEIGHTS,permutations=0)
    with pytest.raises(ValueError): morans_i_permutation([1,2,3,4],CHAIN_WEIGHTS,alternative="upper")



def test_distance_band_correlogram_matches_global_moran_on_first_band():
    from moran_i import morans_i_correlogram
    points=[(0,0),(1,0),(2,0),(3,0)]
    result=morans_i_correlogram(points,[1,2,3,4],[0,1.1,2.1,4.0])
    assert [row["pairs"] for row in result] == [3,2,1]
    assert result[0]["statistic"] == pytest.approx(1/3)
    assert result[1]["statistic"] is not None
    assert result[2]["statistic"] is not None
    assert all(row["expected"] == pytest.approx(-1/3) for row in result)


def test_distance_band_correlogram_reports_empty_bands_and_row_standardizes():
    from moran_i import morans_i_correlogram
    points=[(0,0),(1,0),(2,0)]
    raw=morans_i_correlogram(points,[1,2,3],[0,0.5,1.5,3])
    standardized=morans_i_correlogram(points,[1,2,3],[0,0.5,1.5,3],
                                      row_standardize_weights=True)
    assert raw[0]["pairs"] == 0 and raw[0]["statistic"] is None
    assert raw[1]["pairs"] == 2
    assert standardized[1]["statistic"] is not None


def test_distance_band_correlogram_validates_inputs_and_band_edges():
    from moran_i import morans_i_correlogram
    with pytest.raises(ValueError,match="one 2D"):
        morans_i_correlogram([(0,0)],[1,2],[0,1])
    with pytest.raises(ValueError,match="strictly increasing"):
        morans_i_correlogram([(0,0),(1,0)],[1,2],[0,1,1])
    with pytest.raises(ValueError,match="finite"):
        morans_i_correlogram([(0,0),(float("nan"),0)],[1,2],[0,1])



def test_moran_correlogram_single_band_permutation_matches_global_oracle():
    from moran_i import morans_i_correlogram, morans_i_permutation
    points=[(0,0),(1,0),(2,0),(3,0)]
    values=[1,2,4,8]
    got=morans_i_correlogram(points,values,[0,4],permutations=199,seed=31)[0]
    oracle=morans_i_permutation(values,[[0,1,1,1],[1,0,1,1],[1,1,0,1],[1,1,1,0]],
                                permutations=199,seed=31)
    assert got["p_value"] == pytest.approx(oracle["p_value"])
    assert got["p_value_maxT"] == pytest.approx(got["p_value"])
    assert got["simulation_std"] > 0


def test_moran_correlogram_max_t_adjustment_is_reproducible_and_conservative():
    from moran_i import morans_i_correlogram
    points=[(0,0),(1,0),(2,0),(3,0),(4,0)]
    values=[1,2,3,7,9]
    a=morans_i_correlogram(points,values,[0,1.1,2.1,5],permutations=199,seed=71)
    b=morans_i_correlogram(points,values,[0,1.1,2.1,5],permutations=199,seed=71)
    assert a==b
    for row in a:
        if row["p_value"] is not None and row["p_value_maxT"] is not None:
            assert row["p_value_maxT"] >= row["p_value"]
            assert 0 < row["p_value"] <= 1
            assert 0 < row["p_value_maxT"] <= 1


def test_moran_correlogram_permutation_rejects_invalid_controls_and_constant_data():
    from moran_i import morans_i_correlogram
    points=[(0,0),(1,0),(2,0)]
    with pytest.raises(ValueError,match="permutations"):
        morans_i_correlogram(points,[1,2,3],[0,2],permutations=-1)
    with pytest.raises(ValueError,match="seed"):
        morans_i_correlogram(points,[1,2,3],[0,2],permutations=9,seed=True)
    with pytest.raises(ValueError,match="constant"):
        morans_i_correlogram(points,[2,2,2],[0,2],permutations=9)
