# Non-negative matrix factorization

This package implements Lee–Seung multiplicative updates for the Euclidean/Frobenius objective:

\[
\min_{W,H\geq0}\;\|V-WH\|_F^2.
\]

It uses deterministic positive initialization and normalizes basis columns to remove the scale ambiguity between W and H. Run tests with `python -m pytest -q` from this directory.

The joint problem is non-convex: alternating updates do not guarantee a global optimum, and rank and initialization matter. This small pure-Python implementation is intended for learning and small matrices; it is not optimized for large rasters or tensors. It does not implement generalized-KL NMF, sparse/orthogonal/graph-regularized variants, ICA, MAF, dictionary learning or compressive sensing.
