# Forecast verification baselines

Dependency-free, transparent implementations for a small subset of the Section 10 verification inventory:

- **Contingency table:** hits, misses, false alarms, correct negatives, probability of detection (POD), false alarm ratio (FAR), critical success index (CSI), and equitable threat score (ETS).
- **Brier score:** mean squared error of binary-event probabilities.
- **ROC AUC:** rank-based area under the receiver operating characteristic curve, with average ranks for tied scores.
- **Fractions Skill Score (FSS):** thresholded fields compared through square-neighborhood event fractions, including gridpoint radius zero.

Run from this directory with `python -m pytest -q`.

## Contracts and limitations

Inputs must already be spatially aligned and comparable. FSS uses clipped neighborhoods at domain edges; it does not reproject, regrid, mask missing cells, or account for irregular grid spacing. The FSS zero-denominator convention returns 1 when both fields contain no event; this edge case should be reported explicitly in applied work. The implementation returns the score only, not a recommended skillful scale or universal usefulness threshold.

POD is undefined when no observed events occur; FAR is undefined when no forecast events occur; CSI and ETS can also be undefined for degenerate samples, represented by `None`. The Brier score requires binary outcomes. ROC AUC requires both outcome classes and measures ranking discrimination, not probability calibration.

These are teaching baselines, not a complete forecast-verification suite. SAL, MODE/object-based verification, CRPS and rank histograms, spatial uncertainty, temporal dependence, confidence intervals, and neighborhood/scale sensitivity remain outside this package.
