# Linear systems, elimination, rank and null spaces

**Subject identity:** `SM-FND-002` — Linear algebra and matrix methods  
**Module:** 03  
**Status:** Initial public teaching resource; independent technical review and learner testing outstanding.

## 1. Why this module matters

Modules 01 and 02 introduced matrices, linear combinations, span and independence. This module brings those ideas together to answer four practical questions:

1. Does a system of linear equations have a solution?
2. If it has a solution, is that solution unique?
3. If it is not unique, which changes to the unknowns remain invisible to the equations?
4. How many independent constraints does the model actually contain?

These questions are central to survey control networks, coordinate estimation, parameter fitting, image geometry and many spatial models. They are also easy to answer incorrectly if we count equations without examining their independence.

The key objects are the **rank** and **null space** of a matrix. Gaussian elimination gives a systematic way to reveal them.

## 2. Linear systems in matrix form

A system of (m) linear equations in (n) unknowns can be written

$$
A\mathbf{x}=\mathbf{b},
$$

where:

- (A\) is the (m\times n\) **coefficient matrix**;
- (\mathbf{x}\) is an (n\times1\) vector of unknowns;
- (\mathbf{b}\) is an (m\times1\) vector of known right-hand-side values.

The (i\)-th row describes one equation. The (j\)-th column describes how the (j\)-th unknown contributes across all equations.

The matrix dimensions tell us how many equations and unknowns are represented, but not whether the equations are independent or whether the system is solvable.

### Worked example 1 — a small coordinate-offset model

Suppose unknown offsets (x) and (y) satisfy

$$
\begin{aligned}
x+y&=7,\\
x-y&=1.
\end{aligned}
$$

The matrix form is

$$
\begin{bmatrix}1&1\\1&-1\end{bmatrix}
\begin{bmatrix}x\\y\end{bmatrix}
=
\begin{bmatrix}7\\1\end{bmatrix}.
$$

Adding the equations gives (2x=8), so (x=4). Substitution gives (y=3). The unique solution is

$$
\mathbf{x}=\begin{bmatrix}4\\3\end{bmatrix}.
$$

This example illustrates exact algebra. A real spatial estimation problem may contain noisy observations and require an approximate solution; least squares is treated in Module 06.

## 3. Elementary row operations

A system can be transformed without changing its solution set by applying any of three elementary row operations:

1. Swap two rows.
2. Multiply a row by a non-zero scalar.
3. Add a scalar multiple of one row to another row.

These operations are applied to the **augmented matrix**

$$
[A\mid\mathbf{b}],
$$

which places the right-hand-side column beside the coefficient matrix.

Gaussian elimination uses these operations to create zeros below pivot entries. Continued elimination can produce **reduced row-echelon form (RREF)**, in which each pivot is 1 and is the only non-zero entry in its column.

A **pivot** is a leading non-zero entry in a row after elimination. Pivot columns identify independent columns of the original matrix. The number of pivots is the matrix rank.

### Worked example 2 — elimination to a unique solution

Start with

$$
\left[
\begin{array}{cc|c}
1&1&7\\
1&-1&1
\end{array}
\right].
$$

Replace row 2 by row 2 minus row 1:

$$
\left[
\begin{array}{cc|c}
1&1&7\\
0&-2&-6
\end{array}
\right].
$$

Divide row 2 by (-2), then subtract row 2 from row 1:

$$
\left[
\begin{array}{cc|c}
1&0&4\\
0&1&3
\end{array}
\right].
$$

The RREF directly gives (x=4) and (y=3).

Elimination is an exact mathematical procedure in this presentation. Computer implementations use finite-precision arithmetic, pivoting strategies and numerical tolerances; numerical stability and robust rank decisions belong to numerical analysis.

## 4. Rank: the number of independent directions

The **rank** of a matrix (A), written \(\operatorname{rank}(A)\), is the dimension of its column space. It is also the dimension of its row space and equals the number of pivots in an echelon form.

For an (m\times n) matrix,

$$
0\leq\operatorname{rank}(A)\leq\min(m,n).
$$

Rank measures the number of independent constraints or directions represented by the matrix. It does not simply count rows or columns.

- If some rows are linear combinations of other rows, they do not add independent equation constraints.
- If some columns are linear combinations of other columns, they do not add independent parameter directions.
- A matrix can have more equations than unknowns but still have deficient rank.
- A matrix can have fewer equations than unknowns and still have full row rank, while leaving some parameter combinations undetermined.

The row rank and column rank are always equal. This is a central theorem of finite-dimensional linear algebra.

### Worked example 3 — redundant equations

Consider

$$
A=\begin{bmatrix}
1&2\\
2&4\\
-1&-2
\end{bmatrix}.
$$

The second row is twice the first, and the third row is minus the first. There are three equations represented, but only one independent row direction. Therefore

$$
\operatorname{rank}(A)=1.
$$

The number of equations is three; the number of independent equations is one.

## 5. The null space: changes the equations cannot detect

The **null space** of (A) is the set of all vectors mapped to zero:

$$
\mathcal{N}(A)=\{\mathbf{x}:A\mathbf{x}=\mathbf{0}\}.
$$

It is a subspace of the parameter space. A non-zero vector in the null space represents a change to the unknowns that leaves every modelled equation unchanged.

If (A\mathbf{x}=\mathbf{b}) has one solution (\mathbf{x}_p), then every solution can be expressed as

$$
\mathbf{x}=\mathbf{x}_p+\mathbf{z},
\qquad \mathbf{z}\in\mathcal{N}(A).
$$

Why? Because

$$
A(\mathbf{x}_p+\mathbf{z})
=A\mathbf{x}_p+A\mathbf{z}
=\mathbf{b}+\mathbf{0}
=\mathbf{b}.
$$

Conversely, the difference between any two solutions belongs to the null space. Thus the null space describes precisely the freedom remaining among solutions.

### Worked example 4 — a one-dimensional null space

Let

$$
A=\begin{bmatrix}1&-1\\-1&1\end{bmatrix}.
$$

The homogeneous system (A\mathbf{x}=\mathbf{0}) gives

$$
x_1-x_2=0.
$$

So (x_1=x_2), and every null-space vector has the form

$$
\mathbf{z}=t\begin{bmatrix}1\\1\end{bmatrix},
\qquad t\in\mathbb{R}.
$$

The null space is the line spanned by ((1,1)^T). Adding the same amount to both unknowns leaves their difference unchanged.

This simple result becomes important in height-difference networks: relative observations can determine height differences without determining the common vertical origin.

## 6. The rank–nullity theorem

For a matrix (A\) with (n\) columns,

$$
\operatorname{rank}(A)+\operatorname{nullity}(A)=n,
$$

where **nullity** is the dimension of the null space.

The theorem partitions the parameter space into:

- directions that affect the equations, counted by rank;
- directions invisible to the equations, counted by nullity.

For the matrix in Worked example 4, there are two columns and rank one. Therefore nullity is one.

A system has a unique solution only when it is consistent and the null space contains only the zero vector. For an (m\times n\) matrix, this is equivalent to full column rank:

$$
\operatorname{rank}(A)=n.
$$

Full column rank requires (m\geq n\), but having at least as many equations as unknowns is not sufficient by itself.

## 7. Consistency and the augmented matrix

A system (A\mathbf{x}=\mathbf{b}) is **consistent** if at least one solution exists.

The system is consistent precisely when

$$
\operatorname{rank}(A)=\operatorname{rank}([A\mid\mathbf{b}]).
$$

If adding the right-hand-side column increases the rank, the system is inconsistent.

When the system is consistent:

- If rank equals the number of unknowns (n), the solution is unique.
- If rank is less than (n), there are infinitely many solutions over the real numbers.

This gives three basic cases:

| Condition | Solution structure |
|---|---|
| Inconsistent | No exact solution |
| Consistent and full column rank | Exactly one solution |
| Consistent and rank deficient | Infinitely many solutions |

### Worked example 5 — no exact solution

Consider

$$
\begin{aligned}
x-y&=2,\\
-x+y&=3.
\end{aligned}
$$

Adding the equations gives

$$
0=5,
$$

which is impossible. The coefficient rows are dependent, but the right-hand sides do not have the same dependency. The system is inconsistent.

This can occur in an exact mathematical model when constraints contradict one another. In measurement applications, observations usually contain noise, so a set of equations may not be exactly satisfiable. That does not mean the data are automatically erroneous; it means an approximate estimation model may be appropriate.

## 8. Spatial application — a relative-height network and its datum defect

Consider two unknown point heights (H_1) and (H_2), with two idealised observations of their height difference:

$$
H_2-H_1=2,
\qquad
H_1-H_2=-2.
$$

The system is

$$
\begin{bmatrix}
-1&1\\
1&-1
\end{bmatrix}
\begin{bmatrix}H_1\\H_2\end{bmatrix}
=
\begin{bmatrix}2\\-2\end{bmatrix}.
$$

The two rows are negatives of each other. The coefficient matrix has rank one, although there are two unknown heights.

Its null space is

$$
\mathcal{N}(A)
=
\operatorname{span}
\left\{
\begin{bmatrix}1\\1\end{bmatrix}
\right\}.
$$

One solution is ((H_1,H_2)=(0,2)), but so are ((10,12)), ((100,102)) and every common vertical shift of the pair. The relative difference is determined; the absolute vertical origin is not.

This is a simple **datum defect**: the observation equations do not define the common height datum. The network has one undetermined translation mode.

### 8.1 Add a datum constraint

Suppose an external datum fixes (H_1=100). Add that equation:

$$
\begin{bmatrix}
-1&1\\
1&-1\\
1&0
\end{bmatrix}
\begin{bmatrix}H_1\\H_2\end{bmatrix}
=
\begin{bmatrix}2\\-2\\100\end{bmatrix}.
$$

The augmented model now has rank two, equal to the number of unknowns. The unique solution is

$$
H_1=100,\qquad H_2=102.
$$

The datum constraint removes the common-translation freedom.

A datum can be introduced in different ways: fixing control parameters, imposing exact constraints, or using a suitable inner constraint for a free-network solution. These choices have different interpretations. An arbitrary fixed value is not automatically a physically valid or accurate external datum.

### 8.2 A necessary distinction

The two relative observations in this example are algebraically dependent. In a real network, repeated observations can still contribute precision, redundancy and error-detection capability. The algebraic rank of the design matrix does not by itself describe the stochastic quality or reliability of the observations.

The repository's [measurement-science and survey-adjustment learning path](../../learning-paths/measurement-science-and-survey-adjustment.md) and [constrained GLS implementation](../../implementations/python/covariance-gls/README.md) develop the estimation and stochastic aspects. This example isolates the datum structure only.

## 9. Homogeneous systems and non-homogeneous systems

A **homogeneous** system has zero right-hand side:

$$
A\mathbf{x}=\mathbf{0}.
$$

It always has at least the trivial solution \(\mathbf{x}=\mathbf{0}\). It has non-trivial solutions precisely when the nullity is positive, equivalently when rank is less than the number of columns.

A **non-homogeneous** system has a general right-hand side:

$$
A\mathbf{x}=\mathbf{b}.
$$

It may have no solution, one solution or infinitely many solutions.

The homogeneous system associated with a non-homogeneous system is useful because its null space describes the difference between any two solutions of the original system.

## 10. What rank does not tell you

Rank is an exact algebraic property. It does not, on its own, tell you:

- whether a real observation model is scientifically appropriate;
- whether the chosen datum is physically meaningful;
- whether measurements are accurate or precise;
- whether errors are independent or correlated;
- whether an estimated solution is stable under small perturbations;
- whether a numerical algorithm has correctly identified rank in floating-point arithmetic.

In computational work, matrices may be nearly rank deficient rather than exactly deficient. A numerical method must choose tolerances and account for scale and conditioning. Singular-value decomposition and numerical rank are introduced later; detailed numerical stability belongs to the numerical-analysis foundation.

## 11. Exercises

### Exercise 1 — write a matrix system

Write the equations (2x+y=5) and (x-y=1) as (A\mathbf{x}=\mathbf{b}). Solve the system.

**Worked guidance:** Use (A=\begin{bmatrix}2&1\\1&-1\end{bmatrix}), (\mathbf{x}=(x,y)^T), (\mathbf{b}=(5,1)^T). Adding the equations gives (3x=6), so (x=2), (y=1).

### Exercise 2 — rank by row dependence

Find the rank of

$$
A=\begin{bmatrix}1&2\\2&4\\3&6\end{bmatrix}.
$$

**Worked guidance:** Every row is a multiple of the first non-zero row. There is one pivot and the rank is one.

### Exercise 3 — find a null space

Find the null space of

$$
A=\begin{bmatrix}1&2\\2&4\end{bmatrix}.
$$

**Worked guidance:** The equation is (x_1+2x_2=0). Let (x_2=t); then (x_1=-2t). Thus the null space is the span of ((-2,1)^T), and its dimension is one.

### Exercise 4 — consistency

Determine whether the system (x+2y=3), (2x+4y=7) is consistent.

**Worked guidance:** Doubling the first equation would give (2x+4y=6), not 7. Elimination produces a contradiction, so the system is inconsistent.

### Exercise 5 — number of solutions

A consistent system has four unknowns and coefficient-matrix rank three. How many free parameters does its solution set have?

**Worked guidance:** By rank–nullity, nullity is (4-3=1). The solution set has one free parameter and infinitely many solutions.

### Exercise 6 — identify a datum defect

A model contains two unknown point heights and only their difference is observed. Explain why adding the same constant to both heights does not change the observation, and state the dimension of the null space.

**Worked guidance:** The observation depends on (H_2-H_1). Replacing both heights by (H_1+c) and (H_2+c) leaves the difference unchanged. The invisible common-shift direction is ((1,1)^T); the nullity is one.

### Exercise 7 — remove the defect

For the previous model, suppose (H_1=250.000\,\mathrm{m}) and (H_2-H_1=1.250\,\mathrm{m}). Find (H_2). Explain which equation supplies the datum.

**Worked guidance:** (H_2=251.250\,\mathrm{m}). The fixed (H_1) equation supplies the vertical datum; the difference observation supplies the relative height.

### Exercise 8 — distinguish algebra from measurement quality

A network has two observations whose design-matrix rows are identical. Does this necessarily mean one observation is useless?

**Worked guidance:** No. The rows add no new algebraic direction, but separate observations may still contribute information about precision, repeatability or blunder detection. Their stochastic relationship and measurement design must be examined.

## 12. Connections and limits

This module establishes the linear-system structure required for:

- **Module 04 — Bases, dimension and change of basis:** formalises independent coordinate descriptions and dimension.
- **Module 05 — Inner products, norms and projections:** develops orthogonality and geometric residuals.
- **Module 06 — Least squares and constrained systems:** handles inconsistent or overdetermined observation equations and exact constraints.
- **Module 09 — Matrix factorizations:** develops computational methods such as QR, Cholesky and SVD.

It also connects directly to the repository's free-network adjustment and constrained GLS examples. It does not implement a numerical rank estimator, solve a general large sparse network, select a professional datum, or assess uncertainty and reliability.

## References

- Massachusetts Institute of Technology, Department of Mathematics. [18.06 Linear Algebra — OpenCourseWare, Spring 2010](https://ocw.mit.edu/courses/18-06-linear-algebra-spring-2010/). Course scope includes elimination, matrix spaces, rank, null spaces and linear systems.
- Strang, G. (2021). [Lecture Notes for Linear Algebra](https://www-math.mit.edu/~gs/LectureNotes/). MIT-hosted notes on elimination, rank, null spaces and linear systems.

**Source note:** These references are linked for human study. The MIT course identity and topic coverage are recorded in the repository source register; individual lectures and notes have not been reviewed claim by claim. This module presents original explanations and synthetic spatial examples rather than reproducing course text, figures or exercises.

**Scope:** finite-dimensional real linear systems, elementary Gaussian elimination, exact rank, null spaces, consistency and datum-defect interpretation in a simple relative-height model. Numerical rank, conditioning, sparse solvers, least squares, stochastic adjustment and advanced constraint theory are deferred.
