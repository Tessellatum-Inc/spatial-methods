# Stochastic Lanczos log-determinant

This package estimates log determinants of dense or sparse symmetric positive-definite matrices using stochastic Lanczos quadrature (SLQ).

## Install and test

```bash
python -m pip install -r requirements.txt
python -m pytest -q
```

## Method

For Rademacher probes z, the trace identity gives log|A| = tr(log A) approximately equal to the average of z-transpose log(A) z. Lanczos iteration constructs a small tridiagonal matrix T for each probe; Gauss quadrature approximates each quadratic form by ||z||² e1-transpose log(T) e1. The function returns the average estimate, probe standard error, individual probe estimates and actual Krylov depths.

Dense NumPy arrays and SciPy sparse matrices are supported. The caller is responsible for selecting enough probes and Lanczos steps for the required accuracy. Full reorthogonalisation improves numerical stability at additional memory and compute cost. The returned standard error measures probe variation, not Lanczos truncation bias.

## Limits

The method requires a symmetric positive-definite matrix. Positive Ritz values are checked for each probe, but a finite set of probes is not a formal proof that the full matrix is positive definite. The package does not implement Chebyshev approximations, Pace–Barry methods, sparse Cholesky, preconditioning or distributed trace estimation.

See `algorithms/statistics/stochastic-lanczos-logdet.md`.
