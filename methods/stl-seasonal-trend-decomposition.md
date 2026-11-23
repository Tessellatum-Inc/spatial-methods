# STL seasonal–trend decomposition

STL (Seasonal-Trend decomposition using Loess) decomposes an equally spaced additive series as

\[
y_t = T_t + S_t + R_t,
\]

where trend, seasonal and remainder components are estimated through a sequence of LOESS smoothers. Cleveland et al. (1990) describe smoothing detrended seasonal subseries, removing low-frequency leakage with a low-pass filter, smoothing the deseasonalized series to estimate trend, and iterating. Robust iterations derive bisquare weights from the remainder so isolated aberrant observations have less influence.

## Implemented teaching baseline

The companion dependency-free Python package implements a compact additive STL-style filter with local-linear LOESS and tricube distance weights, cycle-subseries smoothing, a moving-average low-pass sequence, iterative backfitting and optional outer bisquare robustness weights. See the [code and tests](../implementations/python/temporal-models/README.md).

It requires at least two complete cycles, finite equally spaced observations and an integer period. It does not support missing values, irregular timestamps, multiplicative decomposition, calendar effects, automatic parameter selection or the full set of jump/degree controls in the original algorithm. Endpoint handling and compact defaults are pedagogical choices; use a mature implementation such as R stats::stl for production analysis.

## Interpretation and spatial-data cautions

The period is a sample count: monthly data with annual seasonality has period 12; daily data with weekly seasonality has period 7. Seasonal and trend windows determine how quickly each component can evolve. A poor period or overly flexible smoother can move signal between trend, seasonal and remainder. For Earth-observation series, harmonize sensors, inspect acquisition gaps/cloud masks and avoid treating a decomposition component as a causal explanation. This baseline rejects missing observations rather than silently interpolating them.

## Sources

- Cleveland, R. B., Cleveland, W. S., McRae, J. E., & Terpenning, I. (1990). “STL: A Seasonal-Trend Decomposition Procedure Based on Loess.” Journal of Official Statistics, 6(1), 3–73. [Statistics Sweden PDF](https://www.scb.se/contentassets/ca21efb41fee47d293bbee5bf7be7fb3/stl-a-seasonal-trend-decomposition-procedure-based-on-loess.pdf).
- R Core Team. [stats::stl documentation](https://stat.ethz.ch/R-manual/R-devel/library/stats/html/stl.html).

No source text or figures are reproduced.
