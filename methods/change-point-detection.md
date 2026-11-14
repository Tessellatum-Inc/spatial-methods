# Change-point detection for ordered spatial observations

A change point is a boundary at which the data-generating behaviour changes. For a univariate sequence, the boundary convention in this package is the **0-based index of the first observation in the new segment**. The package implements three distinct approaches for piecewise-constant mean changes; they should not be treated as interchangeable tests.

## Objective and segment cost

For observations (y_0,\ldots,y_{n-1}), a segmentation with boundaries (0=\tau_0<\tau_1<\cdots<\tau_m<\tau_{m+1}=n) can minimize

\[
\sum_{j=0}^{m} C(y_{\tau_j:\tau_{j+1}})+\beta m,
\qquad
C(y_{a:b})=\sum_{i=a}^{b-1}(y_i-\bar y_{a:b})^2.
\]

The segment cost is within-segment squared error (SSE), and \(\beta\) penalizes additional boundaries. The penalty, minimum segment length and cost model are substantive modelling choices.

## Three methods

- **CUSUM:** accumulates deviations above and below a target and signals when a running sum crosses a threshold. It is useful for sequential monitoring. The teaching implementation uses a user-supplied target (or sample mean by default), raw-unit threshold and drift. It is not a calibrated hypothesis test and resets the accumulator after each alarm.
- **Binary segmentation:** finds the split with the greatest SSE reduction, then recursively repeats within the resulting segments. It is fast and interpretable, but greedy; early splits constrain later ones and it can miss closely spaced changes.
- **PELT:** dynamic programming minimizes the penalized segmentation objective and prunes candidate previous boundaries under a valid cost-function condition. This package uses the K=0 pruning condition for the SSE mean-shift cost. Expected linear time is possible under regularity conditions; worst-case time remains quadratic. It returns an optimal segmentation for the specified objective when the pruning condition applies, not a universally correct set of real-world events.

## Reproducible implementation

See [the dependency-free Python package](../implementations/python/change-point-detection/README.md) for the algorithms and tests. The package deliberately limits itself to finite univariate data, piecewise-constant means and SSE. It does not implement variance changes, trend/seasonal changes, multivariate changes, missing-data models, online Bayesian inference, BEAST, or spatially coupled change detection.

## Spatial and Earth-observation interpretation

A detected boundary in a satellite-derived time series may reflect a real land-surface transition, but it may also arise from sensor/platform changes, atmospheric correction, cloud/shadow contamination, compositing windows, seasonality, phenology, spatial aggregation, missingness or changes in sampling support. Before interpreting a boundary:

1. harmonize sensor and processing versions;
2. model or remove seasonal structure where appropriate;
3. inspect quality flags and missing-observation patterns;
4. test sensitivity to minimum segment length and penalty;
5. compare with independent observations or known interventions;
6. account for spatial dependence and the multiplicity of testing many pixels.

Do not map every per-pixel alarm as an independent event without controlling spatial/temporal dependence and false discoveries.

## Sources

- Page, E. S. (1954). “Continuous Inspection Schemes.” *Biometrika*, 41(1/2), 100–115. DOI: [10.1093/biomet/41.1-2.100](https://doi.org/10.1093/biomet/41.1-2.100). Foundational CUSUM reference.
- Scott, A. J., & Knott, M. (1974). “A Cluster Analysis Method for Grouping Means in the Analysis of Variance.” *Biometrics*, 30(3), 507–512. DOI: [10.2307/2529204](https://doi.org/10.2307/2529204). Early binary segmentation reference.
- Killick, R., Fearnhead, P., & Eckley, I. A. (2012). “Optimal Detection of Changepoints With a Linear Computational Cost.” *Journal of the American Statistical Association*, 107(500), 1590–1598. DOI: [10.1080/01621459.2012.737745](https://doi.org/10.1080/01621459.2012.737745). PELT and penalized optimal partitioning.

The references establish the method families; they do not validate this teaching implementation for every data-generating process. No paper figures or text are reproduced here.
