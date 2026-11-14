# Planar point-pattern summaries

Dependency-free functions for a small subset of spatial point-process analysis:

- Nearest-neighbor distances and their empirical CDF.
- Homogeneous Ripley's K estimator with rectangular translation edge correction.
- A finite-difference pair-correlation estimate from K(r).

Run with `python -m pytest -q` from this directory.

## Assumptions and limitations

Coordinates must be planar, in a consistent linear unit, and observed in a rectangular window. The K estimator assumes a stationary homogeneous process and isotropy; it is not an inhomogeneous K estimator. Pair correlation is obtained by numerical differentiation and is sensitive to radius spacing/noise. There are no Monte Carlo envelopes, CSR tests, bandwidth selection, intensity estimation, polygon-window corrections, Palm distributions or spatiotemporal statistics. Use a maintained point-process package for inferential analysis and complex observation windows.
