# Weighted head-banging spatial smoother

A robust two-dimensional median smoother using nearly collinear triples around each target point to form low and high screens. A weighted median of the low screen, current value and high screen suppresses isolated spikes while retaining larger-scale edges.

The [Python implementation](../../implementations/python/head-banging/README.md) supports weighted screens, k-nearest neighbours, angular tolerance, a triple cap and iterative convergence.

The implementation uses projected Euclidean coordinates and leaves locations with no qualifying triples unchanged. It does not reproduce all corner rules or automatic parameter-selection features of the NCI Head-Bang software and provides no uncertainty or risk model.

## References

Hansen (1991); Mungiole, Pickle and Simonson (1999).
