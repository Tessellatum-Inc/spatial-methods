# Kelejian–Prucha generalized-moments estimation for spatial-error models

## Model

The spatial-error regression is

\[
y=X\beta+u,\qquad u=\lambda Wu+\varepsilon,
\]

where the innovations are independent, identically distributed, mean zero, have common variance \(\sigma^2\), and possess finite fourth moments. The weights have a zero diagonal and the spatial parameter lies in a stable interval for which \(I-\lambda W\) is nonsingular.

This record describes the homoskedastic-innovation generalized-moments estimator of Kelejian and Prucha (1999), followed by feasible GLS. It is distinct from spatial-lag IV-GMM: there is no endogenous \(Wy\) regressor, and the spatial parameter governs the disturbance process.

## Three innovation moments

Let \(\tilde u\) be a consistent predictor of \(u\), here the OLS residual vector. For a candidate \(\lambda\), construct

\[
\tilde\varepsilon(\lambda)=(I-\lambda W)\tilde u,
\qquad
W\tilde\varepsilon(\lambda).
\]

The iid innovation assumptions imply

\[
E\left[\frac{\varepsilon'\varepsilon}{N}\right]=\sigma^2,
\quad
E\left[\frac{(W\varepsilon)'(W\varepsilon)}{N}\right]
=\sigma^2\frac{\operatorname{tr}(W'W)}{N},
\quad
E\left[\frac{(W\varepsilon)'\varepsilon}{N}\right]=0.
\]

The estimator chooses \((\lambda,\sigma^2)\) to minimise the sum of squared deviations of these three sample moments from their population restrictions, over a bounded parameter region with non-negative variance. For each candidate lambda, the variance is profiled out by a one-dimensional least-squares projection. A grid scan locates the best interval and golden-section refinement supplies a reproducible scalar minimiser.

## Feasible GLS

Given \(\hat\lambda\), filter both sides of the regression:

\[
y^*=(I-\hat\lambda W)y,
\qquad
X^*=(I-\hat\lambda W)X.
\]

OLS on \((y^*,X^*)\) gives feasible GLS coefficients. Under the maintained iid innovation model, the plug-in covariance is

\[
\widehat{\operatorname{Var}}(\hat\beta)
=\hat\sigma^2\left(X^{*'}X^*\right)^{-1}.
\]

The returned covariance is model-based; it is not a heteroskedasticity-robust sandwich.

## Implementation and limitations

The NumPy teaching implementation is `implementations/python/spatial-econometrics/spatial_error_gmm.py`. It returns the spatial error coefficient, feasible-GLS coefficients and fitted values, residuals, filtered innovations, estimated innovation variance, model-based covariance, moment residuals and objective.

The routine uses dense matrices and a bounded scalar search. It assumes the supplied weights are already correctly constructed and aligned. The default parameter bounds are conservative numerical bounds, not a universal proof of stability for every possible non-normal matrix. A boundary minimum is rejected rather than silently reported.

**Not implemented here:** the heteroskedastic innovation extension developed by Kelejian and Prucha (2010), joint SARAR estimation, spatial panels, sparse large-N algorithms, weak-dependence diagnostics, and finite-sample corrections. Do not interpret this routine as a robust-to-heteroskedasticity estimator.

## References

- Kelejian, H. H., & Prucha, I. R. (1999). A generalized moments estimator for the autoregressive parameter in a spatial model. *International Economic Review*, 40(2), 509–533. [https://doi.org/10.1111/1468-2354.00027](https://doi.org/10.1111/1468-2354.00027).
- Kelejian, H. H., & Prucha, I. R. (2010). Specification and estimation of spatial autoregressive models with autoregressive and heteroskedastic disturbances. *Journal of Econometrics*, 157(1), 53–67. [https://doi.org/10.1016/j.jeconom.2009.10.025](https://doi.org/10.1016/j.jeconom.2009.10.025).
