# Ward's agglomerative hierarchical clustering

Ward's method builds a hierarchy by repeatedly merging the pair of clusters
that causes the smallest increase in within-cluster sum of squares. For
clusters A and B with sizes n_A and n_B and centroids mu_A and mu_B, the
increase is

\[
\Delta(A,B)=\frac{n_A n_B}{n_A+n_B}\|\mu_A-\mu_B\|_2^2.
\]

The reference linkage height is sqrt(2 Delta), the common Ward linkage
distance convention. A linkage row records the two cluster identifiers,
merge height and resulting cluster size. Cutting after n-k merges yields k
clusters.

The implementation uses finite Euclidean feature vectors, exact pair search
and deterministic cluster-id tie breaking. Its direct pair search is intended
for small datasets, not large-scale production clustering. Arbitrary
dissimilarity inputs and spatially contiguous constraints are not supported.

See the [Python package](../../implementations/python/ward-clustering/README.md)
and [tests](../../implementations/python/ward-clustering/test_ward_clustering.py).
