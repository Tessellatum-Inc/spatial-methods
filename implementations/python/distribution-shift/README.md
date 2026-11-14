# Spatial distribution-shift statistics

NumPy/SciPy teaching implementations of:
- unbiased squared maximum mean discrepancy (MMD) with a Gaussian RBF kernel;
- unbiased sample energy-distance statistic;
- a reproducible permutation test for MMD (independent/exchangeable rows only);
- a nearest-neighbour predictor-space applicability envelope, calibrated by leave-one-out training distances, with optional feature weights.

Inputs are finite feature matrices with matching dimensions. MMD bandwidth is in feature-space units; standardise features deliberately and report the choice. Both unbiased finite-sample U-statistics can be negative and are not clipped; do not interpret an individual estimate as a guaranteed non-negative distance.

The permutation test assumes exchangeable independent rows. It is not valid for spatially autocorrelated samples without a defensible block/cluster permutation or other spatial null design. The applicability-envelope function is a transparent nearest-neighbour teaching baseline, not an exact Meyer–Pebesma AOA implementation or prediction-error guarantee. It does not use model-derived variable importance or a spatially calibrated threshold. Domain classifiers, kernel mean matching and a spatially valid resampling design remain open.

Run python -m pip install -r requirements.txt and python -m pytest -q.
