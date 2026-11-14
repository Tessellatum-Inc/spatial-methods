# Forecast verification: contingency, probabilistic and neighborhood baselines

Forecast verification asks whether predictions agree with independent verifying observations. Metrics answer different questions and should not be collapsed into a single ranking.

## Categorical event verification

After thresholding forecast and observed values, the contingency table contains hits (H), misses (M), false alarms (F) and correct negatives (C). This package reports:

\[
\mathrm{POD}=\frac{H}{H+M},\quad
\mathrm{FAR}=\frac{F}{H+F},\quad
\mathrm{CSI}=\frac{H}{H+M+F}.
\]

The equitable threat score (ETS) adjusts the hit count by the random-hit expectation
\[
H_r=\frac{(H+M)(H+F)}{H+M+F+C},\qquad
\mathrm{ETS}=\frac{H-H_r}{H+M+F-H_r}.
\]
POD measures event detection, FAR the fraction of forecast events that are false, CSI the overlap of event detections, and ETS adjusts for hits expected by chance. POD and FAR can be misleading when reported without event frequency and sample size.

## Probabilistic verification

For binary outcomes \(o_i\in\{0,1\}\) and forecast probabilities \(p_i\), the Brier score is
\[
\mathrm{BS}=\frac{1}{N}\sum_i(p_i-o_i)^2.
\]
It is a proper score that reflects both calibration and refinement/resolution; it should not be interpreted as a pure discrimination measure. ROC AUC is implemented as a rank statistic with average ranks for ties. It measures discrimination and does not assess calibration.

## Neighborhood verification and FSS

Fractions Skill Score (FSS) thresholds forecast and observed fields, computes the fraction of event cells in a square neighborhood around each grid cell, then compares the fraction fields:
\[
\mathrm{FSS}=1-\frac{\mathrm{FBS}}{\mathrm{FBS}_{\mathrm{worst}}},
\quad
\mathrm{FBS}=\frac{1}{N}\sum_i(f_i-o_i)^2,
\quad
\mathrm{FBS}_{\mathrm{worst}}=\frac{1}{N}\sum_i(f_i^2+o_i^2).
\]
Here \(f_i\) and \(o_i\) are forecast and observed neighborhood event fractions. FSS ranges from zero to one when its denominator is positive. It is scale-dependent: report the threshold, neighborhood geometry/size, grid spacing and domain. A high score at a large neighborhood does not mean the forecast is accurate at the native grid scale.

For ensemble forecasts, the [Python package](../implementations/python/forecast-verification/README.md) also includes empirical-ensemble CRPS and a tie-aware rank histogram. CRPS is a proper score for the predictive distribution; rank histograms diagnose ensemble calibration but can be misleading when dependence, observation error or sample dependence is ignored. The package implements square clipped neighborhoods at boundaries and assumes both grids have already been aligned. It does not implement object-based SAL/MODE, CRPS decomposition, spatial uncertainty intervals or significance tests.

## Sources

- Roberts, N. M., & Lean, H. W. (2008). “Scale-Selective Verification of Rainfall Accumulations from High-Resolution Forecasts of Convective Events.” *Monthly Weather Review*, 136, 78–97. [Paper](https://centaur.reading.ac.uk/31220/1/Roberts2008a.pdf). FSS.
- Brier, G. W. (1950). “Verification of Forecasts Expressed in Terms of Probability.” *Monthly Weather Review*, 78, 1–3. DOI: [10.1175/1520-0493(1950)078<0001:VOFEIT>2.0.CO;2](https://doi.org/10.1175/1520-0493(1950)078%3C0001:VOFEIT%3E2.0.CO;2). Brier score.
- Wilks, D. S. (2011). *Statistical Methods in the Atmospheric Sciences*, 3rd ed. Academic Press. Categorical and probabilistic verification definitions.

No source text or figures are reproduced.
