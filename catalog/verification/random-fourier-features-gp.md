# Verification record: Gaussian random Fourier feature GP

## Implemented scope

- Gaussian covariance convention \(C(h)=\sigma^2\exp[-(h/a)^2]\).
- Spectral frequencies sampled from \(N(0,2a^{-2}I)\).
- Random-phase cosine feature map with covariance scaling.
- Bayesian linear posterior in the finite feature basis.
- Latent posterior means and variances at prediction locations.

## Tests

Tests compare the empirical feature Gram matrix with the exact Gaussian
covariance on a seeded finite fixture, check seeded fit reproducibility,
exercise prediction shapes and non-negative variances, verify the
large-noise prior limit, and reject invalid training/prediction inputs.

## Limits

Approximation is conditional on a finite random basis and supplied
hyperparameters. No hyperparameter optimization, feature-count selection,
streaming updates, non-Gaussian likelihood, non-Gaussian kernels or
posterior uncertainty over the random basis is implemented.
