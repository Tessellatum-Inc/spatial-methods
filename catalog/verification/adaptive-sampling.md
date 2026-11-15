## Adaptive sampling source check

- **UCB1:** Auer, P., Cesa-Bianchi, N., & Fischer, P. (2002), “Finite-time Analysis of the Multiarmed Bandit Problem,” *Machine Learning* 47, 235–256, DOI 10.1023/A:1013689704352. The package implements the basic UCB1 index for stationary bounded-reward arms; contextual/cost-aware/nonstationary variants are not implied. It also implements finite-candidate RBF Gaussian-process regression with Cholesky solves and UCB/EI acquisition; this is a small dense baseline, not a scalable spatial GP.
- **Active learning:** Settles, B. (2009), “Active Learning Literature Survey,” University of Wisconsin–Madison Technical Report 1648. Used as a broad survey reference, not as a source for the specific greedy spatial acquisition heuristic.
- **Implementation boundary:** uncertainty-plus-nearest-selected-distance is an explicit greedy heuristic; it is not Gaussian-process Bayesian optimization, adaptive cluster sampling, or a statistically representative map-validation design.
- **Rights:** metadata and links only; no source text or figures copied.
- **Status:** core reference identities checked; implementation and regression tests authored; deterministic local smoke checks for spatial selection, UCB1, GP-UCB, expected improvement and duplicate-observation jitter passed; repository CI and independent review pending.
