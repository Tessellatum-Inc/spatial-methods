# Gaussian linear inverse problem

Exact dense conditioning for the conjugate linear-Gaussian inverse model:

```
y = A x + epsilon
x ~ Normal(m0, C0)
epsilon ~ Normal(0, R)
```

The posterior mean and covariance are computed with Cholesky solves in observation space. The package also returns marginal observation covariance and the Gaussian log marginal likelihood. It supports correlated observation noise and a non-zero prior mean.

## Run

```bash
python -m pip install -r requirements.txt
python -m pytest -q
```

## Assumptions and limits

The design operator is linear and fixed; prior and noise covariance matrices must be symmetric positive definite. The implementation is dense, with memory quadratic in observation and parameter dimensions and cubic factorisation cost. It does not implement nonlinear inversion, PDE-constrained adjoints, variational optimisation, hyperparameter estimation, sparse/matrix-free solvers, emulators or surrogate models.
