# Numerical integration and quadrature

**Subject identity:** \`SM-FND-016\` — Numerical analysis and scientific computing  
**Module:** 07  
**Status:** Initial public teaching resource; independent numerical-analysis review and learner testing outstanding.

## 1. Why numerical integration matters

Integration accumulates a quantity over an interval, region or volume. In spatial work, it is used to estimate area, terrain and water volume, population totals, pollutant loads, energy or exposure over a region, travel-cost accumulation along a route, and averages of spatial fields. It also appears inside physical models, probability calculations, parameter estimation and the numerical solution of differential equations.

When an antiderivative is unavailable or the input is supplied only at sampled locations, an integral is approximated numerically. The resulting method is called a quadrature rule in one dimension. Numerical integration is not simply “adding up pixels”: a valid calculation must define the quantity being integrated, its units, the spatial measure, the domain, the sampling or interpolation model, and how gaps and boundaries are treated.

This module distinguishes:

1. **Analytic integration:** evaluate an exact mathematical integral where a suitable antiderivative or theorem is available.
2. **Numerical quadrature:** approximate an integral from function evaluations.
3. **Discrete spatial aggregation:** combine measured or modelled cell values with appropriate cell areas, weights or volumes. This may be a numerical approximation to a continuous integral, but the relationship depends on what each cell value represents.

## 2. The integral as an accumulated quantity

For an integrable function \(f(x)\), the definite integral over an interval is

\[
I=\int_a^b f(x)\,\mathrm{d}x.
\]

If \(f\) has units \(U_f\) and \(x\) has units \(U_x\), the integral has units \(U_f U_x\). For example, integrating a cross-sectional area (square metres) along a length (metres) gives a volume (cubic metres).

An average value over a nonzero interval is

\[
\bar f=\frac{1}{b-a}\int_a^b f(x)\,\mathrm{d}x.
\]

For a spatial field \(z(x,y)\) over a region \(A\), the area integral is

\[
I_A=\iint_A z(x,y)\,\mathrm{d}A.
\]

If \(z\) is population density in persons per square kilometre, the area integral gives a population count (subject to the density model and compatible area units). If \(z\) is elevation, the integral over a horizontal area has units of cubic metres and can represent volume relative to the chosen vertical reference surface. The reference surface and sign convention must be stated.

The integral depends on the measure used. In projected planar coordinates, a simple area element is \(\mathrm{d}A=\mathrm{d}x\,\mathrm{d}y\), but the projection distorts area unless the calculation accounts for its scale or uses an appropriate equal-area system. On the ellipsoid or sphere, the area element and geometry differ. Coordinate units alone do not guarantee that a planar coordinate area equals ground area.

## 3. Riemann sums and the idea behind quadrature

Partition \([a,b]\) into subintervals with widths \(\Delta x_i\). A Riemann sum is

\[
I\approx\sum_{i=1}^{n} f(\xi_i)\Delta x_i,
\]

where \(\xi_i\) is a chosen sample point in the \(i\)-th subinterval. As the partition is refined, such sums converge to the integral for suitable integrable functions and partitions.

The sample-point choice leads to familiar rules:

- left or right rectangles use an endpoint value;
- midpoint rectangles use the midpoint of each interval;
- trapezoidal quadrature approximates the function by straight segments;
- Simpson's rule approximates it locally with quadratic polynomials.

A smaller interval width often improves approximation for a smooth function, but it increases evaluations and can amplify data noise or floating-point accumulation error. Refinement is not automatically a cure for a poor model, discontinuity, unsuitable coordinate measure or noisy observations.

## 4. Basic one-dimensional rules

### 4.1 Composite midpoint rule

For \(n\) equal subintervals with width \(h=(b-a)/n\), the composite midpoint rule is

\[
I\approx h\sum_{i=0}^{n-1} f\!\left(a+\left(i+\frac12\right)h\right).
\]

For sufficiently smooth \(f\), its global truncation error is second order, \(O(h^2)\). It can be effective when midpoint evaluations are available and the integrand is smooth over each cell.

### 4.2 Composite trapezoidal rule

For equally spaced samples \(x_i=a+ih\),

\[
I\approx T_n
=h\left[
\frac{f(x_0)}{2}
+\sum_{i=1}^{n-1}f(x_i)
+\frac{f(x_n)}{2}
\right].
\]

For a sufficiently smooth function, its global error is second order. A common error expression is

\[
I-T_n=-\frac{(b-a)h^2}{12}f''(\xi)
\]

for some \(\xi\in(a,b)\), under the standard smoothness assumptions. The formula makes clear that error depends on curvature as well as step size.

The trapezoidal rule is often a natural choice for sampled profiles and piecewise-linear representations. If the piecewise-linear model is itself the intended representation, the trapezoidal calculation integrates that model exactly over each segment; it does not remove uncertainty in the sampled values or prove that the real phenomenon is linear between samples.

### 4.3 Composite Simpson's rule

For an even number \(n\) of equal subintervals,

\[
I\approx S_n
=\frac{h}{3}\left[
f(x_0)+f(x_n)
+4\sum_{\substack{i=1\\i\ \mathrm{odd}}}^{n-1}f(x_i)
+2\sum_{\substack{i=2\\i\ \mathrm{even}}}^{n-2}f(x_i)
\right].
\]

The composite rule has fourth-order global truncation error, \(O(h^4)\), for sufficiently smooth functions. It integrates polynomials up to degree three exactly in exact arithmetic.

The requirement for an even number of subintervals is part of the standard composite formula. If the sample count or spacing does not meet its assumptions, do not silently apply the formula as if it did. Use a justified mixed rule, local polynomial method or another quadrature method and document the choice.

Higher formal order is not always better. Simpson's rule may perform poorly near discontinuities, sharp transitions or noisy samples, and its polynomial assumptions may be inappropriate for a field with abrupt physical boundaries.

## 5. Gaussian quadrature

Gaussian quadrature chooses both the evaluation nodes and weights to integrate polynomials of high degree exactly with relatively few function evaluations. On \([-1,1]\), an \(n\)-point Gauss–Legendre rule has the form

\[
\int_{-1}^{1} f(t)\,\mathrm{d}t
\approx\sum_{i=1}^{n}w_i f(t_i),
\]

where \(t_i\) are the Legendre polynomial roots and \(w_i\) are corresponding weights. It is exact for polynomials of degree up to \(2n-1\), in exact arithmetic.

To integrate over \([a,b]\), map \(t\in[-1,1]\) to

\[
x=\frac{a+b}{2}+\frac{b-a}{2}t,
\qquad
\mathrm{d}x=\frac{b-a}{2}\mathrm{d}t.
\]

Therefore,

\[
\int_a^b f(x)\,\mathrm{d}x
\approx
\frac{b-a}{2}
\sum_{i=1}^{n}w_i
f\!\left(\frac{a+b}{2}+\frac{b-a}{2}t_i\right).
\]

Gaussian quadrature can be very efficient for smooth functions when arbitrary function evaluations are possible. It is less directly suited to a fixed raster or observation table whose values are known only at particular locations. For such data, interpolation or a quadrature rule designed for the sampling structure is required; that introduces additional modelling assumptions.

## 6. Adaptive quadrature

A fixed-step rule uses a prescribed partition. Adaptive quadrature refines the partition where the integrand appears harder to approximate and uses larger intervals where the approximation is adequate.

A common pattern is:

1. Approximate the integral over an interval using a rule.
2. Approximate it again over two or more subintervals.
3. Compare the estimates to obtain an error indicator.
4. Subdivide intervals whose estimated error exceeds their allocated tolerance.
5. Stop when the global error budget is met or a resource limit is reached.

For adaptive Simpson quadrature, a common local error estimate compares one Simpson estimate over an interval with the sum of estimates over its two halves. Under smoothness assumptions, the difference divided by 15 estimates the leading error in the refined estimate. The estimate is not a universal guarantee: it can be misleading for discontinuities, unresolved narrow features, noisy functions or severe cancellation.

Adaptive methods should report the tolerance, evaluation limit, subdivision strategy and convergence status. A routine returning a number is not proof that the requested error bound was achieved.

## 7. Error sources and reliable stopping

Numerical integration has several distinct sources of error:

- **Quadrature truncation error:** the chosen rule approximates the integral rather than evaluating it exactly.
- **Input or model error:** the function may be estimated from measurements, interpolation or a physical model.
- **Domain error:** the integration boundary may be incomplete, misregistered or defined in the wrong coordinate system.
- **Floating-point error:** function evaluations, weighted sums and accumulation use finite precision.
- **Sampling error:** a finite set of observations may fail to resolve important spatial variation.

For adaptive algorithms, an estimated quadrature error is often compared with a mixed tolerance,

\[
E_{\mathrm{est}}\le
\tau_{\mathrm{abs}}+\tau_{\mathrm{rel}}|I_{\mathrm{est}}|,
\]

where the absolute and relative tolerances are selected for the units and scale of the quantity. When the true integral is near zero, a relative tolerance alone is inadequate.

A numerical tolerance should not be confused with the uncertainty of the observations. If a volume is computed from a terrain model with metre-scale vertical uncertainty, driving the quadrature estimate to micrometre-scale numerical error does not make the volume known to that precision.

For long sums, use numerically appropriate accumulation such as pairwise or compensated summation where warranted. The discussion of [floating-point rounding and computational error](floating-point-numbers-rounding-and-computational-error.md) and [numerical stability and backward error](numerical-stability-and-backward-error.md) applies to weighted quadrature sums as well.

## 8. Spatial integration: from a field to an area or volume

For a field \(z(x,y)\) over a region \(A\), a regular-grid approximation may take the form

\[
I_A\approx\sum_{i,j} z_{ij} A_{ij},
\]

where \(A_{ij}\) is the ground area represented by cell \((i,j)\), or the appropriate fractional cell area at the boundary.

This expression is meaningful only after clarifying what \(z_{ij}\) represents. A cell-centre sample, a cell average and a total per cell are different quantities:

- If \(z_{ij}\) is a density or intensive quantity, multiply by the represented area to estimate an extensive total.
- If \(z_{ij}\) is already a per-cell total, summing it is appropriate; multiplying by area again would be wrong.
- If \(z_{ij}\) is a cell average, area-weighted summation estimates the integral over the covered cells.
- If \(z_{ij}\) is a point sample at the cell centre, the cell-area product is a quadrature approximation whose error depends on variation within the cell.

### 8.1 Boundary cells and partial coverage

A region boundary often cuts through raster cells. Counting every intersecting cell as fully inside creates a systematic boundary error. Options include fractional cell-area weights, a geometry-aware overlay, or a finer grid, each with its own computational and geometric error. The chosen method should match the accuracy requirement and the meaning of the raster values.

### 8.2 NoData and missing coverage

A missing cell is not automatically a zero. Excluding NoData cells changes the integration domain; replacing them with zero changes the model. A robust workflow should distinguish:

- outside the intended integration region;
- inside the region but unobserved;
- masked by quality criteria;
- a valid observed zero.

Report the covered area and the treatment of missing values. If the goal is a total over the full region, an explicit gap model or coverage limitation is required.

### 8.3 Coordinate systems and area measure

For regional totals, cell areas should represent the intended ground or surface area. A projected grid may be convenient, but projection scale distortion affects area. Geographic grid cells vary in ground area with latitude. Depending on the application, use an equal-area projection, geodesic/ellipsoidal cell areas, or a justified local approximation.

For terrain-surface area, the surface element is not the same as horizontal map area. For a differentiable elevation surface \(z(x,y)\), a local surface-area element in Cartesian coordinates is

\[
\mathrm{d}A_{\mathrm{surface}}
=
\sqrt{1+\left(\frac{\partial z}{\partial x}\right)^2+
\left(\frac{\partial z}{\partial y}\right)^2}
\,\mathrm{d}x\,\mathrm{d}y.
\]

This connects numerical integration to [numerical differentiation](numerical-differentiation.md). The result depends on the elevation model, horizontal and vertical units, derivative estimation and resolution. It should not be interpreted as a scale-independent “true” terrain area.

## 9. Multidimensional integration and change of variables

A two-dimensional integral over a rectangle can be approximated by applying a one-dimensional quadrature rule along each axis, producing a tensor-product rule. For a general polygon or irregular region, the domain may be partitioned into triangles or other elements, or mapped to a reference domain.

Under a smooth change of variables \((x,y)=T(u,v)\), the integral becomes

\[
\iint_A f(x,y)\,\mathrm{d}A
=
\iint_{\Omega}
f(T(u,v))
\left|\det J_T(u,v)\right|
\,\mathrm{d}u\,\mathrm{d}v,
\]

where \(J_T\) is the Jacobian matrix of the transformation and \(\Omega\) is the transformed domain. The absolute determinant accounts for local area scaling. Omitting it changes the measure and generally produces an incorrect integral.

Monte Carlo integration estimates an integral by sampling points from a suitable probability distribution. For a uniform sample \(X_k\) over a finite region \(A\),

\[
\iint_A f(x,y)\,\mathrm{d}A
\approx
\frac{|A|}{N}\sum_{k=1}^{N} f(X_k).
\]

Its sampling error typically decreases on the order of \(N^{-1/2}\), independently of dimension in this broad rate sense, although constants and variance can be large. It can be useful for high-dimensional or irregular integration problems, but the sampling design, variance estimation and reproducibility must be reported. It is not automatically preferable for low-dimensional smooth spatial fields where deterministic quadrature may be much more efficient.

## 10. Worked example: estimating volume from a profile

Suppose a synthetic cross-sectional profile has measured offsets \(x=(0,10,20)\) metres and cross-sectional heights above a reference level \(h=(0,2,0)\) metres. If the profile is interpreted as piecewise linear, the trapezoidal area is

\[
A\approx 10\left(\frac{0+2}{2}\right)
+10\left(\frac{2+0}{2}\right)
=20\ \mathrm{m}^2.
\]

If this cross-section is assumed constant along a 50 m length, the corresponding prismatic volume is

\[
V=A L=20\times50=1000\ \mathrm{m}^3.
\]

This is exact for the stated piecewise-linear cross-section and constant-section prism model, apart from arithmetic rounding. It is not an estimate of a real excavation or landform unless the profile, reference level, along-track variation and boundary conditions adequately represent that object. Additional cross-sections or a surface model would be needed to represent variation along the length.

## 11. Choosing a method

| Data and problem structure | Reasonable starting point | Important qualification |
|---|---|---|
| Smooth analytic function with cheap evaluations | Gauss–Legendre or adaptive quadrature | State smoothness assumptions and error controls |
| Equally spaced, smooth sampled profile | Composite Simpson or trapezoidal rule | Simpson requires an even number of intervals; noise may favour simpler rules |
| Piecewise-linear profile is the intended model | Trapezoidal rule | Exact for that interpolation model, not necessarily for the underlying phenomenon |
| Integrand has localised difficult regions | Adaptive quadrature | Error indicators can miss unresolved features or discontinuities |
| Raster field over a polygon | Area-weighted cell aggregation or geometry-aware quadrature | Define cell semantics, partial coverage, NoData and ground-area measure |
| High-dimensional integral | Monte Carlo or specialised stochastic methods | Quantify sampling variance and ensure the sampling distribution is correct |

The method should follow the data structure and the quantity being estimated. A higher-order rule cannot compensate for incorrect units, an incomplete domain, poor registration or an invalid model.

## 12. Exercises

### Exercise 1 — Units

A density field is measured in kilograms per square metre and integrated over an area measured in square metres. What are the units of the integral, and what physical quantity does it represent?

### Exercise 2 — Trapezoidal rule

Use the composite trapezoidal rule to approximate the integral of \(f(x)=x^2\) from 0 to 2 using two equal subintervals. Compare the result with the exact integral.

### Exercise 3 — Simpson's rule

Why must the standard composite Simpson's rule use an even number of equal subintervals? What is its polynomial exactness in exact arithmetic?

### Exercise 4 — Raster semantics

A raster cell stores a total population count for that cell, not population density. Explain why multiplying each value by cell area before summing is incorrect.

### Exercise 5 — Missing data

A watershed raster contains NoData cells inside the watershed boundary. Explain why treating those cells as zero can bias a watershed-wide pollutant-load estimate.

### Exercise 6 — Coordinate measure

A regional total is calculated from a geographic-coordinate raster. Why can multiplying every cell value by a single constant cell area be wrong?

### Exercise 7 — Numerical versus observational error

A quadrature routine estimates its integration error to be less than \(10^{-6}\) cubic metres, but the elevation observations have substantial vertical uncertainty. What does the numerical error estimate establish, and what does it not establish?

## 13. Answers and discussion

1. Kilograms. The integral accumulates mass over the area, assuming the density and area refer to compatible spatial measures.
2. With \(h=1\), \(f(0)=0\), \(f(1)=1\), \(f(2)=4\), so \(T_2=1(0/2+1+4/2)=3\). The exact integral is \(8/3\), so the trapezoidal approximation is high by \(1/3\).
3. The rule applies Simpson's parabolic panels over pairs of subintervals, so the number of equal subintervals must be even. It integrates polynomials through degree three exactly in exact arithmetic.
4. The value is already an extensive per-cell total. Multiplying by area would change its units and count the cell area twice.
5. Zero asserts that the pollutant load is known to be absent in those cells. NoData means it is unknown or unavailable; replacing it with zero can understate the total. Coverage and a defensible gap treatment must be reported.
6. Ground area of a geographic-coordinate cell varies with latitude, and may also depend on the chosen geodetic model and cell dimensions. Use cell-specific geodesic/ellipsoidal areas or a justified area-preserving projection.
7. It establishes only that the algorithm's estimated quadrature error is below the stated threshold under its assumptions and error estimator. It does not establish the accuracy of the elevation observations, the surface model, the integration boundary or the resulting real-world volume.

## 14. Connections to other Spatial Methods resources

- [Numerical differentiation](numerical-differentiation.md) supplies gradients used in surface-area integrals and some physical flux calculations.
- [Floating-point numbers, rounding and computational error](floating-point-numbers-rounding-and-computational-error.md) explains finite-precision effects in weighted sums.
- [Sensitivity and perturbation analysis](sensitivity-and-perturbation-analysis.md) provides a framework for assessing how input changes affect an integrated result.
- [Numerical stability and backward error](numerical-stability-and-backward-error.md) discusses reliable accumulation and error interpretation.
- [Electromagnetic observations and radiometric quantities](../remote-sensing-physics/electromagnetic-observations-and-radiometric-quantities.md) provides physical quantities that may be spatially integrated.
- [Coordinate transformation and CRS axis order](../../algorithms/geodesy/crs-transformation.md) is relevant when choosing a coordinate representation for spatial measures.

## 15. Further reading

- Philip J. Davis and Philip Rabinowitz, *Methods of Numerical Integration*, 2nd edition, Academic Press, 1984.
- Kendall E. Atkinson, *An Introduction to Numerical Analysis*, 2nd edition, Wiley, 1989.
- Josef Stoer and Roland Bulirsch, *Introduction to Numerical Analysis*, 3rd edition, Springer, 2002.

These references are starting points for technical review, not claim-by-claim citations. The module remains an initial teaching resource pending independent review and learner testing.
