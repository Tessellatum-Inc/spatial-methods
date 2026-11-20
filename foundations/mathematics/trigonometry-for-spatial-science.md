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

## 7. Slope, grade and vertical angle

Slope is vertical change divided by horizontal run:

$$
\text{grade}=\frac{\Delta z}{\text{horizontal run}}
$$

Percentage grade is:

$$
\text{grade}_{\%}=100\frac{\Delta z}{\text{horizontal run}}
$$

For inclination α measured from the horizontal:

$$
\text{grade}=\tan\alpha
$$

A 5% grade has inclination:

$$
\alpha=\tan^{-1}(0.05)\approx2.86^\circ
$$

Slope distance is not horizontal distance. Given slope distance sd and inclination α in the same vertical plane:

$$
d_h=s_d\cos\alpha,\qquad
\Delta z=s_d\sin\alpha
$$

The vertical-angle reference must be stated: horizontal, zenith, nadir or another convention. Survey instruments may report zenith angles rather than elevation angles. Do not apply these equations to instrument observations until the convention and required corrections are understood.

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
