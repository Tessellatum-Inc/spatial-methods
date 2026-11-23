# Source verification — geographic distribution summaries

## Identity and bibliography
The four source-listed summaries are identified in ArcGIS Pro's measuring geographic distributions documentation: mean center, median center, standard distance and directional distribution (standard deviational ellipse). Kuhn and Kuenne (1962), “An Efficient Algorithm for the Numerical Solution of the Generalized Weber Problem in Spatial Economics,” *Journal of Regional Science*, 4(2), 21–33, DOI 10.1111/j.1467-9787.1962.tb00902.x, is the foundational iterative generalized Weber/median-center reference.

## Technical claims
Mean center is the weighted coordinate mean. Median center minimizes total weighted Euclidean distance and is computed iteratively. Standard distance is the weighted RMS radial distance from the mean center. The standard deviational ellipse is derived from the weighted coordinate covariance matrix; its eigenvectors give principal directions and square-root eigenvalues give principal-axis standard deviations. The implementation defines its orientation as counterclockwise from +x and exposes a scale parameter rather than silently applying a joint-coverage adjustment.

## Implementation and reproduction
Implemented: weighted mean center, weighted geometric median using modified Weiszfeld iteration and coincident-point optimality handling, weighted standard distance, and covariance eigen-axis standard deviational ellipse. Tests cover weighted/unweighted cases, outlier resistance, coincident-point updates, line and isotropic ellipses, scaling, and invalid inputs.

Not implemented: geographic/ellipsoidal distances, line/polygon centroid preprocessing, 3D ellipsoids, central feature, case-field grouping, output GIS geometries or inferential tests. Repository CI is required to establish committed test and notebook status.

## Rights
Mathematical definitions are independently typeset and paraphrased. No proprietary code, images or source text are reproduced.
