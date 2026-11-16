# Fay–Herriot area-level small-area estimation

The Fay–Herriot model relates direct area estimates (y_i) to area-level covariates:

\[
y_i=x_i^T\beta+u_i+e_i,\qquad
u_i\sim N(0,\tau^2),\quad e_i\sim N(0,D_i),
\]

where (D_i) is the known sampling variance of the direct estimate. The empirical-Bayes estimate combines the regression mean and direct estimate:

\[
\hat\theta_i=x_i^T\hat\beta+
\frac{\hat\tau^2}{\hat\tau^2+D_i}
(y_i-x_i^T\hat\beta).
\]

The implementation estimates regression coefficients by generalized least squares and the between-area variance by maximum or restricted maximum likelihood. It returns the shrinkage factors and conditional random-effect posterior variances.

## Assumptions and limitations

The baseline assumes independent Gaussian area effects and known positive sampling variances. The conditional variance is not a full frequentist MSE: it omits uncertainty from estimating regression coefficients and the variance component. It does not implement unit-level models, survey-weighted estimators, Horvitz–Thompson, MRP or spatially structured random effects.

## Verification

Tests cover finite empirical-Bayes estimates, shrinkage under high sampling variance, ML/REML selection and invalid or rank-deficient designs.

See the [implementation package](../../implementations/python/small-area-estimation/README.md).
