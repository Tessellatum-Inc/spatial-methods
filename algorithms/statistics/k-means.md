# Lloyd k-means clustering

Given observations x_i in Euclidean feature space, k-means partitions them
into k non-empty groups and minimizes the within-cluster sum of squares

\[
\sum_{j=1}^{k}\sum_{i:z_i=j}\|x_i-\mu_j\|_2^2,
\qquad
\mu_j=\frac{1}{|C_j|}\sum_{i\in C_j}x_i.
\]

Lloyd's algorithm alternates nearest-centroid assignment and centroid
recalculation until assignments and centroid movement stabilize. The
reference implementation uses k-means++ seeding, multiple starts and a
deterministic farthest-residual repair when a cluster becomes empty.

Features should be on comparable scales. The objective is sensitive to
outliers and can converge to a local minimum. This implementation does not
provide spatial contiguity, capacities, equal-size constraints, automatic k
selection, mini-batch updates or geodesic distance. Use k-medoids when means
are not meaningful or representatives must be observed objects.

See the [Python package](../../implementations/python/k-means/README.md)
and [tests](../../implementations/python/k-means/test_k_means.py).

References: Lloyd (1982), *Least squares quantization in PCM*; Arthur and
Vassilvitskii (2007), *k-means++: The advantages of careful seeding*.
