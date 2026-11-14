# Tucker tensor decomposition by truncated HOSVD

## Model

For an order-N tensor X, Tucker approximation represents the data using a smaller core G and one factor matrix per mode:

\[
\mathcal{X} \approx \mathcal{G}\times_1 A^{(1)}\times_2 A^{(2)}\cdots\times_N A^{(N)}.
\]

Each factor matrix spans a mode-specific subspace. Unlike CP/PARAFAC, Tucker does not require a single shared component count across modes; its multilinear rank is a tuple (R1,...,RN). The core captures interactions among retained mode components.

## Truncated HOSVD algorithm

1. Unfold the tensor along each mode.
2. Compute an SVD of each mode unfolding.
3. Retain the leading Rn left singular vectors as factor matrix A(n).
4. Project the tensor along every mode with the transpose of its factor matrix to obtain the core.
5. Reconstruct by multiplying the core by all factor matrices.

The resulting factor columns are orthonormal. Full admissible multilinear ranks reconstruct the input up to floating-point error. Truncation is a useful subspace approximation but is not generally the globally optimal Tucker fit for the requested ranks; HOOI is an iterative refinement method.

## Implemented baseline

The [NumPy implementation](../implementations/python/tensor-decomposition/README.md) accepts finite, fully observed dense tensors of order two or higher and one positive rank per mode, bounded by each mode-unfolding dimension. It returns the core, factor matrices, reconstruction, multilinear rank and relative Frobenius error. Tests cover exact reconstruction, an exactly low-multilinear-rank tensor, orthonormal factors, the zero tensor and invalid inputs.

## Spatial interpretation

A tensor might encode location × time × variable, raster row × column × spectral band, or region × period × indicator. Tucker factors summarize mode-specific subspaces, while the core describes interactions among them. Axes must be meaningfully aligned: arbitrary reshaping, inconsistent region ordering, changing units, missingness patterns or nonstationary measurement processes can dominate the decomposition. Spatial adjacency is not automatically represented by ordinary Euclidean low-rank factorization; spatial regularization or graph-aware models require additional assumptions and methods.

## Limitations

This is truncated HOSVD, not HOOI or a globally optimal Tucker solver. It does not implement tensor train, t-SVD, missing-data completion, sparse storage, nonnegative/regularized Tucker, rank selection, probabilistic uncertainty or spatially constrained factors. Dense SVDs may be costly. The method assumes complete finite observations and should not be applied by silently replacing missing values with zero.

## Sources

- De Lathauwer, B., De Moor, B., & Vandewalle, J. (2000). “A multilinear singular value decomposition.” *SIAM Journal on Matrix Analysis and Applications*, 21(4), 1253–1278. DOI: 10.1137/S0895479896305696.
- Kolda, T. G., & Bader, B. W. (2009). “Tensor Decompositions and Applications.” *SIAM Review*, 51(3), 455–500. DOI: 10.1137/07070111X.

No source text, figures or datasets are reproduced.
