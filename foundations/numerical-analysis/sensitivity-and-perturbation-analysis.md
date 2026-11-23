# Sensitivity and perturbation analysis

**Subject identity:** `SM-FND-016` — Numerical analysis and scientific computing  
**Module:** 02  
**Status:** Initial public teaching resource; independent numerical-analysis review and learner testing outstanding.

## 1. The question: how much can the answer move?

A spatial computation rarely receives perfect inputs. Coordinates have finite precision; sensor values are quantised; parameters are estimated; and intermediate calculations introduce rounding. Numerical analysis asks how these perturbations affect the computed result.

Sensitivity analysis is not simply a request to calculate more decimal places. It asks how the mathematical problem responds to changes in its inputs, which inputs matter most, and whether the output remains fit for the decision being made.

Keep three sources of variation distinct:

- **Input uncertainty:** uncertainty in the observed or supplied quantities, including measurement uncertainty.
- **Input representation and computational perturbation:** changes caused by finite precision, rounding, conversion or storage.
- **Model discrepancy:** differences between the mathematical model and the physical or social process it represents.

These can coexist, but they have different causes and remedies. A more precise floating-point type cannot remove sensor bias or an unsuitable model.

## 2. Perturbations and first-order approximation

Let a computation be represented by

\[
\mathbf{y}=f(\mathbf{x}),
\]

where \(\mathbf{x}\) is an input vector and \(\mathbf{y}\) is an output vector. Suppose the input is perturbed by \(\Delta\mathbf{x}\). The resulting output change is

\[
\Delta\mathbf{y}
=
f(\mathbf{x}+\Delta\mathbf{x})-f(\mathbf{x}).
\]

If \(f\) is differentiable near \(\mathbf{x}\), a first-order Taylor approximation gives

\[
\Delta\mathbf{y}
\approx
J_f(\mathbf{x})\,\Delta\mathbf{x},
\]

where \(J_f\) is the Jacobian matrix of first partial derivatives:

\[
J_f(\mathbf{x})
=
\begin{bmatrix}
\frac{\partial f_1}{\partial x_1} & \cdots & \frac{\partial f_1}{\partial x_n}\\
\vdots & \ddots & \vdots\\
\frac{\partial f_m}{\partial x_1} & \cdots & \frac{\partial f_m}{\partial x_n}
\end{bmatrix}.
\]

The approximation omits higher-order terms. It is most useful when perturbations are sufficiently small and the function is sufficiently smooth over the relevant neighbourhood. Near discontinuities, singularities, branch changes or geometric degeneracies, a first-order approximation may be misleading.

For a scalar output \(y=f(\mathbf{x})\), the first-order change is

\[
\Delta y
\approx
\nabla f(\mathbf{x})^\mathsf{T}\Delta\mathbf{x}.
\]

The gradient indicates the local direction of greatest increase, while its components show the local sensitivity to each input coordinate.

## 3. Normwise perturbation bounds

A derivative can be used to bound the size of a small output perturbation. For a chosen vector norm and its compatible matrix norm,

\[
\|\Delta\mathbf{y}\|
\lesssim
\|J_f(\mathbf{x})\|\,\|\Delta\mathbf{x}\|.
\]

The symbol \(\lesssim\) is intentional: this is a local first-order bound, not an exact global inequality for arbitrary perturbations.

A large Jacobian norm indicates that some input perturbations may be amplified. A small norm indicates limited absolute amplification in the chosen units and norms. The interpretation depends on scaling: metres and millimetres, or population counts and proportions, should not be mixed casually.

For a linear transformation \(\mathbf{y}=A\mathbf{x}\), the relation is exact:

\[
\Delta\mathbf{y}=A\Delta\mathbf{x},
\qquad
\|\Delta\mathbf{y}\|
\leq
\|A\|\,\|\Delta\mathbf{x}\|.
\]

This is one reason matrix norms are useful in numerical analysis.

## 4. Relative sensitivity and condition numbers

Absolute perturbation is not always the most meaningful measure. A relative condition number compares relative output change with relative input change.

For a differentiable scalar function \(y=f(x)\), where \(x\neq0\) and \(f(x)\neq0\), the local relative condition number is

\[
\kappa_f(x)
=
\left|
\frac{x f'(x)}{f(x)}
\right|.
\]

For a vector function, a common normwise local expression is

\[
\kappa_f(\mathbf{x})
=
\frac{\|J_f(\mathbf{x})\|\,\|\mathbf{x}\|}
{\|f(\mathbf{x})\|},
\]

when the denominator is non-zero and the chosen norms are appropriate. This expression describes worst-case local relative sensitivity under the selected normwise perturbation model.

Condition numbers depend on how the problem is parameterised, scaled and measured. A large value signals sensitivity; it does not prove that a particular algorithm is unstable. An algorithm can be stable while accurately solving a sensitive problem only to the limit allowed by the input perturbation.

Componentwise condition measures may be more informative when input elements have very different magnitudes or when some components are known more accurately than others. A single normwise number can conceal this structure.

## 5. Example: subtracting nearby coordinates

Consider the scalar function

\[
f(a,b)=a-b.
\]

Its absolute perturbation is

\[
\Delta f=\Delta a-\Delta b.
\]

The Jacobian is the row vector

\[
J_f=\begin{bmatrix}1&-1\end{bmatrix}.
\]

Thus, in the absolute sense, perturbations in either input pass directly into the difference. But relative to the small result \(a-b\), the problem may be highly sensitive.

A componentwise relative condition measure for this subtraction is

\[
\kappa_{\mathrm{sub}}
=
\frac{|a|+|b|}{|a-b|},
\]

provided \(a\neq b\). If \(a\) and \(b\) are large and nearly equal, the denominator is small and the condition number is large.

This is directly relevant to local displacements calculated from large projected coordinate values. A small difference may be sensitive to the precision of the stored coordinates even when the subtraction instruction itself is correctly rounded.

Using a local origin can reduce the magnitude of later intermediate values, but it cannot recover information already lost when the original coordinates were rounded or quantised. Preserve original coordinates and record the transformation used.

## 6. Example: distance between two points

For two planar points \(\mathbf{p}_1=(x_1,y_1)\) and \(\mathbf{p}_2=(x_2,y_2)\), their Euclidean distance is

\[
d=\|\mathbf{p}_2-\mathbf{p}_1\|_2.
\]

Suppose the point coordinates are perturbed by \(\Delta\mathbf{p}_1\) and \(\Delta\mathbf{p}_2\). The reverse triangle inequality gives

\[
|\hat d-d|
\leq
\|\Delta\mathbf{p}_2-\Delta\mathbf{p}_1\|_2
\leq
\|\Delta\mathbf{p}_1\|_2+\|\Delta\mathbf{p}_2\|_2,
\]

where \(\hat d\) is the distance computed from the perturbed points.

This is an absolute bound. It remains meaningful when the points coincide. A relative error bound based on division by \(d\), however, becomes uninformative as \(d\) approaches zero. At exact coincidence, the distance function is not differentiable with respect to the displacement vector in the ordinary gradient sense.

The practical lesson is that very short baselines can have large relative sensitivity even when their absolute coordinate perturbations are modest. Whether this matters depends on the intended use, coordinate precision and measurement model.

This analysis concerns planar Euclidean distance. It does not establish that grid distance is an acceptable substitute for ground distance or ellipsoidal geodesic distance.

## 7. Example: affine coordinate transformation

Consider an affine transformation

\[
\mathbf{y}=A\mathbf{x}+\mathbf{t},
\]

where \(A\) is a matrix and \(\mathbf{t}\) is a translation vector. If the input is perturbed but the transformation parameters are fixed,

\[
\Delta\mathbf{y}=A\Delta\mathbf{x}.
\]

Translation does not change the perturbation difference. The linear part controls how perturbations are stretched, compressed, rotated or sheared.

For a pure planar rotation matrix \(R\),

\[
R^\mathsf{T}R=I,
\qquad
\|R\mathbf{v}\|_2=\|\mathbf{v}\|_2.
\]

A rotation therefore preserves Euclidean perturbation magnitude. A general affine transformation need not. If the transformation is invertible, its condition number in the 2-norm,

\[
\kappa_2(A)=\|A\|_2\|A^{-1}\|_2,
\]

describes the ratio between its largest and smallest singular-value scales. A large value indicates that the transformation strongly distorts some directions relative to others.

This is an algebraic sensitivity statement. A real coordinate operation also requires correct reference frames, axis order, units, datum operation and projection choice.

## 8. Sensitivity when transformation parameters are uncertain

If both the input and transformation parameters vary, include them in the input vector rather than treating the transformation as fixed.

For example, let

\[
\mathbf{y}=f(\mathbf{x},\boldsymbol{\theta}),
\]

where \(\boldsymbol{\theta}\) contains parameters such as rotation, scale, translation or calibration coefficients. To first order,

\[
\Delta\mathbf{y}
\approx
J_x\Delta\mathbf{x}
+
J_\theta\Delta\boldsymbol{\theta}.
\]

This shows why parameter uncertainty can dominate output sensitivity even when coordinates are stored at high precision. A numerically exact evaluation of a poorly determined transformation does not create a well-determined result.

When the input perturbations are random with covariance matrix \(\Sigma_x\), a first-order covariance approximation is

\[
\Sigma_y
\approx
J_f\Sigma_xJ_f^\mathsf{T}.
\]

This formula is widely used in uncertainty propagation. It requires a probabilistic interpretation of \(\Sigma_x\), an appropriate local linearisation and a clearly specified model. It is not a generic formula for floating-point rounding error, and it does not capture all nonlinear or non-Gaussian effects.

For measurement uncertainty and covariance semantics, see the repository's measurement-science and covariance foundations. Here, the key point is that the same derivative machinery can describe local sensitivity, while the meaning assigned to the perturbations must be stated separately.

## 9. Scaling and nondimensionalisation

Poor scaling can make a numerically manageable problem appear difficult or cause an algorithm to treat some variables as negligible. For example, a model may combine easting in metres, angles in radians, and population counts in thousands. The raw magnitudes do not directly express their importance.

Scaling can improve numerical behaviour by expressing variables in comparable ranges or by choosing units appropriate to the problem. Nondimensionalisation can expose the governing ratios and remove arbitrary unit choices.

However, scaling must preserve the interpretation of the model. Record the scale factors, apply inverse transformations correctly to outputs, and distinguish numerical scaling from scientific weighting. Rescaling a variable does not make its uncertainty smaller in physical terms.

## 10. A practical sensitivity workflow

For a spatial computation:

1. Identify the input quantities, their units, numeric representations and meaningful ranges.
2. Identify outputs and the decision or tolerance they must support.
3. Write the mathematical mapping from inputs to outputs.
4. Determine whether the mapping is differentiable over the operating region.
5. Use derivatives, Jacobians or perturbation bounds where a local analysis is appropriate.
6. Examine condition numbers or componentwise sensitivity for sensitive operations.
7. Test realistic perturbations, including boundary cases and near-degenerate geometries.
8. Separate input uncertainty, numerical representation effects and model discrepancy.
9. Record assumptions, norms, scaling, units and the range over which conclusions apply.
10. Compare sensitivity results with the application's acceptance criteria.

A sensitivity study should use perturbations grounded in the actual data pipeline. Arbitrary perturbation sizes can produce dramatic but irrelevant results or conceal important effects.

## 11. Exercises

### Exercise 1 — Local derivative

For \(f(x)=x^2\), derive the first-order approximation to \(\Delta f\). Explain why the relative condition number changes with the function's domain.

### Exercise 2 — Coordinate subtraction

For \(a=1\,000\,000.00\) and \(b=1\,000\,000.01\), calculate \(\kappa_{\mathrm{sub}}\). Explain what the value says about relative sensitivity and what it does not say about the actual accuracy of a stored coordinate pair.

### Exercise 3 — Distance bound

Two point coordinates each have a possible Euclidean perturbation of at most \(0.01\ \mathrm{m}\). Use the reverse triangle inequality to bound the absolute distance change. Explain why this does not give a useful universal relative bound for all baselines.

### Exercise 4 — Rotation and scaling

Show that a pure rotation preserves Euclidean perturbation magnitude. Explain why a non-uniform scale can change it.

### Exercise 5 — Covariance propagation

Explain the distinction between propagating a deterministic bounded perturbation and propagating a random input covariance matrix. State the assumptions behind the first-order covariance approximation.

## 12. Answers and discussion

1. Since \(f'(x)=2x\), \(\Delta f\approx2x\Delta x\). For non-zero \(x\), the relative condition number is \(|x(2x)/x^2|=2\). At \(x=0\), the relative expression is undefined even though the function itself is locally well behaved in an absolute sense.
2. The numerator is \(2\,000\,000.01\) and the denominator is \(0.01\), giving approximately \(2.0\times10^8\). The subtraction is highly sensitive in relative terms. This does not reveal the precision, provenance or actual perturbation of the stored inputs.
3. The absolute distance change is no greater than \(0.01+0.01=0.02\ \mathrm{m}\). Dividing by the original distance makes a relative bound grow without limit as the baseline approaches zero.
4. A rotation matrix is orthogonal, so \(R^\mathsf{T}R=I\) and \(\|R\Delta\mathbf{x}\|_2^2=\Delta\mathbf{x}^\mathsf{T}R^\mathsf{T}R\Delta\mathbf{x}=\|\Delta\mathbf{x}\|_2^2\). A non-uniform scale stretches different directions by different factors.
5. A deterministic bound limits possible changes without assigning probabilities. Covariance propagation describes second moments of random variables and requires a probabilistic input model. The first-order formula assumes a sufficiently accurate local linearisation and finite input covariance.

## 13. Connections to other Spatial Methods resources

- [Linear algebra and matrix methods](../linear-algebra/README.md) explains matrix transformations, norms, covariance matrices and least squares.
- [Measurement science and field verification](../measurement-science/measurement-principles-and-field-verification.md) provides the measurement model, uncertainty and traceability context.
- [Coordinate transformation and CRS axis order](../../algorithms/geodesy/crs-transformation.md) illustrates why numerical sensitivity must be considered alongside reference-system correctness.
- [Ellipsoidal geodesic operations](../../algorithms/geodesy/ellipsoidal-geodesic-operations.md) provides a domain-specific context for distance computation.
- [Precision models and snap rounding](../../algorithms/geometry/precision-models.md) addresses finite precision and geometric decision stability.
- [Covariance GLS implementation](../../implementations/python/covariance-gls/README.md) connects matrix conditioning and covariance-aware estimation to a computational workflow.

## 14. Further reading

- Nicholas J. Higham, *Accuracy and Stability of Numerical Algorithms*, 2nd edition, SIAM, 2002. DOI: [10.1137/1.9780898718027](https://doi.org/10.1137/1.9780898718027).
- James W. Demmel, *Applied Numerical Linear Algebra*, SIAM, 1997. DOI: [10.1137/1.9781611971446](https://doi.org/10.1137/1.9781611971446).
- Charles F. Van Loan, *Introduction to Scientific Computing: A Matrix-Vector Approach Using MATLAB*, 2nd edition, Prentice Hall, 2000.

References are starting points for review, not a claim that every statement has been independently checked against the full texts.
