# K-medoids, CLARA and CLARANS

K-medoids partitions observations into k groups represented by observed
objects. Given a symmetric dissimilarity matrix D, the objective is

\[
\min_{M: |M|=k} \sum_i \min_{m\in M} D_{im}.
\]

Unlike k-means, this objective accepts arbitrary dissimilarities and each
representative is an actual observation. PAM (Partitioning Around Medoids)
uses a greedy BUILD phase followed by SWAP improvements. The implementation
uses deterministic input-order tie breaking and stops when no single
medoid/non-medoid exchange improves the objective.

CLARANS (Clustering Large Applications based upon RANdomized Search) samples
medoid/non-medoid swap neighbours and accepts improving moves until a
configured run of unsuccessful samples identifies a local minimum. Repeated
local searches retain the best candidate found.

CLARA (Clustering LARge Applications) runs PAM on repeated samples and
evaluates each resulting medoid set against all observations. Sampling can
reduce the expensive search, but the dense teaching implementation still
stores the full dissimilarity matrix.

See the [tested Python implementation](../../implementations/python/k-medoids/README.md),
[implementation walkthrough](../../implementations/python/k-medoids/implementation-walkthrough.md),
[tests](../../implementations/python/k-medoids/test_k_medoids.py) and
[executable lab](../../notebooks/k-medoids-clara-lab.ipynb).

## Scope and limitations

This package covers PAM k-medoids, sample-based CLARA and randomized CLARANS.
It does not implement constrained or equal-size k-means, spatially contiguous
regionalisation, automatic cluster-count selection or fuzzy memberships.
The matrix is dense and requires O(n²) storage. PAM's repeated candidate
swaps are intended for modest datasets, not very large data without further
indexing or approximation.

## References

- Kaufman, L. and Rousseeuw, P. J. (1990). *Finding Groups in Data: An
  Introduction to Cluster Analysis*. Wiley.
- Reynolds, A. P., Richards, G., de la Iglesia, B. and Rayward-Smith, V. J.
  (2006). Clustering rules: a comparison of partitioning and hierarchical
  clustering algorithms. *Journal of Mathematical Modelling and Algorithms*,
  5, 475–504.
