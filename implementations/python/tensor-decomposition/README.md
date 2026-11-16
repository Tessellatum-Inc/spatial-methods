# Tensor decomposition baselines

This directory contains dense NumPy teaching implementations:
- CP/PARAFAC-ALS for fully observed unconstrained three-way tensors.
- Tucker truncated HOSVD and HOOI for fully observed dense tensors of order two or higher.
- Tensor-train SVD (TT-SVD), with optional internal-rank cap and relative Frobenius truncation budget.
- A data-consistent TT-SVD completion heuristic for partially observed dense tensors.
- FFT-based third-order t-SVD with frequency-domain factors, reconstruction and tubal-rank truncation.

Run python -m pytest -q from this directory.

## Tensor-train decomposition

TT-SVD factorizes a dense tensor into cores G_k with shape (r_k, n_k, r_{k+1}), with boundary ranks one. It performs a sequence of matrix SVDs and truncates each internal rank. max_rank caps every internal rank. tolerance is a relative Frobenius truncation budget distributed across the N-1 splits; rank caps can increase the achieved error beyond that budget. The algorithm is dense and its cost is dominated by unfolding SVDs.

## Missing-data completion

tt_complete alternates between:
1. projecting the current filled tensor onto a rank-capped TT-SVD model; and
2. restoring observed entries exactly.

It supports mean or zero initialization and returns the missing-value change history. Observed RMSE is zero by construction and is not a measure of predictive quality. This is a simple alternating-projection heuristic, not a global optimizer, uncertainty model, or a reproduction of a specialized tensor completion algorithm. Results depend on rank, observation mask, initialization and stopping rule. Use held-out observed entries to assess predictive error.

## Scope and caveats

These implementations do not provide sparse/out-of-core TT, TT-cross, tensor-network optimization, Bayesian completion, robust losses, nonnegative constraints, automatic rank selection, uncertainty estimates or production-scale performance. A low-rank fit is a modeling assumption, not evidence that the missing entries are identifiable.

## Third-order t-SVD

`t_svd.py` implements the classical circular-convolution t-product construction: FFT along mode three, reduced matrix SVD on each frontal frequency slice, and inverse-FFT reconstruction. Its truncation parameter is tubal rank, not CP rank, Tucker multilinear rank or TT rank. The implementation is dense and does not solve missing-data completion.
