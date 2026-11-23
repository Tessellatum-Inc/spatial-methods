# Concentrated maximum likelihood for SAR and SEM

**Status:** implemented teaching baseline; dense matrices; synthetic parameter-recovery checks added. Full repository tests and CI are not yet confirmed.

## What it estimates

Two Gaussian spatial regression models share a one-parameter likelihood profile:

- **Spatial autoregressive lag (SAR/SLM):** \(y=\rho Wy+X\beta+\varepsilon\).
- **Spatial error (SEM):** \(y=X\beta+u,\quad u=\lambda Wu+\varepsilon\).

For either model, the spatial transformation is \(A(\theta)=I-\theta W\), and the log-likelihood contains the Jacobian term \(\log|A(\theta)|\). Omitting that term and minimizing residual sum of squares alone does not produce the spatial maximum-likelihood estimator.

## Profile likelihood

For SAR, at each candidate \(\rho\), regress \(Ay\) on \(X\). For SEM, regress \(Ay\) on \(AX\). In either case, let the resulting residual sum of squares be \(SSR(\theta)\), with \(\hat\sigma^2(\theta)=SSR(\theta)/n\). The concentrated log-likelihood is

\[
\ell_c(\theta)=\log|I-\theta W|
-\frac n2\left[\log(2\pi)+1+\log\left(\frac{SSR(\theta)}n\right)\right].
\]

The implementation scans a one-dimensional grid, then refines around the best grid cell with golden-section maximisation. It retains the best grid point if the local refinement is worse. Once the spatial parameter is selected, the profile regression supplies \(\hat\beta\) and \(\hat\sigma^2\).

## Parameter interval and numerical contract

The default interval is \((-0.98/\|W\|_\infty,\,0.98/\|W\|_\infty)\). The strict norm bound ensures \(|\theta|\|W\|_\infty<1\), so the Neumann-series argument guarantees \(I-\theta W\) is nonsingular throughout the interval. This is a deliberately conservative interval, not the full admissible parameter space. A true parameter outside it will not be recovered by this estimator.

The code uses dense NumPy matrices and repeated log-determinants. It is intended for small teaching examples, not large sparse spatial systems. It assumes Gaussian iid innovations and a correctly specified weights matrix. It does not calculate standard errors, information-matrix covariance, likelihood-ratio tests, robust inference, or impacts. The separate [spatial Durbin ML estimator](spatial-durbin-mle.md) profiles the SDM likelihood; SAC/SARAR estimation remains open.

## Runnable implementation

- [SAR and SEM maximum-likelihood implementation](../../implementations/python/spatial-econometrics/maximum_likelihood.py)
- [Package tests](../../implementations/python/spatial-econometrics/test_spatial_econometrics.py)
- [Package overview](../../implementations/python/spatial-econometrics/README.md)

## Verification targets

The synthetic tests generate SAR and SEM outcomes from known coefficients and spatial parameters, then check approximate recovery, finite likelihood, positive innovation variance and output dimensions. Validation tests cover invalid dimensions, non-finite inputs, rank deficiency and grid settings. These checks are necessary but not sufficient for general numerical correctness; full test execution and comparison against a maintained estimator remain outstanding.

## References

- Anselin, L. (1988), *Spatial Econometrics: Methods and Models*, Kluwer Academic Publishers.
- PySAL, [Maximum Likelihood Estimation — Spatial Lag Model](https://pysal.org/spreg/notebooks/13_ML_estimation_spatial_lag.html), including the concentrated SAR likelihood and discussion of dense versus scalable Jacobian calculations.
- PySAL, [Maximum Likelihood Estimation — Spatial Error Model](https://pysal.org/spreg/notebooks/15_ML_estimation_spatial_error.html).
- PySAL, [spreg API](https://pysal.org/spreg/api.html), which documents maintained ML_Lag and ML_Error implementations.
