# Vectors and vector operations for spatial science

**Foundation domain:** Mathematics for spatial science  
**Subject ID:** SM-FND-001  
**Module:** 07  
**Status:** Initial public foundation; further technical review and expansion required

## 1. Why vectors matter

Many spatial quantities have both magnitude and direction. A displacement is not fully described by its length; a velocity requires speed and direction; a force has magnitude and orientation; a surface gradient indicates both steepness and direction of greatest increase.

A **scalar** is described by magnitude alone in its mathematical representation. A **vector** is an element of a vector space and can be represented by components relative to a chosen basis. In elementary Euclidean settings, vectors are often drawn as directed arrows, but the abstract concept is broader than an arrow on a map.

Vectors are used throughout spatial science:
- displacement between surveyed or mapped points;
- movement and velocity of vehicles, people, water or other objects;
- directions and components of wind or current;
- terrain slope and aspect;
- normals to surfaces and planes;
- sensor orientation and three-dimensional geometry;
- residuals and corrections in estimation and adjustment.

This module introduces vector concepts and common operations. Formal vector spaces, matrix algebra, eigenvalues, coordinate transformations and least-squares systems belong in the linear algebra foundation \(SM-FND-002\). Derivatives and gradients as differential operators belong in calculus \(SM-FND-003\).

## 2. Scalars, points and vectors are different

A **scalar** is a quantity represented by one value, such as distance, mass, temperature or elapsed time.

A **point** identifies a position in a specified coordinate frame. In a Cartesian frame, it may be written \(P=(x,y,z)\).

A **vector** represents a directed quantity or displacement. In a Cartesian basis, it may be written:

\[
\mathbf{v}=\begin{bmatrix}v_x\\v_y\\v_z\end{bmatrix}.
\]

The components describe the vector relative to the chosen axes and basis. A point's coordinate tuple and a vector's component tuple may look numerically identical, but they have different meanings:
- a point locates a position relative to an origin;
- a displacement vector describes a change from one position to another;
- translating the coordinate origin changes point coordinates but does not change a free displacement vector when the axes and scale remain the same.

Vectors attached to a particular point, such as a force acting at a location, may also carry an application point. Whether a vector is treated as free or attached depends on the physical and mathematical context.

## 3. Components and geometric interpretation

In a two-dimensional Cartesian frame:

\[
\mathbf{v}=\begin{bmatrix}v_x\\v_y\end{bmatrix}.
\]

In a three-dimensional frame:

\[
\mathbf{v}=\begin{bmatrix}v_x\\v_y\\v_z\end{bmatrix}.
\]

If the axes are orthogonal and use the same length unit, the magnitude is:

\[
\|\mathbf{v}\|=\sqrt{v_x^2+v_y^2}
\]

in two dimensions, and:

\[
\|\mathbf{v}\|=\sqrt{v_x^2+v_y^2+v_z^2}
\]

in three dimensions.

Magnitude is non-negative and has the units of the vector components when those components are compatible lengths. For a velocity vector, its magnitude is speed and its units are distance per time.

### Example

A displacement has components 30 m east and 40 m north in an orthogonal local frame. Its magnitude is:

\[
\|\mathbf{v}\|=\sqrt{30^2+40^2}=50\;\mathrm{m}.
\]

The magnitude alone does not preserve the direction. Many different vectors have magnitude 50 m.

## 4. Displacement between two points

For points A=\(x_A,y_A\) and B=\(x_B,y_B\) in the same Cartesian frame, the displacement from A to B is:

\[
\overrightarrow{AB}=B-A=
\begin{bmatrix}
x_B-x_A\\
y_B-y_A
\end{bmatrix}.
\]

In three dimensions, include the z-component.

### Worked example

Let A=\(120,80,15\) m and B=\(150,120,27\) m.

\[
\overrightarrow{AB}=
\begin{bmatrix}
30\\40\\12
\end{bmatrix}\;\mathrm{m}.
\]

Its three-dimensional magnitude is:

\[
\sqrt{30^2+40^2+12^2}=\sqrt{2{,}644}\approx51.42\;\mathrm{m}.
\]

Its horizontal magnitude is 50 m. These answer different questions: one includes vertical separation and the other does not.

The displacement is only meaningful if both points are expressed in the same compatible frame and units. Subtracting a longitude-latitude pair from projected metre coordinates is invalid.

## 5. Vector addition and subtraction

Vectors are added component by component:

\[
\mathbf{a}+\mathbf{b}=
\begin{bmatrix}
a_x+b_x\\a_y+b_y
\end{bmatrix}.
\]

Subtraction is addition of the negative vector:

\[
\mathbf{a}-\mathbf{b}=
\begin{bmatrix}
a_x-b_x\\a_y-b_y
\end{bmatrix}.
\]

### Example: chained displacement

A field team moves 120 m east and 80 m north, then 30 m west and 20 m south.

Represent the two displacements as:

\[
\mathbf{a}=\begin{bmatrix}120\\80\end{bmatrix},\qquad
\mathbf{b}=\begin{bmatrix}-30\\-20\end{bmatrix}.
\]

The net displacement is:

\[
\mathbf{a}+\mathbf{b}=\begin{bmatrix}90\\60\end{bmatrix}\;\mathrm{m}.
\]

Its magnitude is:

\[
\sqrt{90^2+60^2}\approx108.17\;\mathrm{m}.
\]

The total distance travelled along the two legs is 250 m, not 108.17 m. Path length and net displacement are different quantities.

## 6. Scalar multiplication

Multiplying a vector by a scalar changes its magnitude and possibly its direction:

\[
k\mathbf{v}=\begin{bmatrix}kv_x\\kv_y\\kv_z\end{bmatrix}.
\]

- If k > 1, the magnitude increases.
- If 0 < k < 1, the magnitude decreases.
- If k = 0, the result is the zero vector.
- If k < 0, the direction reverses and the magnitude is multiplied by |k|.

For example, if a displacement vector is \(20,10\) m, then 2v=\(40,20\) m. The direction is unchanged and the magnitude doubles.

## 7. Unit vectors and direction

A unit vector has magnitude one. For a non-zero vector v:

\[
\hat{\mathbf{v}}=\frac{\mathbf{v}}{\|\mathbf{v}\|}.
\]

For v=\(3,4\), magnitude is 5, so:

\[
\hat{\mathbf{v}}=\left(\frac35,\frac45\right).
\]

A unit vector expresses direction without retaining the original magnitude. It is undefined for the zero vector because division by zero is not defined.

Direction can be represented using components, a unit vector, an angle in a stated plane, or a bearing convention. Bearings require an explicitly stated reference direction and rotation convention. A mathematical angle measured counter-clockwise from positive x is not automatically a surveying azimuth or navigation bearing.

## 8. Dot product

For vectors a and b in Euclidean coordinates, the dot product is:

\[
\mathbf{a}\cdot\mathbf{b}=a_xb_x+a_yb_y+a_zb_z.
\]

It is also related to the angle θ between non-zero vectors:

\[
\mathbf{a}\cdot\mathbf{b}=\|\mathbf{a}\|\|\mathbf{b}\|\cos\theta.
\]

Therefore:

\[
\cos\theta=\frac{\mathbf{a}\cdot\mathbf{b}}{\|\mathbf{a}\|\|\mathbf{b}\|}.
\]

The dot product is zero when two non-zero Euclidean vectors are perpendicular. It is positive for an acute angle and negative for an obtuse angle.

### Worked example

Let a=\(3,4\) and b=(4,−3).

\[
\mathbf{a}\cdot\mathbf{b}=3(4)+4(-3)=12-12=0.
\]

The vectors are perpendicular. Their magnitudes are both 5.

### 8.1 Projection

The scalar projection of a onto a non-zero vector b is:

\[
\operatorname{comp}_{\mathbf b}(\mathbf a)=
\frac{\mathbf a\cdot\mathbf b}{\|\mathbf b\|}.
\]

The vector projection is:

\[
\operatorname{proj}_{\mathbf b}(\mathbf a)=
\frac{\mathbf a\cdot\mathbf b}{\mathbf b\cdot\mathbf b}\mathbf b.
\]

Projection decomposes one vector into a component along another direction and a perpendicular remainder. It is useful in analysing movement along a route, resolving forces and interpreting components relative to a line or direction.

If b is the zero vector, these projection formulas are undefined.

## 9. Cross product

In three-dimensional Euclidean space, the cross product of a and b is a vector perpendicular to both:

\[
\mathbf{a}\times\mathbf{b}=
\begin{bmatrix}
a_yb_z-a_zb_y\\
a_zb_x-a_xb_z\\
a_xb_y-a_yb_x
\end{bmatrix}.
\]

Its magnitude is:

\[
\|\mathbf{a}\times\mathbf{b}\|=
\|\mathbf{a}\|\|\mathbf{b}\|\sin\theta.
\]

This magnitude equals the area of the parallelogram spanned by the two vectors. Half of it is the area of the corresponding triangle.

The cross product is anti-commutative:

\[
\mathbf a\times\mathbf b=-(\mathbf b\times\mathbf a).
\]

The order determines orientation under the chosen right-handed coordinate convention. The cross product is zero for parallel or anti-parallel vectors, including the case where either vector is zero.

### Worked example

Let a=\(1,0,0\) and b=\(0,2,0\). Then:

\[
\mathbf a\times\mathbf b=(0,0,2).
\]

The parallelogram area is 2 square units. The result points along positive z in a right-handed frame.

Cross products are useful for computing surface normals, orientation and areas in three-dimensional geometry. In two dimensions, a scalar determinant-like expression is often used for signed area and orientation; it is not the same object as a three-dimensional cross-product vector.

## 10. Vector equations of lines

A line through point \(\mathbf r_0\) with direction vector \(\mathbf v\) can be represented as:

\[
\mathbf r(t)=\mathbf r_0+t\mathbf v,\qquad t\in\mathbb R.
\]

For a finite segment, restrict \(t\) to \([0,1]\) when \(\mathbf r_0\) is the start point and \(\mathbf r_0+\mathbf v\) is the end point.

This representation is useful for describing straight trajectories, survey baselines and geometric intersections. A path consisting of several straight segments is piecewise linear and requires more than one segment parameterisation.

## 11. Vectors in movement and observation

### 11.1 Velocity

Average velocity over a time interval is displacement divided by elapsed time:

\[
\mathbf v_{avg}=\frac{\Delta\mathbf r}{\Delta t}.
\]

If a vehicle's displacement is \(600,800\) m over 100 s in a local frame, its average velocity vector is \(6,8\) m/s and its speed is 10 m/s.

This is average velocity, not necessarily instantaneous velocity. It also describes net displacement, not the full route path or road-network speed.

### 11.2 Directional fields

A spatial vector field assigns a vector to each location:

\[
\mathbf v=\mathbf v(x,y).
\]

Examples include wind, ocean currents, groundwater flow and movement fields. A field may be sampled at discrete locations or represented by a continuous model. The coordinate frame, units, time reference and measurement method must be known.

### 11.3 Residual and correction vectors

In coordinate estimation, a residual or correction may be represented as a vector of component differences. Its interpretation depends on the model: a residual is not automatically the true error, and a correction is not necessarily a physical movement. Statistical estimation and uncertainty analysis are developed in the relevant foundations.

## 12. Vector operations and terrain

A terrain surface z=f\(x,y\) has directions along which elevation changes. A gradient vector describes the direction of steepest local increase and the rate of increase in a mathematical model:

\[
\nabla f=
\begin{bmatrix}
\partial f/\partial x\\
\partial f/\partial y
\end{bmatrix}.
\]

This expression is introduced only to connect vectors to calculus. Partial derivatives, gradient derivation, slope/aspect computation and differential operators belong in calculus \(SM-FND-003\). The gradient is a vector in the coordinate domain and its components depend on the coordinate units and model.

A downhill direction is opposite the direction of greatest increase under the usual elevation-surface interpretation. Practical terrain analysis must also consider the surface model, horizontal and vertical units, resolution, noise and terrain discontinuities.

## 13. Coordinate dependence and basis

Vector components depend on the basis used to express them. The same geometric vector can have different component values in different coordinate frames, particularly when axes are rotated or scaled.

For example, a displacement described as \(10,0\) in a frame whose x-axis points east may be represented differently in a frame whose axes are rotated. The underlying displacement does not change merely because its coordinate description changes.

For orthonormal Cartesian bases, the familiar dot product and magnitude formulas apply directly. In non-orthogonal bases or more general coordinate systems, metric information is needed to compute lengths and angles correctly. Formal basis changes, matrices and metric tensors require linear algebra and geometry beyond this introductory module.

## 14. Units and dimensional consistency

Vector components must be compatible for addition and subtraction. Adding a displacement in metres to a velocity in metres per second is not meaningful.

Scalar multiplication also has units. Multiplying a displacement vector by a dimensionless scale factor preserves length units; multiplying velocity by time produces a displacement unit.

Dot products and cross products have derived units:
- length dot length has units of area;
- velocity dot velocity has units of speed squared;
- length cross length has units of area.

Always identify whether a vector represents position coordinates, displacement, velocity, acceleration, force, direction or another quantity. Similar numerical arrays can represent physically different objects.

## 15. Common errors

- Treating a point coordinate tuple as a displacement vector without defining the operation.
- Assuming vector components are independent of coordinate frame.
- Adding quantities with incompatible units or physical meanings.
- Confusing path length with the magnitude of net displacement.
- Reporting a vector magnitude but omitting direction where direction matters.
- Treating a bearing as an angle without defining its reference and convention.
- Dividing by the magnitude of a zero vector when constructing a unit vector.
- Using dot-product angle formulas with a zero vector.
- Reversing cross-product order and thereby reversing orientation.
- Applying Cartesian vector formulas directly to longitude-latitude coordinates.
- Assuming a computed terrain gradient is reliable without checking the surface model and units.
- Interpreting residuals as the actual unknown errors.

## 16. Exercises

Use a stated Cartesian frame and show the component calculations.

### Exercise 1 — Displacement and magnitude

A=\(100,250\) m and B=\(160,330\) m.

1. Find the displacement vector from A to B.
2. Calculate its magnitude.
3. Give the corresponding unit vector.

### Exercise 2 — Vector addition and path length

A field worker walks 80 m east and 60 m north, then 20 m west and 10 m south.

1. Represent both legs as vectors.
2. Calculate net displacement.
3. Calculate its magnitude.
4. Calculate total path length.
5. Explain why these distances differ.

### Exercise 3 — Dot product and angle

Let a=\(2,1,2\) and b=\(1,2,2\).

1. Calculate the dot product.
2. Calculate both magnitudes.
3. Calculate the cosine of the angle between them.
4. Determine the angle to the nearest degree.

### Exercise 4 — Projection

Let a=\(6,4\) and b=\(3,0\).

1. Calculate the scalar projection of a onto b.
2. Calculate the vector projection.
3. Calculate the perpendicular component a−proj_b\(a\).

### Exercise 5 — Cross product and area

Let a=\(2,0,0\) m and b=\(0,3,0\) m.

1. Calculate a×b.
2. Find the parallelogram area.
3. Find the triangle area.
4. State how the cross-product direction changes if the order is reversed.

### Exercise 6 — Average velocity

An object moves from \(1,000,2,000\) m to \(1,600,2,800\) m in 200 s.

1. Calculate the displacement vector.
2. Calculate average velocity.
3. Calculate average speed based on net displacement.
4. Explain why this does not necessarily equal average speed along the actual path.

### Exercise 7 — Line and frame interpretation

A line starts at r_0=\(10,20,5\) m and has direction vector v=(2,−1,0.5) m.

1. Write its parametric vector equation.
2. Find the point at t=3.
3. Explain why t must be restricted to [0,1] if the expression is intended to represent only the segment from r_0 to r_0+v.
4. Explain why the component values depend on the coordinate frame.

## 17. Answers and checks

1. **Displacement:** B−A=\(60,80\) m. Magnitude = √\(60²+80²\)=100 m. Unit vector=(0.6,0.8).
2. **Path:** first \(80,60\) m, second (−20,−10) m. Net=\(60,50\) m, magnitude=√6,100≈78.10 m. Path length=80+60+20+10=170 m. The path length sums travelled legs; displacement is the direct change from start to finish.
3. **Dot product:** a·b=2+2+4=8. Both magnitudes are 3. cos θ=8/9≈0.8889, so θ≈27°.
4. **Projection:** a·b=18 and ||b||=3. Scalar projection=6. Vector projection=\(6,0\). Perpendicular component=\(0,4\).
5. **Cross product:** a×b=\(0,0,6\) m². Parallelogram area=6 m²; triangle area=3 m². Reversing order gives (0,0,−6) m².
6. **Velocity:** displacement=\(600,800\) m. Average velocity=\(3,4\) m/s. Magnitude is 5 m/s. This is net displacement divided by time; actual path length may be longer and therefore imply a higher average path speed.
7. **Line:** r\(t\)=\(10,20,5\)+t(2,−1,0.5). At t=3 the point is (16,17,6.5) m. The interval [0,1] parameterises only the segment between the start and end points. Rotating or otherwise changing the coordinate basis changes component descriptions, although the geometric line and vector remain the same.

## 18. Connections across Spatial Methods

- **Spatial algorithms:** vector-based geometry, orientation tests, trajectory calculations, surface normals, displacement and direction analysis.
- **Spatial data collection:** GNSS displacement, total-station coordinate differences, inertial measurements, wind/current sensors and three-dimensional point observations.
- **Spatial recipes:** field traverse calculations, route movement summaries, terrain orientation, 3D site modelling and sensor-vector interpretation.
- **Theoretical foundations:** coordinate geometry \(SM-FND-001\), linear algebra and matrix methods \(SM-FND-002\), calculus and differential methods \(SM-FND-003\), geometry \(SM-FND-006\), geodesy and reference systems \(SM-FND-008\), measurement science \(SM-FND-011\) and numerical analysis \(SM-FND-016\).

## 19. Scope and limitations

This module introduces vectors in familiar two- and three-dimensional Euclidean settings. It does not fully develop abstract vector spaces, bases and dimension, matrix representations, eigenvectors, tensor analysis, differential geometry, vector calculus or stochastic vector estimation.

The elementary formulas assume compatible Cartesian components and, where stated, orthonormal axes. Geographic coordinates, non-orthogonal bases and Earth-referenced vector fields require additional mathematical and geodetic treatment.

All worked numerical examples are hypothetical and do not represent actual field observations.

## 20. Further development

The next module in the current mathematics roadmap is sequences, series and approximation. It will connect repeated numerical processes, discretisation and convergence to spatial computation. Matrix and vector-space theory will be developed in SM-FND-002; differential vector operators will be developed in SM-FND-003.


## References and further reading

The explanations, worked examples and spatial interpretations are original Spatial Methods teaching material. The following open textbooks support the mathematical definitions and operations.

1. **OpenStax.** *Algebra and Trigonometry 2e*, [Section 10.8: Vectors](https://openstax.org/books/algebra-and-trigonometry-2e/pages/10-8-vectors). Used for vector components, magnitude, direction, addition, scalar multiplication, unit vectors and the dot product.
2. **OpenStax.** *Calculus Volume 3*, Chapter 2: [Vectors in Space]\(https://openstax.org/books/calculus-volume-3/pages/2-introduction\), especially Sections 2.1–2.5. Used for three-dimensional vectors, dot and cross products, and vector equations of lines and planes.

**Limitations:** These introductory texts do not replace linear algebra for vector spaces and matrix representations, nor geodesy for Earth-centred frames and transformations. The module's numerical vectors are hypothetical examples.
