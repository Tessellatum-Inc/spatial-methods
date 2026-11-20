# Trigonometry for spatial science

**Subject:** SM-FND-001 — Mathematics for spatial science  
**Module:** 10  
**Status:** Initial public teaching module; technical review remains necessary.

## Purpose and scope

Trigonometry connects angles, lengths and directions. Spatial science uses it to resolve directions into coordinate components, interpret bearings, calculate slopes and height differences, describe rotations, and reason about sensor orientation and line-of-sight geometry.

This module develops **planar trigonometry**. Unless stated otherwise, calculations assume a locally flat Cartesian plane. It does not teach geodetic azimuths, ellipsoidal computations, geodesics, map-projection theory or instrument-specific survey procedures. Those belong in geodesy, measurement science and specialist surveying material.

The essential habit is to define an angle's reference axis, positive direction, unit and quadrant before calculating.

## 1. Angles and conventions

An angle measures rotation from an initial ray to a terminal ray about a vertex. In the standard mathematical convention, the initial ray lies along the positive x-axis, positive angles rotate counterclockwise, and negative angles rotate clockwise. A complete revolution is 360°.

Coterminal angles share a terminal direction. For example, 45°, 405° and −315° represent the same direction because they differ by whole revolutions.

A numeric angle is not a complete direction description without its reference axis and rotation convention. Thirty degrees counterclockwise from east is not the same direction as 30 degrees clockwise from north.

### Degrees and subdivisions

One degree is divided into 60 arcminutes, and one arcminute into 60 arcseconds:

$$
1^\circ=60′,\qquad 1′=60″,\qquad 1^\circ=3600″
$$

Arcminutes and arcseconds are angular units, not units of time. State the quantity explicitly when ambiguity is possible.

### Radians

The radian is the coherent SI derived unit for plane angle. For a circle of radius r, a central angle θ in radians subtends arc length s:

$$
s=r\theta,\qquad \theta=\frac{s}{r}
$$

A full revolution is 2π radians, so:

$$
180^\circ=\pi\text{ rad}
$$

$$
\theta_{rad}=\theta_{deg}\frac{\pi}{180}
\qquad
\theta_{deg}=\theta_{rad}\frac{180}{\pi}
$$

Examples: 90° = π/2 rad; 45° = π/4 rad; 1° = π/180 rad ≈ 0.0174533 rad.

A radian is a ratio of lengths and is dimensionless in SI dimensional analysis, although the unit name rad is retained for clarity.

**Computational warning:** many programming-language trigonometric functions expect radians. Passing a degree value directly can produce a numerically valid answer for the wrong angle. Check the documented convention of the calculator, library or API.

## 2. Right-triangle trigonometry

A right triangle has one 90° angle. Relative to a selected acute angle θ:
- the opposite side is across from θ;
- the adjacent side touches θ but is not the hypotenuse;
- the hypotenuse is opposite the right angle and is the longest side.

The primary ratios are:

$$
\sin\theta=\frac{\text{opposite}}{\text{hypotenuse}}
$$

$$
\cos\theta=\frac{\text{adjacent}}{\text{hypotenuse}}
$$

$$
\tan\theta=\frac{\text{opposite}}{\text{adjacent}}
$$

The mnemonic SOH–CAH–TOA is a memory aid, not a substitute for identifying the sides relative to the chosen angle. The Pythagorean theorem supplies a second constraint:

$$
a^2+b^2=c^2
$$

where a and b are perpendicular legs and c is the hypotenuse.

### Worked example 1 — vertical rise from horizontal run

A straight planar line has a horizontal run of 120 m and an upward inclination of 6°. The vertical rise is:

$$
\Delta z=120\tan(6^\circ)\approx12.61\text{ m}
$$

The slope distance is:

$$
d=\frac{120}{\cos(6^\circ)}\approx120.66\text{ m}
$$

These are geometric results under the stated planar model. They are not a substitute for levelling, instrument calibration, refraction corrections or a terrain model. The angle is assumed to be measured from the horizontal.

## 3. The unit circle

Right-triangle definitions directly describe acute angles. The unit circle extends sine and cosine to any real angle. It has radius 1 and centre at the origin. For θ measured counterclockwise from the positive x-axis, the point on the circle is:

$$
P=(\cos\theta,\sin\theta)
$$

For a circle of radius r, the point relative to its centre is:

$$
(x,y)=(r\cos\theta,r\sin\theta)
$$

The signs depend on the quadrant:

| Quadrant | x / cosine | y / sine |
|---|---:|---:|
| I | positive | positive |
| II | negative | positive |
| III | negative | negative |
| IV | positive | negative |

Tangent is defined where cosine is non-zero:

$$
\tan\theta=\frac{\sin\theta}{\cos\theta}
$$

It is undefined where cos θ = 0, including 90° and 270°.

The Pythagorean identity follows from the unit-circle equation:

$$
\sin^2\theta+\cos^2\theta=1
$$

### Periodicity and angle wrapping

Sine and cosine repeat every full revolution:

$$
\sin(\theta+2\pi k)=\sin\theta
$$

$$
\cos(\theta+2\pi k)=\cos\theta
$$

where k is any integer. Tangent repeats every π radians where defined.

An angle can be normalised to a chosen interval such as [0°, 360°) or [0, 2π). Normalisation changes its representation, not its direction. State the interval expected by a dataset or software interface.

## 4. Inverse trigonometric functions and quadrant checks

Inverse functions recover an angle from a ratio:

$$
\theta=\sin^{-1}\left(\frac{o}{h}\right),\quad
\theta=\cos^{-1}\left(\frac{a}{h}\right),\quad
\theta=\tan^{-1}\left(\frac{o}{a}\right)
$$

Software may call these asin, acos and atan. Their principal-value ranges are restricted, so a one-argument inverse function may not identify the intended quadrant.

For signed coordinate components, use a two-argument arctangent, commonly written atan2(y,x), where available. It uses both signs to identify the quadrant. Confirm the argument order and output range in the software documentation.

For Δx = −3 m and Δy = 4 m, the direction is in quadrant II:

$$
\theta=\operatorname{atan2}(4,-3)\approx126.87^\circ
$$

Computing arctan(4/−3) alone loses quadrant information.

## 5. Mathematical angles, bearings and azimuths

Two conventions frequently appear in spatial work.

**Mathematical angle:** zero along positive x (east in an east-north plane), positive counterclockwise.

**Clockwise-from-north azimuth:** zero at north, increasing clockwise, commonly represented in [0°, 360°).

In a local Cartesian plane with x east and y north, convert mathematical angle θm to clockwise-from-north azimuth A:

$$
A=(90^\circ-\theta_m)\bmod360^\circ
$$

Conversely:

$$
\theta_m=(90^\circ-A)\bmod360^\circ
$$

These equations assume local east-north axes and planar angles. They do not transform geodetic azimuths between reference ellipsoids or account for grid convergence, meridian convergence, magnetic declination or projection distortion.

### Worked example 2 — direction to azimuth

A displacement has east component ΔE = 30 m and north component ΔN = 40 m.

$$
\theta_m=\operatorname{atan2}(40,30)\approx53.13^\circ
$$

$$
A=(90^\circ-53.13^\circ)\bmod360^\circ
\approx36.87^\circ
$$

The displacement is more northward than eastward, so its azimuth should be less than 45°. The result passes this directional check.

Some systems use quadrant bearings, such as N 36.87° E. The starting meridian and direction of turn are encoded in the letters. Do not assume a quadrant-bearing field is interchangeable with a whole-circle azimuth field; read the data specification.

## 6. Resolving lengths into coordinate components

For a planar displacement of length d and mathematical angle θm from positive x:

$$
\Delta x=d\cos\theta_m,\qquad
\Delta y=d\sin\theta_m
$$

For a clockwise-from-north azimuth A in an east-north coordinate system:

$$
\Delta E=d\sin A,\qquad
\Delta N=d\cos A
$$

The sine and cosine positions differ because the reference axes differ.

### Worked example 3 — local traverse components

A point is 250 m from a local origin on an azimuth of 40° clockwise from north:

$$
\Delta E=250\sin40^\circ\approx160.70\text{ m}
$$

$$
\Delta N=250\cos40^\circ\approx191.51\text{ m}
$$

Both increments are positive, and northing is larger than easting. These are local planar components, not a geodetic coordinate solution.

### Worked example 4 — update a local coordinate through a two-leg traverse

A local engineering grid has east and north coordinates. The starting point is:

$
E_0=5000.000\text{ m},\qquad N_0=10000.000\text{ m}
$

Travel 120 m on an azimuth of 35° clockwise from north, then 80 m on an azimuth of 110° clockwise from north. Assume both distances are horizontal, both azimuths use the same local east-north frame, and the area is treated as planar.

For each leg, use:

$
\Delta E=d\sin A,\qquad \Delta N=d\cos A
$

**Leg 1:**

$
\Delta E_1=120\sin35^\circ\approx68.829\text{ m}
$

$
\Delta N_1=120\cos35^\circ\approx98.298\text{ m}
$

The first point is approximately:

$
E_1=5068.829\text{ m},\qquad N_1=10098.298\text{ m}
$

**Leg 2:**

$
\Delta E_2=80\sin110^\circ\approx75.175\text{ m}
$

$
\Delta N_2=80\cos110^\circ\approx-27.362\text{ m}
$

The second leg increases easting and decreases northing because its azimuth is southeast.

Add the two increments to the starting coordinate:

$
E_2=5000.000+68.829+75.175
\approx5144.005\text{ m}
$

$
N_2=10000.000+98.298-27.362
\approx10070.937\text{ m}
$

The final coordinate is approximately (5144.005 m, 10070.937 m). The total travelled distance is 200 m, while the straight-line displacement from start to finish is approximately 160.528 m. Path length and displacement are different quantities.

**Checks and limitations:**
- Both legs have positive easting increments; the second has a negative northing increment. This agrees with the stated quadrants.
- The second azimuth is between 90° and 180°, so it points southeast in this convention.
- The final coordinates retain the starting coordinate's frame and units.
- Rounding intermediate values can create small differences; retain full precision until reporting.
- This is a local planar calculation. It does not adjust a traverse, assess closure, model observation uncertainty, apply grid convergence or produce geodetic coordinates.


## 7. Slope, grade, vertical angle and terrain gradient

### 7.1 Slope between two points

For two points with a vertical difference Δz and a horizontal plan distance d_h, the signed grade is:

$$
g=\frac{\Delta z}{d_h}
$$

Percentage grade is:

$$
g_{\%}=100g=100\frac{\Delta z}{d_h}
$$

A positive grade rises in the direction from the first point to the second; a negative grade falls. If only steepness is required, report the magnitude and state that the sign has been omitted.

For a straight line inclined at elevation angle α above the horizontal:

$$
g=\tan\alpha,\qquad
\alpha=\tan^{-1}(g)
$$

A 5% grade means g = 0.05, not an angle of 5°. Its inclination is:

$$
\alpha=\tan^{-1}(0.05)\approx2.862^\circ
$$

For example, a 12.5 m rise over a horizontal run of 250 m gives:

$$
g=\frac{12.5}{250}=0.05
$$

The grade is 5%, and the line inclination is approximately 2.862°. This is the average grade between the endpoints; it does not describe every point along a curved road or terrain profile.

### 7.2 Horizontal, slope and vertical angles

Three quantities must not be confused:

- **Horizontal distance** is the length of the horizontal projection between two points.
- **Slope distance** is the straight-line distance between them in the vertical plane.
- **Vertical difference** is the signed change in height.

If the elevation angle α is measured from the horizontal and the slope distance is s:

$$
d_h=s\cos\alpha,\qquad
\Delta z=s\sin\alpha
$$

If horizontal distance and vertical difference are known:

$$
s=\sqrt{d_h^2+(\Delta z)^2}
$$

and:

$$
\alpha=\tan^{-1}\left(\frac{\Delta z}{d_h}\right)
$$

A vertical angle is incomplete unless its reference is defined. An **elevation angle** is measured upward from the horizontal (positive above, negative below). A **zenith angle** Z is conventionally measured down from the upward vertical. In the same vertical plane and under this convention:

$$
Z=90^\circ-\alpha
$$

Thus a horizontal sight has α = 0° and Z = 90°. An upward sight has a positive elevation angle and a zenith angle below 90°. A downward sight has a negative elevation angle and a zenith angle above 90°.

Do not assume every instrument, dataset or software package uses the same convention. Confirm whether the reported angle is an elevation, zenith, nadir or another defined quantity before converting it. Instrument observations may also require corrections and a measurement model; these elementary relationships do not provide those procedures.

### 7.3 Terrain gradient: from a line to a surface

A line between two points has one average grade. A terrain surface has a slope that can vary from location to location and by direction.

Represent a smooth surface as:

$$
z=f(x,y)
$$

where x and y are horizontal coordinates in a suitable local Cartesian or projected plane, and z is elevation in a compatible vertical unit. The partial derivatives describe local rates of elevation change:

$$
\frac{\partial z}{\partial x},\qquad
\frac{\partial z}{\partial y}
$$

The gradient vector is:

$$
\nabla z=
\left(
\frac{\partial z}{\partial x},
\frac{\partial z}{\partial y}
\right)
$$

It points in the direction of the steepest local increase in elevation. Its magnitude is the maximum local rise per unit horizontal distance:

$$
\|\nabla z\|=
\sqrt{
\left(\frac{\partial z}{\partial x}\right)^2+
\left(\frac{\partial z}{\partial y}\right)^2
}
$$

For a differentiable surface in a planar coordinate system, the local slope magnitude and angle are:

$$
g=\|\nabla z\|,\qquad
\alpha=\tan^{-1}(\|\nabla z\|)
$$

Percentage slope is 100 times the gradient magnitude. The gradient direction is not the same thing as slope magnitude: one describes orientation, the other steepness.

#### Worked example — local gradient and aspect direction

Consider a simple planar terrain surface:

$$
z(x,y)=100+0.04x-0.03y
$$

Assume x increases east, y increases north, and all three coordinates use metres. The surface has constant partial derivatives:

$$
\frac{\partial z}{\partial x}=0.04,\qquad
\frac{\partial z}{\partial y}=-0.03
$$

Therefore:

$$
\nabla z=(0.04,-0.03)
$$

Its magnitude is:

$$
\|\nabla z\|=\sqrt{0.04^2+(-0.03)^2}=0.05
$$

The local slope is 5%, and the inclination is:

$$
\alpha=\tan^{-1}(0.05)\approx2.862^\circ
$$

The east component is positive and the north component is negative, so the steepest uphill direction is southeast. Its mathematical angle from east is:

$$
\theta_m=\operatorname{atan2}(-0.03,0.04)\approx-36.87^\circ
$$

The corresponding clockwise-from-north azimuth is approximately 126.87°. The steepest downhill direction is the opposite direction, approximately 306.87°.

This example is deliberately a plane, so its gradient is constant everywhere. Real terrain is not generally planar; slope and direction vary across the surface.

### 7.4 From continuous terrain to a raster

A digital elevation model stores elevations at discrete grid locations or cells. It does not directly store the exact derivatives of an unknown continuous terrain surface. A terrain algorithm estimates local derivatives from neighbouring elevation samples, often using finite differences or a fitted local surface.

For a simple regularly spaced grid, a central-difference estimate of the east-west derivative at an interior cell may take the form:

$$
\frac{\partial z}{\partial x}\approx
\frac{z_{i+1,j}-z_{i-1,j}}{2\Delta x}
$$

A corresponding north-south estimate uses the appropriate neighbouring rows and cell spacing. The row direction, axis orientation, cell dimensions, edge handling and NoData policy must be checked. If horizontal and vertical units differ, convert them consistently before calculating slope.

Raster slope therefore depends on more than the formula: it depends on the elevation data, grid spacing and alignment, interpolation or derivative estimator, neighbourhood, surface roughness, noise and processing choices. Different tools can produce different estimates from the same DEM. A smaller cell size alone does not guarantee a more accurate terrain gradient.

The finite-difference expression is an introductory illustration, not a complete terrain-slope algorithm. Detailed stencils, error behaviour, filtering and numerical stability belong in numerical analysis and terrain-processing methods.

### 7.5 Which mathematics is needed?

| Spatial question | Mathematical treatment | Where it belongs |
|---|---|---|
| What is the average grade between two known points? | Rise divided by horizontal run; inverse tangent for angle | This module |
| How do I convert an elevation angle to a zenith angle? | Explicit angular convention and complementary-angle relationship | This module, with instrument conventions checked |
| What is the steepest local direction on a smooth surface? | Partial derivatives and the gradient vector | Calculus and differential methods, SM-FND-003 |
| How do I estimate slope from DEM cells? | Finite differences or local surface fitting, with grid and error considerations | Numerical analysis, SM-FND-016, and terrain algorithms |
| How do I interpret terrain processes and landforms? | Geomorphology and physical terrain context | Earth science and geomorphology, SM-FND-009 |

**Boundary:** elementary trigonometry handles a line or a known local gradient. Calculus defines derivatives and gradients of continuous surfaces. Raster algorithms estimate those derivatives from discrete data. These are connected but not interchangeable tasks.

## 8. Circular geometry and small-angle approximations

For a circle of radius r:

$$
C=2\pi r,\qquad s=r\theta
$$

where θ is in radians. Sector area is:

$$
A_{sector}=\frac{1}{2}r^2\theta
$$

Using degrees directly in these radian formulas gives an incorrect result unless the angle is converted first.

For sufficiently small θ in radians:

$$
\sin\theta\approx\theta,\qquad \tan\theta\approx\theta
$$

These are approximations, not identities. Their adequacy depends on angle magnitude and required tolerance. Precision work should quantify approximation error or use the full function.

## 9. Where spatial science uses trigonometry

- **Surveying and local geometry:** resolve lengths and angles into local components, subject to the correct observation model, corrections and reference frame.
- **Terrain and infrastructure:** relate horizontal run, vertical rise, slope distance and inclination.
- **Remote sensing and imaging:** interpret look direction, incidence angle, field of view and simplified planar line-of-sight geometry. Full sensor models also require optics, calibration and platform-orientation theory.
- **GNSS and navigation:** interpret local direction components and angular conventions. Actual positioning and geodetic azimuth calculations require specialist reference-system and observation models.
- **GIS and computational geometry:** calculate vector directions, rotations and coordinate components. A projected coordinate plane is not globally distortion-free.
- **Field collection:** document angle reference, unit, sign convention, instrument convention, and whether distance is horizontal, slope or three-dimensional.

## 10. A reliable calculation procedure

1. Draw or describe the geometry and identify the unknown.
2. Define coordinate axes and the angle's reference direction.
3. State whether positive rotation is clockwise or counterclockwise.
4. Identify the angle unit and convert if required.
5. Label opposite, adjacent and hypotenuse relative to the chosen angle.
6. Choose the relationship matching the known quantities.
7. Check signs and quadrant before accepting an inverse-trigonometric result.
8. Carry units through the calculation and round only at the end.
9. Check whether the geometry is planar and whether the distance is horizontal, slope, Euclidean 3D or geodesic.
10. Record assumptions and distinguish observations from calculated results.

## 11. Exercises

Retain units and explain at least one reasonableness check.

1. Convert 72° to radians and 1.2 rad to degrees.
2. A right triangle has hypotenuse 50 m and acute angle 32°. Find opposite and adjacent sides.
3. A road rises 18 m over a horizontal run of 360 m. Find percentage grade and inclination.
4. A local displacement has east component −12 m and north component 5 m. Find its mathematical angle and clockwise-from-north azimuth.
5. A 600 m line has azimuth 125° clockwise from north. Find east and north components.
6. Slope distance is 75 m and elevation angle is 8°. Find horizontal distance and vertical rise.
7. Explain why arctan(ΔN/ΔE) alone can return an ambiguous direction and how atan2 helps.
8. A GIS layer stores angles in degrees, while a software function expects radians. Describe the error and conversion.
9. A dataset contains azimuths 359.8° and 0.2°. Explain why their arithmetic mean is misleading and suggest a direction-aware approach.

## 12. Exercise answers

1. 72° = 72π/180 = 0.4π ≈ 1.2566 rad. 1.2 rad × 180/π ≈ 68.75°.
2. Opposite = 50 sin 32° ≈ 26.50 m. Adjacent = 50 cos 32° ≈ 42.40 m. The Pythagorean check gives approximately 50 m.
3. Grade = 18/360 = 0.05 = 5%. Inclination = arctan(0.05) ≈ 2.86°.
4. The vector is in quadrant II. Mathematical angle = atan2(5,−12) ≈ 157.38°. Azimuth = (90−157.38) mod 360 ≈ 292.62°. It points northwest, consistent with the component signs.
5. ΔE = 600 sin 125° ≈ 491.49 m; ΔN = 600 cos 125° ≈ −344.15 m. It points southeast, as expected for an azimuth between 90° and 180°.
6. Horizontal distance = 75 cos 8° ≈ 74.27 m. Rise = 75 sin 8° ≈ 10.44 m.
7. A ratio loses quadrant information and division by zero is possible. A two-argument arctangent uses both signed components; confirm its argument order and output range.
8. Convert degrees to radians by multiplying by π/180. Otherwise the software interprets the degree number as radians.
9. The directions are close across the 0° boundary, but their arithmetic mean is 180°, the opposite direction. Use circular statistics or average unit direction vectors, then recover direction with an appropriate two-argument arctangent. Weighted or uncertain directions require a method consistent with the observation model.

## 13. Boundaries and connections

This is an introductory planar mathematics module, not a field-survey manual or geodetic computation guide.

- **Module 06 — Coordinate geometry and reference frames:** Cartesian points, axes, lines and Euclidean distance.
- **Module 07 — Vectors and vector operations:** components, direction, magnitude, dot products and rotations.
- **SM-FND-008 — Geodesy and reference systems:** ellipsoids, geodetic coordinates, geodesics, geodetic azimuths, reference frames and coordinate transformations.
- **SM-FND-011 — Measurement science:** angular observations, instrument effects, uncertainty, corrections and traceability.
- **SM-FND-006 — Geometry and computational geometry:** geometric constructions, intersections and more general spatial geometry.
- **SM-FND-012 and SM-FND-013 — Remote sensing physics and optics:** sensor geometry, rays, imaging and electromagnetic propagation.

A projected coordinate system may use linear coordinate units, but its axes and scale are defined by a map projection. Grid north, true north and magnetic north are not automatically interchangeable. Earth curvature, ellipsoidal geometry, projection convergence and distortion require appropriate geodetic methods.

## References

- Bureau International des Poids et Mesures (BIPM). *The International System of Units (SI Brochure)*, 9th edition, version 4.01 (June 2026), including plane angle and derived units. [SI Brochure](https://www.bipm.org/en/si-brochure-9). Source record: SM-SRC-000022.
- OpenStax, Rice University. *Algebra and Trigonometry 2e*, sections on trigonometric functions, right-triangle trigonometry, unit circle, inverse trigonometric functions and periodicity. [Textbook](https://openstax.org/books/algebra-and-trigonometry-2e/pages/preface). Source record: SM-SRC-000021.

OpenStax is licensed CC BY-NC-SA 4.0 and states that its material may not be used for training large language models or ingested into generative-AI offerings without prior written permission. This module provides original explanations and spatial examples; it does not reproduce OpenStax text, figures or exercises. The reference is for human study.

**Review limitation:** this is an initial educational module, not an independently peer-reviewed mathematical text. Examples are idealised and planar. No instrument observations, field measurements or geodetic computations are reported.
