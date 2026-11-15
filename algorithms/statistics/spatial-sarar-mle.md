# Joint maximum likelihood for SARAR / SAC

**Status:** implemented dense teaching baseline; synthetic parameter-recovery and search-validation tests added. Full repository tests and CI are not yet confirmed.

## Model

The SARAR (also commonly called SAC) specification combines a spatially lagged dependent variable with spatially correlated disturbances:

\[
y=\rho Wy+X\beta+u,
\qquad
u=\lambda Wu+\varepsilon,
\qquad
\varepsilon\sim N(0,\sigma^2I).
\]

Equivalently, with \(A_\rho=I-\rho W\) and \(A_\lambda=I-\lambda W\),

\[
A_\lambda(A_\rho y-X\beta)=\varepsilon.
\]

This is distinct from the SDM: SARAR adds a spatial error process rather than spatially lagged covariates.

## Concentrated likelihood

For candidate parameters \((\rho,\lambda)\), transform both response and design:

\[
y^*=A_\lambda A_\rho y,
\qquad
X^*=A_\lambda X.
\]

Estimate \(\beta\) by least squares of \(y^*\) on \(X^*\). With residual sum of squares \(SSR(\rho,\lambda)\) and \(\hat\sigma^2=SSR/n\), the concentrated log-likelihood is

\[
\ell_c(\rho,\lambda)=
\log|A_\rho|+\log|A_\lambda|
-\frac n2\left[\log(2\pi)+1+
\log\{SSR(\rho,\lambda)/n\}\right].
\]

The implementation searches a two-dimensional coarse grid to select a starting point, then alternates one-dimensional golden-section maximisations within the corresponding neighbourhoods of that best grid cell. It retains the best result if coordinate refinement does not improve the coarse-grid likelihood.

## Parameter bounds and interpretation

Both parameters are restricted to the conservative interval

\[
\left(-\frac{0.98}{\|W\|_\infty},
\frac{0.98}{\|W\|_\infty}\right),
\]

which guarantees nonsingularity through the Neumann-series condition. This rectangle is conservative and is not the full joint admissible parameter space. The fit's spatial parameter stores \(\rho\); its error parameter stores \(\lambda\). Returned fitted values are the structural predictor \(\rho Wy+X\hat\beta\), and residuals are on the original response scale.

## Limitations

This is a dense-matrix teaching estimator. It assumes Gaussian iid innovations after filtering and a supplied, correctly aligned weights matrix. The two-dimensional profile may be expensive for larger samples; coordinate refinement is not a proof of a global maximum. The implementation does not provide standard errors, robust inference, likelihood-ratio tests, impacts or sparse large-scale estimation. Applied analysis should compare results with established spatial econometrics software and assess sensitivity to weights and model specification.

## Runnable implementation and tests

- [Maximum-likelihood implementation](../../implementations/python/spatial-econometrics/maximum_likelihood.py)
- [Tests](../../implementations/python/spatial-econometrics/test_spatial_econometrics.py)
- [Package overview](../../implementations/python/spatial-econometrics/README.md)
- [Spatial econometrics lab](../../notebooks/spatial-econometrics-lab.ipynb)

## References

- Anselin, L. (1988), *Spatial Econometrics: Methods and Models*, Kluwer Academic Publishers.
- Anselin, L. (2001), “Spatial Econometrics,” in *A Companion to Theoretical Econometrics*.
- PySAL, [spreg API](https://pysal.org/spreg/api.html), including general spatial two-stage least squares estimators for spatial lag and error specifications.
