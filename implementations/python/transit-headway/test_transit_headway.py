import pytest

from transit_headway import headway_metrics


def test_regular_ten_minute_service_has_five_minute_expected_wait():
    result = headway_metrics([0, 600, 1200], service_start=0, service_end=1200)
    assert result["headways"] == [600.0, 600.0]
    assert result["mean_headway"] == 600.0
    assert result["median_headway"] == 600.0
    assert result["headway_cv"] == 0.0
    assert result["expected_wait"] == pytest.approx(300.0)


def test_irregular_headways_use_passenger_arrival_weighting():
    result = headway_metrics([0, 300, 1200], service_start=0, service_end=1200)
    assert result["headways"] == [300.0, 900.0]
    assert result["expected_wait"] == pytest.approx(375.0)
    assert result["headway_cv"] == pytest.approx(0.5)


def test_boundary_gaps_are_included_in_expected_wait():
    result = headway_metrics([300, 900], service_start=0, service_end=1200)
    assert result["headways"] == [600.0]
    assert result["wait_intervals"] == [300.0, 600.0, 300.0]
    assert result["expected_wait"] == pytest.approx(225.0)


def test_departures_are_sorted_and_extended_gtfs_times_are_supported():
    result = headway_metrics([90000, 86400, 88200], service_start=86400, service_end=90000)
    assert result["departures"] == [86400.0, 88200.0, 90000.0]
    assert result["expected_wait"] == pytest.approx(900.0)


def test_one_departure_still_has_window_expected_wait():
    result = headway_metrics([300], service_start=0, service_end=900)
    assert result["headways"] == []
    assert result["mean_headway"] is None
    assert result["headway_cv"] is None
    assert result["expected_wait"] == pytest.approx(250.0)


def test_no_departures_returns_explicit_no_service():
    result = headway_metrics([], service_start=0, service_end=3600)
    assert result["departure_count"] == 0
    assert result["expected_wait"] is None
    assert result["wait_intervals"] == []


@pytest.mark.parametrize(
    "departures,start,end",
    [
        ([1, 1], 0, 10),
        ([-1], 0, 10),
        ([11], 0, 10),
        ([float("nan")], 0, 10),
        ([float("inf")], 0, 10),
        ([1], 10, 10),
        ([1], 11, 10),
    ],
)
def test_invalid_schedule_inputs_are_rejected(departures, start, end):
    with pytest.raises(ValueError):
        headway_metrics(departures, service_start=start, service_end=end)


def test_invalid_non_numeric_inputs_are_rejected():
    with pytest.raises(ValueError):
        headway_metrics(["not-a-time"], service_start=0, service_end=10)
    with pytest.raises(ValueError):
        headway_metrics([1], service_start="bad", service_end=10)
