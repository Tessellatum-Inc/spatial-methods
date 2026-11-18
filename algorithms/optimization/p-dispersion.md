# The max-min p-dispersion problem

## Problem

Given n candidate sites and a distance function d, choose exactly p distinct sites to maximise the minimum pairwise distance among the selected sites:

`max over S, |S| = p of min{d(i,j) : i,j in S, i != j}`.

This is a dispersion objective: it spreads selected facilities or representatives apart. It is not p-median (which minimises demand-weighted assignment cost) or p-center (which minimises the maximum demand-to-facility distance).

## Exact small-instance baseline

The repository includes an [exact exhaustive Python solver](../../implementations/python/p-dispersion/README.md). It enumerates every p-subset, evaluates its closest selected pair and retains the subset with the largest separation. Equal optima use lexicographic candidate-index tie-breaking. A [verification record](../../catalog/verification/p-dispersion.md) describes tests and limits.

## Distance model and cautions

The solver accepts a pairwise distance matrix. Euclidean, geodesic or network distances can be used only if the supplied matrix represents a consistent metric for the actual decision context. Straight-line distance may be inappropriate where barriers, access rights or travel networks determine separation.

## Complexity and limits

There are `binomial(n,p)` candidate subsets; each subset requires evaluating its pairwise distances. This is an exact teaching baseline and small-instance oracle, not a scalable solver. It does not include demand assignment, capacities, service coverage, uncertainty or equity constraints.

## References

- Kuby, M. (1987). Programming models for facility dispersion: the p-dispersion and maxisum dispersion problems. *Geographical Analysis*, 19(4), 315–329. https://doi.org/10.1111/j.1538-4632.1987.tb00133.x
