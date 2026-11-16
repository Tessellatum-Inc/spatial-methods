# Concentrated maximum likelihood for the spatial Durbin model

**Status:** implemented dense teaching baseline; synthetic recovery and collinearity tests added. Full repository tests and CI are not yet confirmed.

## Model

The spatial Durbin model (SDM) is

\[
y=\rho Wy+X\beta+WX\gamma+\varepsilon,
\qquad \varepsilon\sim N(0,\sigma^2 I).
\]

It includes both endogenous spatial feedback in the response and contextual effects from neighbouring covariates. SAR is nested when \(\gamma=0\); SLX is nested when \(\rho=0\), subject to the specification.

## Concentrated likelihood

For a candidate \(\rho\), define \(A(\rho)=I-\rho W\). Regress \(Ay\) on the augmented exogenous design \([X,WX]\). If \(SSR(\rho)\) is the residual sum of squares and \(\hat\sigma^2=SSR/n\), the concentrated Gaussian log-likelihood is

\[
\ell_c(\rho)=\log|I-\rho W|-\frac n2
\left[\log(2\pi)+1+\log\{SSR(\rho)/n\}\right].
\]

The implementation scans a grid over a conservative interval and refines the best grid cell with golden-section maximisation. Coefficients are re-estimated by least squares at the selected value.

## Collinearity and identification

Spatially lagged covariates can be linearly dependent on included covariates. A common example is the lag of a constant under row-standardised weights: \(W\mathbf{1}=\mathbf{1}\). The implementation retains only columns of \(WX\) that add rank beyond \(X\), in stable column order, and returns zero for dropped gamma entries. This is a computational convention, not evidence that a dropped coefficient is truly zero. It means that coefficient is not separately identified by this design and weights matrix.

A complete-graph row-standardised matrix can make every spatially lagged covariate a linear combination of the original design. In that case the SDM collapses to the SAR design and the gamma coefficients cannot be separately estimated. The estimator reports this through zero-filled dropped coefficients rather than pretending the model distinguishes them.

## Parameter interval and limitations

The spatial parameter is restricted to \((-0.98/\|W\|_\infty,0.98/\|W\|_\infty)\), a conservative nonsingularity interval. It is not the full admissible parameter space. The implementation uses dense matrices and repeated log-determinants, assumes Gaussian iid innovations and a correctly specified weights matrix, and does not provide standard errors, weak-identification diagnostics, likelihood-ratio tests, robust inference or sparse large-scale estimation.

## Runnable implementation and tests

- [Maximum-likelihood implementation](../../implementations/python/spatial-econometrics/maximum_likelihood.py)
- [Tests](../../implementations/python/spatial-econometrics/test_spatial_econometrics.py)
- [Package overview](../../implementations/python/spatial-econometrics/README.md)
- [Spatial econometrics lab](../../notebooks/spatial-econometrics-lab.ipynb)

## References

- Anselin, L. (1988), *Spatial Econometrics: Methods and Models*, Kluwer Academic Publishers.
- PySAL, [Maximum Likelihood Estimation — Spatial Lag Model](https://pysal.org/spreg/notebooks/13_ML_estimation_spatial_lag.html).
- PySAL, [spreg API](https://pysal.org/spreg/api.html), including ML_Lag and SLX/SDM model specifications.
