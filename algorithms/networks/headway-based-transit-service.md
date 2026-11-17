# Headway-based transit service and expected waiting time

- **Kind:** transit service metric
- **Domain:** public transport operations and accessibility
- **Status:** tested deterministic departure-schedule baseline
- **Version:** 0.1

## Headway summaries

Given ordered departure times (t_1,ldots,t_n), consecutive headways are
(h_i=t_{i+1}-t_i). Report mean and median headway and the population
coefficient of variation (standard deviation divided by mean) when at least
two headways are available. These describe the observed timetable and do not
by themselves measure passenger waiting time.

## Expected wait for random passenger arrivals

For passengers arriving uniformly over a service window of duration (T),
with deterministic departures and no capacity constraints, the expected wait
is the time integral of time-to-next-departure divided by (T). If the
successive intervals between the window boundaries and departures are
(g_1,ldots,g_m), each interval contributes a triangular wait-time area
(g_j^2/2), giving

[
E[W]=\frac{\sum_{j=1}^{m}g_j^2}{2T}.
]

This is the exact expected wait under the stated uniform-arrival and
deterministic-service assumptions. For perfectly regular headways (h), it
reduces to (h/2). Uneven service increases expected wait relative to a
regular schedule with the same mean interval because the squared gaps give
long intervals disproportionate influence.

The implementation includes the partial intervals from service-window start
to first departure and from last departure to service-window end. With no
departures, it returns an explicit no-service result rather than a numeric
wait estimate.

## Implementation

The Python reference implementation accepts numeric times in a consistent
unit, sorts departures, validates uniqueness and service-window membership,
and reports departure count, consecutive headways, mean/median headway,
headway coefficient of variation, boundary-inclusive wait intervals and
expected wait. Extended service-day times above 24:00 are valid numeric
values.

## Limitations

This is not a GTFS parser or a complete frequency-based accessibility model.
It does not combine routes, stops, transfers, walking, in-vehicle time,
capacity, passenger demand profiles, reliability or real-time delay data.
The uniform-arrival assumption is inappropriate when passenger arrivals are
timetable-coordinated or demand varies materially within the service window.

## References and derivation

The expected-wait expression is derived directly by integrating the linear
time-to-next-departure function over each interval. Headway and service
frequency are standard public-transport service descriptors; see the Transit
Capacity and Quality of Service Manual, TCRP Report 165 (Transportation
Research Board, 2013), for the broader service-quality context.

## Reproducibility

Run `python -m pytest -q` in the package directory. Tests cover regular and
irregular headways, boundary intervals, extended service-day times, one-trip
and no-service windows, and invalid schedule inputs.
