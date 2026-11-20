# Linear combinations, span, independence and subspaces

**Subject identity:** `SM-FND-002` — Linear algebra and matrix methods  
**Module:** 02  
**Status:** Initial public teaching resource; independent technical review and learner testing outstanding.

## 1. Why these ideas matter

Module 01 introduced vectors, matrices and linear transformations. This module asks a deeper question:

**What can a collection of vectors represent, and what can it not represent?**

That question appears in spatial work whenever we ask whether:

- a set of coordinate directions can represent every displacement in a plane or in three-dimensional space;
- a collection of observations contains enough independent information to estimate unknown parameters;
- one model variable is redundant because it can be formed from others;
- a control network constrains every unknown, or leaves one or more movements undetermined;
- a set of raster or sensor variables contains distinct information or repeated combinations.

The concepts of linear combination, span, linear independence and subspace describe the structure of these possibilities. They are prerequisites for understanding rank, null spaces and the solution structure of linear systems in Module 03.

## 2. Linear combinations: building vectors from other vectors

Given vectors \(\mathbf{v}_1,\ldots,\mathbf{v}_k\), a **linear combination** is any vector of the form

$$
\mathbf{u}=c_1\mathbf{v}_1+c_2\mathbf{v}_2+\cdots+c_k\mathbf{v}_k,
$$

where the coefficients \(c_i\) are scalars.

The coefficients may be positive, negative or zero. They specify how much of each vector contributes to the result.

### Worked example 1 — combining local directions

Let

$$
\mathbf{e}_1=\begin{bmatrix}1\\0\end{bmatrix},
\qquad
\mathbf{e}_2=\begin{bmatrix}0\\1\end{bmatrix}.
$$

For coefficients 6 and −3,

$$
6\mathbf{e}_1-3\mathbf{e}_2
=
\begin{bmatrix}6\\-3\end{bmatrix}.
$$

Every two-dimensional vector can be written as a linear combination of these two particular vectors. They provide independent east-like and north-like directions in this abstract Cartesian example. The labels east and north are illustrative; a real coordinate system must define its axis directions and reference.

A vector may have many different linear-combination representations if the generating vectors are dependent. If the generating vectors are independent, the representation within their span is unique. The formal reasoning for uniqueness is developed in Section 5.

## 3. Span: the set of all possible combinations

The **span** of a collection of vectors is the set of every linear combination that can be made from them:

$$
\operatorname{span}\{\mathbf{v}_1,\ldots,\mathbf{v}_k\}
=
\left\{
\sum_{i=1}^{k}c_i\mathbf{v}_i:
c_i\in\mathbb{R}
\right\}.
$$

Span is a set, not one vector. It describes the complete collection of directions and positions reachable through the allowed combinations.

### 3.1 One non-zero vector in the plane

Let

$$
\mathbf{v}=\begin{bmatrix}2\\1\end{bmatrix}.
$$

Its span is

$$
\operatorname{span}\{\mathbf{v}\}
=
\left\{
\begin{bmatrix}2c\\c\end{bmatrix}:c\in\mathbb{R}
\right\}.
$$

This is a line through the origin. It does not cover the whole plane. For example, \((0,1)^T\) is not a multiple of \((2,1)^T\).

### 3.2 Two independent vectors in the plane

The vectors

$$
\mathbf{v}_1=\begin{bmatrix}1\\0\end{bmatrix},
\qquad
\mathbf{v}_2=\begin{bmatrix}0\\1\end{bmatrix}
$$

span \(\mathbb{R}^2\), because every vector \((x,y)^T\) can be written as

$$
x\mathbf{v}_1+y\mathbf{v}_2
=
\begin{bmatrix}x\\y\end{bmatrix}.
$$

Two suitably independent directions are sufficient to span the plane.

### 3.3 Three vectors need not add a new direction

In \(\mathbb{R}^2\), consider

$$
\mathbf{v}_1=\begin{bmatrix}1\\0\end{bmatrix},
\quad
\mathbf{v}_2=\begin{bmatrix}0\\1\end{bmatrix},
\quad
\mathbf{v}_3=\begin{bmatrix}1\\1\end{bmatrix}.
$$

The third vector is already the sum of the first two. All three together still span only \(\mathbb{R}^2\); the third vector adds no new direction.

## 4. Subspaces

A **subspace** is a subset of a vector space that is itself a vector space under the same addition and scalar multiplication operations.

For a subset \(W\) of a real vector space, the subspace test is:

1. The zero vector belongs to \(W\).
2. If \(\mathbf{u},\mathbf{v}\in W\), then \(\mathbf{u}+\mathbf{v}\in W\).
3. If \(\mathbf{u}\in W\) and \(c\in\mathbb{R}\), then \(c\mathbf{u}\in W\).

These conditions ensure closure under linear combinations.

In \(\mathbb{R}^2\), the following are subspaces:

- the set containing only the zero vector;
- any line through the origin;
- the entire plane.

A line that does not pass through the origin is not a subspace. For example, the set of points satisfying \(y=2x+3\) does not contain the zero vector. It is an affine line, not a linear subspace.

This distinction matters in spatial modelling: a set of locations constrained to a line offset from an origin is not the same mathematical object as a vector subspace of displacements.

### Worked example 2 — test a proposed spatial constraint set

Consider vectors in \(\mathbb{R}^2\) satisfying \(y=2x\).

- The zero vector satisfies the equation.
- If \(y_1=2x_1\) and \(y_2=2x_2\), then \(y_1+y_2=2(x_1+x_2)\).
- If \(y=2x\), then \(cy=2(cx)\) for any scalar \(c\).

It is therefore a subspace: a line through the origin.

Now consider \(y=2x+3\). The zero vector does not satisfy the equation, so this set is not a subspace. It is a translated line.

## 5. Linear independence and dependence

A collection of vectors is **linearly independent** if the equation

$$
c_1\mathbf{v}_1+\cdots+c_k\mathbf{v}_k=\mathbf{0}
$$

has only the trivial solution

$$
c_1=c_2=\cdots=c_k=0.
$$

If there is a non-trivial set of coefficients that produces the zero vector, the vectors are **linearly dependent**.

An equivalent interpretation is useful: a collection is dependent if at least one vector can be written as a linear combination of the others.

### Worked example 3 — a dependent set

Let

$$
\mathbf{v}_1=\begin{bmatrix}1\\2\end{bmatrix},
\quad
\mathbf{v}_2=\begin{bmatrix}3\\1\end{bmatrix},
\quad
\mathbf{v}_3=\begin{bmatrix}4\\3\end{bmatrix}.
$$

Since \(\mathbf{v}_3=\mathbf{v}_1+\mathbf{v}_2\),

$$
\mathbf{v}_1+\mathbf{v}_2-\mathbf{v}_3=\mathbf{0}.
$$

The coefficients \((1,1,-1)\) are not all zero. The set is linearly dependent.

The third vector contributes no new direction to the span. It may still be useful as a measurement or a repeated observation in an application, but it is not an independent direction in the vector-space sense.

### Worked example 4 — independent directions

Let

$$
\mathbf{u}_1=\begin{bmatrix}1\\0\end{bmatrix},
\qquad
\mathbf{u}_2=\begin{bmatrix}1\\1\end{bmatrix}.
$$

Suppose

$$
a\mathbf{u}_1+b\mathbf{u}_2=\mathbf{0}.
$$

Then

$$
\begin{bmatrix}a+b\\b\end{bmatrix}
=
\begin{bmatrix}0\\0\end{bmatrix}.
$$

The second component gives \(b=0\), and the first then gives \(a=0\). Only the trivial solution exists, so the vectors are independent. They also span the plane.

## 6. Independence, uniqueness and redundancy

If a vector can be represented in more than one way using a collection of generators, the collection is dependent. To see why, suppose

$$
\mathbf{x}=\sum_i a_i\mathbf{v}_i
\qquad\text{and}\qquad
\mathbf{x}=\sum_i b_i\mathbf{v}_i.
$$

Subtracting gives

$$
\sum_i(a_i-b_i)\mathbf{v}_i=\mathbf{0}.
$$

If the vectors are independent, every coefficient difference must be zero, so \(a_i=b_i\) for all \(i\). The representation is unique.

If the vectors are dependent, a non-zero combination equals zero. That dependency can be added to or subtracted from a representation without changing the represented vector. The coefficients are therefore not unique.

This is the algebraic meaning of redundancy among generators. It is not automatically a bad thing. Redundant observations can improve precision or permit quality checks; redundant parameter directions can instead signal an unidentifiable model. The role of the vectors and the model must be distinguished.

## 7. Column vectors and the geometry of a matrix

A matrix can be understood through its columns. If

$$
A=
\begin{bmatrix}
|&|&&|\\
\mathbf{a}_1&\mathbf{a}_2&\cdots&\mathbf{a}_n\\
|&|&&|
\end{bmatrix},
$$

then

$$
A\mathbf{c}=c_1\mathbf{a}_1+\cdots+c_n\mathbf{a}_n.
$$

The set of all possible outputs as \(\mathbf{c}\) varies is the **column space** of \(A\), equivalently the span of its columns.

This gives a geometric interpretation of a matrix equation:

$$
A\mathbf{c}=\mathbf{b}
$$

has a solution precisely when \(\mathbf{b}\) belongs to the column space of \(A\). This statement does not yet tell us how many solutions exist. That requires rank and null-space analysis in Module 03.

### Worked example 5 — a target outside the span

Let

$$
A=\begin{bmatrix}1&2\\2&4\end{bmatrix}.
$$

Its second column is twice its first, so its column space is the line spanned by \((1,2)^T\).

The target

$$
\mathbf{b}=\begin{bmatrix}3\\6\end{bmatrix}
$$

is in the column space, because it is \(3\) times the first column.

But

$$
\mathbf{d}=\begin{bmatrix}3\\5\end{bmatrix}
$$

is not in the column space: no scalar multiple of \((1,2)^T\) gives both 3 and 5. Thus \(A\mathbf{c}=\mathbf{d}\) has no exact solution.

This is a geometric statement about the model's possible outputs. In an overdetermined measurement problem, an exact solution may not exist even when an approximate least-squares solution does. Least squares is treated later.

## 8. Spatial application: independent information in a simplified control model

Suppose a simplified local model uses two unknown horizontal displacement components, east and north:

$$
\mathbf{x}=\begin{bmatrix}e\\n\end{bmatrix}.
$$

Two idealised observation directions are represented by

$$
\mathbf{a}_1=\begin{bmatrix}1\\0\end{bmatrix},
\qquad
\mathbf{a}_2=\begin{bmatrix}0\\1\end{bmatrix}.
$$

Together they span the two-component parameter space. Each contributes a distinct direction.

Now suppose a third observation direction is

$$
\mathbf{a}_3=\begin{bmatrix}1\\1\end{bmatrix}.
$$

It is a combination of the first two. It does not increase the dimension of the span, although a real additional observation in that direction could still provide useful redundant evidence and improve an estimate under a stochastic model.

This distinction is fundamental in surveying and spatial estimation:

- **Parameter-direction independence** concerns whether columns of a design matrix introduce new directions in parameter space.
- **Observation redundancy** concerns the number and configuration of observations relative to unknowns and constraints.
- **Precision** concerns the uncertainty of estimates under a stochastic model.
- **Reliability** concerns the ability to detect errors and the influence of observations.

These are related but not interchangeable. Counting observations alone does not establish that all unknowns are identifiable or that the network is reliable.

The repository's [survey-adjustment learning path](../../learning-paths/measurement-science-and-survey-adjustment.md) and [covariance GLS implementation](../../implementations/python/covariance-gls/README.md) provide application contexts. The present module supplies only the vector-space language, not a complete network-design test.

## 9. What dependence does—and does not—tell us

Linear dependence establishes an algebraic relationship among vectors. Its practical interpretation depends on what the vectors represent.

- If they are coordinate directions, dependence means one direction is redundant for spanning the same space.
- If they are columns of a design matrix, dependence can indicate that some parameter combinations cannot be distinguished from the model equations alone.
- If they are observations, dependence in a simplified algebraic representation does not by itself determine their statistical covariance or usefulness.
- If they are raster variables, one exact linear combination is redundant in the represented data, but near-dependence, noise, scaling and nonlinear relationships require further analysis.

Do not infer that an additional observation is worthless merely because a direction is linearly dependent. Its stochastic contribution may still improve estimation or quality control.

## 10. Common errors and checks

- **Confusing a span with a list:** span contains every linear combination, not only the listed vectors.
- **Calling an offset line a subspace:** every subspace contains the zero vector.
- **Treating more vectors as more dimensions:** dependent vectors do not add a new direction.
- **Confusing independence with perpendicularity:** independent vectors need not be orthogonal.
- **Confusing observation count with identifiability:** geometry and model structure matter, not only the number of rows.
- **Equating dependence with useless data:** repeated or dependent observations may still improve precision or support checks.
- **Ignoring units and semantics:** vector-space operations require compatible quantities and a coherent component interpretation.
- **Assuming a numerical result establishes exact independence:** practical computation needs numerical-rank and conditioning analysis, covered in numerical analysis and later matrix methods.

A useful workflow is: define what each vector represents; write the combination equation; inspect whether any vector can be formed from the others; describe the span; and only then interpret the result in the application.

## 11. Exercises

### Exercise 1 — span of one vector

Describe the span of \((3,-2)^T\) in \(\mathbb{R}^2\). Is \((6,-4)^T\) in the span? Is \((3,2)^T\)?

**Worked guidance:** The span is the line through the origin in direction \((3,-2)^T\). The first target is twice the vector and is in the span. The second is not a scalar multiple, so it is not in the span.

### Exercise 2 — independence by coefficients

Determine whether \((1,2)^T\) and \((2,4)^T\) are independent.

**Worked guidance:** They are dependent because the second is twice the first. For example, \(2\mathbf{v}_1-\mathbf{v}_2=\mathbf{0}\) is a non-trivial dependence relation.

### Exercise 3 — independence without perpendicularity

Determine whether \((1,0)^T\) and \((1,1)^T\) are independent. Are they perpendicular?

**Worked guidance:** They are independent because \(a(1,0)^T+b(1,1)^T=(a+b,b)^T=0\) implies \(b=0\) and then \(a=0\). Their dot product is 1, so they are not perpendicular.

### Exercise 4 — subspace test

Is the set of all vectors \((x,y)^T\) satisfying \(y=-3x\) a subspace of \(\mathbb{R}^2\)? What about \(y=-3x+4\)?

**Worked guidance:** The first set is a line through the origin and is closed under addition and scalar multiplication, so it is a subspace. The second does not contain the zero vector and is not a subspace.

### Exercise 5 — matrix column space

Let

$$
A=\begin{bmatrix}1&2\\3&6\end{bmatrix}.
$$

1. Describe the column space.
2. Is \((4,12)^T\) in it?
3. Is \((4,10)^T\) in it?

**Worked guidance:** The second column is twice the first, so the column space is the line spanned by \((1,3)^T\). The first target is not a scalar multiple because 4 and 12 correspond to a factor of 4, so it is in the span. The second target is not on that line, so it is not in the span.

### Exercise 6 — simplified observation directions

A local two-parameter model has direction vectors \((1,0)^T\), \((0,1)^T\), and \((2,1)^T\).

1. Express the third vector as a combination of the first two.
2. Does it add a new dimension to their span?
3. Could a real observation in that direction still be useful?

**Worked guidance:** \((2,1)^T=2(1,0)^T+(0,1)^T\). It adds no new dimension; the first two already span the plane. A real observation can still provide additional redundant evidence and potentially improve precision or reliability, depending on its uncertainty and the observation model.

### Exercise 7 — exact representability

For the matrix in Worked example 5, determine whether \((5,10)^T\) and \((5,9)^T\) belong to the column space.

**Worked guidance:** The column space is the line \(y=2x\). The first target lies on it; the second does not. Therefore the first target can be represented exactly as a column combination and the second cannot.

## 12. Connections and limits

This module prepares the reader for:

- **Module 03 — Linear systems, elimination, rank and null spaces:** formalises the number of independent directions and the solution structure of \(A\mathbf{x}=\mathbf{b}\).
- **Module 04 — Bases, dimension and change of basis:** explains minimal independent generating sets and coordinate representation.
- **Module 05 — Inner products and projections:** introduces orthogonality and geometric approximation.
- **Module 06 — Least squares and constrained systems:** uses these structures to estimate parameters from imperfect or redundant observations.

It does not yet provide algorithms for computing numerical rank, a complete theory of parameter identifiability, covariance analysis, network reliability or a treatment of near-linear dependence. Those require later modules and the numerical-analysis and measurement-science foundations.

## References

- Massachusetts Institute of Technology, Department of Mathematics. [18.06 Linear Algebra — OpenCourseWare, Spring 2010](https://ocw.mit.edu/courses/18-06-linear-algebra-spring-2010/). Course scope includes linear combinations, vector spaces, column spaces and null spaces, linear independence and matrix equations.
- Strang, G. (2021). [Lecture Notes for Linear Algebra](https://www-math.mit.edu/~gs/LectureNotes/). MIT-hosted notes on linear combinations, subspaces, linear independence and matrix structure.

**Source note:** These references are linked for human study. The MIT course materials were checked for identity and topic coverage; individual lectures and notes have not been reviewed claim by claim. This module uses original spatial explanations and worked examples and does not reproduce source text, figures or exercises.

**Scope:** introductory finite-dimensional real vector spaces and subspaces, linear combinations, span and linear independence. Abstract vector spaces over other fields, bases and dimension in full generality, numerical rank, singular-value analysis and computational conditioning are deferred.
