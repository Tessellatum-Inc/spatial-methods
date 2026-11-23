# Source verification — Tucker tensor decomposition: HOSVD and HOOI

## Identity and bibliography
- De Lathauwer, De Moor & Vandewalle (2000), “A multilinear singular value decomposition,” *SIAM Journal on Matrix Analysis and Applications*, 21(4), 1253–1278, DOI 10.1137/S0895479896305696.
- Kolda & Bader (2009), “Tensor Decompositions and Applications,” *SIAM Review*, 51(3), 455–500, DOI 10.1137/07070111X.

## Technical claims checked
- Tucker uses a core tensor and mode-specific factor matrices; CP/PARAFAC instead sums rank-one terms.
- HOSVD obtains mode subspaces from left singular vectors of each unfolding and projects the tensor to a core.
- Truncated HOSVD is not generally the best-fit Tucker approximation for a fixed multilinear rank.
- HOOI iteratively updates mode subspaces and can improve a truncated HOSVD fit, but is a local alternating method rather than a global-optimality guarantee.

## Implementation/reproduction
Implemented: dense, fully observed, finite N-way tensors (order >= 2), truncated HOSVD, HOOI refinement, reconstruction and relative Frobenius error. Ranks are bounded by each mode-unfolding dimension. Tests are authored for exact reconstruction, exact low multilinear rank, orthogonality, zero input, HOOI error refinement and validation.

Not implemented: missing-data completion, sparse tensors, nonnegative or regularized models, tensor train, t-SVD, rank selection, or spatially constrained factors. Test files are not evidence of a passing repository test run; run pytest and record its result separately.

## Rights
Original explanatory text and bibliographic metadata only. No source figures, code or datasets are reproduced.
