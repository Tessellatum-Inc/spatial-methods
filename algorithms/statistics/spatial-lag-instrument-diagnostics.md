# First-stage relevance diagnostics for spatial-lag instruments

## Purpose and model

In the spatial autoregressive model

\[
y=\rho Wy+X\beta+u,
\]

the spatial lag \(Wy\) is endogenous. A common instrument set is

\[
Z=[X,WX,\ldots,W^qX].
\]

Before interpreting 2SLS or IV-GMM estimates, inspect whether the excluded spatial lags explain meaningful variation in \(Wy\) after controlling for \(X\). Spatially lagged instruments can be highly collinear or weak; adding more powers of \(W\) is not automatically an improvement.

## First-stage tests

The unrestricted first stage regresses \(Wy\) on the linearly independent columns of \([X,WX,\ldots,W^qX]\). The restricted first stage uses \(X\) alone. If \(q_e\) independent excluded columns remain, the partial coefficient of determination is

\[
R^2_{partial}=\frac{SSR_R-SSR_U}{SSR_R}.
\]

The classical joint-exclusion statistic is

\[
F=\frac{(SSR_R-SSR_U)/q_e}{SSR_U/(N-p)},
\]

where \(p\) is the number of retained unrestricted first-stage columns. This is the conventional homoskedastic partial F statistic.

The implementation also computes an HC1 heteroskedasticity-robust covariance for the unrestricted first stage. The robust joint-exclusion Wald statistic is reported as an F-scaled statistic:

\[
F_{HC1}=\frac{\hat\pi_E'\widehat V_{HC1}(\hat\pi_E)^{-1}\hat\pi_E}{q_e}.
\]

Both statistics are returned with numerator and denominator degrees of freedom. HC1 is heteroskedasticity-robust under independent-observation asymptotics; it is not robust to spatially correlated first-stage disturbances.

## Interpretation and important limits

- A small partial \(R^2\) and low first-stage statistics are warning signs that the excluded instruments add little predictive information beyond \(X\).
- Do not treat a first-stage F of 10 as a universal pass/fail threshold. Weak-instrument critical values depend on the estimator, number of endogenous regressors, number of instruments, covariance assumptions and tolerated bias or size distortion.
- The HC1 robust Wald F returned here is **not** the Kleibergen–Paap rk Wald F statistic. The implementation has one endogenous regressor and provides transparent first-stage summaries, not a full rank-based weak-identification test.
- Neither relevance statistic tests instrument exogeneity or the exclusion restriction. Spatial lags of covariates may be invalid if they directly affect the outcome through omitted spatial channels.
- With many spatial-lag instruments, instrument proliferation and collinearity can degrade finite-sample performance. Instrument order should be justified, not maximised mechanically.
- These diagnostics do not provide Anderson–Rubin or conditional likelihood-ratio confidence sets. Conventional second-stage t-tests can remain misleading under weak identification.

## Implementation

The dense NumPy implementation is `implementations/python/spatial-econometrics/instrument_diagnostics.py`. It constructs spatial lags of X, drops dependent columns in stable order, estimates restricted and unrestricted first stages, and returns partial R-squared, classical partial F, HC1 robust Wald F, degrees of freedom, coefficients and HC1 standard errors.

## References

- Keane, M. P., & Neal, T. (2024). A practical guide to weak instruments. *Annual Review of Economics*, 16, 185–212. [https://doi.org/10.1146/annurev-economics-092123-111021](https://doi.org/10.1146/annurev-economics-092123-111021).
- Kelejian, H. H., & Prucha, I. R. (1998). A generalized spatial two-stage least squares procedure for estimating a spatial autoregressive model with autoregressive disturbances. *The Journal of Real Estate Finance and Economics*, 17, 99–121.
- Liu, X., & Lee, L.-F. (2013). Two-stage least squares estimation of spatial autoregressive models with endogenous regressors and many instruments. *Econometric Reviews*, 32(5–6), 734–753. [https://doi.org/10.1080/07474938.2013.741018](https://doi.org/10.1080/07474938.2013.741018).
