import math
import random
import pytest
from d_infinity import d_infinity_flow_accumulation, d_infinity_flow_fractions


def test_planar_eastward_slope_routes_east():
    dem = [[-float(c) for c in range(5)] for _ in range(5)]
    assert d_infinity_flow_fractions(dem)[2][2] == ((2, 3, 1.0),)


def test_planar_direction_halfway_between_east_and_northeast_splits_equally():
    angle = math.pi / 8
    dem = [[-c * math.cos(angle) + r * math.sin(angle)
            for c in range(5)] for r in range(5)]
    links = d_infinity_flow_fractions(dem)[2][2]
    assert len(links) == 2
    assert [(r, c) for r, c, _ in links] == [(2, 3), (1, 3)]
    assert [w for _, _, w in links] == pytest.approx([0.5, 0.5])


def test_sink_and_nodata_contract():
    result = d_infinity_flow_fractions([[5, 5, None], [5, 1, 5], [5, 5, 5]])
    assert result[1][1] == tuple()
    assert result[0][2] is None


def test_eastward_accumulation_and_mass_conservation():
    dem = [[float(4 - c) for c in range(4)] for _ in range(3)]
    links = d_infinity_flow_fractions(dem)
    accumulation = d_infinity_flow_accumulation(dem, links)
    assert accumulation == [[1.0, 2.0, 3.0, 4.0]] * 3
    assert sum(accumulation[r][3] for r in range(3)) == 12.0


def test_weighted_initial_contributions():
    dem = [[float(4 - c) for c in range(4)] for _ in range(2)]
    links = d_infinity_flow_fractions(dem)
    initial = [[2.0] * 4 for _ in range(2)]
    assert d_infinity_flow_accumulation(dem, links, initial=initial) == [
        [2.0, 4.0, 6.0, 8.0], [2.0, 4.0, 6.0, 8.0]
    ]


def test_random_dem_links_are_downhill_and_conserve_fraction_and_mass():
    rng = random.Random(20261115)
    dem = [[rng.uniform(0, 100) for _ in range(15)] for _ in range(13)]
    links = d_infinity_flow_fractions(dem, cell_width=2, cell_height=3)
    for r in range(13):
        for c in range(15):
            assert len(links[r][c]) <= 2
            if links[r][c]:
                assert sum(w for _, _, w in links[r][c]) == pytest.approx(1)
            for rr, cc, _ in links[r][c]:
                assert dem[rr][cc] < dem[r][c]
    accumulation = d_infinity_flow_accumulation(dem, links)
    sinks = sum(accumulation[r][c] for r in range(13) for c in range(15)
                if not links[r][c])
    assert sinks == pytest.approx(13 * 15)


def test_invalid_inputs_and_graphs():
    with pytest.raises(ValueError):
        d_infinity_flow_fractions([[1, 2], [3]])
    with pytest.raises(ValueError):
        d_infinity_flow_fractions([[1, float("nan")]])
    with pytest.raises(ValueError):
        d_infinity_flow_fractions([[1]], cell_width=0)
    with pytest.raises(ValueError, match="strictly lower"):
        d_infinity_flow_accumulation([[2, 1]], [[((0, 1, 1.0),), ((0, 0, 1.0),)]])
    with pytest.raises(ValueError, match="sum to one"):
        d_infinity_flow_accumulation([[2, 1]], [[((0, 1, 0.5),), tuple()]])
