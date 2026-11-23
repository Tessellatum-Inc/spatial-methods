# Spatial-lag Anderson–Rubin confidence-set inversion

Stable ID: SA-STAT-SPATIAL-LAG-AR-CONFIDENCE · Teaching implementation

## Purpose

The Anderson–Rubin test evaluates a proposed spatial-lag coefficient without relying on strong first-stage instruments for its null-size argument. Inverting it gives a confidence set that can be disconnected, empty, or unbounded.

## Inversion

For each candidate rho, form y0 = y - rho Wy, regress on [X, WX, ..., W^qX], and test joint exclusion of the added spatial instruments. Retain candidates whose selected test statistic does not exceed the supplied critical value.

- Classical partial F: exact under iid homoskedastic Gaussian linear-model assumptions.
- HC1 robust Wald chi-square: asymptotic under independent-observation sampling; not spatial-HAC robust.
- Instrument validity remains essential.

## Grid approximation and limits

The implementation evaluates a caller-supplied, strictly increasing rho grid. Adjacent accepted grid points are reported as connected segments. Endpoints are grid approximations, not refined roots. A segment touching a grid edge is explicitly marked as grid-limited, so expand the search before treating it as a finite endpoint. The caller supplies a critical value matching the selected statistic. Disconnected components are retained rather than collapsed into one interval.

## Python example

~~~python
from spatial_lag_ar_confidence import spatial_lag_ar_confidence_set

result = spatial_lag_ar_confidence_set(
    y, X, W, np.linspace(-0.8, 0.8, 161),
    critical_value=3.84, test="robust",
)
print(result.segments)
~~~

## Repository implementation

- Implementation: ../../implementations/python/spatial-econometrics/spatial_lag_ar_confidence.py
- Candidate test: ../../implementations/python/spatial-econometrics/spatial_lag_anderson_rubin.py
- Tests: ../../implementations/python/spatial-econometrics/test_spatial_econometrics.py
- Related algorithm: spatial-lag-anderson-rubin.md
