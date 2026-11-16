# Conjugate gradient and Kronecker matrix-free operators

## Conjugate gradient

For a symmetric positive-definite system (Ax=b), conjugate gradient builds successive search directions in the Krylov subspace and updates the solution using matrix-vector products. The reference implementation supports dense NumPy and SciPy sparse matrices and optional Jacobi preconditioning. It returns the solution, convergence flag, iteration count and residual diagnostics.

## Kronecker product operator

For factors (A_1,\ldots,A_k), the Kronecker product (A_1\otimes\cdots\otimes A_k) can be applied without materialising the full matrix. The implementation reshapes the input into a tensor and applies each factor along its corresponding axis. This is useful when separable covariance or precision structure is available and the factor dimensions are manageable.

## Limits

The package does not construct GMRF precision matrices, sample GMRFs, perform circulant embedding, estimate covariance parameters or implement distributed/preconditioned solver families beyond Jacobi. CG requires an SPD matrix; convergence depends on conditioning and preconditioning.

## Verification

Tests compare dense and sparse CG solutions with direct analytic solves and compare rectangular and three-factor Kronecker operators with explicit `numpy.kron` products.

See the [implementation package](../../implementations/python/spatial-linear-solvers/README.md).
