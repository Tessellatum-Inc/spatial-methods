# Headway-based transit service and expected waiting time

- **Kind:** transit service metric
- **Domain:** public transport operations and accessibility
- **Status:** deterministic timetable baseline with optional piecewise-constant passenger arrival rates
- **Version:** 0.2

## Headway summaries

For ordered departure times, consecutive headways are differences between adjacent departures. Report mean, median and population coefficient of variation when at least two headways are available. These describe the timetable, not passenger waiting time.

## Expected wait

For uniformly arriving passengers over a service window, let g_j be the positive intervals between the window boundaries and departures. Integrating the linearly decreasing time-to-next-departure over each interval gives:

\[
E[W]=\frac{\sum_j g_j^2}{2T}.
\]

Boundary intervals are included. For equal intervals h, this reduces to h/2.

## Piecewise-constant arrival rates

When passenger arrival intensity differs across the window, assign a non-negative relative rate r_j to each positive interval g_j. Assuming a constant rate within each interval:

\[
E[W]=\frac{\sum_j r_j g_j^2/2}{\sum_j r_j g_j}.
\]

Rates need not sum to one. Scaling every rate by the same positive constant leaves the result unchanged. Zero-rate intervals contribute no passengers. If all rates are zero, expected wait is undefined and the implementation returns None. This is a coarse demand profile, not an estimate of arrival rates from observed passengers.

## Scope and limitations

The Python implementation accepts numeric times, supports extended service-day values, validates unique departures and service-window membership, and reports headways, boundary-inclusive intervals and expected wait. It does not parse GTFS, combine routes/stops/transfers, model capacity, estimate passenger arrival profiles, or represent stochastic delays and real-time operations. State the arrival assumptions with every reported estimate.
