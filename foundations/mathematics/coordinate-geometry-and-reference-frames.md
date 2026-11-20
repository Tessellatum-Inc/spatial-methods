# Coordinate geometry and reference frames for spatial science

**Foundation domain:** Mathematics for spatial science  
**Subject ID:** SM-FND-001  
**Module:** 06  
**Status:** Initial public foundation; further technical review and expansion required

## 1. Why coordinate geometry matters

Spatial questions often require us to describe where something is, how far apart two things are, whether a path crosses a boundary, or how a geometric object changes under a transformation. Coordinate geometry connects geometric ideas to numerical representations.

It allows us to describe:
- points as ordered coordinate tuples;
- lines and planes through equations;
- distances, directions, midpoints and intersections;
- circles, spheres and other geometric loci;
- local coordinate frames for engineering, surveying, robotics and field work;
- the relationship between a coordinate tuple and the reference frame in which it is expressed.

A coordinate is not a complete description of location by itself. Its meaning depends on the coordinate system, units, axis order, origin, orientation and, for Earth-referenced coordinates, the coordinate reference system and its datum and projection conventions.

This module develops the mathematical and geometric ideas. It does not replace geodesy, map-projection theory or formal coordinate reference system operations.

## 2. Geometry, coordinates and reference frames

**Geometry** studies properties and relationships of figures, such as distance, angle, incidence, intersection and shape.

A **coordinate system** assigns numerical values to points using a defined set of axes and conventions.

A **reference frame** establishes the origin, orientation, scale and convention used to express coordinates. In practical spatial work, a coordinate reference system (CRS) provides a more complete specification for relating coordinates to the Earth or to a defined engineering space.

A two-dimensional Cartesian coordinate system is often written as (x,y). A three-dimensional Cartesian system is written as (x,y,z). The coordinates are measured relative to a selected origin and axes.

### 2.1 The origin and axes

In a standard two-dimensional Cartesian plane:
- the x-axis is horizontal in the conventional diagram;
- the y-axis is vertical;
- the axes intersect at the origin (0,0);
- positive and negative directions are defined along each axis.

The drawing convention does not mean that x is always east or y is always north. A local engineering frame may use different axis conventions. A GIS layer may use easting and northing, longitude and latitude, or another axis order. Always inspect the actual CRS and data specification.

In three dimensions, the z-axis adds a third independent coordinate direction. It may represent height in a local Cartesian frame, but a z coordinate is not automatically an elevation above mean sea level. The vertical datum and height type matter.

## 3. Ordered pairs and triples

A point in a two-dimensional Cartesian plane is represented by an ordered pair:

\[
P=(x,y).
\]

A point in three-dimensional Cartesian space is represented by an ordered triple:

\[
P=(x,y,z).
\]

The order matters. (10,20) and (20,10) are generally different points. The same numerical tuple can also describe different physical positions if interpreted in different frames, units or coordinate systems.

### Example

Let A = (120,80) and B = (170,200), with coordinates in metres in a stated local grid.

The displacement from A to B is described componentwise as:

\[
(170-120,\;200-80)=(50,120)\;\mathrm{m}.
\]

This describes the coordinate difference in that frame. Whether those values correspond to east/north displacement depends on how the frame axes were defined.

## 4. Distance between points

For two points A=(x_1,y_1) and B=(x_2,y_2) in a Euclidean plane, the distance is:

\[
d(A,B)=\sqrt{(x_2-x_1)^2+(y_2-y_1)^2}.
\]

This follows from the Pythagorean theorem: the coordinate differences form the perpendicular sides of a right triangle.

### Worked example

Let A=(120,80) m and B=(170,200) m.

\[
\begin{aligned}
d(A,B)&=\sqrt{(170-120)^2+(200-80)^2}\\
&=\sqrt{50^2+120^2}\\
&=\sqrt{16{,}900}\\
&=130\;\mathrm{m}.
\end{aligned}
\]

This is planar Euclidean distance. It is appropriate only when the coordinate values are in a suitable Cartesian metric frame and the required distance is adequately represented by that plane. It is not a universal formula for distances between longitude/latitude pairs or for long distances over the Earth's surface.

### 4.1 Three-dimensional distance

For A=(x_1,y_1,z_1) and B=(x_2,y_2,z_2):

\[
d(A,B)=\sqrt{(x_2-x_1)^2+(y_2-y_1)^2+(z_2-z_1)^2}.
\]

The three coordinates must be expressed in compatible units and in the same Cartesian frame. Combining horizontal coordinates in metres with an unrelated height value, or mixing different vertical references, produces an invalid geometric result.

## 5. Midpoints and internal division

The midpoint of a line segment joining A=(x_1,y_1) and B=(x_2,y_2) is:

\[
M=\left(\frac{x_1+x_2}{2},\frac{y_1+y_2}{2}\right).
\]

For the previous points A=(120,80) and B=(170,200):

\[
M=(145,140)\;\mathrm{m}.
\]

The midpoint is equidistant from the endpoints in the Euclidean plane.

More generally, a point a fraction t of the way from A to B is:

\[
P(t)=A+t(B-A),\qquad 0\leq t\leq1.
\]

In two dimensions:

\[
P(t)=\big(x_1+t(x_2-x_1),\;y_1+t(y_2-y_1)\big).
\]

At t=0 the point is A; at t=1 it is B; at t=0.5 it is the midpoint. Values outside [0,1] describe points on the extended line, not on the closed segment.

## 6. Lines in the plane

A straight line can be represented in several equivalent ways, depending on its orientation and the problem.

### 6.1 Slope-intercept form

\[
y=mx+c,
\]

where m is the slope and c is the y-intercept.

For two distinct points with different x coordinates:

\[
m=\frac{y_2-y_1}{x_2-x_1}.
\]

A slope of 2 means that y increases by 2 coordinate units for each 1-unit increase in x. The slope is dimensionless when both axes use the same unit; otherwise it has output-units per input-unit.

Vertical lines cannot be represented as y=mx+c because their slope is undefined. Use another representation.

### 6.2 Point-slope form

A line through (x_1,y_1) with slope m is:

\[
y-y_1=m(x-x_1).
\]

### 6.3 General form

\[
ax+by+c=0.
\]

Here a and b are not both zero. This form represents vertical as well as non-vertical lines. Multiplying all coefficients by the same non-zero number produces an equivalent line, so the coefficients are not a unique identifier of the line.

### 6.4 Parametric form

A line through point P_0=(x_0,y_0) with direction vector (u,v) can be expressed as:

\[
(x,y)=(x_0,y_0)+t(u,v),\qquad t\in\mathbb{R}.
\]

This representation is useful for computing intersections and describing paths. Vector operations receive a fuller treatment in the next module.

### Worked example: a line through two points

Find the line through A=(2,3) and B=(6,11).

\[
m=\frac{11-3}{6-2}=2.
\]

Using point-slope form:

\[
y-3=2(x-2),
\]

so:

\[
y=2x-1.
\]

Substitution verifies both points: when x=2, y=3; when x=6, y=11.

## 7. Parallel and perpendicular lines

Two non-vertical lines are parallel when they have equal slopes. In general form, their normal coefficients are proportional.

Two non-vertical lines are perpendicular when their slopes satisfy:

\[
m_1m_2=-1.
\]

This slope rule requires both slopes to be defined and non-zero. A horizontal line is perpendicular to a vertical line, even though the vertical slope is undefined.

In spatial applications, perpendicularity depends on the metric and coordinate frame. A drawing that appears orthogonal on a map may not preserve ground angles everywhere if the projection distorts angles or scale.

## 8. Intersections of lines

An intersection is a point satisfying the equations of both lines.

Consider:

\[
y=2x+1
\]

and:

\[
y=-x+7.
\]

At the intersection:

\[
2x+1=-x+7.
\]

Therefore x=2 and y=5. The lines intersect at (2,5).

Two distinct lines in a plane may intersect once, be parallel and never intersect, or coincide and share every point. The equations and their coefficients determine which case applies.

Intersections are used in boundary construction, network geometry, survey computations and spatial overlay, but robust computational geometry must also address finite precision, nearly parallel lines, coincident segments and geometric tolerances.

## 9. Circles and other loci

A **locus** is the set of points satisfying a geometric condition.

The circle with centre (a,b) and radius r is:

\[
(x-a)^2+(y-b)^2=r^2.
\]

Its interior disk, including the boundary, is:

\[
(x-a)^2+(y-b)^2\leq r^2.
\]

For a centre C=(300,400) m and radius 250 m:

\[
(x-300)^2+(y-400)^2=62{,}500
\]

describes the circular boundary, while:

\[
(x-300)^2+(y-400)^2\leq62{,}500
\]

describes the disk.

This is a planar Euclidean model. A 250 m geodesic buffer around a location on the Earth is not generally a perfect circle in arbitrary map coordinates. The appropriate distance model and projection must be selected for the application.

Other loci include:
- a perpendicular bisector: points equidistant from two fixed points;
- a line: points satisfying a linear equation;
- a plane: points satisfying a linear equation in three coordinates;
- a sphere: points at a fixed three-dimensional Euclidean distance from a centre.

## 10. Planes and three-dimensional geometry

A plane in three-dimensional Cartesian space can be represented as:

\[
ax+by+cz+d=0,
\]

where a, b and c are not all zero.

The coefficients a, b and c describe a normal direction to the plane. The equation defines a flat two-dimensional surface embedded in three-dimensional space.

### Worked example: a plane

Consider:

\[
z=100+0.02x-0.01y.
\]

Rearrange:

\[
0.02x-0.01y-z+100=0.
\]

This is a plane. If x, y and z are all expressed in metres in one local Cartesian frame, the coefficients of x and y are dimensionless slopes, and the constant has units of metres.

A terrain surface may be approximated locally by a plane, but actual terrain may curve, contain abrupt features or depart substantially from this model.

### 10.1 Sphere

A sphere centred at (a,b,c) with radius r is:

\[
(x-a)^2+(y-b)^2+(z-c)^2=r^2.
\]

The corresponding solid ball uses ≤ rather than =. These equations are useful geometric models but do not account for Earth curvature or geodetic distance.

## 11. Coordinate frames: origin, orientation and scale

A coordinate frame is defined by more than a set of numbers. At minimum, a Cartesian frame requires:
- an origin;
- axis directions and orientation;
- a unit or scale convention;
- a dimensionality (two or three dimensions);
- an axis order and sign convention.

A point can have different coordinate tuples in different frames. The physical point is unchanged; its numerical description changes.

### 11.1 A simple translation between local frames

Suppose frame B has the same axis orientation and scale as frame A, but its origin is shifted by (100,−50) m relative to A. Under this explicitly defined convention:

\[
x_B=x_A-100,\qquad y_B=y_A+50.
\]

A point with coordinates (250,300) m in A has coordinates (150,350) m in B.

The inverse mapping is:

\[
x_A=x_B+100,\qquad y_A=y_B-50.
\]

This is a simple translation. If the frames also differ in orientation or scale, additional operations are needed. In three dimensions, rotations and translations require careful axis and handedness conventions; matrix methods treat these operations in depth.

### 11.2 Local engineering frames

A local frame can be useful for a construction site, laboratory, mobile robot or small field survey. It may be defined with an origin at a project control point and axes aligned with a site baseline or another practical direction.

A local frame is not automatically tied to a national or global reference system. To relate it to another frame, the relationship must be defined and established from suitable control or transformation information.

## 12. Cartesian coordinates and geographic coordinates are not interchangeable

Geographic coordinates commonly describe position using angular latitude and longitude, with a specified geodetic reference system. They are not ordinary Cartesian x and y coordinates measured in metres.

Consequences include:
- angular coordinate differences are not uniform ground distances;
- longitude scale varies with latitude;
- longitude wraps at a meridian convention;
- the shortest path on an ellipsoid is not generally a straight line in a longitude-latitude plot;
- map projections introduce spatially varying distortion.

Do not apply the planar Euclidean distance formula directly to latitude and longitude values and interpret the result as metres. Use an appropriate geodesic method or transform to a suitable projected/local metric frame for the task.

Likewise, do not assume every projected coordinate system preserves distance, area, shape and direction simultaneously. Projection choice and distortion are matters of cartographic and geodetic theory.

## 13. Coordinate tuples need metadata

A coordinate pair such as (36.8, −1.3) is ambiguous without context. It could be interpreted as longitude and latitude in degrees, or as two numerical coordinates in another system. The order, units and reference system must be known.

For reproducible spatial work, record:
- CRS identifier and full definition where needed;
- coordinate axis order and units;
- horizontal datum/reference frame and coordinate epoch where relevant;
- vertical reference and height type for z values;
- transformation operation and required grids, if coordinates were transformed;
- stated accuracy or uncertainty where available;
- local frame origin, orientation and scale if not using a standard CRS.

A CRS label alone may not capture every detail needed for high-accuracy work. Dynamic reference frames, coordinate epochs, vertical datums and operation selection are treated in geodesy.

## 14. Geometry calculations and numerical caution

Coordinate geometry is exact within its mathematical model, but real data and computer calculations are not infinitely precise.

Common complications include:
- coordinates stored with finite precision;
- nearly coincident or nearly parallel lines;
- rounding before rather than after a calculation;
- inconsistent units or axis order;
- invalid or mismatched reference systems;
- uncertainty in the measured coordinates;
- inappropriate planar approximations over large areas.

A geometric result should be interpreted in light of the input data quality and the assumptions of the coordinate model. A computed intersection may be numerically precise but still be uncertain because the source coordinates are uncertain.

Numerical conditioning, robust predicates and floating-point error belong to numerical analysis and computational geometry. Measurement uncertainty belongs to measurement science.

## 15. Common errors

- Treating coordinate values as meaningful without a coordinate system and units.
- Assuming x always means east and y always means north.
- Reversing axis order.
- Mixing coordinates from different reference frames.
- Treating a z value as an orthometric height without checking its vertical reference.
- Applying planar distance formulas directly to longitude and latitude.
- Assuming a map projection preserves all geometric properties.
- Confusing a line with a finite line segment.
- Using slope-intercept form for a vertical line.
- Assuming an apparent right angle on a map is necessarily a right angle on the ground.
- Ignoring uncertainty and numerical tolerance when interpreting computed intersections.
- Treating a local engineering frame as if it were automatically georeferenced.

## 16. Exercises

State the coordinate frame and units you assume. Show intermediate calculations.

### Exercise 1 — Distance and midpoint

In a local Cartesian frame, A=(40,30) m and B=(160,80) m.

1. Calculate the planar distance AB.
2. Calculate the midpoint.
3. State why the result is not automatically a geodesic distance.

### Exercise 2 — Line through two points

Find an equation for the line through P=(−1,4) and Q=(3,12).

1. Calculate its slope.
2. Write the point-slope equation.
3. Convert it to slope-intercept form.
4. Verify both points.

### Exercise 3 — Intersection

Find the intersection of:

\[
2x+y=11
\]

and:

\[
x-y=1.
\]

Explain how substitution verifies the result.

### Exercise 4 — Circle and spatial threshold

A facility is at C=(500,700) m in a suitable local planar frame. A screening distance is set at 300 m.

1. Write the equation for the boundary.
2. Write the inequality for the area within or on the boundary.
3. Determine whether P=(680,940) m is inside the disk.
4. State two reasons why a real service-area analysis may require more than this circle.

### Exercise 5 — Three-dimensional distance

A=(10,20,5) m and B=(40,60,17) m in the same Cartesian 3D frame.

1. Calculate the three-dimensional distance.
2. Calculate the horizontal distance.
3. Explain why the two results answer different questions.

### Exercise 6 — Local frame translation

Frame B has the same orientation and scale as frame A, with coordinates related by:

\[
x_B=x_A-250,\qquad y_B=y_A+100.
\]

1. Transform A-frame point (900,450) m into B.
2. Write the inverse mapping.
3. Recover the original coordinates.
4. Explain which frame properties were assumed identical.

### Exercise 7 — Geographic coordinates

A dataset contains points with pairs such as (36.8, −1.3).

1. Give two possible interpretations of the numbers.
2. Explain why the coordinate order and units must be checked.
3. Explain why a Euclidean distance calculated directly from these values is not a ground distance in metres.
4. Name the kind of method needed for an Earth-surface distance.

## 17. Answers and checks

1. **Distance and midpoint:** coordinate differences are (120,50) m. Distance is √(120²+50²) = √16,900 = 130 m. Midpoint is (100,55) m. This is planar Euclidean distance in the assumed local frame, not automatically an ellipsoidal surface distance.
2. **Line:** slope = (12−4)/(3−(−1)) = 2. Point-slope form: y−4 = 2(x+1). Slope-intercept form: y=2x+6. Substitution gives 4 at x=−1 and 12 at x=3.
3. **Intersection:** from x−y=1, y=x−1. Substitute into 2x+y=11: 3x−1=11, so x=4 and y=3. Check: 2(4)+3=11 and 4−3=1.
4. **Circle:** boundary (x−500)²+(y−700)²=90,000; disk uses ≤90,000. For P, differences are (180,240), so squared distance is 32,400+57,600=90,000. It lies exactly on the boundary. Real accessibility or travel analysis may depend on barriers, road/path networks, travel time, terrain, entrances and the appropriate Earth-distance model.
5. **3D distance:** differences are (30,40,12) m. Three-dimensional distance is √(900+1,600+144)=√2,644≈51.42 m. Horizontal distance is √(900+1,600)=50 m. The first includes vertical separation; the second measures only the horizontal plane.
6. **Translation:** B coordinates are (650,550) m. Inverse: x_A=x_B+250 and y_A=y_B−100. Applying it returns (900,450) m. The frames were assumed to share axis orientation, handedness, scale and units; only their origins differ by the stated offset.
7. **Geographic coordinates:** the pair might be longitude 36.8° and latitude −1.3°, or another ordered pair in a different system. Axis order and CRS must be verified. Degrees are angular units and their ground scale varies with location and direction. Use an appropriate ellipsoidal geodesic calculation or a suitable projected/local metric method for the required accuracy and extent.

## 18. Connections across Spatial Methods

- **Spatial algorithms:** geometric distance, line intersection, point-in-region tests, coordinate conversion, buffering and geometric construction.
- **Spatial data collection:** local control frames, site grids, instrument coordinate systems, sensor trajectories and 3D observations.
- **Spatial recipes:** field-site layout, proximity screening, boundary construction, route geometry and coordinate QA.
- **Theoretical foundations:** functions and mappings (SM-FND-001), linear algebra and matrix methods (SM-FND-002), geometry and computational geometry (SM-FND-006), geodesy and reference systems (SM-FND-008), cartographic theory (SM-FND-010), measurement science (SM-FND-011) and numerical analysis (SM-FND-016).

## 19. Scope and limitations

This module introduces coordinate geometry in Cartesian spaces and the role of reference frames. It does not provide a complete treatment of:
- vector spaces, matrix transformations, rotations and least-squares coordinate fitting;
- Euclidean, affine, projective or non-Euclidean geometry as formal mathematical subjects;
- geodetic datums, reference frames, coordinate epochs, map projections or geodesic algorithms;
- computational geometry robustness and floating-point predicates;
- measurement uncertainty propagation for coordinate-derived quantities.

These topics have dedicated homes in the neighbouring foundations and algorithm collections. Worked examples use hypothetical Cartesian coordinates and do not represent surveyed or georeferenced locations.

## 20. Further development

The next module introduces vectors and vector operations: displacement, magnitude, direction, components, dot and cross products, and their spatial interpretations. Matrix methods and formal coordinate transformation models will be developed in the linear algebra foundation.
