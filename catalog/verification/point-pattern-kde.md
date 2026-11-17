# Source verification — adaptive planar kernel density estimation

## Identity and source scope

The source entry groups adaptive/variable-bandwidth kernel density estimation,
Silverman's bandwidth rule and cross-validated bandwidth selection. These are
related but distinct choices: a pilot density determines local bandwidths,
a normal-reference rule supplies a global starting scale, and cross-validation
scores candidate global bandwidths against held-out events.

## Implemented scope

The dependency-light Python package provides:
- fixed-bandwidth isotropic bivariate Gaussian intensity estimation;
- Abramson-style sample-point adaptation using leave-one-out pilot densities,
  a geometric-mean reference and configurable bandwidth-factor clipping;
- Silverman's isotropic bivariate normal-reference bandwidth
  \(h=s n_{eff}^{-1/6}\), with pooled RMS coordinate spread and Kish
  effective sample size;
- weighted leave-one-out log-likelihood selection over a caller-supplied
  candidate grid.

The package includes a reproducible teaching notebook, implementation
walkthrough, analytic tests and direct-oracle comparisons.

## Independent verification

Tests compare:
- fixed and adaptive surfaces against direct Gaussian-kernel calculations;
- the LOO candidate scores against an independently written nested-loop
  calculation;
- Silverman's rule against the bivariate formula and weighted effective
  sample-size calculation;
- translation invariance and coordinate-scale equivariance;
- alpha-zero equivalence, event-weight behaviour and input validation.

The Python package is registered in the repository's package CI matrix; the
notebook is executed by the repository notebook workflow.

## Limitations and remaining work

No edge correction is applied, so intensity is biased downward near a
rectangular observation-window boundary. The LOO search only evaluates the
candidate bandwidths supplied by the caller. The normal-reference rule assumes
an approximately Gaussian reference distribution. Adaptive pilot estimates
are direct O(n²) calculations and grid evaluation is O(nm); LOO selection is
O(n²c) for n events and c candidates. These methods are transparent teaching
baselines, not large-data indexed estimators. Isotropic bandwidths, planar
Euclidean distance and rectangular study windows are assumed.

## Rights

The implementation is independently written from the mathematical method
description. No source code, prose or figures are reproduced from external
sources.
