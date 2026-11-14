# GNSS ambiguity and dual-frequency baselines

This package contains three deliberately bounded pieces:

- **Integer least squares:** Cholesky-based sphere enumeration for the two best integer candidates, given a float ambiguity vector and positive-definite covariance. This is not LAMBDA decorrelation.
- **Dual-frequency combinations:** geometry-free difference, first-order ionosphere-free range combination, and wide-lane phase difference.\n- **Geometry-free cycle-slip screening:** sequential quadratic prediction with a configurable residual threshold and optional gap reset. It flags candidate discontinuities but does not identify or repair integer slips.\n- **Melbourne–Wübbena screening:** running-mean/noise-threshold discontinuity screen with optional epoch-gap reset; the noise floor is user-configurable.

All range observables are expected in metres; wide-lane inputs are phase cycles. The ionosphere-free formula removes the first-order dispersive ionospheric term under the standard frequency-squared model. It does not remove higher-order ionosphere, multipath, hardware biases, noise or modelling errors. The geometry-free combination retains ionospheric content and is useful in quality-control workflows, but is not by itself a complete cycle-slip detector.

Run tests with `python -m pytest -q` from this directory. These are teaching components, not a raw-observation GNSS processor; there is no ambiguity float estimator, LAMBDA reduction, full TurboEdit/Springer implementation, integer slip repair, PPP-AR engine or integrity monitor.
