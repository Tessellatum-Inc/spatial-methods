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
