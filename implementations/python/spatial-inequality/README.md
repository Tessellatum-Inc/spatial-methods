# Spatial inequality and segregation measures

Dependency-free area-level implementations of weighted Gini, Theil T, Theil L, Shannon entropy of population distribution, the two-group Duncan-Duncan dissimilarity index, and two-group isolation/interaction exposure indices.

## Quick start

~~~python
from inequality import (
    weighted_gini, theil_t, theil_l, spatial_entropy,
    dissimilarity_index, exposure_indices,
)

per_capita_income = [12, 18, 24, 40]
population = [100, 200, 150, 50]
print(weighted_gini(per_capita_income, population))
print(theil_t(per_capita_income, population))
print(theil_l(per_capita_income, population))
print(spatial_entropy(population))
print(dissimilarity_index([80, 20], [20, 80]))
print(exposure_indices([80, 20], [20, 80]))
~~~

## What each measure means

The weighted Gini uses a sorted cumulative-weight implementation with O(n log n) time rather than an explicit all-pairs O(n²) calculation.

- **Weighted Gini:** inequality of nonnegative area-level values, weighted by population or another exposure.
- **Theil T and L:** decomposable entropy-based inequality indices; T supports zero values, while L requires strictly positive values in every positive-weight area.
- **Spatial entropy:** Shannon entropy of how a population total is distributed across supplied areas; normalized entropy is 0-1. It uses area shares, not adjacency.
- **Dissimilarity:** the share of either of two groups that would need to be redistributed across areas for equal group distributions.
- **Isolation and interaction:** the average within-area group-A and group-B shares experienced by a randomly selected group-A member. With exactly two groups, they sum to one.

## Important scope boundary

The phrase "spatial inequality" covers more than these formulas. This package's Gini is a population-weighted inequality summary over area values, not a distance-weighted spatial Gini or spatial autocorrelation statistic. Spatial entropy is not a neighbourhood entropy or spatial information-theory model. Dissimilarity and exposure indices do not account for adjacency, distance decay, uncertainty, within-area mixing or the modifiable areal unit problem. The package does not implement multi-group segregation decomposition, clustering/proximity measures, concentration or centralization indices.

## Run

~~~bash
python -m pytest -q
~~~
