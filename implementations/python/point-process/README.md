# Planar point-pattern summaries

Dependency-free functions for a small subset of spatial point-process analysis:

- Nearest-neighbor distances and their empirical CDF.
- Homogeneous Ripley's K estimator with rectangular translation edge correction.
- Inhomogeneous K with externally supplied pointwise intensities and rectangular translation correction.
- Circular Poisson spatial scan statistic for areal case counts with a population offset and conditional multinomial Monte Carlo p-value.
- A finite-difference pair-correlation estimate from K(r).
- A conditional multinomial Monte Carlo quadrat-count test for homogeneous complete spatial randomness (CSR).

Run with `python -m pytest -q` from this directory.

## Quadrat test interpretation

The quadrat test conditions on the observed point count and compares equal-area cell counts with a uniform multinomial null. It uses a one-sided upper-tail Pearson statistic with a plus-one Monte Carlo p-value, so it avoids relying on a large-expected-count chi-square approximation. Grid dimensions and origin are analyst choices; the test is scale-dependent and cannot distinguish interaction from first-order intensity variation. It is not a multi-scale replacement for K or an inhomogeneous point-process model.

## Assumptions and limitations

Coordinates must be planar, in a consistent linear unit, and observed in a rectangular window. The homogeneous K estimator assumes stationarity/homogeneity and isotropy. The inhomogeneous estimator requires one strictly positive intensity estimate per observed point and assumes second-order intensity-reweighted stationarity; it does not fit an intensity surface or select its bandwidth. Pair correlation is obtained by numerical differentiation and is sensitive to radius spacing/noise. There are no K-function Monte Carlo envelopes, automatic intensity estimation, bandwidth selection, polygon-window corrections, Palm distributions, non-circular scan windows, scan covariates, temporal scanning or secondary-cluster extraction. Use a maintained point-process package for inferential analysis and complex observation windows.
