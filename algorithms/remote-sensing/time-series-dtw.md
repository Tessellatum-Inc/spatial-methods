# Dynamic time warping and time-weighted DTW

Dynamic time warping aligns ordered sequences by minimizing accumulated local distance along a monotone path. The reference implementation uses Euclidean distance for univariate or multivariate observations and supports an optional Sakoe-Chiba index window.

Time-weighted DTW adds a logistic temporal mismatch penalty:
\[
p(\Delta t)=\frac{1}{1+\exp[-\alpha(|\Delta t|-\beta)]}.
\]
Timestamps must use a common numeric unit and be non-decreasing. Calibrate alpha and beta to that unit and application.

See the [implementation](../../implementations/python/time-series-dtw/README.md) and [tests](../../implementations/python/time-series-dtw/test_dtw.py).

The package is a distance baseline, not a trained classifier. It does not implement TempCNN, Transformer, InceptionTime, TimeMatch, missing-data imputation, sensor harmonization or benchmark reproduction. Unconstrained warping can create implausible alignments; a window limits but does not eliminate this risk.
