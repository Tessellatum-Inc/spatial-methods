import pytest
from transit_headway import headway_metrics


def test_regular_service():
    r = headway_metrics([0,600,1200], service_start=0, service_end=1200)
    assert r["headways"] == [600.0,600.0]
    assert r["expected_wait"] == pytest.approx(300)
    assert r["headway_cv"] == 0


def test_irregular_headways_and_boundary_gaps():
    r = headway_metrics([300,900], service_start=0, service_end=1200)
    assert r["wait_intervals"] == [300,600,300]
    assert r["expected_wait"] == pytest.approx(225)


def test_extended_service_day_and_sorting():
    r = headway_metrics([90000,86400,88200], service_start=86400, service_end=90000)
    assert r["departures"] == [86400,88200,90000]
    assert r["expected_wait"] == pytest.approx(900)


def test_piecewise_arrival_rates():
    r = headway_metrics([300,1200], service_start=0, service_end=1500,
                        arrival_weights=[2,1,1])
    assert r["expected_wait"] == pytest.approx((2*300**2/2+900**2/2+300**2/2)/1800)
    assert r["arrival_weight_total"] == 1800


def test_uniform_rates_equal_default():
    a = headway_metrics([200,700], service_start=0, service_end=1000)
    b = headway_metrics([200,700], service_start=0, service_end=1000,
                        arrival_weights=[1,1,1])
    assert a["expected_wait"] == pytest.approx(b["expected_wait"])


def test_zero_rates_and_no_service_are_undefined():
    r = headway_metrics([300,600], service_start=0, service_end=900,
                        arrival_weights=[0,0,0])
    assert r["expected_wait"] is None
    assert headway_metrics([], service_start=0, service_end=900)["expected_wait"] is None


@pytest.mark.parametrize("weights", [[1,2],[-1,1,1],[1,float("nan"),1],
                                     [1,float("inf"),1],["x",1,1]])
def test_invalid_arrival_rates(weights):
    with pytest.raises(ValueError, match="arrival_weights"):
        headway_metrics([300,600], service_start=0, service_end=900,
                        arrival_weights=weights)


def test_weights_for_empty_service_must_be_empty():
    with pytest.raises(ValueError, match="arrival_weights"):
        headway_metrics([], service_start=0, service_end=900, arrival_weights=[1])


@pytest.mark.parametrize("departures,start,end", [
    ([1,1],0,10), ([-1],0,10), ([11],0,10),
    ([float("nan")],0,10), ([float("inf")],0,10),
    ([1],10,10), ([1],11,10), (["bad"],0,10),
])
def test_invalid_schedules(departures,start,end):
    with pytest.raises(ValueError):
        headway_metrics(departures, service_start=start, service_end=end)


def test_one_departure_and_numeric_boundaries():
    r = headway_metrics([300], service_start=0, service_end=900)
    assert r["expected_wait"] == pytest.approx(250)
    with pytest.raises(ValueError):
        headway_metrics([1], service_start="bad", service_end=10)
