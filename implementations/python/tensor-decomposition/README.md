# Tensor decomposition baselines

This directory contains two distinct dense NumPy teaching implementations:

- CP/PARAFAC-ALS (cp_als.py): a sum of rank-one components with one shared component index.
- Tucker truncated HOSVD and HOOI (tucker_hosvd.py): mode-specific subspaces and a smaller interaction core, with HOOI iterative refinement.

Run with `python -m pytest -q` from this directory.

## Tucker/HOSVD and HOOI scope

The implementation supports finite, fully observed dense tensors of order two or higher. Truncated HOSVD computes leading left singular vectors of each mode unfolding and projects the tensor to a core. HOOI starts from that model and cyclically updates each mode subspace to reduce reconstruction error. Factor columns are orthonormal. Both return a reconstruction and relative Frobenius error; HOOI also returns its error history and sweep count.

Truncated HOSVD is not generally the best-fit Tucker approximation for a requested multilinear rank. HOOI is an iterative local refinement, not a guarantee of the global optimum; results can depend on initialization and local stationary points. Neither implementation includes missing-data completion, sparse tensors, constraints, regularization, automatic rank selection or uncertainty estimates. Dense unfoldings and SVDs can be expensive.

## CP/PARAFAC scope

The CP implementation is a small dense, fully observed, unconstrained three-way ALS baseline. It does not support missing entries, sparse tensors, nonnegativity, regularization, streaming or automatic rank selection. ALS can be sensitive to initialization and ill-conditioning; reconstruction error does not establish factor identifiability.

These are learning implementations, not production-scale tensor libraries or substitutes for validating model assumptions in a spatial application.
