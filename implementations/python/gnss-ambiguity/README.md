# GNSS ambiguity and dual-frequency baselines

This package contains two deliberately bounded pieces:

- **Integer least squares:** Cholesky-based sphere enumeration for the two best integer candidates, given a float ambiguity vector and positive-definite covariance. This is not LAMBDA decorrelation.
- **Dual-frequency combinations:** geometry-free difference, first-order ionosphere-free range combination, and wide-lane phase difference.

All range observables are expected in metres; wide-lane inputs are phase cycles. The ionosphere-free formula removes the first-order dispersive ionospheric term under the standard frequency-squared model. It does not remove higher-order ionosphere, multipath, hardware biases, noise or modelling errors. The geometry-free combination retains ionospheric content and is useful in quality-control workflows, but is not itself a cycle-slip detector.

Run tests with `python -m pytest -q` from this directory. These are teaching components, not a raw-observation GNSS processor; there is no ambiguity float estimator, LAMBDA reduction, cycle-slip detector, PPP-AR engine or integrity monitor.
