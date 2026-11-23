# Numerical differentiation

**Subject identity:** `SM-FND-016` — Numerical analysis and scientific computing  
**Module:** 06  
**Status:** Initial public teaching resource; independent numerical-analysis review and learner testing outstanding.

## 1. Why numerical differentiation matters

Differentiation describes how a quantity changes with respect to another quantity. In spatial science, derivatives appear in terrain slope and aspect, gradients of continuous fields, rates of change along trajectories, sensitivity of model outputs to parameters, optimisation, physical fluxes and the analysis of spatially varying processes.

When an analytic derivative is unavailable, inconvenient or defined only through sampled values, it may be approximated numerically. That approximation introduces a new numerical problem: the step size must be large enough to limit rounding effects but small enough to represent local change. The input values may also be noisy, irregularly spaced or uncertain.

This module separates three situations:

1. **Analytic differentiation:** differentiate a known mathematical expression.
2. **Numerical differentiation:** approximate a derivative by evaluating a mathematical function at selected points.
3. **Differentiation of observations:** estimate local change from sampled measurements or raster values, where measurement noise, sampling geometry and interpolation are part of the model.

These are related but not interchangeable. A finite-difference formula applied to noisy observations does not reveal an exact physical derivative.

## 2. Derivative definitions and spatial meaning

For a scalar function (f(x)), the derivative at (x), when it exists, is

\[
f'(x)=\lim_{h\to0}\frac{f(x+h)-f(x)}{h}.
\]

The derivative is a local rate of change. Its units are the units of (f) divided by the units of (x). If (f) is elevation in metres and (x) is horizontal distance in metres, the derivative is dimensionless (metres per metre). If (x) is longitude in degrees, the derivative has units of metres per degree and its interpretation varies with latitude and reference model.

For a scalar field (z(x,y)), the gradient is

\[
\nabla z=
\begin{bmatrix}
\partial z/\partial x\\
\partial z/\partial y
\end{bmatrix}.
\]

The gradient points in the direction of greatest local increase in the coordinate plane. Its magnitude is the maximum directional rate of increase per unit coordinate distance. This interpretation assumes that the coordinate axes and units are appropriate for the intended metric calculation. Derivatives with respect to angular coordinates should not be treated as ground-distance derivatives without accounting for the reference system and local scale.

For a differentiable scalar field and a unit direction vector \(\mathbf{u}\), the directional derivative is

\[
D_{\mathbf{u}}z=\nabla z\cdot\mathbf{u}.
\]

For a vector-valued function, the corresponding first derivative is a Jacobian matrix. Its role in sensitivity and perturbation analysis is introduced in [Module 02](sensitivity-and-perturbation-analysis.md).

## 3. Finite-difference approximations

Finite differences replace a limiting process with evaluations at a finite separation (h). The formulas below assume the function is sufficiently smooth over the stencil and that the chosen points are in its valid domain.

### 3.1 Forward difference

\[
f'(x)\approx\frac{f(x+h)-f(x)}{h}.
\]

A Taylor expansion gives

\[
\frac{f(x+h)-f(x)}{h}
=f'(x)+\frac{h}{2}f''(x)+O(h^2).
\]

The leading truncation error is therefore first order in (h), conventionally described as (O(h)). The formula uses a point ahead of (x), which can be useful at a domain boundary where values behind the point are unavailable.

### 3.2 Backward difference

\[
f'(x)\approx\frac{f(x)-f(x-h)}{h}.
\]

Its leading truncation error is also first order:

\[
\frac{f(x)-f(x-h)}{h}
=f'(x)-\frac{h}{2}f''(x)+O(h^2).
\]

It is useful when only values at or before the evaluation point are available.

### 3.3 Central difference

\[
f'(x)\approx\frac{f(x+h)-f(x-h)}{2h}.
\]

The symmetric stencil cancels the leading even-order contribution, giving

\[
\frac{f(x+h)-f(x-h)}{2h}
=f'(x)+\frac{h^2}{6}f'''(x)+O(h^4).
\]

Its leading truncation error is second order, (O(h^2)), for a sufficiently smooth function. It often provides a more accurate estimate than a one-sided difference at the same step size, but it requires function values on both sides of the point.

### 3.4 Second derivative

A common central approximation to the second derivative is

\[
f''(x)\approx
\frac{f(x+h)-2f(x)+f(x-h)}{h^2}.
\]

For a sufficiently smooth function, its leading truncation error is (O(h^2)). Second derivatives are particularly sensitive to noise because the differencing operation amplifies high-frequency variation.

## 4. Truncation error, roundoff and step-size selection

A smaller (h) does not always produce a better derivative estimate.

**Truncation error** arises because a finite stencil approximates a limiting derivative. For the central first-difference formula, the leading truncation term is proportional to (h^2).

**Roundoff and cancellation** arise because nearby function values may be almost equal. Their subtraction can discard significant digits. Dividing the resulting difference by a very small (h) can magnify the effect.

A simplified error model for a first derivative has the form

\[
E(h)\approx C_1h^p+C_2\frac{\epsilon_{\mathrm{mach}}}{h},
\]

where (p=1) for a basic one-sided difference and (p=2) for the central difference, (C_1) and (C_2) depend on the function and implementation, and \(\epsilon_{\mathrm{mach}}\) represents a scale for floating-point error. This is a model, not a universal error bound.

Balancing the two terms gives the qualitative step-size relationships

\[
h_{\mathrm{opt}}\propto
\epsilon_{\mathrm{mach}}^{1/(p+1)}.
\]

Thus, under the simplified model, a one-sided first difference has a characteristic scale proportional to \(\epsilon_{\mathrm{mach}}^{1/2}\), while a central first difference has a scale proportional to \(\epsilon_{\mathrm{mach}}^{1/3}\). The proportionality constants and appropriate scaling depend on the function, units and higher derivatives. These expressions are not instructions to use those raw numbers as universal step sizes.

A practical step-size policy should:

- scale (h) to the magnitude and units of (x);
- account for the expected scale of (f) and its derivatives;
- avoid steps that cross discontinuities, boundaries or changes in model regime;
- test more than one step size and look for a stable range;
- report the stencil, step size, precision and any boundary treatment;
- distinguish numerical error from noise and uncertainty in input observations.

The connection to [floating-point arithmetic](floating-point-numbers-rounding-and-computational-error.md) and [numerical stability](numerical-stability-and-backward-error.md) is direct: cancellation can dominate a mathematically consistent difference formula.

## 5. Differentiating sampled spatial data

For gridded data, the derivative estimate depends on grid geometry as well as the values.

For equally spaced one-dimensional samples (z_i=z(x_i)), with spacing (\Delta x), an interior central difference is

\[
\left.\frac{\partial z}{\partial x}\right|_{i}
\approx\frac{z_{i+1}-z_{i-1}}{2\Delta x}.
\]

A one-sided difference is usually needed at an edge unless the data are extended using a justified boundary model. The choice of boundary condition is part of the method, not a harmless software detail.

For a regular two-dimensional grid with axis-aligned spacings \(\Delta x\) and \(\Delta y\), a simple interior gradient estimate is

\[
\frac{\partial z}{\partial x}\approx
\frac{z_{i,j+1}-z_{i,j-1}}{2\Delta x},
\qquad
\frac{\partial z}{\partial y}\approx
\frac{z_{i+1,j}-z_{i-1,j}}{2\Delta y},
\]

where the indexing convention must be stated explicitly. In raster arrays, row indices commonly increase downward, while map northing often increases upward. A sign error can therefore reverse the reported north-south derivative.

These expressions assume a regular grid in a suitable Cartesian coordinate system. For rotated or skewed grids, derivatives along grid axes must be transformed to the desired coordinate basis. For geographic coordinates, angular spacing is not a constant ground distance; use an appropriate projected or geodetic treatment.

### 5.1 Nonuniform sample spacing

If the left and right intervals differ, define (h_-=x_i-x_{i-1}) and (h_+=x_{i+1}-x_i). A three-point derivative formula at (x_i) is

\[
f'(x_i)\approx
-\frac{h_+}{h_-(h_-+h_+)}f(x_{i-1})
+\frac{h_+-h_-}{h_-h_+}f(x_i)
+\frac{h_-}{h_+(h_-+h_+)}f(x_{i+1}).
\]

This formula is exact for quadratic functions and has a leading error that depends on the spacing and higher derivatives. It is not equivalent to applying the equal-spacing formula with an average interval.

### 5.2 Noise amplification

Differentiation is a high-pass operation in the sense that rapid changes and high-frequency variation contribute strongly to the derivative. For independent measurement errors with variance \(\sigma^2\), the central-difference estimate

\[
\widehat{f'}=\frac{Y_{i+1}-Y_{i-1}}{2h}
\]

has noise variance

\[
\operatorname{Var}(\widehat{f'})=
\frac{\sigma^2}{2h^2},
\]

assuming equal independent errors at the two samples. As (h) decreases, this variance increases. Correlated errors require covariance terms and can change the result.

Smoothing before differentiation can reduce noise but changes the effective spatial scale and may attenuate real features or shift edges. The smoothing model, window, scale and boundary treatment should be reported. Smoothing is not a substitute for understanding the measurement process.

## 6. Higher-order formulas and extrapolation

Wider stencils can improve formal order when the function is smooth and evaluations are reliable. For example, a five-point central approximation to the first derivative is

\[
f'(x)\approx
\frac{f(x-2h)-8f(x-h)+8f(x+h)-f(x+2h)}{12h},
\]

with leading truncation error of order (O(h^4)).

Higher formal order does not guarantee greater accuracy in noisy or irregular data. Wider stencils combine more observations, may cross discontinuities and can amplify measurement errors. Stencil choice should follow the sampling geometry and smoothness assumptions.

Richardson extrapolation combines estimates at different step sizes to cancel a leading truncation term. If an approximation satisfies

\[
D(h)=f'(x)+Ch^p+O(h^{p+1}),
\]

then, under the same smoothness and error assumptions,

\[
D_{\mathrm{R}}=
\frac{2^pD(h/2)-D(h)}{2^p-1}
\]

cancels the (Ch^p) term. Extrapolation can fail to help when roundoff, noise, discontinuities or inconsistent boundary treatment dominate.

## 7. Automatic differentiation and complex-step differentiation

Finite differences estimate derivatives from nearby function values. Two other approaches are often available in computational models.

**Automatic differentiation (AD)** applies the chain rule to the sequence of elementary operations in a program. It computes derivatives of the implemented computational graph up to floating-point effects; it is not the same as symbolic algebra and does not approximate derivatives by choosing a finite step. AD is valuable for optimisation and differentiable models, but unsupported operations, control flow, external libraries and non-differentiable operations require care.

**Complex-step differentiation** uses an analytic extension of a real-valued function to complex inputs. Under appropriate conditions,

\[
f'(x)\approx\frac{\operatorname{Im}(f(x+ih))}{h}.
\]

It can avoid the subtractive cancellation in ordinary finite differences and permits very small (h). It is not universally applicable: the implementation must preserve complex arithmetic and the function must have the required analytic behaviour. Operations that discard imaginary parts, non-analytic functions, branch cuts and conditional logic can invalidate the result.

The method used to obtain a derivative should be documented because AD, finite differences and complex-step methods have different assumptions and failure modes.

## 8. Worked example: slope from a sampled elevation profile

Consider three synthetic elevation samples on a straight, equally spaced profile:

| Distance (x) (m) | Elevation (z) (m) |
|---:|---:|
| 0 | 102.0 |
| 10 | 103.5 |
| 20 | 106.0 |

At the middle sample, the central-difference estimate is

\[
\frac{\mathrm{d}z}{\mathrm{d}x}
\approx\frac{106.0-102.0}{20}=0.20.
\]

The local estimated rise is 0.20 metres per metre, or 20 percent grade. The corresponding angle is \(\arctan(0.20)\), approximately \(11.31^\circ\).

This is a derivative estimate at the middle location, not a claim that the terrain is a straight plane between all observations. The three samples are synthetic and equally spaced; real terrain estimates depend on resolution, interpolation, noise, grid orientation, horizontal reference system and the chosen neighbourhood.

## 9. Practical quality checks

Before publishing or using a numerical derivative:

1. State the independent variables, dependent variable, units and coordinate reference.
2. State whether the input is an analytic function, simulated data or measured observations.
3. Document the stencil, spacing, order and boundary treatment.
4. Check axis orientation and whether the grid is regular, rotated or geographic.
5. Compare estimates at multiple step sizes or resolutions where appropriate.
6. Assess sensitivity to noise, smoothing and outliers.
7. Check for discontinuities, nodata gaps, sharp boundaries and changes in physical regime.
8. Compare with an analytic derivative, manufactured solution or independently justified benchmark when available.
9. Report uncertainty or limitations separately from floating-point and truncation error.

## 10. Exercises

### Exercise 1 — Difference formula and order

For (f(x)=x^2), derive the forward and central difference approximations to (f'(x)). Identify their truncation errors.

### Exercise 2 — Step-size trade-off

Why can reducing (h) initially improve a central-difference derivative estimate but eventually make it worse?

### Exercise 3 — Spatial units

A raster stores elevation in metres and has a projected grid spacing of 30 metres in both horizontal axes. What are the units of the estimated partial derivatives? Why would the same interpretation be unsafe if the horizontal coordinates were longitude and latitude in degrees?

### Exercise 4 — Noise variance

Assume independent elevation errors with variance \(\sigma^2\) at the two samples used by a central difference. Derive the variance of the derivative estimate.

### Exercise 5 — Nonuniform spacing

The left and right sample intervals around a point are 5 m and 15 m. Why is it incorrect to apply the equal-spacing central-difference formula using 10 m as the spacing?

### Exercise 6 — Method selection

You need gradients from a noisy digital elevation model. Name at least four factors that should be decided or checked before selecting a derivative operator.

## 11. Answers and discussion

1. For (f(x)=x^2), the forward difference is (((x+h)^2-x^2)/h=2x+h), so its error relative to (2x) is (h). The central difference is (((x+h)^2-(x-h)^2)/(2h)=2x), exact for this quadratic in exact arithmetic. Its general truncation order for smooth functions is (O(h^2)).
2. A smaller step reduces truncation error, but nearby function values become harder to distinguish in finite precision. Subtractive cancellation and division by (h) amplify roundoff; for observed data, smaller separation also amplifies measurement noise.
3. The derivatives are metres of elevation per metre of horizontal distance, dimensionless as a ratio. Longitude and latitude are angular coordinates with ground distances varying by location and direction, so a metric gradient needs an appropriate coordinate transformation or geodetic treatment.
4. With independent equal-variance errors, the numerator is the difference of two independent errors and has variance (2\sigma^2). Dividing by (2h) gives variance (2\sigma^2/(4h^2)=\sigma^2/(2h^2)).
5. The equal-spacing formula assumes symmetric samples at (x_i-h) and (x_i+h). Here the points are not symmetric about the centre; use a nonuniform-grid formula or fit a local model that accounts for actual coordinates.
6. Relevant factors include horizontal CRS and units, grid spacing and orientation, noise level and correlation, terrain scale/features of interest, stencil and boundary behaviour, nodata handling, smoothing choices and validation against known or independent data.

## 12. Connections to other Spatial Methods resources

- [Floating-point numbers, rounding and computational error](floating-point-numbers-rounding-and-computational-error.md) explains finite-precision effects in small differences.
- [Sensitivity and perturbation analysis](sensitivity-and-perturbation-analysis.md) develops derivatives and Jacobians as local sensitivity tools.
- [Convergence, iterative methods and stopping criteria](convergence-iterative-methods-and-stopping-criteria.md) provides numerical context for iterative estimation.
- [Root finding and nonlinear equation solving](root-finding-and-nonlinear-equation-solving.md) uses derivatives in Newton-type methods.
- [Electromagnetic observations and radiometric quantities](../remote-sensing-physics/electromagnetic-observations-and-radiometric-quantities.md) provides an example of physical quantities whose spatial variation may be analysed.

## 13. Further reading

- James F. Epperson, *An Introduction to Numerical Methods and Analysis*, 2nd edition, Wiley, 2013.
- Kendall E. Atkinson and Weimin Han, *Elementary Numerical Analysis*, 3rd edition, Wiley, 2004.
- Randall J. LeVeque, *Finite Difference Methods for Ordinary and Partial Differential Equations*, SIAM, 2007.

These references are starting points for technical review, not claim-by-claim citations. The module remains an initial teaching resource pending independent review and learner testing.
