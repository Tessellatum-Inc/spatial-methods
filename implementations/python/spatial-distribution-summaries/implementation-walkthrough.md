# Spatial distribution summaries — implementation walkthrough

## 1. Mean center
The mean center is the weighted arithmetic mean of coordinate values. It is quick to calculate but sensitive to distant outliers.

## 2. Median center
The median center minimizes the sum of weighted Euclidean distances. The implementation uses Weiszfeld iteration. When an iterate coincides with one or more input points, a modified Vardi-Zhang step checks the subgradient optimality condition and avoids division by zero.

## 3. Standard distance
The standard distance is the square root of the weighted mean squared radial distance from the mean center. It gives one scalar measure of dispersion.

## 4. Standard deviational ellipse
The weighted coordinate covariance matrix is symmetric and positive semidefinite. Its eigenvectors define the principal directions; square roots of eigenvalues give the semiaxes. The orientation convention is explicitly counterclockwise from the positive x-axis.

## 5. Scope
These functions accept projected planar point coordinates. They do not build polygons or ellipses, interpret geographic coordinates geodesically, or provide inferential tests.


## 6. Circular and directional statistics

The companion `directional_statistics.py` module converts each angle to the unit circle and computes mean sine/cosine components. The circular mean is undefined when those components cancel. Rayleigh's test uses the resultant length and a finite-sample approximation, while Kuiper's statistic sums the upper and lower empirical-CDF deviations and is therefore invariant to rotating the angular origin. The von Mises density uses the modified Bessel normalizer; the rose histogram bins normalized angles and optionally accumulates nonnegative weights.

These are deliberately distinct deliverables. Rayleigh is a focused unimodal-concentration test, Kuiper is a broader omnibus uniformity test, and neither corrects for spatial or temporal dependence. The Kuiper p-value is asymptotic. See the canonical lesson for assumptions and interpretation.
