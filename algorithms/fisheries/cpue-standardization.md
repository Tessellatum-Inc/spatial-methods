# Catch per unit effort standardization

## Model

The log-linear model is

\[
Y_i\sim\operatorname{Poisson}(\mu_i)
\quad\text{or}\quad
Y_i\sim\operatorname{NB2}(\mu_i,\alpha),\qquad
\log\mu_i=\log E_i+\beta_0+x_i^T\beta.
\]

Effort (E_i) is a fixed exposure offset. Under NB2, variance is (mu_i+\alpha\mu_i^2). The standardized index predicts expected catch at unit effort and the sample-mean covariate vector.

## Interpretation and limits

Standardization adjusts the observed catch rate for the covariates and likelihood included in the model. It does not guarantee removal of all catchability variation. This reference implementation has linear covariate effects and no spatial/temporal random fields, GAM smooths, zero-inflation, vessel effects, stock assessment or effort-allocation optimization. Review convergence, residual structure and sensitivity before operational use.

## Verification

Tests use seeded synthetic Poisson and NB2 data with known coefficients/dispersion, check the effort offset and predictions, and exercise input validation.

See the [implementation package](../../implementations/python/cpue-standardization/README.md).
