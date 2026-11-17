# Lloyd k-means implementation verification

Implemented: finite 2-D numeric input validation; k-means++ initialization;
Lloyd assignment/update; multiple starts; deterministic empty-cluster repair;
within-cluster sum-of-squares objective and convergence metadata.

Independent tests recompute inertia from returned labels and cluster means,
check separated groups, seeded repeatability, duplicate observations, k=n,
and invalid controls/data.

Not implemented: constrained/equal-size assignments, spatial contiguity,
automatic k selection, mini-batch updates, spherical/kernel variants and
geodesic distance.
