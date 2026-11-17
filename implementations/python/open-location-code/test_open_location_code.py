import math
import pytest
from open_location_code import encode, decode


def test_known_googleplex_full_code_contains_reference_coordinate():
    code = encode(37.422, -122.084)
    assert code == "849VCWC8+R9"
    south, west, north, east = decode(code)
    assert south <= 37.422 < north
    assert west <= -122.084 < east


def test_encoding_is_case_and_longitude_wrap_stable():
    assert encode(0, 181) == encode(0, -179)
    assert decode("849vcwc8+r9") == decode("849VCWC8+R9")


@pytest.mark.parametrize("length", range(10, 16))
def test_supported_lengths_produce_nested_cells(length):
    code = encode(-1.286389, 36.817223, length)
    bounds = decode(code)
    assert len(code.replace("+", "")) == length
    assert bounds[0] <= -1.286389 < bounds[2]
    assert bounds[1] <= 36.817223 < bounds[3]


def test_poles_and_antimeridian_are_bounded():
    for lat, lon in ((90, 180), (-90, -180), (0, 540)):
        bounds = decode(encode(lat, lon))
        assert -90 <= bounds[0] < bounds[2] <= 90
        assert -180 <= bounds[1] < bounds[3] <= 180


@pytest.mark.parametrize("lat,lon", [(91, 0), (-91, 0), (math.inf, 0), (0, math.nan)])
def test_invalid_coordinates_are_rejected(lat, lon):
    with pytest.raises(ValueError):
        encode(lat, lon)


@pytest.mark.parametrize("length", [9, 16, 10.5, True])
def test_invalid_code_lengths_are_rejected(length):
    with pytest.raises(ValueError):
        encode(0, 0, length)


@pytest.mark.parametrize("code", ["", "849VCWC8", "849VCWC8+R", "849VCWC8+R9X", "849VCWC8+R!", "849VCWC+R9"])
def test_invalid_or_short_codes_are_rejected(code):
    with pytest.raises(ValueError):
        decode(code)
