# Two-step heteroskedasticity-robust spatial-lag GMM

## Purpose

The spatial autoregressive (SAR) model contains an endogenous spatially lagged outcome:

\[
y=\rho Wy+X\beta+u.
\]

Because \(Wy\) is generally correlated with \(u\), OLS is inconsistent. Instrumental variables provide a route to identification when \(X\) is exogenous and suitable spatial lags of \(X\) are relevant and excluded from the structural equation. Generalised method of moments (GMM) makes the moment conditions explicit and allows an efficient second step under heteroskedasticity.

## Structural equation and instruments

Let \(R=[Wy\;X]\) be the \(N\times k\) structural regressor matrix. Construct

\[
Z=[X,\;WX,\;W^2X,\ldots,W^qX]
\]

and remove linearly dependent columns in stable order. The maintained moment condition is

\[
E[z_i u_i]=0,\qquad u_i=y_i-R_i\theta,\qquad
\theta=(\rho,\beta')'.
\]

The first-step weighting matrix is the conventional 2SLS choice based on \(Z'Z/N\). The first-step estimate minimises the quadratic sample moments.

## Two-step heteroskedasticity-robust GMM

Given first-step residuals \(\hat u_i^{(1)}\), estimate the covariance of the instrument moments as

\[
\hat S_1=\frac1N\sum_{i=1}^N z_i z_i'(\hat u_i^{(1)})^2.
\]

The second-step weighting matrix is \(\hat S_1^{-1}\). The resulting estimator is

\[
\hat\theta_{GMM}=
\left(R'Z\hat S_1^{-1}Z'R\right)^{-1}
R'Z\hat S_1^{-1}Z'y.
\]

Scaling by \(N\) in the implementation is arranged consistently in the sample moments and normal equations. A heteroskedasticity-robust sandwich covariance is calculated using the second-step residual moment covariance. Standard errors are the square roots of its diagonal.

When the model is overidentified, the reported Hansen-style criterion is the second-step moment quadratic using the first-step residual-based optimal weighting matrix. Its nominal degrees of freedom are the number of independent instruments minus the number of structural regressors. The implementation reports the statistic and degrees of freedom; it does not report a p-value.

## Implemented baseline

The file implementations/python/spatial-econometrics/spatial_gmm.py provides spatial_lag_gmm. It returns the SAR coefficient estimates, fitted values, residuals, robust covariance and standard errors, first- and second-step objectives, overidentification statistic, and instrument/regressor counts.

## Assumptions and limitations

- X and the selected spatial lags of X must be exogenous and valid instruments. The software cannot establish these substantive assumptions.
- Instrument relevance is checked through numerical rank conditions, not a weak-instrument statistic. Users should assess strength and sensitivity to instrument order.
- The estimator addresses heteroskedasticity in the IV moment covariance. It does not model spatially autocorrelated structural errors; use an appropriate SARAR/error specification when that dependence is part of the model.
- It is a cross-sectional linear IV-GMM estimator, not the full Kelejian–Prucha spatial-error GMM procedure and not a generic estimator for arbitrary spatial panels.
- The moment covariance must be full rank, and the sample must exceed the number of independent instruments. Highly collinear or excessive spatial lags are rejected rather than silently regularised.
- The implementation uses dense matrices and is intended for small teaching datasets. No weak-instrument robust confidence intervals, finite-sample corrections, or p-value calculation for the J statistic are provided.

## Relation to 2SLS

The first step is the standard 2SLS GMM weighting choice. The second step updates the weighting matrix using squared first-step residuals, yielding heteroskedasticity-robust efficient GMM under the maintained moment conditions. This is not simply a new name for 2SLS: it changes the weighting matrix and reports a robust covariance estimate.

## Further reading

- Kelejian, H. H. and Prucha, I. R. (1998). A generalized spatial two-stage least squares procedure for estimating a spatial autoregressive model with autoregressive disturbances. Journal of Real Estate Finance and Economics, 17, 99–121.
- Hansen, L. P. (1982). Large sample properties of generalized method of moments estimators. Econometrica, 50(4), 1029–1054.
