# Verification dossier: random-walker segmentation

## Implemented scope

Four-neighbour multi-label random-walker segmentation on 2D scalar or multichannel arrays, with fixed seed labels and sparse Dirichlet Laplacian solve.

## Independent tests

Tests cover propagation across a two-region image, exact seed preservation, probability normalization, analytic linear harmonic probabilities for a one-dimensional uniform-weight grid, multichannel input, sorted class labels, fully seeded rasters and malformed inputs.

## Exclusions

GrabCut, seeded region growing, eight-neighbour graph variants, physical pixel spacing and production-scale iterative solvers remain open. The grouped source row is Partial.