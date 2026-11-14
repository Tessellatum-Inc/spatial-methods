# Tucker tensor decomposition: HOSVD and HOOI

## Model

For an order-N tensor X, Tucker approximation represents the data using a smaller core G and one factor matrix per mode:

\[
\mathcal{X} \approx \mathcal{G}\times_1 A^{(1)}\times_2 A^{(2)}\cdots\times_N A^{(N)}.
\]

Each factor matrix spans a mode-specific subspace. Unlike CP/PARAFAC, Tucker does not require a single shared component count across modes; its multilinear rank is a tuple (R1,...,RN). The core captures interactions among retained mode components.

## Truncated HOSVD

1. Unfold the tensor along each mode.
2. Compute an SVD of each mode unfolding.
3. Retain the leading Rn left singular vectors as factor matrix A(n).
4. Project the tensor along every mode with the transpose of its factor matrix to obtain the core.
5. Reconstruct by multiplying the core by all factor matrices.

The resulting factor columns are orthonormal. Truncated HOSVD is a useful subspace approximation but is not generally the globally optimal Tucker fit for the requested ranks.

## Higher-order orthogonal iteration (HOOI)

HOOI starts from HOSVD factor matrices. It cycles through the modes; for each mode, it projects the original tensor onto the current subspaces of all other modes, unfolds the result along the mode being updated, and replaces that factor with the leading left singular vectors. A full sweep is followed by a core projection and reconstruction-error calculation. The implementation stops when the improvement is below a relative tolerance or the iteration limit is reached.

HOOI is a local alternating optimization method. It can improve the HOSVD fit, but it is not a proof of global optimality and can depend on initialization.

## Implemented baseline

The [NumPy implementation](../implementations/python/tensor-decomposition/README.md) accepts finite, fully observed dense tensors of order two or higher and one positive rank per mode, bounded by each mode-unfolding dimension. It provides HOSVD and HOOI, returning the core, factors, reconstruction and relative Frobenius error. HOOI additionally returns error history and iteration count. Tests cover exact reconstruction, low multilinear rank, orthonormal factors, HOOI refinement and invalid inputs.

## Spatial interpretation

A tensor might encode location × time × variable, raster row × column × spectral band, or region × period × indicator. Tucker factors summarize mode-specific subspaces, while the core describes interactions among them. Axes must be meaningfully aligned: arbitrary reshaping, inconsistent region ordering, changing units, missingness patterns or nonstationary measurement processes can dominate the decomposition. Spatial adjacency is not automatically represented by ordinary Euclidean low-rank factorization; spatial regularization or graph-aware models require additional assumptions and methods.

## Limitations

These are dense HOSVD/HOOI baselines, not missing-data completion, sparse storage, nonnegative/regularized Tucker, tensor train, t-SVD, rank selection, probabilistic uncertainty or spatially constrained factors. Dense SVDs may be costly. The methods assume complete finite observations and should not be applied by silently replacing missing values with zero.

## Sources

- De Lathauwer, B., De Moor, B., & Vandewalle, J. (2000). “A multilinear singular value decomposition.” *SIAM Journal on Matrix Analysis and Applications*, 21(4), 1253–1278. DOI: 10.1137/S0895479896305696.
- Kolda, T. G., & Bader, B. W. (2009). “Tensor Decompositions and Applications.” *SIAM Review*, 51(3), 455–500. DOI: 10.1137/07070111X.

No source text, figures or datasets are reproduced.
