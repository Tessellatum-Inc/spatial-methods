# Verification record: simple, ordinary and universal kriging

## Implemented scope

- Simple kriging with supplied known constant mean.
- Ordinary kriging with an unknown constant mean.
- Universal kriging with intercept and planar x/y drift.
- Spherical, exponential and Gaussian covariance structures.
- Nugget and optional observation-noise diagonal terms.
- Multi-target prediction, weights and latent-field conditional variance.

## Tests

Tests include a one-observation simple-kriging closed form, constant-field
ordinary kriging and unit-sum weights, exact planar-trend reproduction,
zero-nugget interpolation at sample locations, an independent block-system
oracle for universal kriging, and invalid/rank-deficient inputs.

## Limits

Dense solves only; no variogram fitting, automatic anisotropy, external
covariates, co-kriging, block support, local neighbourhood selection or
parameter uncertainty. The solver rejects singular systems rather than
using a pseudo-inverse.
