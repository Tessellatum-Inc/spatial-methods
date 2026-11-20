# Vectors, matrices and linear transformations

**Subject identity:** `SM-FND-002` — Linear algebra and matrix methods  
**Module:** 01  
**Status:** Initial public teaching resource; independent technical review and learner testing outstanding.

## 1. Why linear algebra matters in spatial science

A spatial workflow often begins with observations or coordinates and ends with a transformed, estimated or summarised set of values. Linear algebra provides a common language for describing how collections of numbers relate.

Examples include:

- transforming a coordinate vector from one local Cartesian frame to another;
- representing a set of survey observations using a design matrix;
- combining spectral bands or variables in a multivariate analysis;
- expressing a linear model as a matrix equation;
- representing covariance among several measurements.

The central idea is that a vector is not merely a column of numbers and a matrix is not merely a rectangular table. They represent structured quantities and operations. Their dimensions, units, coordinate meanings and ordering must be understood.

This module establishes notation and operations. It does not yet teach the complete theory of vector spaces, rank, least squares, eigenanalysis or matrix factorisation; those are developed in later modules.

## 2. Scalars, vectors and matrices

A **scalar** is a single number. Depending on the model, it may represent a distance, an angle, a scale factor, a population count or an estimated parameter.

A **vector** is an ordered collection of components. A column vector with three components is written

$$
\mathbf{x}=\begin{bmatrix}x_1\\x_2\\x_3\end{bmatrix}.
$$

The components may represent coordinates, velocity components, residuals, parameters or measurements. The interpretation is supplied by the model, not by the column shape alone.

A **matrix** is a rectangular array of values:

$$
A=\begin{bmatrix}
a_{11}&a_{12}&a_{13}\\
a_{21}&a_{22}&a_{23}
\end{bmatrix}.
$$

This matrix has 2 rows and 3 columns, so its dimensions are \(2\times3\). The entry \(a_{ij}\) is in row \(i\), column \(j\).

A vector with \(n\) components can be treated as an \(n\times1\) matrix. A row vector has dimensions \(1\times n\). Keep row and column orientation explicit: many formula and software errors arise from silently switching conventions.

## 3. Dimensions are part of the mathematics

The dimensions of an object constrain which operations are defined.

If \(A\) is \(m\times n\) and \(B\) is \(n\times p\), then the product \(AB\) is defined and has dimensions \(m\times p\). The inner dimensions must agree.

For a matrix-vector product, if \(A\) is \(m\times n\) and \(\mathbf{x}\) is \(n\times1\), then

$$
A\mathbf{x}=\mathbf{b}
$$

produces an \(m\times1\) vector.

The number of columns in \(A\) must equal the number of entries in \(\mathbf{x}\). The output has one component for each row of \(A\).

Dimensions are not a substitute for semantic checks. A matrix multiplication may be dimensionally valid while combining incompatible units, different coordinate orders or unrelated quantities.

## 4. Vector addition and scalar multiplication

Two vectors can be added only when they have the same number of components and compatible meanings:

$$
\begin{bmatrix}x_1\\x_2\end{bmatrix}
+
\begin{bmatrix}y_1\\y_2\end{bmatrix}
=
\begin{bmatrix}x_1+y_1\\x_2+y_2\end{bmatrix}.
$$

A scalar multiplies every component:

$$
c\begin{bmatrix}x_1\\x_2\end{bmatrix}
=
\begin{bmatrix}cx_1\\cx_2\end{bmatrix}.
$$

For example, suppose a local planar displacement is

$$
\mathbf{d}=\begin{bmatrix}12\\-5\end{bmatrix}\;\mathrm{m}.
$$

A scale factor of 2 gives

$$
2\mathbf{d}=\begin{bmatrix}24\\-10\end{bmatrix}\;\mathrm{m}.
$$

This is a mathematical scaling operation. Whether doubling a measured displacement is meaningful depends on the application.

## 5. Linear combinations

A linear combination of vectors \(\mathbf{v}_1,\ldots,\mathbf{v}_k\) is a sum of scalar multiples:

$$
\mathbf{y}=c_1\mathbf{v}_1+\cdots+c_k\mathbf{v}_k.
$$

This simple structure appears throughout spatial analysis.

For example, if two raster-derived variables are represented at a cell by a vector

$$
\mathbf{x}=\begin{bmatrix}x_1\\x_2\end{bmatrix},
$$

then a weighted index

$$
s=0.7x_1+0.3x_2
$$

is a linear combination. The coefficients do not automatically make the index scientifically valid: variable scaling, direction, units, weights and the decision context still need justification.

A set of vectors can be arranged as the columns of a matrix. Then a linear combination is compactly written as

$$
A\mathbf{c}=c_1\mathbf{a}_1+\cdots+c_n\mathbf{a}_n,
$$

where \(\mathbf{a}_i\) are the columns of \(A\), and \(\mathbf{c}\) contains the coefficients.

This column view becomes central when studying linear systems, rank and least squares.

## 6. Matrix addition and multiplication

Matrices can be added when they have the same dimensions:

$$
\begin{bmatrix}1&2\\3&4\end{bmatrix}
+
\begin{bmatrix}5&6\\7&8\end{bmatrix}
=
\begin{bmatrix}6&8\\10&12\end{bmatrix}.
$$

Matrix multiplication combines rows of the first matrix with columns of the second. For example,

$$
A=\begin{bmatrix}1&2\\3&4\end{bmatrix},
\qquad
B=\begin{bmatrix}2&0\\1&3\end{bmatrix}
$$

gives

$$
AB=\begin{bmatrix}4&6\\10&12\end{bmatrix}.
$$

In general, matrix multiplication is **not commutative**: \(AB\) and \(BA\) may both be defined, but need not be equal. In this example,

$$
BA=\begin{bmatrix}2&4\\10&14\end{bmatrix}.
$$

Order matters because the operations are applied in sequence.

The identity matrix leaves a compatible vector unchanged:

$$
I_n\mathbf{x}=\mathbf{x}.
$$

For two dimensions,

$$
I_2=\begin{bmatrix}1&0\\0&1\end{bmatrix}.
$$

The zero matrix contains only zeros and maps every compatible vector to the zero vector.

## 7. A matrix as a linear transformation

A matrix can represent a function that maps an input vector to an output vector:

$$
T(\mathbf{x})=A\mathbf{x}.
$$

A transformation is linear when it preserves vector addition and scalar multiplication:

$$
T(\mathbf{x}+\mathbf{y})=T(\mathbf{x})+T(\mathbf{y}),
$$

$$
T(c\mathbf{x})=cT(\mathbf{x}).
$$

A linear transformation maps the zero vector to the zero vector. Translation by a non-zero vector is therefore not a linear transformation in ordinary Cartesian coordinates; it is an **affine** transformation.

### Worked example 1 — rotation in a local Cartesian plane

A counterclockwise rotation by angle \(\theta\) about the origin is represented by

$$
R(\theta)=
\begin{bmatrix}
\cos\theta&-\sin\theta\\
\sin\theta&\cos\theta
\end{bmatrix}.
$$

For \(\theta=90^\circ\),

$$
R=
\begin{bmatrix}0&-1\\1&0\end{bmatrix}.
$$

Apply it to a local point vector

$$
\mathbf{x}=\begin{bmatrix}4\\2\end{bmatrix}\;\mathrm{m}:
\qquad
R\mathbf{x}=
\begin{bmatrix}-2\\4\end{bmatrix}\;\mathrm{m}.
$$

The vector has been rotated about the origin. Its Euclidean length is unchanged:

$$
\sqrt{4^2+2^2}=\sqrt{(-2)^2+4^2}=\sqrt{20}\;\mathrm{m}.
$$

This is an ideal planar example. Real coordinate operations require declared source and target reference systems, axis order, units, datum and projection information. A planar rotation matrix is not a general CRS transformation.

### Worked example 2 — an affine coordinate operation

A two-dimensional affine transformation can be written

$$
\mathbf{y}=A\mathbf{x}+\mathbf{t},
$$

where \(A\) is a 2-by-2 linear part and \(\mathbf{t}\) is a translation vector.

Let

$$
A=\begin{bmatrix}1&0\\0&-1\end{bmatrix},
\quad
\mathbf{t}=\begin{bmatrix}100\\50\end{bmatrix}\;\mathrm{m},
\quad
\mathbf{x}=\begin{bmatrix}12\\8\end{bmatrix}\;\mathrm{m}.
$$

Then

$$
\mathbf{y}=
\begin{bmatrix}1&0\\0&-1\end{bmatrix}
\begin{bmatrix}12\\8\end{bmatrix}
+
\begin{bmatrix}100\\50\end{bmatrix}
=
\begin{bmatrix}112\\42\end{bmatrix}\;\mathrm{m}.
$$

The reflection and translation are mathematical components of this example. They are not a recommended geodetic transformation model.

## 8. Homogeneous coordinates: representing affine operations with matrices

A translation can be represented as a matrix operation by adding a homogeneous coordinate. Represent a planar point \((x,y)\) as

$$
\tilde{\mathbf{x}}=
\begin{bmatrix}x\\y\\1\end{bmatrix}.
$$

The affine transformation above becomes

$$
\tilde{\mathbf{y}}=
\begin{bmatrix}
1&0&100\\
0&-1&50\\
0&0&1
\end{bmatrix}
\tilde{\mathbf{x}}.
$$

For \((x,y)=(12,8)\), the result is \((112,42,1)\). The first two components are the transformed planar coordinates.

Homogeneous coordinates are widely used to compose transformations in graphics, robotics, photogrammetry and computer vision. The last coordinate is part of the representation; it is not an extra measured height or a third spatial axis.

## 9. Spatial applications: the same algebra, different meanings

### 9.1 Coordinate operations

A local planar transformation may use a matrix to rotate, reflect, scale or shear coordinate components. The operation must declare axis order, units, origin and frame. A coordinate pair without a reference system is not enough to establish geographic meaning.

See [coordinate transformation and CRS axis order](../../algorithms/geodesy/crs-transformation.md). That algorithm record describes CRS operations and their geodetic requirements; this module only introduces the matrix language.

### 9.2 Measurement and estimation models

Many observation models can be expressed as

$$
A\mathbf{x}\approx\mathbf{b}.
$$

Here \(\mathbf{x}\) may contain unknown parameters, \(\mathbf{b}\) observed quantities and \(A\) coefficients describing how the unknowns contribute to observations.

In the repository's survey-adjustment examples, the design matrix connects unknown point heights to observed height differences. The full interpretation also depends on datum constraints, observation covariance, units and the stochastic model.

See [measurement science and survey adjustment](../../learning-paths/measurement-science-and-survey-adjustment.md) and the [covariance GLS implementation](../../implementations/python/covariance-gls/README.md).

### 9.3 Multivariate analysis

A data matrix may store observations in rows and variables in columns. If \(X\) has \(n\) rows and \(p\) columns, it contains \(n\) observations of \(p\) variables, subject to the chosen data convention.

PCA forms a covariance matrix from centered data and studies its eigenvectors and eigenvalues. This module introduces matrix notation; the statistical meaning, scaling choices and spectral analysis require later modules and probability/statistics foundations.

See [principal component analysis](../../algorithms/statistics/pca.md).

## 10. Common mistakes and checks

- **Ignoring dimensions:** check row and column counts before multiplying.
- **Treating multiplication as commutative:** in general, \(AB\ne BA\).
- **Mixing units:** a dimensionally valid matrix product may still combine metres, degrees, counts or incompatible physical quantities.
- **Ignoring axis order:** east-north and north-east are different component conventions.
- **Confusing point and displacement:** translations affect points but not free displacement vectors.
- **Calling every coordinate operation linear:** translations make an affine operation; map projections are generally nonlinear.
- **Assuming a matrix defines its own meaning:** the data model must specify what rows, columns and components represent.
- **Assuming numerical output proves correctness:** the model, input data, reference system and implementation still require checks.

A useful minimum checklist is: identify the object represented by each vector; record dimensions; state units and coordinate conventions; verify the operation order; and interpret the output in the original problem.

## 11. Exercises

### Exercise 1 — dimensions

Let \(A\) have dimensions \(3\times2\), \(B\) have dimensions \(2\times4\), and \(\mathbf{x}\) have dimensions \(4\times1\).

1. What are the dimensions of \(AB\)?
2. Is \(A\mathbf{x}\) defined?
3. Is \(B\mathbf{x}\) defined?

**Worked guidance:** \(AB\) is \(3\times4\). \(A\mathbf{x}\) is not defined because 2 does not equal 4. \(B\mathbf{x}\) is defined and has dimensions \(2\times1\).

### Exercise 2 — matrix multiplication order

Using the matrices in Section 6, calculate \(BA\) and compare it with \(AB\). Explain why the results differ.

**Worked guidance:** \(BA=\begin{bmatrix}2&4\\10&14\end{bmatrix}\), while \(AB=\begin{bmatrix}4&6\\10&12\end{bmatrix}\). Matrix multiplication composes transformations in an order; reversing that order generally changes the result.

### Exercise 3 — rotate a displacement

Rotate the local displacement \((3,1)\) metres counterclockwise by 90 degrees. Calculate the output and compare its length with the original.

**Worked guidance:** The output is \((-1,3)\) metres. Both lengths are \(\sqrt{10}\) metres.

### Exercise 4 — distinguish a point from a displacement

A local point is \((20,30)\) metres and a displacement is \((4,-2)\) metres. A translation vector is \((100,50)\) metres.

1. Apply the translation to the point.
2. Explain whether the displacement should also receive the translation.

**Worked guidance:** The translated point is \((120,80)\) metres. The displacement remains \((4,-2)\) metres: a translation changes the origin-relative location of a point, not the difference between two points.

### Exercise 5 — build a weighted combination

Two aligned raster variables at one cell have values 0.2 and 0.8. Calculate \(0.25x_1+0.75x_2\). State two reasons why the resulting value may not be a defensible suitability score.

**Worked guidance:** The result is 0.65. It may be indefensible if the variables are on incompatible scales or if the weights and criterion directions have not been justified. Alignment alone does not make variables comparable.

### Exercise 6 — affine transformation

Apply the affine transformation in Section 7 to the point \((5,3)\) metres.

**Worked guidance:** \(A\mathbf{x}=(5,-3)^T\); adding \((100,50)^T\) gives \((105,47)^T\) metres.

## 12. Connections and limits

This module supplies the notation used by later modules on subspaces, linear systems, rank, projections, least squares, eigenanalysis and matrix factorizations. It also supports, but does not replace:

- geodesy and coordinate reference theory;
- measurement science and stochastic observation models;
- numerical analysis and computational stability;
- probability and statistical inference;
- geometry and spatial representation.

It does not teach a complete coordinate transformation procedure, survey adjustment, PCA implementation or numerical solver. Those remain in their respective canonical resources.

## References

- Massachusetts Institute of Technology, Department of Mathematics. [18.06 Linear Algebra — OpenCourseWare, Spring 2010](https://ocw.mit.edu/courses/18-06-linear-algebra-spring-2010/). Course scope includes matrix multiplication, vector spaces, column space and nullspace, least squares, eigenvalues, positive definite matrices, linear transformations and decompositions.
- Strang, G. (2021). [Lecture Notes for Linear Algebra](https://www-math.mit.edu/~gs/LectureNotes/). MIT-hosted notes covering linear combinations, matrix-vector multiplication, subspaces, matrix products and linear systems.

**Source note:** The MIT course pages and notes were checked for identity and topic coverage on 2026-11-20. This module presents original spatial explanations and worked examples; it does not reproduce MIT course text, figures or exercises. The references are learning resources, not claim-by-claim verification or independent review.

**Scope:** introductory real-valued vector and matrix notation, elementary matrix operations, linear maps and planar affine examples. Complex vector spaces, abstract vector-space axioms, full linear-system theory, least squares, spectral theory and numerical analysis are deferred to later modules or specialist foundations.
