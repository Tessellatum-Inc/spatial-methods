# Dynamic and time-weighted time warping

NumPy reference implementation for ordered univariate and multivariate sequences.

Includes accumulated Euclidean dynamic time warping, an optional Sakoe-Chiba index window, a logistic temporal mismatch penalty, and optional alignment paths.

Run:
    python -m pip install -r requirements.txt
    pytest -q

Import dtw and time_weighted_dtw from dtw.py. Timestamps must share a numeric unit and be non-decreasing. The alpha and beta penalty parameters must be calibrated to that unit. Returned scores are accumulated path costs, not normalized distances.

This package implements distance baselines, not a trained classifier. It does not implement TempCNN, Transformer, InceptionTime, TimeMatch, cloud-gap imputation, sensor harmonization, probabilistic calibration, or benchmark reproduction. Complexity is quadratic without a narrow Sakoe-Chiba window.
