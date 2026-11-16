import numpy as np
import pytest
from flat_resolution import resolve_flats

NEIGHBOURS = ((-1,-1),(-1,0),(-1,1),(0,-1),(0,1),(1,-1),(1,0),(1,1))


def test_flat_plateau_routes_to_lower_outlet():
    dem = np.array([[9,9,9,9,9,9,9],[9,9,9,9,9,9,9],
                    [9,5,5,5,5,5,3],[9,9,9,9,9,9,9],
                    [9,9,9,9,9,9,9]], dtype=float)
    resolved = resolve_flats(dem)
    assert resolved[2,1] > resolved[2,2] > resolved[2,5]
    for r,c in ((2,1),(2,2),(2,3),(2,4),(2,5)):
        assert any(0 <= r+dr < 5 and 0 <= c+dc < 7
                   and resolved[r+dr,c+dc] < resolved[r,c]
                   for dr,dc in NEIGHBOURS)


def test_every_flat_cell_has_a_lower_neighbour():
    dem = np.array([[8,8,8,8,8],[8,4,4,4,8],[8,4,4,4,8],
                    [8,4,4,4,2],[8,8,8,8,1]], dtype=float)
    out = resolve_flats(dem)
    for r in range(1,4):
        for c in range(1,4):
            assert any(0 <= r+dr < 5 and 0 <= c+dc < 5
                       and out[r+dr,c+dc] < out[r,c] for dr,dc in NEIGHBOURS)


def test_flat_without_lower_outlet_is_unchanged():
    dem = np.array([[5,5,5],[5,1,5],[5,5,5]], dtype=float)
    np.testing.assert_array_equal(resolve_flats(dem), dem)


def test_nonflat_and_nodata_preserved():
    dem = np.array([[5.,4.,np.nan],[6.,3.,2.]])
    out = resolve_flats(dem)
    assert out[0,0] == 5 and out[0,1] == 4 and np.isnan(out[0,2])


def test_masks_and_explicit_epsilon():
    dem = np.array([[10,10,10,10],[10,5,5,4],[10,5,5,3]], dtype=float)
    out = resolve_flats(dem, epsilon=0.1)
    assert out[1,1] > out[1,2]
    with pytest.raises(ValueError, match="higher terrain"):
        resolve_flats(dem, epsilon=6.0)
    mask = np.ones_like(dem, dtype=bool); mask[1,1] = False
    assert np.isnan(resolve_flats(dem, valid_mask=mask)[1,1])


def test_invalid_inputs():
    with pytest.raises(ValueError, match="epsilon"):
        resolve_flats([[2,2]], epsilon=0)
    with pytest.raises(ValueError, match="valid_mask"):
        resolve_flats([[2,2]], valid_mask=np.ones((1,3)))
    with pytest.raises(ValueError, match="at least one valid"):
        resolve_flats([[np.nan]])
