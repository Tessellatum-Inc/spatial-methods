# Spatial HAC covariance for spatial-lag 2SLS

## Model and estimator

Consider

\[
y=\rho Wy+X\beta+u,
\]

where \(Wy\) is endogenous and \(X\) is exogenous. Construct the instrument matrix

\[
H=[X,WX,\ldots,W^qX],
\]

and let \(Z=[Wy,X]\). The estimator is conventional 2SLS,

\[
\hat\theta=(\hat Z'Z)^{-1}\hat Z'y,
\qquad \hat Z=P_HZ,
\qquad P_H=H(H'H)^{-1}H'.
\]

## Conley-style spatial HAC covariance

Given projected planar coordinates \(s_i\), define pairwise distances \(d_{ij}=\|s_i-s_j\|\) and a declared bandwidth \(c>0\). The Wendland C2 compact-support kernel is

\[
K_{ij}=\begin{cases}
(1-r_{ij})^4(4r_{ij}+1),&r_{ij}<1,\\
0,&r_{ij}\geq1,
\end{cases}
\qquad r_{ij}=d_{ij}/c.
\]

Let \(\hat u_i=y_i-z_i'\hat\theta\) and \(g_i=\hat z_i\hat u_i\). The HAC meat and sandwich are

\[
\hat S=\sum_i\sum_j K_{ij}g_i g_j',
\qquad
\widehat V=(\hat Z'Z)^{-1}\hat S(Z'\hat Z)^{-1}.
\]

An optional finite-sample multiplier \(n/(n-k)\) is applied by default.

## Assumptions and limitations

- Coordinates must be projected planar coordinates in a common linear unit. Longitude/latitude degrees are not appropriate inputs.
- The bandwidth is a substantive dependence-range choice and should be reported and sensitivity-tested; the routine does not select it automatically.
- The kernel estimates residual cross-covariance only within the declared distance support. It does not repair invalid instruments, weak identification, omitted variables or misspecified spatial weights.
- This is a spatial HAC covariance for 2SLS, not an alternative estimator and not a weak-instrument-robust confidence procedure.
- The implementation uses dense distance and kernel matrices and is intended for teaching-sized samples.

## Implementation

See `implementations/python/spatial-econometrics/spatial_2sls_hac.py`. The implementation uses the same Wendland C2 kernel as the companion OLS spatial-HAC routine, but uses projected IV regressors in the sandwich.

## References

- Conley, T. G. (1999). GMM estimation with cross sectional dependence. *Journal of Econometrics*, 92(1), 1–45. https://doi.org/10.1016/S0304-4076(98)00084-0.
- Kelejian, H. H., & Prucha, I. R. (2007). HAC estimation in a spatial framework. *Journal of Econometrics*, 140(1), 131–154. https://doi.org/10.1016/j.jeconom.2006.09.005.
