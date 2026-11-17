# Source verification — space-time K-function

## Identity and bibliography
- Diggle et al. (1995), “Second-order analysis of space-time clustering,” *Statistical Methods in Medical Research*, 4(2), 124–136. DOI 10.1177/096228029500400203.
- Ohser (1983), “On estimators for the reduced second moment measure of point processes,” *Mathematical Operationsforschung und Statistik*, 14, 63–71.

## Technical claims
- The K-function summarizes event-pair counts within spatial and temporal separation thresholds.
- Rectangular translation correction weights pairs by reciprocal spatial and temporal overlap fractions.
- Temporal lag is symmetric and absolute.

## Implementation and tests
- NumPy pairwise estimator with rectangular spatial and temporal translation correction.
- Tests cover a hand-computed two-event weight, monotonicity in radius/time lag, event-order invariance and invalid inputs.

## Limits and rights
Homogeneous stationary rectangular-window baseline; zero-overlap pairs are omitted. No inhomogeneous, marked, anisotropic or irregular-window correction. Original code and explanatory text; bibliographic metadata only.
