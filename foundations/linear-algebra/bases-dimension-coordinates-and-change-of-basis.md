# Bases, dimension, coordinates and change of basis

**Subject identity:** `SM-FND-002` — Linear algebra and matrix methods  
**Module:** 04  
**Status:** Initial public teaching resource; independent technical review and learner testing outstanding.

## 1. Why bases matter in spatial science

A spatial quantity can be described using different coordinate directions without changing the underlying quantity.

A displacement might be described using east and north components, local instrument axes, along-track and cross-track components, or another convenient pair of directions. The numbers change when the basis changes; the geometric vector does not.

This module develops the distinction between:

- a vector and its coordinate representation;
- a basis and an arbitrary collection of directions;
- dimension and the number of coordinates used to write a vector;
- a change of basis and a physical transformation of a spatial object;
- a change in coordinate origin and a change in vector basis.

These distinctions are essential when moving between local and global descriptions, interpreting sensor axes, working with coordinate frames, and reading transformation matrices.

## 2. What is a basis?

A **basis** of a vector space is a set of vectors that satisfies two conditions:

1. The vectors are linearly independent.
2. They span the entire vector space.

The first condition prevents redundant directions. The second ensures that every vector in the space can be represented.

For a finite-dimensional vector space, every basis contains the same number of vectors. That number is the **dimension** of the space.

Examples:

- The plane \(\mathbb{R}^2\) has dimension 2. A basis contains two independent vectors.
- Three-dimensional Euclidean vector space \(\mathbb{R}^3\) has dimension 3. A basis contains three independent vectors.
- The space of real polynomials of degree at most 2 has dimension 3, with one possible basis \(\{1,x,x^2\}\).

A basis is not necessarily orthogonal, equally scaled, or aligned with familiar compass directions. Those are additional properties that may be useful in particular applications.

### Worked example 1 — two different bases for the plane

The standard basis of the plane is

$$
\mathbf{e}_1=\begin{bmatrix}1\\0\end{bmatrix},
\qquad
\mathbf{e}_2=\begin{bmatrix}0\\1\end{bmatrix}.
$$

Another possible basis is

$$
\mathbf{b}_1=\begin{bmatrix}1\\0\end{bmatrix},
\qquad
\mathbf{b}_2=\begin{bmatrix}1\\1\end{bmatrix}.
$$

The second pair is independent: neither vector is a scalar multiple of the other. It spans the plane because any \((x,y)^T\) can be written as

$$
(x-y)\mathbf{b}_1+y\mathbf{b}_2
=
\begin{bmatrix}x\\y\end{bmatrix}.
$$

Both pairs are bases of the same two-dimensional vector space. Their directions are different, but neither changes the plane itself.

## 3. Dimension is not the number of entries you happen to write

The dimension of a vector space is the number of elements in any one of its bases. It is an intrinsic property of the space, not a property of a particular coordinate notation.

A vector in a two-dimensional space can be written with two coordinates in any basis of that space. Writing it using three numbers does not automatically make the underlying space three-dimensional. The representation may be redundant or may belong to a larger ambient space with constraints.

For example, points on a line in three-dimensional space have three Cartesian coordinates, but their displacement vectors along that line form a one-dimensional vector subspace. The ambient space is three-dimensional; the line's direction space is one-dimensional.

This distinction appears in constrained movement, road centreline geometry, profile measurements, and low-dimensional models embedded in larger spatial spaces.

## 4. Coordinates are coefficients relative to a basis

Let \(V\) be an \(n\)-dimensional vector space with ordered basis

$$
\mathcal{B}=\{\mathbf{b}_1,\ldots,\mathbf{b}_n\}.
$$

Every vector \(\mathbf{v}\in V\) can be written uniquely as

$$
\mathbf{v}=c_1\mathbf{b}_1+\cdots+c_n\mathbf{b}_n.
$$

The column

$$
[\mathbf{v}]_{\mathcal{B}}
=
\begin{bmatrix}c_1\\\vdots\\c_n\end{bmatrix}
$$

is the **coordinate vector of** \(\mathbf{v}\) **relative to** basis \(\mathcal{B}\).

The vector and its coordinate column are not the same mathematical object. The vector is the quantity being represented; the coordinate column records its coefficients in a chosen basis.

If the basis changes, the coordinate column usually changes even though the vector remains the same.

### Worked example 2 — expressing a vector in a non-standard basis

Use the basis from Worked example 1:

$$
\mathbf{b}_1=\begin{bmatrix}1\\0\end{bmatrix},
\qquad
\mathbf{b}_2=\begin{bmatrix}1\\1\end{bmatrix}.
$$

Let the vector, expressed in standard Cartesian coordinates, be

$$
\mathbf{v}=\begin{bmatrix}5\\3\end{bmatrix}.
$$

We seek coefficients \(a,b\) such that

$$
a\mathbf{b}_1+b\mathbf{b}_2=\mathbf{v}.
$$

This gives

$$
\begin{bmatrix}1&1\\0&1\end{bmatrix}
\begin{bmatrix}a\\b\end{bmatrix}
=
\begin{bmatrix}5\\3\end{bmatrix}.
$$

The second row gives \(b=3\), and the first gives \(a=2\). Thus

$$
[\mathbf{v}]_{\mathcal{B}}
=
\begin{bmatrix}2\\3\end{bmatrix}.
$$

The vector has standard coordinates \((5,3)^T\), but coordinates \((2,3)^T\) in the chosen non-standard basis. Both describe the same vector.

## 5. The basis matrix

Suppose the basis vectors are written as columns in some reference coordinate system:

$$
B=
\begin{bmatrix}
|&&|\\
\mathbf{b}_1&\cdots&\mathbf{b}_n\\
|&&|
\end{bmatrix}.
$$

If \(\mathbf{c}_{\mathcal{B}}\) contains the vector's coordinates in basis \(\mathcal{B}\), its reference-coordinate representation is

$$
\mathbf{v}=B\mathbf{c}_{\mathcal{B}}.
$$

Because the basis vectors are independent, the square basis matrix is invertible. Therefore,

$$
\mathbf{c}_{\mathcal{B}}=B^{-1}\mathbf{v}.
$$

The columns of \(B\) are not arbitrary: they must be independent and must be expressed in the same reference coordinate system. If the columns are dependent, they do not form a basis and the inverse does not exist.

For the previous example,

$$
B=
\begin{bmatrix}1&1\\0&1\end{bmatrix},
\qquad
B^{-1}=
\begin{bmatrix}1&-1\\0&1\end{bmatrix}.
$$

Then

$$
B^{-1}\begin{bmatrix}5\\3\end{bmatrix}
=
\begin{bmatrix}2\\3\end{bmatrix}.
$$

This is the algebraic operation that converts the reference coordinates into coefficients relative to the new basis.

## 6. Changing from one basis to another

Let \(B\) and \(C\) be two basis matrices whose columns are both expressed in the same reference coordinate system. A vector can be represented in either basis:

$$
\mathbf{v}=B\mathbf{c}_B=C\mathbf{c}_C.
$$

Equating the two expressions gives

$$
\mathbf{c}_C=C^{-1}B\mathbf{c}_B.
$$

The matrix

$$
P_{C\leftarrow B}=C^{-1}B
$$

converts coordinate columns from basis \(B\) to basis \(C\). The arrow notation is a reminder of the direction: coordinates *in B* are converted to coordinates *in C*.

The inverse conversion is

$$
P_{B\leftarrow C}=B^{-1}C
=(P_{C\leftarrow B})^{-1}.
$$

The order matters. Matrix multiplication is not generally commutative, so reversing the order produces a different operation.

### Worked example 3 — change between two bases

Let the old basis be the standard basis, so \(B=I\), and let the new basis be

$$
C=\begin{bmatrix}1&1\\0&1\end{bmatrix}.
$$

For the vector whose old coordinates are

$$
\mathbf{c}_B=\begin{bmatrix}5\\3\end{bmatrix},
$$

the new coordinates are

$$
\mathbf{c}_C=C^{-1}B\mathbf{c}_B
=
\begin{bmatrix}1&-1\\0&1\end{bmatrix}
\begin{bmatrix}5\\3\end{bmatrix}
=
\begin{bmatrix}2\\3\end{bmatrix}.
$$

To check, reconstruct the vector:

$$
C\mathbf{c}_C
=
\begin{bmatrix}1&1\\0&1\end{bmatrix}
\begin{bmatrix}2\\3\end{bmatrix}
=
\begin{bmatrix}5\\3\end{bmatrix}.
$$

The coordinate values changed, but the reconstructed vector did not.

## 7. Orthogonal rotated bases

A particularly useful case is a rotated orthonormal basis in a two-dimensional Euclidean plane.

Let the new basis be rotated counter-clockwise by angle \(\theta\) relative to the old Cartesian basis. Its basis matrix is

$$
R=
\begin{bmatrix}
\cos\theta&-\sin\theta\\
\sin\theta&\cos\theta
\end{bmatrix}.
$$

The columns are the new unit basis directions expressed in old coordinates. Since the basis is orthonormal,

$$
R^{-1}=R^T.
$$

For a vector with old coordinate column \(\mathbf{v}_{old}\), the new coordinate column is

$$
\mathbf{v}_{new}=R^T\mathbf{v}_{old}.
$$

The transpose appears because we are changing the coordinate description of the same vector. By contrast, multiplying the old coordinate column by \(R\) rotates the vector's components in the old coordinate frame. These are inverse-direction operations and should not be confused.

### Worked example 4 — local axes rotated by 30 degrees

Suppose a local instrument frame is rotated counter-clockwise by \(30^\circ\) relative to a reference frame. A vector has old coordinates

$$
\mathbf{v}_{old}=\begin{bmatrix}10\\0\end{bmatrix}.
$$

The coordinates in the rotated local basis are

$$
\mathbf{v}_{new}
=
\begin{bmatrix}
\cos30^\circ&\sin30^\circ\\
-\sin30^\circ&\cos30^\circ
\end{bmatrix}
\begin{bmatrix}10\\0\end{bmatrix}
=
\begin{bmatrix}5\sqrt{3}\\-5\end{bmatrix}.
$$

The negative second component is consistent with the vector lying clockwise from the new first axis. Reconstructing with \(R\) returns \((10,0)^T\).

The sign depends on the declared rotation direction and axis convention. Always state whether the angle describes the orientation of the new axes relative to the old axes or an active rotation of the vector.

## 8. Spatial interpretation — local and global frames

Spatial measurements often use a convenient local frame:

- an instrument may report directions in its own horizontal and vertical axes;
- a mobile mapping platform may describe motion in body-fixed forward, right and up axes;
- an engineering site may use a local grid aligned to a project baseline;
- a raster neighbourhood may be analysed in row and column directions.

A basis change can express a vector measured in one frame using another frame's axes. For a pure change of basis, the underlying vector is unchanged.

But a practical spatial reference-frame operation may involve much more than a basis change. It may include:

- a different origin or translation;
- a different scale or unit;
- rotation and axis convention;
- a map projection;
- a datum or reference-frame transformation;
- epoch-dependent transformations or vertical reference operations.

A map projection is generally nonlinear over a region. A geodetic coordinate operation may also require ellipsoid, datum, epoch and operation-grid information. These are not all captured by a single constant basis matrix. See the repository's [CRS transformation and axis-order resource](../../algorithms/geodesy/crs-transformation.md) for that broader subject.

## 9. Vectors versus points: why the origin matters

A vector represents a displacement or direction and is independent of the choice of coordinate origin. A point is a position relative to an origin.

If a point has coordinates \(\mathbf{x}_A\) in frame A and frame B has a different origin, converting point coordinates may require a translation as well as a basis conversion.

For example, if the same physical point has position vectors relative to two origins, and the basis matrices are \(B\) and \(C\), then the coordinate relation has the form

$$
\mathbf{x}_C=C^{-1}(B\mathbf{x}_B+\mathbf{t}),
$$

where \(\mathbf{t}\) is the displacement from origin C to origin A, expressed in the common reference-coordinate system under this convention.

The exact sign and frame in which translation is expressed depend on the declared transformation convention. The important distinction is that a translation changes point coordinates but does not change a free displacement vector.

This is why affine transformations of points and linear transformations of vectors should not be treated as identical operations.

## 10. Common mistakes

- **Calling any independent-looking directions a basis:** independence alone is insufficient; the vectors must also span the target space.
- **Treating coordinates as the vector itself:** coordinate values depend on the chosen basis.
- **Confusing dimension with ambient coordinate count:** a constrained subspace can have lower dimension than the space in which it is embedded.
- **Reversing the change-of-basis matrix:** if \(\mathbf{v}=B\mathbf{c}_B=C\mathbf{c}_C\), then \(\mathbf{c}_C=C^{-1}B\mathbf{c}_B\).
- **Confusing passive and active rotation:** changing axes and rotating a vector are inverse descriptions under the same convention.
- **Ignoring the origin:** vectors and points behave differently under translation.
- **Calling every CRS transformation a basis change:** projection, datum, epoch, scale and vertical operations can require additional models and parameters.

## 11. Exercises

### Exercise 1 — test a basis

Do the vectors \((1,2)^T\) and \((2,4)^T\) form a basis for \(\mathbb{R}^2\)?

**Worked guidance:** No. The second vector is twice the first, so the pair is dependent and cannot span the plane. The dimension of the plane is two, but the pair supplies only one independent direction.

### Exercise 2 — coordinates in a non-standard basis

Let

$$
B=\begin{bmatrix}1&0\\1&1\end{bmatrix},
\qquad
\mathbf{v}=\begin{bmatrix}4\\7\end{bmatrix}.
$$

Find the coordinates of \(\mathbf{v}\) in basis \(B\).

**Worked guidance:** Solve \(B\mathbf{c}=\mathbf{v}\). The equations are \(c_1=4\) and \(c_1+c_2=7\), so \(\mathbf{c}=(4,3)^T\).

### Exercise 3 — reconstruct a vector

Using Exercise 2, reconstruct the original vector from its basis coordinates.

**Worked guidance:** \(B(4,3)^T=(4,7)^T\). The reconstruction confirms the coordinate representation.

### Exercise 4 — change of basis

Let

$$
B=I,
\qquad
C=\begin{bmatrix}1&1\\0&1\end{bmatrix},
\qquad
\mathbf{c}_B=\begin{bmatrix}6\\2\end{bmatrix}.
$$

Find \(\mathbf{c}_C\).

**Worked guidance:** \(C^{-1}=\begin{bmatrix}1&-1\\0&1\end{bmatrix}\). Thus \(\mathbf{c}_C=C^{-1}B\mathbf{c}_B=(4,2)^T\).

### Exercise 5 — dimension in an embedded space

The displacement vectors of points constrained to a straight line in three-dimensional space are all scalar multiples of one non-zero direction vector. What is the dimension of this displacement subspace?

**Worked guidance:** One. The subspace has a basis consisting of that single direction vector, even though it is embedded in three-dimensional space.

### Exercise 6 — interpret a rotated frame

A new orthonormal coordinate frame is rotated counter-clockwise by angle \(\theta\) relative to an old frame. Which matrix converts old vector coordinates to new vector coordinates?

**Worked guidance:** If \(R\) has the new basis vectors as columns expressed in old coordinates, then the conversion is \(R^T\). The matrix \(R\) reconstructs old coordinates from new coordinates.

### Exercise 7 — point or vector?

A survey point is reported in a local engineering grid whose origin differs from the global grid origin. Is a rotation matrix alone necessarily sufficient to convert the point coordinates?

**Worked guidance:** No. A point conversion generally needs the origin translation as well as any rotation or scale. A free displacement vector is not affected by origin translation.

### Exercise 8 — diagnose the conceptual error

A colleague says: “The vector changed because its coordinates changed after I switched from east/north axes to local instrument axes.” Explain the correction.

**Worked guidance:** The coordinate representation changed because the basis changed. Under a pure basis change, the geometric vector remains the same. The colleague should distinguish the vector from its coordinate column.

## 12. Connections and limits

This module prepares for:

- **Module 05 — Inner products, norms, orthogonality and projections:** develops lengths, angles and orthogonal decomposition, including why orthonormal bases simplify coordinate conversion.
- **Module 06 — Least squares and constrained systems:** uses coordinate and parameter representations in estimation.
- **Module 08 — Eigenvalues and eigenvectors:** studies directions preserved by a linear transformation.
- **Module 09 — Matrix factorizations:** provides computational tools for solving systems and changing representations.

It also connects to geodetic reference systems, local engineering grids, sensor frames and coordinate operations. It does not specify a production CRS transformation, solve a full 3D datum transformation, or establish a surveying reference frame.

## References

- Massachusetts Institute of Technology, Department of Mathematics. [18.06 Linear Algebra — OpenCourseWare, Spring 2010](https://ocw.mit.edu/courses/18-06-linear-algebra-spring-2010/). Course scope includes vector spaces, bases, coordinates and change of basis.
- Strang, G. (2021). [Lecture Notes for Linear Algebra](https://www-math.mit.edu/~gs/LectureNotes/). MIT-hosted notes on vector spaces, bases and linear transformations.

**Source note:** These references are linked for human study. The MIT course identity and topic coverage are recorded in the repository source register; individual lectures and notes have not been reviewed claim by claim. This module presents original explanations and synthetic examples rather than reproducing course text, figures or exercises.

**Scope:** finite-dimensional real vector spaces, ordered bases, coordinate columns, basis matrices, change of basis, orthonormal planar rotations and the distinction between points and vectors under translation. Nonlinear projections, geodetic datum transformations, time-dependent frames and numerical conditioning are deferred.
