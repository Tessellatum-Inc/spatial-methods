# Interpolation and approximation

**Subject identity:** \`SM-FND-016\` — Numerical analysis and scientific computing  
**Module:** 08  
**Status:** Initial public teaching resource; independent numerical-analysis review and learner testing outstanding.

## 1. The problem: estimating values between or beyond observations

Spatial datasets rarely provide a value at every location or time of interest. A survey measures selected points, a sensor samples a field at discrete locations, and a raster represents a continuous phenomenon on a finite grid. Interpolation and approximation provide mathematical ways to construct a usable function from these finite inputs.

The distinction matters:

- **Interpolation** constructs a function that passes through the supplied data points (subject to the method's definition and numerical precision).
- **Approximation** constructs a function that represents the data according to a chosen criterion, but generally does not pass through every observation.
- **Extrapolation** estimates beyond the spatial or temporal support of the observations. It relies on assumptions that are usually stronger and less testable than those required for interpolation.

A surface that passes exactly through every observation is not necessarily the most accurate representation of the underlying phenomenon. If observations contain measurement error, exact interpolation may reproduce noise as if it were real structure. Conversely, smoothing or approximation may suppress genuine local features. The method must reflect the data-generating process and intended use.

## 2. Mathematical formulation

Given distinct sample locations \(x_0,\ldots,x_n\) and observed values \(y_0,\ldots,y_n\), interpolation seeks a function \(p(x)\) satisfying

\[
p(x_i)=y_i,\qquad i=0,\ldots,n.
\]

Approximation instead chooses a function \(g(x;\boldsymbol{\theta})\), parameterised by \(\boldsymbol{\theta}\), to minimise an objective such as a weighted sum of squared residuals:

\[
\min_{\boldsymbol{\theta}}
\sum_{i=1}^{n}w_i
\left[y_i-g(x_i;\boldsymbol{\theta})\right]^2.
\]

The weights \(w_i\) may reflect a statistical model or deliberate importance weighting. Their meaning should be documented; inverse-variance weights are justified only when the corresponding error model is appropriate.

For spatial coordinates \(\mathbf{s}_i=(x_i,y_i)\), the corresponding surface problem is

\[
\hat z(\mathbf{s})=\mathcal{I}
\left\{(\mathbf{s}_i,z_i)\right\},
\]

where \(\mathcal{I}\) denotes a chosen interpolation operator. The output is not determined by the observations alone. It also depends on the method, distance metric, neighbourhood, support, parameters, boundary treatment and assumptions about spatial continuity.

## 3. Polynomial interpolation

### 3.1 Lagrange form

For \(n+1\) distinct one-dimensional nodes, the unique polynomial of degree at most \(n\) passing through all observations can be written

\[
p_n(x)=\sum_{i=0}^{n}y_i L_i(x),
\]

where

\[
L_i(x)=
\prod_{\substack{j=0\\j\ne i}}^{n}
\frac{x-x_j}{x_i-x_j}.
\]

Each basis polynomial is one at its own node and zero at all other nodes, so \(p_n(x_i)=y_i\).

The existence and uniqueness of this polynomial do not imply that it is a good approximation between nodes. High-degree global polynomials can oscillate strongly, especially near interval boundaries, and the computation can be ill-conditioned.

### 3.2 Newton divided differences

Newton's form expresses the polynomial using nested products:

\[
p_n(x)=a_0
+a_1(x-x_0)
+a_2(x-x_0)(x-x_1)+\cdots.
\]

The coefficients are divided differences. For example,

\[
f[x_i,x_{i+1}]
=\frac{y_{i+1}-y_i}{x_{i+1}-x_i}.
\]

Higher-order divided differences are defined recursively. Newton's representation is convenient when adding observations because the existing polynomial representation can be extended with another term. It does not eliminate the conditioning problems of a high-degree global polynomial.

### 3.3 Runge phenomenon and node choice

Equally spaced nodes can produce large oscillations in high-degree polynomial interpolation, a behaviour illustrated by the Runge phenomenon. Increasing polynomial degree is therefore not a reliable universal strategy for improving interpolation.

For a smooth function on a bounded interval, Chebyshev-distributed nodes often reduce the worst interpolation error compared with equally spaced nodes. Stable barycentric evaluation is commonly preferred to directly expanding a high-degree polynomial into monomial coefficients. The choice of nodes and evaluation algorithm is part of numerical stability, not just mathematical notation.

## 4. Piecewise interpolation

Instead of fitting one global polynomial, piecewise methods construct a local function over each interval or element.

### 4.1 Piecewise linear interpolation

For \(x_i\le x\le x_{i+1}\),

\[
p(x)=
y_i+
\frac{x-x_i}{x_{i+1}-x_i}(y_{i+1}-y_i).
\]

This is simple, local and shape-preserving between two endpoints: the interpolated value remains between \(y_i\) and \(y_{i+1}\). The function is continuous when adjacent segments share their observed endpoints, but its derivative may jump at sample nodes.

Piecewise linear interpolation is often appropriate when a simple, transparent local model is preferred. It does not imply that the real process is linear at sub-sample scales.

### 4.2 Cubic splines

A cubic spline uses a cubic polynomial on each interval and imposes continuity conditions at the knots. A standard cubic spline is typically constructed so that the function, first derivative and second derivative are continuous at interior knots. Additional boundary conditions are required, such as natural, clamped or not-a-knot conditions.

Natural cubic splines set the second derivative to zero at both ends. Clamped splines specify endpoint first derivatives. These are different modelling assumptions and can produce different results, especially near the boundaries.

Splines can provide smooth curves without the oscillation often associated with one high-degree global polynomial. However, cubic splines can overshoot data near sharp transitions, and their smoothness assumptions may be inappropriate at physical discontinuities or abrupt boundaries.

### 4.3 Shape-preserving interpolation

Methods such as piecewise cubic Hermite interpolation can preserve monotonicity under suitable slope-selection rules. They are useful when overshoot would be misleading, for example when interpolating a monotone profile or a bounded physical quantity.

Shape preservation is a constraint on the interpolant, not evidence that the underlying phenomenon is monotone between observations. The selected shape properties should be justified by domain knowledge.

## 5. Multidimensional spatial interpolation

Spatial interpolation extends the one-dimensional problem to points or regions in two or more dimensions. The method should account for the geometry and sampling design.

Common families include:

- **Triangulation-based linear interpolation:** partition the sample locations into triangles and interpolate linearly within each triangle. It is local and transparent but has piecewise planar facets and does not naturally extend beyond the convex hull without an additional rule.
- **Inverse distance weighting (IDW):** calculate a weighted average of nearby observations, often with weights proportional to inverse distance raised to a power. It is exact at sample locations under common formulations but can create bull's-eye patterns and depends on distance, power and neighbourhood choices.
- **Radial basis functions (RBFs):** combine basis functions of distance from sample locations, optionally with a polynomial term. Their behaviour depends on the kernel, shape parameters, smoothing and numerical solution of the resulting system.
- **Kriging:** uses a stochastic spatial model, including a variogram or covariance structure, to form a predictor and often a prediction variance. Its assumptions and model fitting are part of the method; it is not simply a distance-weighted average.

No method is universally best. Sampling geometry, spatial anisotropy, barriers, discontinuities, trend, variable support, data uncertainty and the intended prediction domain all influence the choice.

### 5.1 Distance is a model choice

IDW, many RBF methods and spatial neighbourhood definitions depend on distance. Euclidean distance in projected coordinates may be reasonable over a local area when the projection distortion is acceptable. Angular differences in longitude and latitude are not a uniform ground-distance metric. Large regions may require geodesic distances or a suitable projection.

Anisotropy means spatial dependence varies with direction. A distance model may account for it by transforming coordinates or using direction-dependent structures, but the orientation and scale should be supported by the phenomenon and data rather than selected solely to improve a visual result.

### 5.2 Barriers and discontinuities

A straight-line distance can connect points that are close in map space but separated by a river boundary, ridge, wall, coastline or other barrier. Likewise, a smooth interpolator can blur across a fault, land-cover boundary or abrupt change in physical regime.

Possible responses include partitioning the domain, using network or cost distance, incorporating barrier-aware covariance structures, or modelling distinct regimes separately. The method should not interpolate through a barrier merely because the software can do so.

## 6. Approximation and regression

When observations are noisy, fitting a model that passes through every point may overfit. Approximation instead balances fit and complexity.

For a linear model in parameters,

\[
\mathbf{y}\approx A\boldsymbol{\beta},
\]

ordinary least squares chooses

\[
\hat{\boldsymbol{\beta}}
=\arg\min_{\boldsymbol{\beta}}
\|\mathbf{y}-A\boldsymbol{\beta}\|_2^2.
\]

Weighted least squares uses a weight matrix when the error structure justifies it. The numerical solution should generally use stable factorisation methods such as QR or SVD rather than forming normal equations blindly; see [numerical stability and backward error](numerical-stability-and-backward-error.md) and the [least-squares foundation](../linear-algebra/least-squares-and-constrained-systems.md).

A more flexible model may reduce training residuals while predicting worse at unsampled locations. Complexity, regularisation and validation are therefore central to approximation. A smoothing spline, for example, balances data fit with a penalty on curvature; the smoothing parameter controls the trade-off between fidelity and smoothness.

The distinction between fitting and prediction is essential: a model can be an excellent interpolant of the observed samples and still be a poor predictor of the spatial process.

## 7. Raster resampling is not the same as spatial interpolation

Raster resampling estimates values on a new grid from an existing raster. It is a grid-to-grid transformation and should be distinguished from constructing a continuous spatial surface from scattered observations.

Common resampling rules include:

- **Nearest neighbour:** copies the value from the nearest source cell. It preserves categorical labels and original values but can create blocky patterns.
- **Bilinear:** computes a weighted average of the four surrounding cell-centre values. It is often used for continuous rasters but smooths local variation.
- **Cubic convolution:** uses a larger neighbourhood and a cubic weighting function. It can produce smoother images but may overshoot or create values outside the local source range.

For categorical data, interpolating class codes numerically is generally meaningless; nearest neighbour or a category-aware aggregation is more appropriate. For continuous data, the resampling method should reflect the quantity, source resolution and intended use.

Resampling does not create new measurement information. Reprojecting a raster may change pixel values and spatial support; repeated resampling can introduce additional smoothing or artefacts. Preserve the original data and document the transformation, target grid, resolution, alignment and resampling kernel.

## 8. Boundaries, support and extrapolation

An interpolator is most defensible within the region supported by observations and the method's assumptions. Predictions outside the convex hull of scattered points, beyond a sampled time range, or across unobserved gaps are extrapolations or weakly supported estimates.

A spatial workflow should identify:

- the observation footprint and convex hull;
- holes and internal gaps in the sampling design;
- physical boundaries and barriers;
- the support of each observation (point, line, area or volume);
- whether the prediction target has the same support;
- any extrapolation beyond observed coverage.

A point measurement, a cell average and a polygon-wide total are not interchangeable. Changing support can require aggregation, disaggregation or a change-of-support model rather than ordinary interpolation.

## 9. Validation and uncertainty

Interpolation and approximation should be assessed using observations that were not used to fit or tune the model. Common diagnostics include mean error, mean absolute error and root mean squared error:

\[
\mathrm{ME}=\frac{1}{n}\sum_{i=1}^{n}(\hat y_i-y_i),
\]

\[
\mathrm{MAE}=\frac{1}{n}\sum_{i=1}^{n}|\hat y_i-y_i|,
\qquad
\mathrm{RMSE}=
\sqrt{\frac{1}{n}\sum_{i=1}^{n}(\hat y_i-y_i)^2}.
\]

Random train/test splits can be misleading for spatial data because nearby training and test observations may be strongly correlated. Spatial block cross-validation or spatially separated holdouts can better assess transfer to unsampled locations, although the validation design should reflect the intended deployment domain.

Validation scores do not automatically describe uncertainty everywhere. Prediction uncertainty depends on the model, sampling geometry, measurement error, parameter estimation and distance from observations. Kriging variance, for example, is conditional on the fitted covariance model and its assumptions; it is not a universal measure of total uncertainty.

A sound assessment should examine residual maps, error by distance and region, directional patterns, boundary behaviour, outliers, and performance in the conditions where the method will actually be used. Avoid selecting a model solely by a single aggregate score.

## 10. Worked example: linear interpolation along a profile

Two synthetic observations describe a profile: at \(x_0=0\) m, the elevation is \(z_0=100\) m; at \(x_1=20\) m, the elevation is \(z_1=104\) m. The piecewise-linear interpolant at \(x=5\) m is

\[
z(5)=100+\frac{5-0}{20-0}(104-100)=101\ \mathrm{m}.
\]

The calculation is exact for the linear model connecting the two observations. It does not prove that the actual terrain elevation at 5 m is 101 m. A ridge, channel or other feature between the samples could make the real profile differ substantially. The spacing and sampling design determine what features can be resolved.

## 11. Method-selection guide

| Data and objective | Candidate method | Key checks |
|---|---|---|
| Sparse profile with local piecewise-linear assumption | Linear interpolation | Sampling gaps, sharp features and units |
| Smooth one-dimensional curve | Cubic spline | Boundary conditions, overshoot and smoothness |
| Scattered points over a local surface | Triangulation, IDW or RBF | Geometry, barriers, anisotropy and support |
| Spatially correlated observations with a defensible covariance model | Kriging | Variogram fit, stationarity, anisotropy and prediction variance |
| Noisy observations where exact fit is undesirable | Regression or smoothing approximation | Model complexity, residual structure and validation |
| Reprojecting a categorical raster | Nearest-neighbour resampling | Class integrity and grid alignment |
| Reprojecting a continuous raster | Bilinear or cubic resampling | Smoothing, overshoot, source resolution and repeated resampling |

The candidate list is not a ranking. The appropriate method depends on the phenomenon, measurement process, sampling design, support and prediction objective.

## 12. Exercises

### Exercise 1 — Interpolation versus approximation

Explain the difference between an interpolant and a least-squares approximation. Why might exact interpolation be undesirable for noisy survey observations?

### Exercise 2 — Linear interpolation

Two profile samples are \(z(10)=50\) m and \(z(30)=58\) m. Estimate the interpolated value at \(x=15\) m using a linear model.

### Exercise 3 — Global polynomial risk

Why can increasing the degree of a polynomial interpolant make the result worse between equally spaced observations?

### Exercise 4 — Raster resampling

Which common resampling method is generally appropriate for a categorical land-cover raster, and why is bilinear interpolation usually inappropriate for class codes?

### Exercise 5 — Spatial validation

Why can random cross-validation overestimate the predictive performance of a spatial interpolator? Describe one alternative validation design.

### Exercise 6 — Extrapolation

A set of elevation observations occupies a small convex region. A model is used to predict a surface well outside that region. What additional risk does this introduce?

### Exercise 7 — Support

Explain why interpolating point measurements to a grid does not automatically produce valid cell-average values.

## 13. Answers and discussion

1. An interpolant passes through the supplied data points, while an approximation minimises a chosen discrepancy and need not pass through each observation. Exact interpolation may reproduce measurement noise as if it were genuine spatial variation.
2. The linear fraction is \((15-10)/(30-10)=1/4\). The estimate is \(50+(1/4)(58-50)=52\) m.
3. High-degree global polynomials can oscillate strongly between nodes, particularly near interval boundaries. Conditioning and node placement also affect the computed result; higher degree is not a guarantee of better approximation.
4. Nearest neighbour generally preserves the original class labels. Bilinear interpolation averages numeric codes, but class identifiers are nominal categories and their arithmetic mean has no meaningful class interpretation.
5. Nearby observations may be correlated, so a randomly withheld point can be predicted using nearly redundant nearby training points. Spatial block or geographically separated holdouts better test prediction at less-sampled locations when that matches the intended use.
6. The model is extrapolating beyond the observation support. Its assumptions are less constrained by data, so predictions may be highly sensitive to model choice and unobserved spatial structure.
7. A point sample represents a value at a location, while a cell average represents an integral over an area divided by that area. Constructing cell averages requires an explicit support and aggregation model; point interpolation alone does not establish that relationship.

## 14. Connections to other Spatial Methods resources

- [Numerical integration and quadrature](numerical-integration-and-quadrature.md) explains how interpolated fields can be integrated and why support and area measures matter.
- [Numerical differentiation](numerical-differentiation.md) explains derivative estimation from sampled and interpolated fields.
- [Sensitivity and perturbation analysis](sensitivity-and-perturbation-analysis.md) provides tools for understanding how input and parameter changes affect model outputs.
- [Numerical stability and backward error](numerical-stability-and-backward-error.md) explains conditioning and stable least-squares computation.
- [Covariance matrices and multivariate structure](../linear-algebra/covariance-matrices-and-multivariate-structure.md) supports weighted models and covariance-based spatial prediction.
- [Coordinate transformation and CRS axis order](../../algorithms/geodesy/crs-transformation.md) is relevant when distance, direction and area depend on coordinate representation.

## 15. Further reading

- Philip J. Davis, *Interpolation and Approximation*, Dover Publications, 1975.
- Carl de Boor, *A Practical Guide to Splines*, revised edition, Springer, 2001.
- Roberts, D. R., Bahn, V., Ciuti, S., Boyce, M. S., Elith, J., Guillera-Arroita, G., Hauenstein, S., Lahoz-Monfort, J. J., Schröder, B., Thuiller, W., Warton, D. I., Wintle, B. A., Hartig, F. and Dormann, C. F. (2017). “Cross-validation strategies for data with temporal, spatial, hierarchical, or phylogenetic structure.” *Ecography*, 40(8), 913–929.
- Noel A. C. Cressie, *Statistics for Spatial Data*, revised edition, Wiley, 1993.

These references are starting points for technical review, not claim-by-claim citations. The module remains an initial teaching resource pending independent review and learner testing.
