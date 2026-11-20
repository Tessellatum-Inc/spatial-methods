# Inner products, norms, orthogonality and projections

**Subject identity:** `SM-FND-002` — Linear algebra and matrix methods  
**Module:** 05  
**Status:** Initial public teaching resource; independent technical review and learner testing outstanding.

## 1. Why geometry needs more than coordinates

Modules 01–04 developed vectors, matrices, linear systems and coordinate bases. We can now describe a vector's components, but several practical questions remain:

- How long is a displacement?
- What is the angle between two directions?
- When are two directions perpendicular?
- What is the closest point on a line or plane to a measured location?
- How can a vector be separated into a component along a direction and a component perpendicular to it?

These questions require an additional mathematical structure: an **inner product**. From it we obtain lengths, angles, orthogonality and projections. Those ideas underpin distance calculations, cross-track error, geometric fitting, residual analysis and least-squares estimation.

The formulas in this module use real vector spaces and, unless stated otherwise, the ordinary Euclidean inner product.

## 2. The inner product

For vectors \(\mathbf{u},\mathbf{v}\in\mathbb{R}^n\), the standard Euclidean inner product is the dot product:

$$
\langle\mathbf{u},\mathbf{v}\rangle
=\mathbf{u}^T\mathbf{v}
=\sum_{i=1}^{n}u_i v_i.
$$

For example,

$$
\mathbf{u}=\begin{bmatrix}2\\1\end{bmatrix},
\qquad
\mathbf{v}=\begin{bmatrix}3\\4\end{bmatrix}
$$

give

$$
\langle\mathbf{u},\mathbf{v}\rangle
=2(3)+1(4)=10.
$$

An inner product is a function that assigns a real number to a pair of vectors and satisfies four properties:

1. **Symmetry:** \(\langle\mathbf{u},\mathbf{v}\rangle=\langle\mathbf{v},\mathbf{u}\rangle\).
2. **Linearity in the first argument:** \(\langle a\mathbf{u}+b\mathbf{w},\mathbf{v}\rangle=a\langle\mathbf{u},\mathbf{v}\rangle+b\langle\mathbf{w},\mathbf{v}\rangle\).
3. **Linearity in the second argument** (for real vector spaces), following from symmetry.
4. **Positive definiteness:** \(\langle\mathbf{v},\mathbf{v}\rangle\geq0\), with equality only when \(\mathbf{v}=\mathbf{0}\).

Different inner products can be defined on the same vector space. The standard dot product is especially natural for orthonormal Cartesian coordinates, but it is not the only possible choice.

## 3. Norms: measuring vector length

An inner product induces a norm:

$$
\|\mathbf{v}\|
=\sqrt{\langle\mathbf{v},\mathbf{v}\rangle}.
$$

For the Euclidean dot product,

$$
\|\mathbf{v}\|
=\sqrt{v_1^2+v_2^2+\cdots+v_n^2}.
$$

For example, if

$$
\mathbf{v}=\begin{bmatrix}3\\4\end{bmatrix},
$$

then

$$
\|\mathbf{v}\|=\sqrt{3^2+4^2}=5.
$$

A norm satisfies non-negativity, definiteness, absolute homogeneity and the triangle inequality. These properties make it a consistent measure of vector magnitude.

### Worked example 1 — displacement length

A local Cartesian displacement is 120 m east and 50 m north:

$$
\mathbf{d}=\begin{bmatrix}120\\50\end{bmatrix}\mathrm{m}.
$$

Its Euclidean length is

$$
\|\mathbf{d}\|
=\sqrt{120^2+50^2}
=130\,\mathrm{m}.
$$

This is a planar horizontal distance under the stated local Cartesian model. It is not automatically a geodesic distance on the Earth's surface, a slope distance, or a ground distance corrected for projection scale and elevation.

## 4. Angles and the Cauchy–Schwarz inequality

For non-zero vectors in a Euclidean inner-product space, the angle \(\theta\) between them is defined by

$$
\cos\theta
=
\frac{\langle\mathbf{u},\mathbf{v}\rangle}
{\|\mathbf{u}\|\,\|\mathbf{v}\|}.
$$

The Cauchy–Schwarz inequality guarantees that the ratio lies between −1 and 1:

$$
|\langle\mathbf{u},\mathbf{v}\rangle|
\leq\|\mathbf{u}\|\,\|\mathbf{v}\|.
$$

The inequality is also useful beyond angle calculations: it bounds inner products and supports proofs of norm properties.

Interpretation in Euclidean geometry:

- \(\theta=0^\circ\): same direction;
- \(\theta=90^\circ\): perpendicular directions;
- \(\theta=180^\circ\): opposite directions.

The zero vector has no defined direction, so an angle involving it is undefined.

### Worked example 2 — angle between two directions

Let

$$
\mathbf{u}=\begin{bmatrix}1\\0\end{bmatrix},
\qquad
\mathbf{v}=\begin{bmatrix}1\\1\end{bmatrix}.
$$

Then \(\langle\mathbf{u},\mathbf{v}\rangle=1\), \(\|\mathbf{u}\|=1\), and \(\|\mathbf{v}\|=\sqrt{2}\). Therefore,

$$
\cos\theta=\frac{1}{\sqrt{2}},
\qquad
\theta=45^\circ.
$$

The dot product gives an angle only after the coordinate metric and units are appropriate to the geometry being modelled.

## 5. Orthogonality

Two vectors are **orthogonal** if their inner product is zero:

$$
\mathbf{u}\perp\mathbf{v}
\quad\Longleftrightarrow\quad
\langle\mathbf{u},\mathbf{v}\rangle=0.
$$

For the standard Euclidean dot product, non-zero orthogonal vectors meet at a right angle.

For example,

$$
\begin{bmatrix}2\\1\end{bmatrix}
\quad\text{and}\quad
\begin{bmatrix}1\\-2\end{bmatrix}
$$

are orthogonal because \(2(1)+1(-2)=0\).

A set of non-zero vectors is **orthogonal** if every distinct pair is orthogonal. It is **orthonormal** if it is orthogonal and every vector has unit norm.

An orthogonal set of non-zero vectors is linearly independent. An orthonormal basis is particularly useful because coordinate extraction becomes a simple inner product with each basis vector.

Orthogonality depends on the chosen inner product. Vectors that are perpendicular under one metric need not be orthogonal under another.

## 6. The Gram matrix and non-orthonormal coordinates

In Module 04, a vector was represented by coordinates relative to a basis matrix \(B\). If the basis is not orthonormal, the ordinary dot product of the coordinate columns does not, in general, equal the physical Euclidean inner product of the represented vectors.

Suppose

$$
\mathbf{u}=B\mathbf{c},
\qquad
\mathbf{v}=B\mathbf{d}.
$$

Then

$$
\mathbf{u}^T\mathbf{v}
=\mathbf{c}^T B^T B\mathbf{d}.
$$

Define the **Gram matrix**

$$
G=B^TB.
$$

The inner product in these basis coordinates is therefore

$$
\langle\mathbf{u},\mathbf{v}\rangle
=\mathbf{c}^T G\mathbf{d}.
$$

If the basis is orthonormal, \(G=I\), and the expression reduces to \(\mathbf{c}^T\mathbf{d}\). If the basis is oblique or differently scaled, the Gram matrix carries the geometric information needed to calculate lengths and angles correctly.

This is one reason that coordinate values should not be treated as if they always lived in an orthonormal Cartesian frame.

## 7. Projection onto a direction

The **projection** of a vector \(\mathbf{v}\) onto a non-zero vector \(\mathbf{a}\) is the component of \(\mathbf{v}\) in the direction of \(\mathbf{a}\):

$$
\operatorname{proj}_{\mathbf{a}}(\mathbf{v})
=
\frac{\langle\mathbf{v},\mathbf{a}\rangle}
{\langle\mathbf{a},\mathbf{a}\rangle}\mathbf{a}.
$$

The scalar coefficient tells us how far along \(\mathbf{a}\) the projection lies. The vector projection has the same units as \(\mathbf{v}\).

The residual component is

$$
\mathbf{r}
=\mathbf{v}-\operatorname{proj}_{\mathbf{a}}(\mathbf{v}).
$$

It is orthogonal to \(\mathbf{a}\):

$$
\langle\mathbf{r},\mathbf{a}\rangle=0.
$$

Thus a vector splits into two perpendicular parts: one along the selected direction and one perpendicular to it.

### Worked example 3 — along-track and cross-track components

Let a route's local direction be

$$
\mathbf{a}=\begin{bmatrix}3\\4\end{bmatrix},
$$

and a displacement from the route origin be

$$
\mathbf{v}=\begin{bmatrix}10\\0\end{bmatrix}\mathrm{m}.
$$

Since \(\mathbf{v}^T\mathbf{a}=30\) and \(\mathbf{a}^T\mathbf{a}=25\), the projection is

$$
\operatorname{proj}_{\mathbf{a}}(\mathbf{v})
=\frac{30}{25}\begin{bmatrix}3\\4\end{bmatrix}
=\begin{bmatrix}3.6\\4.8\end{bmatrix}\mathrm{m}.
$$

The perpendicular component is

$$
\mathbf{r}
=\begin{bmatrix}10\\0\end{bmatrix}
-\begin{bmatrix}3.6\\4.8\end{bmatrix}
=\begin{bmatrix}6.4\\-4.8\end{bmatrix}\mathrm{m}.
$$

Check orthogonality:

$$
\mathbf{r}^T\mathbf{a}
=6.4(3)-4.8(4)=0.
$$

The along-direction projection has length 6 m, and the perpendicular component has length 8 m. The decomposition is exact for the infinite line through the origin in direction \(\mathbf{a}\).

## 8. Projection onto a subspace

A line is a one-dimensional subspace. A plane through the origin is a two-dimensional subspace in three-dimensional space. Projection can be generalised to any finite-dimensional subspace.

Let the columns of \(Q\) form an orthonormal basis for a subspace. The orthogonal projection matrix is

$$
P=QQ^T.
$$

The projected vector and residual are

$$
\widehat{\mathbf{v}}=P\mathbf{v},
\qquad
\mathbf{r}=(I-P)\mathbf{v}.
$$

The residual is orthogonal to every vector in the subspace. The projection is the unique vector in that subspace with the smallest Euclidean distance to \(\mathbf{v}\).

If the columns of \(B\) are independent but not orthonormal, the projection matrix is

$$
P=B(B^TB)^{-1}B^T.
$$

This formula assumes full column rank, so \(B^TB\) is invertible. In numerical computation, one generally avoids explicitly forming matrix inverses and uses suitable factorizations or orthogonal bases instead. Those computational details belong to later modules and numerical analysis.

A valid orthogonal projection matrix is symmetric and idempotent:

$$
P^T=P,
\qquad
P^2=P.
$$

Idempotence means projecting a vector already in the subspace does not change it.

## 9. Spatial application — closest point on a line segment

Consider a straight segment from point \(A\) to point \(B\), with local Cartesian coordinates

$$
A=\begin{bmatrix}0\\0\end{bmatrix},
\qquad
B=\begin{bmatrix}100\\0\end{bmatrix}\mathrm{m}.
$$

A measured point is

$$
X=\begin{bmatrix}35\\12\end{bmatrix}\mathrm{m}.
$$

The direction vector is \(\mathbf{d}=B-A=(100,0)^T\). The unconstrained projection parameter is

$$
t=\frac{(X-A)^T\mathbf{d}}{\mathbf{d}^T\mathbf{d}}
=\frac{3500}{10000}=0.35.
$$

The projected point is

$$
P=A+t\mathbf{d}
=\begin{bmatrix}35\\0\end{bmatrix}\mathrm{m}.
$$

The perpendicular offset is 12 m. Because \(0\leq t\leq1\), the projected point lies on the finite segment.

For a finite segment, the nearest point is obtained by clamping the parameter:

$$
t_{segment}=\min(1,\max(0,t)).
$$

If \(t<0\), the closest point on the segment is endpoint A. If \(t>1\), it is endpoint B. The projection onto the infinite supporting line and the closest point on the finite segment are therefore different problems near or beyond the endpoints.

This calculation can support cross-track distance, map matching and point-to-segment proximity. It is not by itself a complete road-matching algorithm: real networks require topology, candidate selection, direction, connectivity, uncertainty and possibly a suitable projected coordinate system.

## 10. Orthogonality and least squares

Suppose a vector \(\mathbf{y}\) is approximated by a vector in the column space of a design matrix \(A\). The least-squares projection chooses the modelled vector \(A\widehat{\mathbf{x}}\) that minimises the squared Euclidean residual norm:

$$
\min_{\mathbf{x}}\|\mathbf{y}-A\mathbf{x}\|^2.
$$

At a least-squares solution, the residual

$$
\mathbf{r}=\mathbf{y}-A\widehat{\mathbf{x}}
$$

is orthogonal to every column of \(A\):

$$
A^T\mathbf{r}=\mathbf{0}.
$$

These are the **normal equations**:

$$
A^TA\widehat{\mathbf{x}}=A^T\mathbf{y}.
$$

This geometric condition says that no further improvement is possible by moving the fitted vector along any direction available in the model's column space.

This is an introductory geometric interpretation, not a recommendation to solve numerical problems by explicitly forming and inverting \(A^TA\). Conditioning, rank deficiency, weighted least squares and computational solution methods are developed later.

For weighted least squares, the geometry changes with the chosen positive-definite weight matrix. A residual that is orthogonal under a weighted inner product need not be orthogonal under the ordinary Euclidean dot product.

## 11. Common mistakes and limits

- **Using the dot product as a distance:** the dot product is a scalar; the norm is the length.
- **Forgetting to divide by the direction's squared length:** the projection formula works for non-unit directions because of the denominator.
- **Projecting onto the wrong object:** a line, a ray and a finite segment have different feasible sets.
- **Assuming all coordinate axes are orthonormal:** non-orthonormal bases require their Gram matrix to recover the Euclidean metric.
- **Treating orthogonality as independent of the metric:** a different inner product can change which vectors are orthogonal.
- **Assuming residuals are always Euclidean-perpendicular:** weighted and constrained estimation have different geometric conditions.
- **Confusing a geometric nearest point with a valid spatial match:** network structure and domain constraints still matter.

The formulas assume a real finite-dimensional vector space and a stated inner product. Distances on the Earth's curved surface, geodesic azimuths, map-projection scale, terrain distance and three-dimensional physical measurement require additional modelling.

## 12. Exercises

### Exercise 1 — compute an inner product and norm

Let \(\mathbf{u}=(2,3)^T\) and \(\mathbf{v}=(4,-1)^T\). Find \(\langle\mathbf{u},\mathbf{v}\rangle\) and \(\|\mathbf{u}\|\).

**Worked guidance:** The inner product is \(2(4)+3(-1)=5\). The norm is \(\sqrt{2^2+3^2}=\sqrt{13}\).

### Exercise 2 — test orthogonality

Are \((3,2)^T\) and \((2,-3)^T\) orthogonal?

**Worked guidance:** Their dot product is \(3(2)+2(-3)=0\), so they are orthogonal under the standard Euclidean inner product.

### Exercise 3 — calculate an angle

Find the angle between \((1,0)^T\) and \((1,\sqrt{3})^T\).

**Worked guidance:** Their dot product is 1 and their norms are 1 and 2. Thus \(\cos\theta=1/2\) and \(\theta=60^\circ\).

### Exercise 4 — project onto a direction

Project \(\mathbf{v}=(4,3)^T\) onto \(\mathbf{a}=(1,0)^T\). Find the residual.

**Worked guidance:** The projection is \((4,0)^T\); the residual is \((0,3)^T\). Their dot product is zero.

### Exercise 5 — project onto a non-unit direction

Project \(\mathbf{v}=(6,2)^T\) onto \(\mathbf{a}=(2,1)^T\).

**Worked guidance:** The coefficient is \((6(2)+2(1))/(2^2+1^2)=14/5\). The projection is \((28/5,14/5)^T\). The residual is \((2/5,-4/5)^T\), which has zero dot product with \(\mathbf{a}\).

### Exercise 6 — finite segment or infinite line?

A point projects onto the supporting line of a segment with parameter \(t=1.4\). Where is its nearest point on the finite segment?

**Worked guidance:** Clamp the parameter to 1. The nearest point is endpoint B. The perpendicular projection onto the infinite line lies beyond the segment.

### Exercise 7 — understand a non-orthonormal basis

If a basis matrix is \(B\), why is \(\mathbf{c}^T\mathbf{d}\) not generally the Euclidean inner product of vectors represented by coordinate columns \(\mathbf{c}\) and \(\mathbf{d}\)?

**Worked guidance:** The physical vectors are \(B\mathbf{c}\) and \(B\mathbf{d}\). Their inner product is \(\mathbf{c}^TB^TB\mathbf{d}\). The Gram matrix \(B^TB\) is the coordinate representation of the metric. It equals the identity only for an orthonormal basis.

### Exercise 8 — least-squares geometry

In ordinary least squares, what does \(A^T\mathbf{r}=0\) mean geometrically?

**Worked guidance:** The residual is orthogonal to every column of the design matrix and therefore to the entire column space. The fitted vector is the orthogonal projection of the observations onto that model space.

## 13. Connections and limits

This module prepares for:

- **Module 06 — Least squares and constrained systems:** derives estimation from projection geometry and extends it to weighted and constrained models.
- **Module 07 — Symmetric matrices and quadratic forms:** formalises squared lengths and quadratic objectives.
- **Module 08 — Eigenvalues and eigenvectors:** uses inner products and orthogonality to interpret symmetric transformations.
- **Module 09 — Matrix factorizations:** develops QR and related computational methods for projection and least squares.

It also connects to cross-track distance, point-to-line and point-to-segment geometry, local coordinate frames, residual interpretation and spatial matching. It does not establish a complete map-matching method or a geodetic distance procedure.

## References

- Massachusetts Institute of Technology, Department of Mathematics. [18.06 Linear Algebra — OpenCourseWare, Spring 2010](https://ocw.mit.edu/courses/18-06-linear-algebra-spring-2010/). Course scope includes orthogonality, projections, least squares and inner products.
- Strang, G. (2021). [Lecture Notes for Linear Algebra](https://www-math.mit.edu/~gs/LectureNotes/). MIT-hosted notes on orthogonality, projections and least squares.

**Source note:** These references are linked for human study. The MIT course identity and topic coverage are recorded in the repository source register; individual lectures and notes have not been reviewed claim by claim. This module presents original explanations and synthetic examples rather than reproducing course text, figures or exercises.

**Scope:** real finite-dimensional inner-product spaces, Euclidean dot products, induced norms, angles, orthogonality, Gram matrices, projections onto directions and subspaces, and the geometric least-squares condition. Weighted estimation, numerical algorithms, geodesic metrics and advanced projection methods are deferred.
