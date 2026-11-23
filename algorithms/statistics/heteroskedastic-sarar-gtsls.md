# Three-step heteroskedastic SARAR generalized spatial 2SLS

## Model

The SARAR(1,1) model is

\[
y=X\beta+\rho Wy+u,\qquad u=\lambda Wu+\varepsilon,
\]

where \(Wy\) is endogenous and the innovations may have unknown observation-specific variances.

## Three-step estimator

For the common-weights case \(M=W\), the implementation follows Kelejian and Prucha (2010):

1. **Initial 2SLS.** Set \(Z=[X,Wy]\) and construct \(H=[X,WX,\ldots,W^qX]\), retaining independent columns. Estimate the regression parameters by 2SLS and form \(\tilde u=y-Z\tilde\delta\).
2. **Heteroskedastic disturbance GM.** Estimate \(\lambda\) from the two zero-diagonal quadratic moments using \(\tilde u\). The implementation reuses the standalone two-moment KP GM routine.
3. **Cochrane–Orcutt GTSLS.** Transform \(y_*=(I-\tilde\lambda W)y\) and \(Z_*=(I-\tilde\lambda W)Z\). Re-estimate by 2SLS using the original instrument matrix \(H\), not a transformed instrument matrix.

The third-step estimator is

\[
\hat\delta=
(\hat Z_*'Z_*)^{-1}\hat Z_*'y_*,
\qquad \hat Z_*=P_HZ_*,
\qquad P_H=H(H'H)^{-1}H'.
\]

## Reported covariance

The implementation reports an HC1 sandwich conditional on the estimated \(\tilde\lambda\), treating the transformed regressors and instruments as fixed. This is a useful conditional diagnostic, **not** the full joint asymptotic covariance derived in the paper. The latter accounts for the dependence between first-stage IV estimation and the GM disturbance estimate and requires the joint covariance construction in the paper's Theorem 4.

## Scope and assumptions

- \(X\) is exogenous; \(Wy\) is instrumented using the spatial lags of X.
- The two-step disturbance GM requires a consistent predictor of u. In this three-step estimator it is supplied by the initial spatial 2SLS residuals.
- The routine assumes the same spatial weights matrix for the endogenous outcome lag and the disturbance process.
- It does not implement the complete paper-level joint covariance, Wald tests involving \(\rho\) and \(\lambda\), or optimally weighted GM. Do not interpret its conditional HC1 standard errors as those full joint standard errors.
- Dense matrices are intended for teaching-sized examples. Instrument validity, rank, spatial-weight normalization and parameter-space assumptions remain substantive modelling requirements.

## Implementation

See `implementations/python/spatial-econometrics/spatial_sarar_gtsls.py`. The lower-level moment estimator is in `heteroskedastic_spatial_error_gm.py`.

## Reference

Kelejian, H. H., & Prucha, I. R. (2010). Specification and estimation of spatial autoregressive models with autoregressive and heteroskedastic disturbances. *Journal of Econometrics*, 157(1), 53–67. https://doi.org/10.1016/j.jeconom.2009.10.025.
