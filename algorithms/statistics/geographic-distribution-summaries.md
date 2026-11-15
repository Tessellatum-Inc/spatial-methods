# Mean center, median center, standard distance and standard deviational ellipse

These summaries describe the centre, compactness and directional spread of a planar point distribution.

- **Mean center:** weighted arithmetic mean of x and y.
- **Median center:** weighted geometric median minimizing total Euclidean distance.
- **Standard distance:** weighted root-mean-square radial distance from the mean center.
- **Standard deviational ellipse:** principal-axis standard deviations and orientation from the weighted coordinate covariance matrix.

The [implementation](../../implementations/python/spatial-distribution-summaries/README.md) includes a modified Weiszfeld geometric-median solver and explicit ellipse orientation and scaling conventions.

## Assumptions and limitations

Use projected planar coordinates. These are descriptive summaries, not cluster tests. The implementation accepts points only; it does not handle line/polygon centroids, geographic distances, 3D ellipsoids, grouped case fields or output geometry construction.

## References

Kuhn and Kuenne (1962), “An Efficient Algorithm for the Numerical Solution of the Generalized Weber Problem in Spatial Economics,” *Journal of Regional Science*, 4(2), 21–33. DOI 10.1111/j.1467-9787.1962.tb00902.x.
