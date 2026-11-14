## Change-point detection source check

- **Page (1954), CUSUM:** Page, E. S. “Continuous Inspection Schemes,” *Biometrika* 41(1/2), 100–115. DOI 10.1093/biomet/41.1-2.100. Canonical bibliographic identity checked against the DOI record; the package implements a simple two-sided tabular accumulator, not a reproduction of every Page scheme or its operating-characteristic derivation.
- **Scott & Knott (1974), binary segmentation:** “A Cluster Analysis Method for Grouping Means in the Analysis of Variance,” *Biometrics* 30(3), 507–512. DOI 10.2307/2529204. Used as an early reference for recursive mean segmentation. Later literature also attributes related formulations to Edwards & Cavalli-Sforza and Sen & Srivastava; do not imply a single exclusive origin.
- **Killick, Fearnhead & Eckley (2012), PELT:** “Optimal Detection of Changepoints With a Linear Computational Cost,” *JASA* 107(500), 1590–1598. DOI 10.1080/01621459.2012.737745. The package implements the SSE mean-shift objective with K=0 pruning; linear expected complexity is conditional, with quadratic worst case.
- **Implementation scope:** finite univariate observations, piecewise-constant mean, SSE segment cost. CUSUM threshold calibration, penalty selection, spatial dependence, seasonality, sensor discontinuities and missingness remain outside the package.
- **Rights:** bibliographic metadata and DOI links only; no article text or figures copied.
- **Status:** identity and core bibliography checked; technical scope documented; local tests authored. CI execution and independent code review still pending.
