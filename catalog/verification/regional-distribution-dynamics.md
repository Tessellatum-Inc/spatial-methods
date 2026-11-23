# Source verification — regional distribution dynamics

## Identity and bibliography
- Rey (2001), “Spatial Empirics for Economic Growth and Convergence,” *Geographical Analysis* 33(3), 195–214, DOI 10.1111/j.1538-4632.2001.tb00444.x.
- Rey & Janikas (2005), “Regional convergence, inequality, and space,” *Journal of Economic Geography* 5(2), 155–176, DOI 10.1093/jnlecg/lbh044.
- Anselin (1995), “Local Indicators of Spatial Association—LISA,” *Geographical Analysis* 27(2), 93–115, DOI 10.1111/j.1538-4632.1995.tb00338.x.

## Technical and implementation scope
Implemented: pooled-quantile first-order Markov transitions; spatial Markov transitions conditioned on a row-standardized lag class; descriptive Moran-quadrant transitions; sigma-dispersion summaries. The code is a transparent teaching baseline, not a reproduction of every statistic or empirical result in the cited studies.

Not implemented: beta-convergence regressions, conditional convergence, spatial panel econometrics, continuous transition-density estimation, formal stationarity tests, uncertainty intervals, permutation significance for local Moran statistics, LISA multiple-testing correction or causal identification.

## Reproduction
Tests are authored for transition counts, row normalization, spatial conditioning, LISA states, sigma-dispersion and invalid inputs. Repository CI/test status must be checked separately; authoring tests is not evidence that they have passed.

## Rights
Bibliographic metadata and original explanatory text only. No source figures, article text or data are reproduced.
