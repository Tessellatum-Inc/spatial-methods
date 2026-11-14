# Tensor decomposition baselines

This directory contains two distinct dense NumPy teaching implementations:

- CP/PARAFAC-ALS (cp_als.py): a sum of rank-one components with one shared component index.
- Tucker truncated HOSVD (tucker_hosvd.py): mode-specific subspaces and a smaller interaction core.

Run with `python -m pytest -q` from this directory.

## Tucker/HOSVD scope

Supports finite, fully observed dense tensors of order two or higher. It computes leading left singular vectors of each mode unfolding, projects the tensor to a core, and reconstructs the truncated approximation. Factor columns are orthonormal. The returned relative Frobenius error describes the supplied input and ranks.

Truncated HOSVD is not generally the best-fit Tucker approximation for a requested multilinear rank. Higher-order orthogonal iteration (HOOI) can refine the subspaces. This implementation does not include HOOI, missing-data completion, sparse tensors, constraints, regularization, automatic rank selection or uncertainty estimates. Dense unfoldings and SVDs can be expensive.

## CP/PARAFAC scope

The CP implementation is a small dense, fully observed, unconstrained three-way ALS baseline. It does not support missing entries, sparse tensors, nonnegativity, regularization, streaming or automatic rank selection. ALS can be sensitive to initialization and ill-conditioning; reconstruction error does not establish factor identifiability.

These are learning implementations, not production-scale tensor libraries or substitutes for validating model assumptions in a spatial application.
