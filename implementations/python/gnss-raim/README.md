# GNSS residual-based RAIM baseline

This package provides a small, explicit snapshot implementation for a linearised measurement model:

- Generalised least squares with a supplied positive-definite observation covariance.
- A global residual chi-square consistency test with known Gaussian noise covariance.
- Single-measurement leave-one-out fault-exclusion candidates, using a Bonferroni-adjusted subset-test level and reporting unique, ambiguous or unresolved outcomes.

The caller supplies the design matrix, observation vector and covariance. The model does not construct satellite geometry, troposphere/ionosphere corrections, clock states, measurement stochastic models or a navigation solution from raw GNSS observations.

**Integrity boundary:** this is an educational residual-based FDE baseline, not aviation-certified RAIM/ARAIM. It does not calculate horizontal/vertical protection levels, missed-detection or false-alarm integrity risk bounds, availability, continuity, multi-fault hypotheses, solution separation, fault slopes, or temporal monitoring. A unique deletion candidate is not a guarantee that the measurement is faulty. Threshold calibration assumes a correct linearised model and known Gaussian covariance.

Run `python -m pytest -q` from this directory.
