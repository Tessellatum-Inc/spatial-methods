# Graph-fused spatial regression

A dependency-light NumPy implementation of location-specific linear coefficients with two penalties:

- elementwise L1 sparsity on coefficients;
- graph total variation on differences between adjacent location coefficient vectors.

The ADMM solver reports objective value, primal/dual residual history and a convergence flag. Supply an explicit undirected edge list and an integer location index for every observation.

Run python -m pytest -q from this directory.

This is a dense small/medium teaching implementation. It is not geographically weighted regression or LASSO, a spatial lag/error model, CAR/BYM, or a full inferential spatially varying coefficient model. Intercept columns supplied by the caller are penalized like all other coefficients.
