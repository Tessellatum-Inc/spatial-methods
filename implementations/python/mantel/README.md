# Mantel and partial Mantel tests

Dependency-free teaching implementations for Pearson correlation between aligned pairwise distance matrices and the conventional partial-correlation extension.

~~~bash
python -m pip install -r requirements.txt
python -m pytest -q
~~~

~~~python
from mantel import mantel_test, partial_mantel_test
simple = mantel_test(distance_x, distance_y, permutations=999, seed=7)
partial = partial_mantel_test(distance_x, distance_y, geographic_distance,
                             permutations=999, seed=7)
~~~

Inputs must be finite, square, symmetric, non-negative distance matrices with zero diagonals, at least three observations and non-constant upper triangles. Observation order must match. The statistic is Pearson correlation of unique upper-triangle entries. Permutations relabel rows and columns together; cells are never shuffled independently. Monte Carlo p-values use the plus-one correction.

## Critical interpretation

The permutation test assumes exchangeability of observation labels under the null. It is not a general-purpose correction for spatial autocorrelation. Guillot and Rousset (2013) demonstrated serious Type I error inflation for simple and partial Mantel tests when both variables are spatially autocorrelated; adding geographic distance to a partial Mantel test does not generally fix this. A 2024 benchmark distinguishes hypotheses genuinely formulated in terms of distances from hypotheses about raw variables converted into distances: conversion can discard information and change the question. Prefer models aligned with the raw-data question, and use spatially structured null models when spatial dependence is central.

This implementation reproduces conventional tests so learners can examine and critique them; it does not claim calibrated inference under spatial autocorrelation.
