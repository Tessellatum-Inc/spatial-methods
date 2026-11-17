# Verification dossier: Gaussian linear inverse problem

## Implemented
- Exact posterior mean and covariance for a linear-Gaussian observation model.
- Non-zero Gaussian prior mean and correlated positive-definite observation noise.
- Posterior marginal standard deviations and Gaussian log marginal likelihood.
- Cholesky-based solves without explicit covariance inversion.

## Independent tests
Tests include a closed-form scalar posterior, multivariate covariance symmetry/PSD, an uninformative observation operator, correlated observation noise, non-positive-definite covariance rejection and dimension/non-finite input validation.

## Exclusions
Nonlinear and PDE-constrained inversion, adjoints, variational approximations, sparse/matrix-free computation, hyperparameter fitting and emulator/surrogate construction remain open.
