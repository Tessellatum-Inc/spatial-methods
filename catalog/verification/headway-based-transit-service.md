# Verification record — transit headway and expected waiting time

## Identity and scope

This record covers a deterministic timetable-derived headway summary and the
expected waiting time for passengers arriving uniformly during a declared
service window. It is not a GTFS implementation or a complete transit
accessibility model.

## Mathematical check

For an interval of length (g), passenger arrival time is uniform on the
interval and the wait until its ending departure decreases linearly from
(g) to zero. The integrated wait is (g^2/2). Summing over all intervals
and dividing by the full service-window duration (T) yields
(E[W]=\sum g_i^2/(2T)). The initial and final partial intervals are
included, so the result is not biased by assuming a departure exactly at each
window boundary.

For equal intervals (h), the expression reduces to (h/2). For unequal
intervals it weights long gaps quadratically. This is a mathematical
derivation under uniform passenger arrivals and deterministic departures,
not a claim about timetable-coordinated arrivals or stochastic operations.

## Implementation and tests

Implemented in `implementations/python/transit-headway/transit_headway.py`.
The independent test module covers:

- Regular 10-minute service and the 5-minute expected-wait result.
- Unequal 5- and 15-minute intervals and the 6.25-minute expected wait.
- Initial and terminal partial intervals.
- Sorting and GTFS extended service-day times.
- A single departure and a no-service window.
- Duplicate, out-of-window, non-finite and non-numeric inputs.

## Known gaps

GTFS parsing, service calendars, frequency-based trips with `exact_times=0`,
route/stop aggregation, transfers, network accessibility, passenger demand
profiles, capacity constraints, stochastic delays and real-time updates are
not implemented. This method is a transparent component, not a complete
transit service analysis workflow.

## Rights

The code and prose are original reference material based on the stated
mathematical derivation. No GTFS feed, proprietary source code, figures or
third-party text are reproduced.
