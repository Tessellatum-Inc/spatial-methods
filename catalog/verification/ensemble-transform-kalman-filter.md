# Verification record: ensemble transform Kalman filter

## Identity
- Canonical record: batch linear ensemble transform Kalman analysis.
- Implementation: implementations/python/state-estimation/ensemble_square_root.py.
- Classification: symmetric ensemble-space ETKF analysis, not a generic umbrella implementation of all ensemble square-root filters.

## Bibliographic verification
- Bishop, Etherton & Majumdar (2001), Monthly Weather Review 129(3), 420–436, DOI 10.1175/1520-0493(2001)129<0420:ASWTET>2.0.CO;2, introduces the ETKF.
- Whitaker & Hamill (2002), Monthly Weather Review 130(7), 1913–1924, DOI 10.1175/1520-0493(2002)130<1913:EDAWPO>2.0.CO;2, presents the EnSRF variant and the no-perturbed-observation rationale.

## Technical checks
- Forecast sample covariance uses denominator N-1.
- Mean update is computed in ensemble space.
- Symmetric transform is the positive-definite inverse square root scaled by sqrt(N-1).
- Analysis ensemble sample covariance matches the linear Kalman analysis covariance for the supplied ensemble covariance.
- Full observation-error covariance is supported.

## Reproduction and rights
- Original NumPy implementation and tests.
- Tests compare analysis mean/covariance against the conventional Kalman equations, check determinism and validate malformed inputs.
- No third-party code, figures or data are reproduced. The stochastic EnKF companion is tested separately against large-ensemble Kalman moments and observation-perturbation covariance.
- Repository CI pending.



## Companion method: stochastic EnKF

The state-estimation package also contains a stochastic perturbed-observation
EnKF analysis. It computes sample state/observation cross-covariance, adds
independent Gaussian perturbations with covariance R to each ensemble member's
observation, and applies the ensemble Kalman gain. This is a separate
algorithmic variant from the deterministic ETKF; it is not folded into the
ETKF identity record.
