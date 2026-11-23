# Tensor-train decomposition and missing-data completion

## Tensor-train representation

For an order-N tensor X with dimensions n_1,...,n_N, a tensor-train (TT) representation writes each entry as a chain contraction:

X(i_1,...,i_N) = G_1(1,i_1,:) G_2(:,i_2,:) ... G_N(:,i_N,1).

The k-th core has shape (r_{k-1}, n_k, r_k), with boundary ranks r_0=r_N=1. The internal ranks control representation size and expressiveness. Unlike CP, TT uses a sequence of intermediate ranks; unlike Tucker, it does not require one dense core whose size is the product of all multilinear ranks.

## Implemented TT-SVD

The companion implementation applies sequential matrix SVDs to tensor unfoldings. At each split, it retains a selected number of singular directions, reshapes the left singular vectors into a TT core, and passes the truncated singular values/right singular vectors to the next split.

- max_rank imposes a cap on every internal rank.
- tolerance is a relative Frobenius truncation budget distributed across the N-1 splits.
- The returned reconstruction and relative Frobenius error expose the actual approximation.

The standard TT-SVD truncation has a quasi-optimal Frobenius error bound in exact arithmetic for the chosen truncation budget. A restrictive rank cap can exceed the requested tolerance. This implementation is dense and uses NumPy SVD; it is not a sparse or out-of-core algorithm.

## Implemented missing-data heuristic

The completion routine alternates two projections:
1. project the current filled tensor onto a rank-capped TT model using TT-SVD;
2. overwrite observed locations with their original values.

The routine supports mean or zero initialization and stops when the relative change in missing entries is small. It enforces observed-data fidelity exactly, but this does not establish accuracy at unobserved locations. The method is nonconvex as a whole, initialization- and rank-dependent, and not guaranteed to converge to a global minimizer. Its convergence criterion is a change criterion, not a predictive validation score.

For meaningful evaluation, hold out a subset of known entries, fit using the remaining mask, and measure error on held-out values. Select ranks and stopping settings using that validation process rather than the observed-entry residual.

## Comparison and boundaries

- **CP:** sum of rank-one factors, one shared component index.
- **Tucker:** mode-specific subspaces and a smaller interaction core.
- **TT:** chain of three-way cores with intermediate ranks.
- **TT completion here:** alternating projection baseline, not a specialized optimization solver.

No TT-cross, sparse TT, tensor-network contraction planner, robust completion, Bayesian uncertainty, automatic rank selection, or large-scale distributed implementation is included.

## References

- Oseledets, I. V. (2011). Tensor-train decomposition. SIAM Journal on Scientific Computing, 33(5), 2295–2317. DOI: 10.1137/090752286.
- Grasedyck, L. (2010). Hierarchical singular value decomposition of tensors. SIAM Journal on Matrix Analysis and Applications, 31(4), 2029–2054. DOI: 10.1137/090764189.
- Kressner, D., & Tobler, C. (2014). Algorithm  the tensor train format. In related work on tensor completion, use primary method-specific sources before describing any implementation as a reproduction.

No source code, figures or data are copied.
