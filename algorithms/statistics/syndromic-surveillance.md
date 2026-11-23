# Syndromic surveillance: CUSUM and EARS

## Purpose

Syndromic surveillance looks for unusual changes in health-related counts
before a definitive diagnosis or final case classification is available.
Sequential detectors can flag deviations from an expected baseline, but an
alert is a signal for investigation, not proof of an outbreak or a causal
explanation.

## CUSUM

For observations x_t, target μ and non-negative reference allowance k, the
two-sided tabular CUSUM recursions are

    S_t+ = max(0, S_(t-1)+ + x_t - μ - k)
    S_t- = max(0, S_(t-1)- + μ - x_t - k)

An alarm occurs when either statistic reaches decision threshold h. The
reference implementation accepts μ, k and h from the caller. Threshold
calibration depends on the in-control process, desired false-alarm rate,
autocorrelation and reporting mechanism; no universal threshold is implied.

## EARS-style C1, C2 and C3

The package provides an explicitly specified EARS-style score family:

- C1 compares the current count with the immediately preceding baseline
  window.
- C2 compares with a baseline window ending two observations before the
  current day by default.
- C3 sums the positive C2 scores over the current and preceding two days.

The standardized score uses the baseline mean and a scale equal to the
maximum of sample standard deviation, square root of the mean and one. The
variance floor prevents division by zero and avoids an unrealistically small
scale for low counts. A score is unavailable until its baseline is complete.

This explicit implementation should not be conflated with every published
EARS operational configuration. Weekday/seasonality adjustment, overdispersion
models, population offsets, covariates and reporting-delay correction require
additional modelling and validation. Farrington's quasi-Poisson regression
detector is a separate method and is not claimed here.

## Spatial extensions

Spatial and space-time surveillance requires a defined neighbourhood or
interaction graph, population-at-risk denominators, a null model and a
multiple-testing or sequential calibration strategy. Spatial scan statistics are implemented separately in the point-process package; the univariate functions here do not replace spatial or space-time scan analysis.

## Implementation and tests

See [the Python reference package](../../implementations/python/syndromic-surveillance/README.md)
for the recursions, score definitions, edge cases and tests.

## References

- Page, E. S. (1954). Continuous Inspection Schemes. *Biometrika*, 41(1/2),
  100–115. https://doi.org/10.1093/biomet/41.1-2.100
- Fricker, R. D. Jr. (2013). *Introduction to Statistical Methods for
  Biosurveillance*. Cambridge University Press.
- Hutwagner, L. et al. (2003). The Bioterrorism Preparedness and Response
  Early Aberration Reporting System (EARS). *Journal of Urban Health*, 80,
  i89–i96. https://doi.org/10.1093/jurban/jtg041


## Farrington-style seasonal exceedance

For a weekly series, the implementation builds a reference set from the same week and neighbouring weeks in each of the preceding seasonal cycles. It fits a log-linear mean with a linear time trend using Poisson IRLS, estimates quasi-Poisson dispersion from weighted Pearson residuals, and optionally downweights large historical residuals. The one-sided upper prediction approximation uses a cube-root transform and a normal quantile. This is a small, dependency-free teaching baseline; it does not reproduce the full Farrington GLIM algorithm or the improved Noufaily flexible implementation.
