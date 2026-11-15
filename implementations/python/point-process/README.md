# Planar point-pattern summaries

Dependency-free functions for a small subset of spatial point-process analysis:

- Nearest-neighbor distances and their empirical CDF.
- Homogeneous Ripley's K estimator with rectangular translation edge correction.
- Inhomogeneous K with externally supplied pointwise intensities and rectangular translation correction.
- A finite-difference pair-correlation estimate from K(r).

Run with `python -m pytest -q` from this directory.

## Assumptions and limitations

Coordinates must be planar, in a consistent linear unit, and observed in a rectangular window. The homogeneous K estimator assumes stationarity/homogeneity and isotropy. The inhomogeneous estimator requires one strictly positive intensity estimate per observed point and assumes second-order intensity-reweighted stationarity; it does not fit an intensity surface or select its bandwidth. Pair correlation is obtained by numerical differentiation and is sensitive to radius spacing/noise. There are no Monte Carlo envelopes, CSR tests, automatic intensity estimation, bandwidth selection, polygon-window corrections, Palm distributions or spatiotemporal statistics. Use a maintained point-process package for inferential analysis and complex observation windows.
