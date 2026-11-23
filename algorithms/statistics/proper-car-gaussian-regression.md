# Gaussian proper conditional autoregressive (CAR) regression

## Model

Let \(A\) be a symmetric, non-negative adjacency matrix with zero diagonal, and let \(D=\operatorname{diag}(A\mathbf 1)\). The proper-CAR precision matrix is

\[
Q=\tau(D-\alpha A), \qquad \tau>0.
\]

Conditional on covariates, the Gaussian response is

\[
y\mid X,\alpha,\tau \sim
N\left(X\beta,\;[\tau(D-\alpha A)]^{-1}\right).
\]

This is a proper Gaussian CAR model, not an intrinsic CAR (ICAR) model. ICAR uses a singular graph Laplacian precision and requires constraints or a generalised-inverse treatment; this implementation does not fit ICAR or BYM.

## Positive-definiteness constraint

Write \(B=D^{-1/2}AD^{-1/2}\). Since

\[
D-\alpha A=D^{1/2}(I-\alpha B)D^{1/2},
\]

positive definiteness requires \(1-\alpha\lambda_j(B)>0\) for every eigenvalue. Thus the admissible interval is bounded by the reciprocal of the smallest negative and largest positive eigenvalues. The implementation derives this interval from the symmetric eigenspectrum and searches slightly inside its boundaries.

The graph must be symmetric, non-negative, have no self-links, and contain no isolated observations. The model uses the adjacency/weight matrix as supplied; it does not silently symmetrise or row-standardise it.

## Concentrated maximum likelihood

For fixed \(\alpha\), let \(Q_0=D-\alpha A\). Generalised least squares gives

\[
\hat\beta(\alpha)=(X^TQ_0X)^{-1}X^TQ_0y.
\]

Let \(R(\alpha)=(y-X\hat\beta)^TQ_0(y-X\hat\beta)\). The maximum-likelihood precision is \(\hat\tau=n/R(\alpha)\). Substitution yields the concentrated log likelihood

\[
\ell_c(\alpha)=\tfrac12\log|Q_0|
-\tfrac n2\left[\log(2\pi)+1+\log\{R(\alpha)/n\}\right].
\]

The implementation scans a bounded grid, then refines around the best grid cell with golden-section search. It reports \(\hat\alpha\), \(\hat\tau\), GLS coefficients, variance scale (1/tau) and node-specific conditional variances (1/(tau * degree)) \(1/\hat\tau\), fitted mean, residuals, admissible interval and evaluation count.

## Implementation and tests

- Code: [proper_car.py](../../implementations/python/spatial-econometrics/proper_car.py)
- Tests: [spatial econometrics test suite](../../implementations/python/spatial-econometrics/test_spatial_econometrics.py)
- The synthetic recovery test generates Gaussian errors using a Cholesky factor of the known precision matrix.
- Additional tests cover finite likelihood output, parameter bounds, graph symmetry, isolated nodes, rank and search controls.

## Interpretation and limitations

- \(\alpha\) controls conditional dependence among neighbouring residuals; \(\tau\) is a precision scale.
- \(\beta\) describes the conditional mean, not a spatially lagged response.
- The returned fitted values are \(X\hat\beta\). Spatial dependence is represented in the covariance/precision, not in a \(Wy\) mean term.
- This is a dense small-problem teaching estimator. It does not calculate standard errors, posterior distributions, model-comparison corrections, spatially varying coefficients, covariate-dependent precision, or robust inference.
- It does not implement ICAR, BYM/BYM2, Leroux CAR, multivariate CAR, areal count likelihoods, or missing-data inference. Those are separate model families and should not be conflated with this proper-CAR Gaussian model.

## References

- Besag, J. (1974). Spatial interaction and the statistical analysis of lattice systems. *Journal of the Royal Statistical Society: Series B*, 36(2), 192–236.
- Cressie, N. (1993). *Statistics for Spatial Data*. Wiley.
- Rue, H. and Held, L. (2005). *Gaussian Markov Random Fields: Theory and Applications*. Chapman & Hall/CRC.
