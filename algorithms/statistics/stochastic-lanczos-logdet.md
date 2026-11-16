# Stochastic Lanczos quadrature for log determinants

For a symmetric positive-definite matrix A, log(det(A)) equals tr(log(A)). With independent Rademacher probe vectors z, Hutchinson's identity estimates the trace by the average of z-transpose log(A) z. Lanczos iteration builds a small symmetric tridiagonal matrix T from each probe's Krylov subspace. Gauss quadrature approximates each quadratic form by ||z|| squared times the first-coordinate quadratic form of log(T).

The implementation diagonalises T, evaluates the logarithm of its positive Ritz values, and averages the probe estimates. It supports dense NumPy and SciPy sparse matrices and optionally applies two-pass full reorthogonalisation.

## Accuracy and limits

Probe count controls stochastic trace error, while Lanczos depth controls quadrature truncation. The reported probe standard error does not include Lanczos truncation bias. Validate convergence by increasing both controls on representative matrices. The implementation requires symmetric positive-definite input; checking positive Ritz values for finite probes is not a formal global positive-definiteness proof.

Chebyshev polynomial approximations, Pace–Barry, sparse Cholesky, preconditioners and distributed trace estimators remain open.

## Verification

Tests compare diagonal and non-diagonal small SPD matrices against exact numpy.linalg.slogdet, compare a SciPy sparse diagonal matrix with its analytic log determinant, verify seeded reproducibility, and reject nonsymmetric, non-finite, indefinite and invalid-control inputs.

See the [implementation package](../../implementations/python/stochastic-logdet/README.md).
