import numpy as np
import pytest
from least_cost import least_cost_distance

def test_uniform_cost_surface_matches_euclidean_path_lengths():
    result=least_cost_distance(np.ones((3,3)),[(1,1)])
    assert result[1,2]==1
    np.testing.assert_allclose(result[0,0],2**0.5)
    four=least_cost_distance(np.ones((3,3)),[(1,1)],connectivity=4)
    assert four[0,0]==2

def test_rectangular_cell_spacing_changes_diagonal_cost():
    result=least_cost_distance(np.ones((3,3)),[(1,1)],cell_size_x=2,cell_size_y=1)
    np.testing.assert_allclose(result[0,2],np.hypot(2,1))
    np.testing.assert_allclose(result[0,0],np.hypot(2,1))

def test_high_cost_cells_are_avoided_when_detour_is_cheaper():
    cost=np.ones((3,5)); cost[:,2]=100
    result=least_cost_distance(cost,[(1,0)],connectivity=4)
    assert result[1,4] < 200

def test_nodata_is_a_barrier_and_unreachable_valid_cells_are_infinite():
    cost=np.array([[1,np.nan,1],[1,np.nan,1],[1,np.nan,1]],float)
    result=least_cost_distance(cost,[(1,0)])
    assert np.isinf(result[1,2])
    assert np.isnan(result[1,1])

def test_nonuniform_endpoint_costs_are_integrated_by_arithmetic_mean():
    result=least_cost_distance([[1,3,1]],[(0,0)],connectivity=4)
    np.testing.assert_allclose(result,[[0,2,4]])

def test_non_finite_cells_are_barriers():
    result=least_cost_distance([[1,np.inf,1]],[(0,0)],connectivity=4)
    assert np.isinf(result[0,2])

def test_multiple_sources_choose_lowest_accumulated_cost():
    result=least_cost_distance(np.ones((1,5)),[(0,0),(0,4)],connectivity=4)
    np.testing.assert_allclose(result,[[0,1,2,1,0]])

def test_corner_cutting_can_be_forbidden():
    cost=np.array([[1,np.nan],[np.nan,1]],float)
    blocked=least_cost_distance(cost,[(0,0)],prevent_corner_cutting=True)
    allowed=least_cost_distance(cost,[(0,0)],prevent_corner_cutting=False)
    assert np.isinf(blocked[1,1])
    assert np.isfinite(allowed[1,1])

def test_invalid_sources_costs_and_parameters_are_rejected():
    with pytest.raises(ValueError,match="at least one"):
        least_cost_distance([[1]],[])
    with pytest.raises(ValueError,match="outside"):
        least_cost_distance([[1]],[(1,0)])
    with pytest.raises(ValueError,match="valid"):
        least_cost_distance([[np.nan]],[(0,0)])
    with pytest.raises(ValueError,match="non-negative"):
        least_cost_distance([[-1]],[(0,0)])
    with pytest.raises(ValueError,match="connectivity"):
        least_cost_distance([[1]],[(0,0)],connectivity=6)


from least_cost import least_cost_corridor


def test_zero_tolerance_corridor_matches_unique_four_neighbour_path():
    result = least_cost_corridor(np.ones((5, 5)), (2, 0), (2, 4),
                                 connectivity=4, tolerance=0)
    expected = np.zeros((5, 5), dtype=bool)
    expected[2, :] = True
    np.testing.assert_array_equal(result["corridor"], expected)
    assert result["optimal_cost"] == pytest.approx(4.0)
    np.testing.assert_allclose(result["through_cost"][2], 4.0)


def test_corridor_expands_with_additive_tolerance_and_respects_barriers():
    cost = np.ones((5, 5))
    cost[2, 2] = np.nan
    narrow = least_cost_corridor(cost, (2, 0), (2, 4),
                                 connectivity=4, tolerance=0)
    wide = least_cost_corridor(cost, (2, 0), (2, 4),
                               connectivity=4, tolerance=2)
    assert not narrow["corridor"][2, 2]
    assert not wide["corridor"][2, 2]
    assert wide["corridor"].sum() >= narrow["corridor"].sum()
    assert np.all(np.isfinite(wide["through_cost"][wide["corridor"]]))


def test_corridor_costs_match_independent_exhaustive_path_oracle():
    cost = np.array([[1., 2., 1.], [1., 4., 1.], [1., 1., 1.]])
    # Enumerate every simple 4-neighbour path on this tiny grid.
    from functools import lru_cache
    start, finish = (0, 0), (0, 2)
    paths = []
    def visit(cell, seen, total):
        if cell == finish:
            paths.append(total)
            return
        r, c = cell
        for dr, dc in ((-1, 0), (1, 0), (0, -1), (0, 1)):
            nxt = (r + dr, c + dc)
            if (0 <= nxt[0] < 3 and 0 <= nxt[1] < 3 and
                    nxt not in seen and np.isfinite(cost[nxt])):
                edge = 0.5 * (cost[cell] + cost[nxt])
                visit(nxt, seen | {nxt}, total + edge)
    visit(start, {start}, 0.0)
    result = least_cost_corridor(cost, start, finish, connectivity=4)
    assert result["optimal_cost"] == pytest.approx(min(paths))
    assert result["corridor"][0, 0] and result["corridor"][0, 2]


def test_corridor_rejects_invalid_tolerance_and_disconnected_target():
    with pytest.raises(ValueError, match="tolerance"):
        least_cost_corridor([[1, 1]], (0, 0), (0, 1), tolerance=-1)
    with pytest.raises(ValueError, match="unreachable"):
        least_cost_corridor([[1, np.nan, 1]], (0, 0), (0, 2), connectivity=4)
