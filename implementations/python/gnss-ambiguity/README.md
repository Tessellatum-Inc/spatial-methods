# GNSS ambiguity and dual-frequency baselines

This package contains four deliberately bounded pieces:

- **Integer least squares:** a transparent Cholesky sphere-enumeration baseline and a LAMBDA-reduced solver with integer Gauss transformations, covariance permutations and depth-first conditional search. Both accept a supplied float ambiguity vector and positive-definite covariance; neither estimates float ambiguities from raw observations.
- **Dual-frequency combinations:** geometry-free difference, first-order ionosphere-free range combination, wide-lane phase difference, and Melbourne–Wübbena wide-lane observable in cycles. Phase inputs for MW are cycles; code inputs are metres.
- **Geometry-free cycle-slip screening:** sequential quadratic prediction with a configurable residual threshold and optional gap reset. It flags candidate discontinuities but does not identify or repair integer slips.
- **Melbourne–Wübbena screening:** running-mean/noise-threshold discontinuity screen with optional epoch-gap reset; the noise floor is user-configurable.

All range observables are expected in metres; wide-lane phase differences and MW output are in cycles. The ionosphere-free formula removes the first-order dispersive ionospheric term under the standard frequency-squared model. It does not remove higher-order ionosphere, multipath, hardware biases, noise or modelling errors. MW retains receiver/satellite bias terms and is exposed to code noise and multipath; some paired slips are invisible to the wide-lane combination.

Run tests with python -m pytest -q from this directory. These are teaching components, not a raw-observation GNSS processor; there is no ambiguity float estimator, full TurboEdit/Springer implementation, integer slip repair, PPP-AR engine or integrity monitor.
