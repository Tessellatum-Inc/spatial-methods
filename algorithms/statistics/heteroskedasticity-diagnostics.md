# Heteroskedasticity diagnostics for spatial-regression baselines

## Purpose

Spatial regression workflows should distinguish spatial dependence from non-constant error variance. These tests diagnose the latter after an OLS baseline; they do not test spatial autocorrelation and do not select SAR, SEM or SDM specifications.

## Koenker studentized Breusch–Pagan

Regress squared OLS residuals on the original nonconstant regressors and an intercept. The LM statistic is \(nR^2\), asymptotically chi-square with degrees of freedom equal to the auxiliary design rank minus one. The studentized form is less dependent on Gaussian errors than the original Breusch–Pagan variance-score test, but still relies on the usual large-sample auxiliary-regression approximation.

## White's general test

Augment the auxiliary design with squares and pairwise products of nonconstant regressors. Again, the statistic is \(nR^2\), with degrees of freedom given by the rank of the auxiliary design excluding its intercept. The implementation removes linear dependencies among generated terms through an SVD basis, which matters when regressors are collinear after squaring or interaction expansion.

## Implementation and interpretation

Runnable reference: [heteroskedasticity_diagnostics.py](../../implementations/python/spatial-econometrics/heteroskedasticity_diagnostics.py).

Both tests return the LM statistic, asymptotic chi-square p-value, auxiliary degrees of freedom and auxiliary \(R^2\). Small p-values are evidence against constant conditional variance, not proof of a particular variance model. White's expansion can become large quickly; use it judiciously with modest sample sizes and a limited number of regressors.

These tests do not replace heteroskedasticity-robust standard errors, spatial HAC covariance estimation, or a model-specific heteroskedastic spatial estimator. A non-rejection does not establish homoskedasticity.

## Validation

Tests compare statistics with independently constructed auxiliary regressions, cover redundant generated White terms, and reject invalid/rank-deficient designs. Run the spatial-econometrics test suite with `python -m pytest -q`.

## References

- Breusch, T. S., & Pagan, A. R. (1979). A simple test for heteroscedasticity and random coefficient variation. *Econometrica*, 47(5), 1287–1294.
- Koenker, R. (1981). A note on studentizing a test for heteroscedasticity. *Journal of Econometrics*, 17(1), 107–112.
- White, H. (1980). A heteroskedasticity-consistent covariance matrix estimator and a direct test for heteroskedasticity. *Econometrica*, 48(4), 817–838.
