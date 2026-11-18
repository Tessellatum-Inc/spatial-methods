# Walkthrough: exact max-min p-dispersion

1. Start from a pairwise distance matrix whose rows and columns refer to the same candidate set. Validate symmetry, non-negativity, finiteness and a zero diagonal.
2. Enumerate every size-p subset of candidate indices.
3. For each subset, calculate all pairwise distances among its selected sites and retain the minimum. This is the subset's separation score.
4. Keep the subset with the largest minimum separation. Strict improvement and lexicographic combination order provide deterministic tie-breaking.

The number of subsets is `binomial(n, p)`. This exact implementation is valuable for small examples, regression tests and validating heuristics, but it is not suitable for large candidate sets. The distance matrix determines the metric: Euclidean, geodesic or network distances can be supplied if computed consistently before solving.
