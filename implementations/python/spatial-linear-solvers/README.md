# Spatial linear solvers and Kronecker operators

NumPy/SciPy reference kernels for symmetric positive-definite linear systems and matrix-free Kronecker products.

## Install and test

```bash
python -m pip install -r requirements.txt
python -m pytest -q
```

## Conjugate gradient

`conjugate_gradient` solves (Ax=b) for symmetric positive-definite dense or SciPy sparse matrices. It supports an optional Jacobi preconditioner, an initial guess, relative/absolute-scaled residual tolerance and iteration cap. The result reports convergence and residual diagnostics. The routine rejects non-positive search curvature rather than silently continuing on a non-SPD matrix.

## Kronecker matrix-vector product

`kronecker_matvec` applies (A_1\otimes A_2\otimes\cdots\otimes A_k) to a vector by reshaping and applying each factor along one tensor axis. It supports rectangular factors and avoids constructing the full Kronecker matrix.

## Scope

These are numerical kernels, not a complete Gaussian Markov random field workflow. Sparse precision construction, sampling, circulant embedding, FFT-based covariance simulation, boundary conditions and structured covariance estimation remain open.

See `algorithms/statistics/spatial-linear-solvers.md`.
