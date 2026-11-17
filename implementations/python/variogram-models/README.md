# Variogram models and directional analysis

This package adds three theoretical semivariogram families (spherical,
exponential and Gaussian), weighted nonlinear least-squares and dense restricted-maximum-likelihood
(REML) fitting of nugget, partial sill and range, directional pair filtering, and Matheron, Cressie-Hawkins, Dowd and Genton empirical estimators. It also supports fixed geometric anisotropy (major-axis azimuth and minor/major range ratio) in directional binning and REML covariance fitting. Genton uses
the Q_n order statistic of pairwise differences among increments within each
lag class; it requires at least two point pairs in a class and is quadratic
in the number of pairs in that class.

Azimuth is clockwise from north and is treated as undirected modulo 180°.
Coordinate units determine lag, range and bandwidth units. Pair-count weights
are used in fitting; they are a pragmatic teaching default, not a universal
statistical optimum. Model choice, lag design, anisotropy parameter estimation and
uncertainty estimation remain analyst decisions. REML assumes a constant
unknown mean and an isotropic Gaussian covariance; it is a dense small-data
baseline, not a scalable likelihood engine.

Run pytest -q in this directory.
