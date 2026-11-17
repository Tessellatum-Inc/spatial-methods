# Variogram models and directional analysis

This package adds four theoretical semivariogram families (spherical,
exponential, Gaussian and Matérn), weighted nonlinear least-squares and dense restricted-maximum-likelihood
(REML) fitting of nugget, partial sill and range, directional pair filtering, and Matheron, Cressie-Hawkins, Dowd and Genton empirical estimators. It also supports fixed or REML-estimated geometric anisotropy (major-axis azimuth and minor/major range ratio). Genton uses
the Q_n order statistic of pairwise differences among increments within each
lag class; it requires at least two point pairs in a class and is quadratic
in the number of pairs in that class.

Azimuth is clockwise from north and is treated as undirected modulo 180°.
Coordinate units determine lag, range and bandwidth units. Pair-count weights
are used in fitting; they are a pragmatic teaching default, not a universal
statistical optimum. Model choice and lag design remain analyst decisions. Optional anisotropy estimation jointly searches azimuth and minor/major range ratio, constrained to [0.1, 1]. REML assumes a constant
unknown mean and an isotropic Gaussian covariance; it is a dense small-data
baseline, not a scalable likelihood engine.

Run pytest -q in this directory.


The Matérn model accepts a fixed smoothness parameter nu (default 1.5); the covariance is evaluated with the modified Bessel function. The range parameter is the Matérn scale, not the practical-range convention used by the spherical/exponential/Gaussian forms.
