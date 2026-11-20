# Functions and relationships in spatial science

**Foundation domain:** Mathematics for spatial science  
**Subject ID:** SM-FND-001  
**Module:** 05  
**Status:** Initial public foundation; further technical review and expansion required

## 1. Why functions matter in spatial science

A function is a precise way to describe how one quantity or object is associated with another. Spatial science uses functions to represent:

- how a location is transformed from one coordinate system to another;
- how elevation varies across a terrain surface;
- how distance changes as a point moves;
- how a sensor responds to an incoming signal;
- how travel cost depends on location and network conditions;
- how an environmental quantity varies over space and time.

Functions are not merely algebraic formulas. They can map numbers to numbers, coordinates to coordinates, locations to values, sets to sets, or structured records to other records. The essential requirement is that the mapping is well-defined for its stated domain.

## 2. Definition: domain, codomain and range

A function f from a set X to a set Y assigns each element of X exactly one element of Y:

\[
f:X\rightarrow Y.
\]

- **Domain** X: the set of permitted inputs.
- **Codomain** Y: the declared set in which outputs lie.
- **Range** (or image): the subset of Y that the function actually produces.

For every x in X, there is exactly one output f\(x\) in Y. Different inputs may have the same output unless the function has additional properties.

### Example: converting map distance to ground distance

For a map with representative fraction 1:s, define:

\[
f(M)=sM,
\]

where M is map distance and f\(M\) is represented ground distance, with both distances expressed in compatible units.

If \(M\) is measured in centimetres and \(s=25{,}000\), then:

\[
f(2\;\mathrm{cm})=50{,}000\;\mathrm{cm}=500\;\mathrm{m}.
\]

A reasonable domain might be non-negative map distances for a particular map. The output is non-negative ground distance under this simplified scale model. The formula does not establish map accuracy or account for local projection scale variation.

## 3. A function is more than a formula

A function can be described by a rule, table, graph, algorithm or physical process. For example, a digital elevation model can be interpreted as a mapping from horizontal locations to elevation values:

\[
z=f(x,y).
\]

The input is a horizontal position and the output is an elevation. The function is only defined where the terrain model has valid coverage and a meaningful elevation value. No-data areas, water surfaces, interpolation choices, vertical reference and data quality affect its interpretation.

The same function may be represented in several ways:
- an equation or analytical expression;
- a lookup table or sampled grid;
- a piecewise rule;
- a numerical algorithm;
- an empirical model fitted to observations.

These representations are not automatically equivalent. A raster stores samples at cells or grid locations; it does not by itself specify a unique continuous surface between them.

## 4. Independent and dependent variables

An independent variable is an input used to describe a relationship. A dependent variable is an output whose value is represented as depending on the inputs in that model.

For a simplified elevation profile:

\[
z=f(s),
\]

s may represent distance along a chosen transect and z the modelled elevation at that distance.

The labels do not imply that the input is physically independent of every other process, or that the relationship is causal. They describe the mathematical role of the variables in the chosen representation.

For a spatiotemporal field:

\[
q=f(x,y,t),
\]

the output q depends on horizontal position and time. The function could represent temperature, concentration, rainfall intensity or another quantity, subject to the domain, units, observation method and model assumptions.

## 5. Evaluating functions and interpreting outputs

To evaluate a function, substitute an admissible input into its rule.

Suppose a simplified planar elevation surface is:

\[
z(x,y)=100+0.02x-0.01y,
\]

where x and y are horizontal offsets in metres from a local origin and z is elevation in metres relative to a stated vertical datum.

At \(x,y\) = \(100,200\):

\[
z(100,200)=100+0.02(100)-0.01(200)=100\;\mathrm{m}.
\]

This is a simple plane, not a realistic terrain model. Its coefficients represent constant slopes in the x and y directions under the chosen local coordinate convention. A real terrain surface is more complex and requires observations, interpolation or another modelling method.

### 5.1 Units of a function

The input and output units should be explicit. In the example above, the coefficients 0.02 and −0.01 are dimensionless when z, x and y are all measured in metres. More generally, the coefficient units must make every term compatible with the output unit.

For a function that maps time to distance, the input may be seconds and output metres. For a function that maps position to temperature, the input is a coordinate and the output is a temperature quantity. Do not treat a function's numerical values as unit-free merely because software stores them as numbers.

## 6. Common function types

### 6.1 Constant functions

A constant function has the form:

\[
f(x)=c.
\]

Every admissible input produces the same output. A constant elevation surface is a flat plane; a constant temperature field is a spatially uniform model. These may be useful idealisations but rarely describe every detail of a real environment.

### 6.2 Linear and affine functions

A linear function in one real variable has the form f\(x\) = ax and passes through the origin. An affine function has the form:

\[
f(x)=ax+b.
\]

The intercept b allows an offset. In applied spatial modelling, the word *linear* is sometimes used more loosely for affine relationships; distinguish the formal meaning when it matters.

A two-dimensional affine coordinate mapping can be written:

\[
\begin{aligned}
x'&=a_{11}x+a_{12}y+t_x,\\
y'&=a_{21}x+a_{22}y+t_y.
\end{aligned}
\]

This represents a combination of linear transformation and translation. It can express rotation, scaling, shear and translation in a planar model. Whether it is suitable for a particular geodetic coordinate operation is a separate question; datum transformations and map projections require domain-specific models.

### 6.3 Polynomial functions

A polynomial function is a finite sum of powers of its input:

\[
f(x)=a_nx^n+\cdots+a_1x+a_0.
\]

Polynomials can approximate smooth relationships over a limited domain. They may be used in calibration, surface fitting and interpolation. High-degree polynomials can oscillate, behave poorly near boundaries or extrapolate unrealistically. A good fit to observed points does not guarantee a physically meaningful surface.

### 6.4 Exponential functions

An exponential function has the variable in the exponent:

\[
f(x)=ab^x,
\]

where \(b>0\). It can describe idealised multiplicative growth or decay. Spatial examples may include simplified models of attenuation, decay or population change, but the functional form must be justified by the relevant process and data.

### 6.5 Logarithmic functions

A logarithmic function is the inverse of an exponential function over an appropriate domain:

\[
f(x)=\log_b(x),\qquad x>0.
\]

It is useful for representing multiplicative relationships and broad dynamic ranges. Its argument must be dimensionless in a physical interpretation, usually by forming a ratio to a reference quantity. See the preceding module on ratios and logarithms for the core identities and examples.

### 6.6 Piecewise functions

A piecewise function uses different rules in different parts of its domain:

\[
f(x)=\begin{cases}
f_1(x),&x\in D_1,\\
f_2(x),&x\in D_2.
\end{cases}
\]

A classification rule, speed limit by road segment, land-cover response by class or sensor calibration curve may be piecewise. Boundaries between cases must be defined so that inputs are not accidentally omitted or assigned conflicting outputs.

### 6.7 Discrete functions and lookup mappings

A discrete function may map an integer cell index, feature identifier or category to a value. For example, a raster array maps row-column indices to stored cell values. The index domain is discrete; the values may be continuous measurements or categorical labels.

A category code is not automatically a numerical measurement. Arithmetic on class identifiers is usually meaningless unless a justified ordering or quantitative interpretation exists.

## 7. Injective, surjective and bijective mappings

These properties describe how a function relates its inputs to outputs.

- **Injective \(one-to-one\):** different inputs always produce different outputs.
- **Surjective (onto):** every element of the declared codomain is produced by at least one input.
- **Bijective:** both injective and surjective; each codomain element corresponds to exactly one input.

These definitions depend on the chosen domain and codomain.

### Spatial example: squaring

Consider:

\[
f(x)=x^2.
\]

On all real numbers, this is not injective because \(f(2)=f(-2)\). Its range is non-negative real numbers. If its domain is restricted to \(x\geq0\) and its codomain is also non-negative real numbers, it becomes bijective.

The same algebraic rule can therefore have different mapping properties under different domain and codomain choices.

### Why this matters

A coordinate transformation intended to be reversible should normally be one-to-one over its valid region. Some spatial operations are deliberately many-to-one: aggregating many raster cells into one summary, assigning many points to the same administrative region, or classifying a continuous range into one category. Such operations lose information and cannot generally be inverted uniquely.

## 8. Inverse functions

If a function is bijective between its domain and codomain, it has an inverse function:

\[
f^{-1}:Y\rightarrow X
\]

such that:

\[
f^{-1}(f(x))=x
\]

and:

\[
f(f^{-1}(y))=y
\]

for all admissible values.

For the affine one-dimensional mapping:

\[
y=3x+6,
\]

solve for x:

\[
x=\frac{y-6}{3}.
\]

Therefore:

\[
f^{-1}(y)=\frac{y-6}{3}.
\]

The inverse recovers the input exactly under the mathematical model.

### 8.1 Inverses in spatial data

Examples include:
- converting from one unit to another and back;
- reversing a reversible coordinate mapping over its valid domain;
- recovering a source value from a calibration equation when the response is invertible;
- converting a map distance back to its ground-distance equivalent under the same fixed scale model.

Not every spatial operation has a unique inverse. Raster resampling, aggregation, clipping, classification, rounding and lossy compression can discard information. A reverse operation may be approximate or impossible.

A map projection may have a mathematical inverse over a defined valid region, but projection singularities, cut lines, domain restrictions and numerical issues matter. A practical coordinate transformation must use the appropriate geodetic operation and reference metadata, not merely an arbitrary inverse of a planar formula.

## 9. Composition of functions

Function composition applies one mapping after another. If f maps X to Y and g maps Y to Z, then:

\[
(g\circ f)(x)=g(f(x)).
\]

The output of the first function becomes the input of the second. The codomain of the first must be compatible with the domain of the next.

### Worked example: unit conversion followed by scale conversion

A map segment is measured as 0.04 m on a map with RF 1:25,000.

First convert metres to centimetres:

\[
f(m)=100m.
\]

Then convert map centimetres to ground metres:

\[
g(c)=\frac{25{,}000c}{100}.
\]

The composed mapping is:

\[
(g\circ f)(m)=\frac{25{,}000(100m)}{100}=25{,}000m.
\]

\[For m = 0.04 m:\]

\[
(g\circ f)(0.04)=1{,}000\;\mathrm{m}.
\]

This example makes units and sequence explicit. A software pipeline that silently assumes a different input unit would produce a result wrong by a scale factor.

### 9.1 Composition is generally not commutative

In general:

\[
g\circ f\ne f\circ g.
\]

Changing the order of operations can change the result or make a composition undefined. This matters in spatial workflows: reprojecting, clipping, aggregating, filtering and resampling in different orders may produce different outputs.

## 10. Functions of several variables

Spatial phenomena often depend on more than one input:

\[
z=f(x,y)
\]

or:

\[
q=f(x,y,t).
\]

A function of two horizontal coordinates may represent elevation, temperature or another field. A function of three inputs may represent a quantity changing over space and time.

A location is not the same thing as a measured value at that location. The coordinate pair identifies an input to the model; the function returns the modelled quantity.

### 10.1 Distance as a function

For a fixed point \(a,b\), planar Euclidean distance from a variable point \(x,y\) is:

\[
d(x,y)=\sqrt{(x-a)^2+(y-b)^2}.
\]

The function maps a two-dimensional location to a non-negative scalar distance. Its units are the same as the coordinate units, assuming a suitable planar metric coordinate system.

The function's level set d\(x,y\) = r describes a circle of radius r around \(a,b\). The set d\(x,y\) ≤ r describes a closed disk. This connects functions to geometric loci and spatial selection.

### 10.2 Terrain as a surface

A digital terrain model may be conceptualised as:

\[
z=f(x,y).
\]

The model's domain is the horizontal area with valid elevation coverage. Its range is the set of elevation values produced. The function may be represented by a raster, triangulated surface, contour-derived model or another data structure.

The representation determines what can be queried directly and how values between observations are handled. A raster's cell values are samples; interpolation creates estimates between sample locations and introduces modelling assumptions.

## 11. Coordinate transformations as mappings

A coordinate transformation maps coordinates in one representation to coordinates in another:

\[
T:(x,y)\mapsto(x',y').
\]

A coordinate tuple is the representation of a location under a specified reference system. The transformation changes the coordinate representation; it does not move the physical point.

A simple planar translation is:

\[
T(x,y)=(x+t_x,y+t_y).
\]

Its inverse is:

\[
T^{-1}(x',y')=(x'-t_x,y'-t_y).
\]

This mapping is bijective over the plane. Real coordinate reference transformations may involve map projections, datum operations, axis order, units, epochs, grids and valid-area restrictions. Those topics belong to the geodesy and reference-systems foundation and the corresponding algorithms. This module establishes the function concept only.

## 12. Deterministic and stochastic relationships

A deterministic function assigns a fixed output to each input under its model. Given the same input and parameters, it returns the same output.

A stochastic model represents uncertainty or variability. One notation is:

\[
Y=f(X)+\varepsilon,
\]

where X is an input, f\(X\) is a modelled component and ε represents an error or stochastic component under a specified model.

This is only a general pattern. The distribution, dependence, bias, covariance and interpretation of ε must be specified for a real analysis. A random variable is not the same thing as an unknown but fixed value, and not every discrepancy should be treated as random noise.

Spatial observations may be correlated because they share sensors, acquisition times, environmental conditions, processing steps or reference data. The probability and covariance foundations develop these ideas in depth.

## 13. Empirical functions and model fitting

An empirical function is selected or estimated using observed data. Suppose observations (xᵢ,yᵢ) are collected and a model f(x;θ) is proposed, where θ represents unknown parameters.

The model may be fitted by minimising a discrepancy measure, maximising a likelihood or applying another estimation method. The chosen objective, error model, sample design and assumptions influence the fitted function.

A fitted function should be evaluated beyond how closely it follows the data used to construct it. Consider:
- whether the model form is scientifically plausible;
- whether observations cover the domain of intended use;
- whether residual patterns indicate model inadequacy;
- whether predictions are stable near boundaries;
- whether extrapolation is justified;
- whether uncertainty is reported;
- whether independent or held-out data are available for evaluation.

Interpolation estimates within the support of observations; extrapolation predicts outside that support. Extrapolation is often more fragile because the model is being used where evidence is sparse or absent.

## 14. Common errors

- Defining a formula without stating its domain, codomain or units.
- Assuming a function is invertible because it has an algebraic expression.
- Confusing a coordinate input with the physical quantity returned by a model.
- Treating raster samples as a uniquely defined continuous surface.
- Assuming all coordinate transformations are simple affine functions.
- Ignoring units between composed functions.
- Assuming that the order of processing operations does not matter.
- Treating a fitted relationship as causal.
- Extrapolating far beyond the observed domain without evidence.
- Treating a deterministic formula as a complete uncertainty model.
- Assuming a category code has meaningful numerical spacing.
- Reporting a model output without describing the validity of its input domain.

## 15. Exercises

Show your reasoning and state the domain, units and assumptions for each function.

### Exercise 1 — Domain, codomain and range

A function maps a non-negative distance M in centimetres to ground distance G in metres using a map scale of 1:50,000:

\[
f(M)=500M.
\]

1. State a reasonable domain.
2. State a reasonable codomain.
3. State the range if the domain is all non-negative real values.
4. Calculate f(3.5).

### Exercise 2 — Invertibility

Consider:

\[
f(x)=x^2.
\]

1. Explain why it is not one-to-one on all real numbers.
2. Restrict its domain so that it has an inverse with non-negative outputs.
3. Write the inverse.
4. Explain why the domain restriction is necessary.

### Exercise 3 — Function composition and units

A field measurement is recorded in millimetres. It must be converted to metres and then multiplied by a scale factor of 10,000 to produce a corresponding ground distance in metres.

1. Define the two functions.
2. Compose them in the correct order.
3. Calculate the ground distance for an input of 85 mm.
4. Explain what would happen if the millimetre-to-metre conversion were omitted.

### Exercise 4 — Terrain surface

A simplified surface is:

\[
z(x,y)=250+0.04x+0.03y,
\]

where x and y are local horizontal offsets in metres and z is elevation in metres.

1. Calculate elevation at \(100,200\).
2. State the units of the coefficients.
3. Explain why the surface is planar.
4. Give two reasons a real terrain surface may not follow this model.

### Exercise 5 — Distance function

A facility is at \(300,400\) in a suitable local planar coordinate system. Define the Euclidean distance function from this facility.

1. Calculate the distance to point \(600,800\).
2. State the units if coordinates are metres.
3. Write the inequality describing locations within 250 m.
4. Describe the geometric shape of this set.

### Exercise 6 — Coordinate mapping

A simplified mapping is:

\[
T(x,y)=(x+100,y-50).
\]

1. Transform \(250,300\).
2. Derive the inverse mapping.
3. Apply the inverse to your transformed coordinate.
4. Explain why this is a change of coordinate representation rather than physical movement.

### Exercise 7 — Deterministic and empirical models

A team fits a function to observed temperatures and location coordinates.

1. Explain the difference between an analytical deterministic model and an empirical fitted model.
2. Identify three checks needed before using the fitted model outside the sample locations.
3. Explain why a fitted surface does not automatically describe causal environmental processes.

## 16. Answers and checks

1. **Map-scale function:** domain M ≥ 0 cm; codomain G ≥ 0 m; range [0,∞) m. f(3.5) = 1,750 m.
2. **Invertibility:** f(2) = f(−2) = 4, so the function is not injective on all real numbers. Restrict domain to x ≥ 0; inverse is f⁻¹\(y\) = √y for y ≥ 0.
3. **Composition:** first h(mm) = mm/1,000 metres; then g\(m\) = 10,000m. Composition gives 10 × mm metres. For 85 mm, output is 850 m. Omitting conversion gives a result 1,000 times too large.
4. **Terrain:** z\(100,200\) = 250 + 4 + 6 = 260 m. Coefficients are dimensionless for metre inputs and metre output. The expression is affine in x and y, so equal increments in either coordinate produce constant elevation increments. Real terrain has curvature, local features, discontinuities and measurement/interpolation error.
5. **Distance:** d\(x,y\) = √((x−300)²+(y−400)²). At \(600,800\), d = √\(300²+400²\) = 500 m. Within 250 m: (x−300)²+(y−400)² ≤ 250², a closed disk in the assumed plane.
6. **Mapping:** T\(250,300\) = \(350,250\). Inverse T⁻¹(x',y') = \(x'−100,y'+50\). Applying it returns \(250,300\). The mapping changes coordinate values under a stated convention, not the point's physical location.
7. **Models:** an analytical model is specified from an assumed relationship; an empirical model is estimated from observations. Check data coverage and sampling, residual structure and independent predictive performance; also inspect uncertainty and extrapolation. A spatial association alone does not identify a causal process.

## 17. Connections across Spatial Methods

- **Spatial algorithms:** coordinate transformations, raster evaluation, interpolation, distance functions, surface fitting, reclassification and model prediction.
- **Spatial data collection:** sensor response functions, calibration curves, observation models and sampling of spatial fields.
- **Spatial recipes:** terrain modelling, proximity analysis, environmental surface estimation, unit conversion and coordinate processing.
- **Theoretical foundations:** linear algebra and matrix methods \(SM-FND-002\), calculus and differential methods \(SM-FND-003\), probability and statistical inference \(SM-FND-004\), geometry \(SM-FND-006\), geodesy and reference systems \(SM-FND-008\), measurement science \(SM-FND-011\) and numerical analysis \(SM-FND-016\).

## 18. Scope and limitations

This module establishes the language of functions and mappings. It does not provide a full treatment of matrix transformations, derivatives, continuity, interpolation theory, regression, probability models, geodetic transformations or numerical approximation. Those subjects require dedicated mathematical and domain-specific treatment.

All worked numerical examples are hypothetical. They do not constitute survey results, calibrated sensor models or validated environmental predictions.

## 19. Further development

The next module develops coordinate geometry and reference frames: points, lines, planes, geometric loci, coordinate descriptions and the relationship between geometric objects and their numerical representations. Vector and matrix operations will be treated in greater depth in their dedicated foundations.


## References and further reading

The explanations and spatial examples are original Spatial Methods teaching material. These references support the mathematical treatment of functions and relationships.

1. **OpenStax.** *Algebra and Trigonometry 2e*. [Chapter 3: Functions](https://openstax.org/books/algebra-and-trigonometry-2e/pages/3-introduction-to-functions), including function notation, domains and ranges, composition and inverse functions.
2. **OpenStax.** *Algebra and Trigonometry 2e*. [Chapter 4: Linear Functions](https://openstax.org/books/algebra-and-trigonometry-2e/pages/4-introduction-to-linear-functions), [Chapter 5: Polynomial and Rational Functions](https://openstax.org/books/algebra-and-trigonometry-2e/pages/5-introduction-to-polynomial-and-rational-functions), and [Chapter 6: Exponential and Logarithmic Functions](https://openstax.org/books/algebra-and-trigonometry-2e/pages/6-introduction-to-exponential-and-logarithmic-functions). Used for common function families and their properties.
3. **Esri.** [Coordinate systems, map projections, and transformations](https://doc.esri.com/en/arcgis-pro/latest/help/mapping/properties/coordinate-systems-and-projections.html). Used for the applied interpretation of coordinate transformations as spatial mappings. It is product documentation and does not replace geodetic theory.

**Limitations:** Empirical functions and fitted models require data, model diagnostics and domain-specific validation. A function's mathematical form alone does not establish a causal or physically valid relationship.
