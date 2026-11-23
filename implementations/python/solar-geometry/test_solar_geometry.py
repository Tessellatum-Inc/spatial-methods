from datetime import datetime, timezone, timedelta
import pytest
from solar_geometry import solar_position, extraterrestrial_irradiance

def test_equinox_equator_midday_sun_is_high_and_near_south():
    result = solar_position(0, 0, datetime(2024, 3, 20, 12, 7, 52, tzinfo=timezone.utc))
    assert result["solar_elevation_deg"] > 89
    assert result["solar_azimuth_deg"] == pytest.approx(180, abs=3)

def test_timezone_equivalent_instants_produce_same_position():
    utc = datetime(2024, 6, 21, 12, tzinfo=timezone.utc)
    local = datetime(2024, 6, 21, 15, tzinfo=timezone(timedelta(hours=3)))
    assert solar_position(-1.3, 36.8, utc) == pytest.approx(solar_position(-1.3, 36.8, local))

def test_sun_is_below_horizon_at_midnight_at_equator_equinox():
    result = solar_position(0, 0, datetime(2024, 3, 20, 0, tzinfo=timezone.utc))
    assert result["solar_elevation_deg"] < -80

def test_azimuth_and_elevation_bounds_over_full_day():
    for hour in range(24):
        result = solar_position(40, -75, datetime(2024, 6, 21, hour, tzinfo=timezone.utc))
        assert 0 <= result["solar_azimuth_deg"] < 360
        assert -90 <= result["solar_elevation_deg"] <= 90
        assert result["solar_zenith_deg"] == pytest.approx(90-result["solar_elevation_deg"])

def test_extraterrestrial_horizontal_irradiance_is_zero_at_night():
    result = extraterrestrial_irradiance(0, 0, datetime(2024, 3, 20, 0, tzinfo=timezone.utc))
    assert result["normal_irradiance_w_m2"] > 1300
    assert result["horizontal_irradiance_w_m2"] == 0

def test_horizontal_irradiance_does_not_exceed_normal():
    result = extraterrestrial_irradiance(0, 0, datetime(2024, 3, 20, 12, tzinfo=timezone.utc))
    assert 0 <= result["horizontal_irradiance_w_m2"] <= result["normal_irradiance_w_m2"]

@pytest.mark.parametrize("lat,lon,dt", [
    (91, 0, datetime(2024, 1, 1, tzinfo=timezone.utc)),
    (0, 181, datetime(2024, 1, 1, tzinfo=timezone.utc)),
    (float("nan"), 0, datetime(2024, 1, 1, tzinfo=timezone.utc)),
    (0, 0, datetime(2024, 1, 1)),
])
def test_invalid_position_inputs_are_rejected(lat, lon, dt):
    with pytest.raises(ValueError):
        solar_position(lat, lon, dt)

def test_invalid_solar_constant_is_rejected():
    with pytest.raises(ValueError):
        extraterrestrial_irradiance(0, 0, datetime(2024, 3, 20, 12, tzinfo=timezone.utc), 0)
