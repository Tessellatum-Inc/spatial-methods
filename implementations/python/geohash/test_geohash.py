import pytest
from geohash import decode, decode_bounds, encode


def test_known_geohash_reference():
    assert encode(42.6, -5.6, precision=5) == "ezs42"
    lat, lon = decode("ezs42")
    assert lat == pytest.approx(42.60498, abs=0.001)
    assert lon == pytest.approx(-5.6030, abs=0.001)


def test_round_trip_centres_within_cell_bounds():
    for lat, lon in [(-90,-180), (90,180), (0,0), (1.2921,36.8219), (-33.9,151.2)]:
        code = encode(lat, lon, 8)
        south, north, west, east = decode_bounds(code)
        assert south <= lat <= north
        assert west <= lon <= east


def test_precision_controls_cell_resolution():
    coarse = decode_bounds(encode(10,20,3))
    fine = decode_bounds(encode(10,20,8))
    assert fine[1]-fine[0] < coarse[1]-coarse[0]
    assert fine[3]-fine[2] < coarse[3]-coarse[2]


def test_decode_is_case_insensitive():
    assert decode("EZS42") == decode("ezs42")


@pytest.mark.parametrize("args", [
    (91,0,5), (-91,0,5), (0,181,5), (0,-181,5),
    (float("nan"),0,5), (0,float("inf"),5),
    (0,0,0), (0,0,13), (0,0,True),
])
def test_encode_rejects_invalid_inputs(args):
    with pytest.raises(ValueError):
        encode(*args)


@pytest.mark.parametrize("value", ["", "hello!", "0123456789bcdefghjkmnpqrstuvwxyz", None])
def test_decode_rejects_invalid_geohashes(value):
    with pytest.raises(ValueError):
        decode_bounds(value)
