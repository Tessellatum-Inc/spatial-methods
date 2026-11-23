# Verification record — transit headway and expected waiting time

## Scope
Deterministic timetable-derived headway summaries and passenger expected wait under uniform or supplied piecewise-constant arrival rates. This is not a GTFS parser or full transit accessibility model.

## Mathematical check
For an interval g, time-to-next-departure decreases linearly from g to zero, so the integrated wait area is g^2/2. At constant relative arrival rate r, passenger-weighted wait area is r*g^2/2 and total arrival weight is r*g. Therefore:

\[
E[W]=\frac{\sum_j r_j g_j^2/2}{\sum_j r_j g_j}.
\]

Setting all rates to one recovers the uniform-arrival expression because positive intervals partition the service window. Scaling all rates equally does not change the result.

## Implementation and tests
Implemented in implementations/python/transit-headway/transit_headway.py. Tests cover regular and irregular schedules, boundary intervals, extended service-day times, piecewise rates, equivalence to uniform rates, zero-rate behavior, invalid rates and invalid schedules. The package is in the Python CI matrix. A passing CI run remains required for environment verification.

## Gaps
GTFS parsing, service calendars, route/stop aggregation, transfers, network accessibility, empirical arrival profiles, capacity, stochastic delays and real-time updates remain outside scope.
