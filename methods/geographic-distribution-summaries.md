# Geographic distribution summaries

These descriptive summaries answer different questions about the centre, compactness and directional spread of a set of planar locations. Use a projected coordinate system so Euclidean distances and covariance have meaningful linear units.

## Mean center

For points (x_i,y_i) and nonnegative weights w_i with positive total,

\[
\bar x_w=\frac{\sum_i w_i x_i}{\sum_i w_i},\qquad
\bar y_w=\frac{\sum_i w_i y_i}{\sum_i w_i}.
\]

The mean center is sensitive to outlying locations.

## Median center

The geometric median minimizes

\[
m^*=\arg\min_m\sum_i w_i\lVert x_i-m\rVert_2.
\]

It is less influenced by distant outliers than the mean center. The implementation uses modified Weiszfeld iteration and handles candidate iterates that coincide with observations through a subgradient optimality check. Multiple minimizers can exist in degenerate configurations.

## Standard distance

The weighted standard distance is the root-mean-square radial distance from the weighted mean center:

\[
SD_w=\sqrt{\frac{\sum_i w_i[(x_i-\bar x_w)^2+(y_i-\bar y_w)^2]}{\sum_i w_i}}.
\]

It is a single scalar summary of compactness.

## Standard deviational ellipse

The weighted population covariance matrix is

\[
C=\frac{1}{\sum_i w_i}
\sum_i w_i
\begin{pmatrix}
(x_i-\bar x_w)^2 & (x_i-\bar x_w)(y_i-\bar y_w)\\
(x_i-\bar x_w)(y_i-\bar y_w) & (y_i-\bar y_w)^2
\end{pmatrix}.
\]

The eigenvectors give the principal directions and square roots of the eigenvalues give the principal-axis standard deviations. The implementation reports orientation counterclockwise from +x. Its default semiaxis scale is 1; a scale of approximately 1.515 gives the joint 68.3-percent ellipse for a bivariate normal distribution (the square root of the 68.3rd percentile of chi-square with two degrees of freedom). Do not assume that an unadjusted one-standard-deviation ellipse contains 68 percent of a two-dimensional normal distribution.

## Scope and cautions

These are descriptive summaries, not tests of spatial clustering or directional significance. The ellipse assumes a Euclidean projected plane and summarizes second moments; it can be strongly influenced by outliers. The median center minimizes total Euclidean distance but is iterative. The package accepts point coordinates only, not line/polygon geometries, geographic coordinates, 3D data or grouped case fields.

## References

- Kuhn, H. W. and Kuenne, R. E. (1962). “An Efficient Algorithm for the Numerical Solution of the Generalized Weber Problem in Spatial Economics.” *Journal of Regional Science*, 4(2), 21–33. DOI [10.1111/j.1467-9787.1962.tb00902.x](https://doi.org/10.1111/j.1467-9787.1962.tb00902.x).
- Esri, ArcGIS Pro documentation: [Median Center](https://doc.esri.com/en/arcgis-pro/latest/tool-reference/spatial-statistics/median-center.html), [Standard Distance](https://doc.esri.com/en/arcgis-pro/latest/tool-reference/spatial-statistics/standard-distance.html), and [How Directional Distribution works](https://doc.esri.com/en/arcgis-pro/latest/tool-reference/spatial-statistics/h-how-directional-distribution-standard-deviationa.html).
