# Verification — Haar-detail MAD sensor-noise estimator

**Implementation:** [Python package](../../implementations/python/sensor-noise-estimation/README.md)  
**Walkthrough:** [Haar detail and robust scale](../../implementations/python/sensor-noise-estimation/implementation-walkthrough.md)

## Scope verified

- Orthonormal 2x2 Haar diagonal detail with unmatched final row/column dropped.
- Robust Gaussian scale estimate from median absolute deviation divided by the standard-normal MAD constant.
- Independent per-band estimates for HxWxB arrays.
- Explicit finite-value, dimensionality and minimum-size validation.

## Tests

- Constant image and planar ramp have zero diagonal detail.
- Seeded Gaussian noise recovers known sigma within a stated tolerance.
- Smooth planar trend plus Gaussian noise recovers sigma within a stated tolerance.
- Three-band cube recovers ordered, distinct noise levels.
- Invalid dimensions, non-finite values and empty band stacks are rejected.
- Odd dimensions exercise the documented crop policy.

## Limits

This verifies a first-order estimator under a white-Gaussian/additive-noise assumption. It does not validate a complete physical sensor model, correlated or periodic noise, Poisson/heteroscedastic noise, cross-band covariance, or noise estimation under arbitrary textured scenes.
