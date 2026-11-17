# Transit headway and expected waiting time

A dependency-free reference implementation for service-frequency summaries
from a known departure timetable.

## Run

```bash
python -m pip install -r requirements.txt
python -m pytest -q
```

## Example

```python
from transit_headway import headway_metrics

metrics = headway_metrics(
    [0, 600, 1200, 1800],
    service_start=0,
    service_end=1800,
)
print(metrics["mean_headway"])  # 600 seconds
print(metrics["expected_wait"])  # 300 seconds
```

## Contract

- All times use one consistent numeric unit. Seconds are recommended.
- GTFS extended service-day times (for example, 25:00 represented as 90000)
  are supported; convert GTFS `HH:MM:SS` strings before calling.
- Departures are sorted internally, must be unique and must lie inside the
  supplied closed service window.
- Mean, median and coefficient of variation describe gaps between actual
  departures; they do not include partial boundary gaps.
- Expected wait assumes passengers arrive uniformly at random during the
  service window. It includes the initial and final partial intervals and is
  calculated as `sum(gap ** 2) / (2 * service_duration)`.
- A window with no departures reports `expected_wait=None`, not zero.
- This is a service-frequency metric, not a network accessibility model. It
  does not parse GTFS, model transfers, estimate in-vehicle time, or handle
  stochastic delays and bunching beyond the observed departure sequence.

See the [algorithm note](../../../algorithms/networks/headway-based-transit-service.md)
and [verification record](../../../catalog/verification/headway-based-transit-service.md).
