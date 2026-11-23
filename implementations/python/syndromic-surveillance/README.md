# Syndromic surveillance reference detectors

Pure-Python sequential monitoring primitives for univariate count series.

## Included methods

- Two-sided tabular CUSUM with user-supplied target, allowance and decision
  threshold.
- EARS-style C1, C2 and C3 scores with explicit baseline windows, variance
  floor and configurable alert threshold.

## EARS score contract

C1 compares the current count with the immediately preceding baseline window.
C2 compares it with a baseline window ending a configurable number of
observations before the current day (default two). Scores standardize the
excess over the baseline mean using the maximum of sample standard deviation,
square root of the baseline mean and one. C3 sums the positive C2 scores over
the current and previous two days. Values are unavailable until the relevant
baseline exists.

This is a transparent educational EARS-style variant. Operational EARS
implementations differ in details and should be checked against the selected
surveillance protocol. The package includes a bounded Farrington-style seasonal quasi-Poisson exceedance baseline, but does not implement the full original GLIM or improved Noufaily variants. Weekday/seasonality adjustment, population offsets, covariate adjustment,
spatial scan statistics or space-time cluster detection.

## CUSUM calibration

CUSUM's target, reference allowance and threshold are explicit inputs. The
package does not estimate an in-control distribution, select an average-run-
length target or calibrate thresholds for a particular disease or reporting
system. Count autocorrelation, reporting delays and changing denominators
must be handled by the analyst.

## Run

    python -m pytest -q

Only the Python standard library is required at runtime; pytest is the test
runner.


The Farrington-style routine samples the same seasonal window from prior cycles, fits a log-linear trend by IRLS, optionally downweights large historical residuals, estimates Pearson overdispersion and computes a cube-root normal upper prediction approximation. It is intentionally not represented as an exact reproduction of Farrington (1996) or Noufaily et al. (2013); see the algorithm record for assumptions and limitations.
