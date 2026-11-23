# Inverse-distance weighting (IDW)

Dependency-free planar interpolation from point samples. For query q, each
sample i receives weight w_i = d(q,i)^(-p), normalized to sum to one. The
default power is p=2. Optional maximum-neighbour and radius controls bound
the contributing sample set.

An exact query/sample coordinate match returns the mean of all observations
at that coordinate, avoiding division by zero. If a radius is supplied and
no sample falls within it, the prediction is None. Neighbour ties are stable
by original sample order.

## Limits

IDW is deterministic but is not a geostatistical covariance model. It does
not estimate a variogram, kriging weights, prediction variance, anisotropy,
barriers, network distances, nonstationary trends or uncertainty intervals.
Coordinate units and projection are the caller's responsibility; Euclidean
distance in longitude/latitude degrees is generally inappropriate for
regional work.

## Tests

    python -m pytest -q
