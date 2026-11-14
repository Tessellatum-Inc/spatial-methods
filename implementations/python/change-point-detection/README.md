# Change-point detection teaching package

Dependency-free univariate baselines for **mean changes**:

- **CUSUM:** two-sided tabular cumulative-sum alarm detector.
- **Binary segmentation:** greedy recursive split selection using reduction in within-segment squared error.
- **PELT:** penalized optimal partitioning with pruning for squared-error segment cost.

## Run

From this directory:

```bash
python -m pytest -q
```

## Scope and limitations

The methods assume an ordered, one-dimensional series. The segmentation methods use piecewise-constant segment means and squared-error loss; they do not detect every possible change in variance, trend, seasonality, distribution or spatial dependence. Binary segmentation is greedy and need not find the global optimum. PELT minimizes the specified penalized objective; its linear expected complexity depends on conditions and its worst case is quadratic. The implementation disables pruning for minimum segment lengths above one, using exact O(n²) dynamic programming in that constrained case. Penalty selection is a modelling decision, not automatic statistical calibration. CUSUM's threshold and drift are in raw data units here and require domain-specific calibration.

For spatial or Earth-observation time series, account for seasonality, missing observations, sensor changes, spatial dependence, multiple testing and acquisition artefacts before interpreting a detected boundary as a real process change. This package is a transparent teaching baseline, not a production monitoring system.
