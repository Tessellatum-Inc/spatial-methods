import itertools
import random

import pytest

from spatial_encodings import (
    geohash_decode,
    geohash_encode,
    hilbert_decode,
    hilbert_encode,
    morton_decode,
    morton_encode,
)


@pytest.mark.parametrize("bits", [1, 2, 3, 8, 16])
def test_morton_round_trip_all_small_cells(bits):
    side = 1 << min(bits, 3)
    for x, y in itertools.product(range(side), repeat=2):
        assert morton_decode(morton_encode(x, y, bits), bits) == (x, y)


@pytest.mark.parametrize("bits", [1, 2, 3, 8, 16])
def test_hilbert_round_trip_all_small_cells(bits):
    side = 1 << min(bits, 3)
    for x, y in itertools.product(range(side), repeat=2):
        distance = hilbert_encode(x, y, bits)
        assert hilbert_decode(distance, bits) == (x, y)


def test_hilbert_indices_are_a_bijection_on_small_grid():
    bits = 3
    side = 1 << bits
    distances = {hilbert_encode(x, y, bits) for x, y in itertools.product(range(side), repeat=2)}
    assert distances == set(range(side * side))


def test_morton_indices_are_a_bijection_on_small_grid():
    bits = 4
    side = 1 << bits
    codes = {morton_encode(x, y, bits) for x, y in itertools.product(range(side), repeat=2)}
    assert codes == set(range(side * side))


def test_geohash_known_reference_and_round_trip_bounds():
    assert geohash_encode(42.6, -5.6, 5) == "ezs42"
    lat_bounds, lon_bounds = geohash_decode("ezs42")
    assert lat_bounds[0] <= 42.6 <= lat_bounds[1]
    assert lon_bounds[0] <= -5.6 <= lon_bounds[1]


def test_geohash_is_case_insensitive_on_decode():
    assert geohash_decode("ezs42") == geohash_decode("EZS42")


def test_geohash_precision_narrows_bounds():
    coarse = geohash_decode(geohash_encode(-1.28, 36.82, 4))
    fine = geohash_decode(geohash_encode(-1.28, 36.82, 8))
    assert fine[0][1] - fine[0][0] < coarse[0][1] - coarse[0][0]
    assert fine[1][1] - fine[1][0] < coarse[1][1] - coarse[1][0]


@pytest.mark.parametrize(
    "function,args",
    [
        (morton_encode, (-1, 0, 4)),
        (morton_encode, (0, 16, 4)),
        (morton_encode, (True, 0, 4)),
        (morton_decode, (-1, 4)),
        (morton_decode, (256, 4)),
        (hilbert_encode, (0, 0, 0)),
        (hilbert_decode, (256, 4)),
        (geohash_encode, (91, 0, 5)),
        (geohash_encode, (0, 181, 5)),
        (geohash_encode, (0, 0, 13)),
        (geohash_decode, ("not-a-geohash!",)),
    ],
)
def test_invalid_inputs_are_rejected(function, args):
    with pytest.raises(ValueError):
        function(*args)


def test_seeded_round_trip_on_large_integer_grids():
    rng = random.Random(20261115)
    for bits in (10, 16, 24, 32):
        for _ in range(100):
            x = rng.randrange(1 << bits)
            y = rng.randrange(1 << bits)
            assert morton_decode(morton_encode(x, y, bits), bits) == (x, y)
            distance = hilbert_encode(x, y, bits)
            assert hilbert_decode(distance, bits) == (x, y)
