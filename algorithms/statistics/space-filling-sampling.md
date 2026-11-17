# Space-filling sampling designs

## Purpose

Space-filling designs distribute a finite set of evaluations across a
continuous parameter domain. They are useful when a spatial model, simulator,
or expensive objective function must be evaluated at a limited number of
locations. They are not automatically probability samples of a geographic
population: the design objective and the target inferential population must
be distinguished.

## Latin hypercube sampling

For n samples and d dimensions, divide each dimension's interval into n
equal-width strata. Independently permute the n strata in each dimension and
select one value inside each selected stratum. Consequently every one-
dimensional marginal has exactly one observation in every stratum.

For dimension j with bounds [a_j,b_j], stratum s has width
(b_j-a_j)/n. Random jitter chooses a point uniformly within that interval;
a centered design uses its midpoint. The method provides marginal
stratification, not a guarantee of low discrepancy or good joint separation.

## Maximin criterion

For a design X, its maximin score is

    delta(X) = min_{i != j} distance(x_i, x_j)

A maximin design seeks to maximize this minimum separation. The implementation
generates multiple LHS candidates and selects the one with the greatest
minimum Euclidean distance after scaling each dimension to [0,1]. This is a
transparent multi-start heuristic: the returned candidate is best among the
generated set, not necessarily globally optimal.

## Spatial thinning

Spatial thinning removes nearby candidate locations until every retained pair
is separated by at least a chosen Euclidean distance. The implementation uses
a seeded randomized sequential-inhibition baseline: shuffle candidate indices,
then retain a point only when it is at least the requested distance from every
already retained point. It returns original row indices so associated
attributes can be kept aligned. The reference implementation is O(n*m*d),
where m is the retained count, and is not a maximum-cardinality solution.

## K-means coverage

Given a finite set of candidate locations, k-means partitions observations
into k groups and represents each group by its centroid. The implementation
uses deterministic farthest-first initialization and Lloyd assignment/update
steps. The objective is within-cluster squared Euclidean distance, not the
maximin criterion. It is sensitive to coordinate units and outliers; use
projected coordinates or a metric-appropriate implementation for geographic
coordinates. A centroid need not coincide with an input candidate location.

## Complexity

For n LHS points in d dimensions, generation is O(nd) apart from per-dimension
permutation work O(d n). Scoring one maximin candidate is O(n^2 d), so C
candidates cost O(C n^2 d). Each k-means iteration costs O(n k d), plus
centroid updates O(n d); at most I iterations give O(I n k d).

## Limitations

- Independent LHS permutations do not control pairwise correlation.
- Euclidean distance in longitude/latitude degrees is not a valid general
  distance for geographic design.
- Maximin quality depends on candidate count and random seed.
- K-means can converge to a local minimum and is sensitive to initialization.
- Neither method supplies design-based inclusion probabilities by itself.
- The source's "coffee-house" term is retained as unresolved rather than
  assigned a guessed definition.

## Implementation and tests

The [reference package](../../implementations/python/spatial-sampling-design/README.md)
implements LHS, centered LHS, multi-start maximin LHS, spatial thinning, a pairwise-distance score and deterministic k-means coverage. Tests check marginal strata,
reproducibility, candidate selection, clustering behaviour and validation.

## References

- McKay, M. D., Beckman, R. J., & Conover, W. J. (1979). A Comparison of
  Three Methods for Selecting Values of Input Variables in the Analysis of
  Output from a Computer Code. *Technometrics*, 21(2), 239–245.
  https://doi.org/10.1080/00401706.1979.10489755
- Morris, M. D. & Mitchell, T. J. (1995). Exploratory designs for computer
  experiments. *Journal of Statistical Planning and Inference*, 43(3),
  381–402. https://doi.org/10.1016/0378-3758(94)00035-T
