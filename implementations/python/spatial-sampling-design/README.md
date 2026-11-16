# Spatial sampling design

Pure-Python reference implementations for bounded continuous space-filling
sampling and point-cloud coverage summaries.

## Included algorithms

- **Latin hypercube sampling (LHS):** stratifies every coordinate dimension
  into n equal-width intervals and places exactly one sample in each interval.
- **Centered LHS:** uses each interval midpoint rather than random within-cell
  jitter.
- **Maximin LHS:** generates multiple randomized LHS candidates and retains the
  design maximizing minimum pairwise Euclidean distance after range
  normalization. It is a multi-start heuristic, not a global optimum proof.
- **K-means coverage:** deterministic farthest-first initialization followed
  by Lloyd centroid updates for a supplied point set. It is a local clustering
  heuristic, not an exact facility-location solver.

## Scope and assumptions

Bounds define a finite axis-aligned rectangle/hyperrectangle. LHS samples are
uniform within each stratum in each dimension; this does not imply arbitrary
joint distributions or spatially uniform coverage under a non-Euclidean
distance. Maximin uses normalized Euclidean distance, so each dimension has
equal range weight. K-means uses ordinary Euclidean distance and arithmetic
centroids; projected coordinates or another suitable metric are required for
geographic coordinates.

The source's "coffee-house" design label is not implemented because the source
does not define its construction or objective sufficiently to identify one
reproducible algorithm. Spatially constrained designs, unequal inclusion
probabilities, optimal-design criteria and uncertainty estimation are outside
this package.

## Run

    python -m pytest -q

The implementation uses only the Python standard library; pytest is the test
runner.
