# Variogram models and directional analysis

This package adds three theoretical semivariogram families (spherical,
exponential and Gaussian), weighted nonlinear least-squares fitting of nugget,
partial sill and range, directional pair filtering, and both Matheron and
Cressie-Hawkins empirical estimators.

Azimuth is clockwise from north and is treated as undirected modulo 180°.
Coordinate units determine lag, range and bandwidth units. Pair-count weights
are used in fitting; they are a pragmatic teaching default, not a universal
statistical optimum. Model choice, lag design, anisotropy diagnostics and
uncertainty estimation remain analyst decisions.

Run pytest -q in this directory.
