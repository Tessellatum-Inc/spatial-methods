# Change-point detection teaching package

Dependency-free univariate baselines for mean changes:

- **CUSUM:** two-sided tabular cumulative-sum alarm detector.
- **Binary segmentation:** greedy recursive split selection using reduction in within-segment squared error.
- **PELT:** penalized optimal partitioning with K=0 pruning for the unconstrained minimum segment length; when a larger minimum segment length is requested, exact unpruned dynamic programming is used to preserve the constraint.
- **BOCPD:** Bayesian online run-length inference for a Gaussian likelihood with known observation variance and an unknown segment mean under a Normal prior; see [model assumptions](online-README.md).

## Run

From this directory:

```bash
python -m pytest -q
```

## Scope and limitations

The methods assume an ordered, one-dimensional series. The segmentation methods use piecewise-constant segment means and squared-error loss; they do not detect every possible change in variance, trend, seasonality or spatial dependence. Binary segmentation is greedy and need not find the global optimum. PELT minimizes the specified penalized objective; its linear expected complexity depends on conditions and its worst case is quadratic. The implementation disables pruning for minimum segment lengths above one, using exact O(n²) dynamic programming in that constrained case.

CUSUM's threshold and drift are in raw data units here and require domain-specific calibration. BOCPD's hazard and Gaussian prior/known-variance assumptions require explicit modelling; it is not the full Student-t model commonly used in the literature.

For spatial or Earth-observation time series, account for seasonality, missing observations, sensor changes, spatial dependence, multiple testing and acquisition artefacts before interpreting a detected boundary as a real process change. This package is a transparent teaching baseline, not a production monitoring system.
