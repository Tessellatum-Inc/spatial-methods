# Joint distributions, covariance and dependence

**Subject:** \`SM-FND-004\` — Probability and statistical inference  
**Module:** 03  
**Status:** Initial researched teaching resource; independent technical review and learner testing pending.

## 1. Why joint behaviour matters

Spatial observations rarely exist in isolation. A survey point has east and north coordinate errors; a terrain cell may have elevation and slope; a satellite pixel may have several spectral bands; a location may have both demand and accessibility attributes.

A **joint probability distribution** describes possible values of two or more random variables together. Individual distributions are its marginal distributions. A conditional distribution describes one component given information about another. Knowing every marginal distribution does not, in general, determine the joint distribution: dependence structure is additional information.

Let \(\mathbf{X}=[X_1,\ldots,X_p]^T\) be a random vector. Its joint distribution is the probability model for its combined outcomes.

## 2. Joint, marginal and conditional distributions

For two discrete variables,

\[
p_{X,Y}(x,y)=P(X=x,Y=y),
\]

with non-negative entries summing to one over all possible pairs. For continuous variables with joint density \(f_{X,Y}\), probabilities are integrals over regions:

\[
P((X,Y)\in A)=\iint_A f_{X,Y}(x,y)\,dx\,dy.
\]

A density value is not itself a point probability.

For discrete variables, marginalisation gives

\[
p_X(x)=\sum_y p_{X,Y}(x,y);
\]

for continuous variables,

\[
f_X(x)=\int_{-\infty}^{\infty}f_{X,Y}(x,y)\,dy.
\]

Marginalisation removes the other variable from the description; it does not imply independence.

For discrete variables with \(P(Y=y)>0\),

\[
P(X=x\mid Y=y)=\frac{P(X=x,Y=y)}{P(Y=y)}.
\]

For continuous variables where the marginal density is positive,

\[
f_{X\mid Y}(x\mid y)=\frac{f_{X,Y}(x,y)}{f_Y(y)}.
\]

Independence means the joint distribution factors into the product of its marginals. For discrete variables, \(p_{X,Y}(x,y)=p_X(x)p_Y(y)\); for continuous variables, \(f_{X,Y}(x,y)=f_X(x)f_Y(y)\) over the relevant support. Independence is a property of the joint distribution, not something established merely because a scatterplot looks diffuse or a sample correlation is small.

## 3. Covariance and correlation

For variables with finite second moments,

\[
\operatorname{Cov}(X,Y)
=E[(X-\mu_X)(Y-\mu_Y)]
=E[XY]-E[X]E[Y].
\]

Positive covariance indicates positive linear co-variation; negative covariance indicates negative linear co-variation; zero covariance indicates no linear co-variation captured by this second-moment measure. Covariance has product units. If \(X\) is measured in metres and \(Y\) in seconds, covariance has units metre-seconds.

For constants \(a,b,c,d\),

\[
\operatorname{Cov}(aX+b,cY+d)=ac\operatorname{Cov}(X,Y).
\]

The population correlation is

\[
\rho_{XY}=\frac{\operatorname{Cov}(X,Y)}{\sigma_X\sigma_Y},
\]

when both standard deviations are finite and non-zero. It is dimensionless and lies between -1 and 1. Zero correlation means zero linear correlation, not necessarily independence. Correlation near zero does not necessarily imply weak nonlinear dependence. A high correlation does not prove causation: common drivers, spatial trends, shared measurement conditions and selection effects can produce association.

Given paired observations \((x_i,y_i)\), the usual unbiased sample covariance in an ordinary unweighted sample is

\[
s_{XY}=\frac{1}{n-1}\sum_{i=1}^{n}(x_i-\bar{x})(y_i-\bar{y}),
\]

and the sample correlation is \(r_{XY}=s_{XY}/(s_Xs_Y)\). These are sample statistics, not the unknown population parameters. Complex sampling, weights, repeated observations and spatial dependence require appropriate methods.

## 4. The covariance matrix

For a random vector \(\mathbf{X}\) with mean \(\boldsymbol{\mu}=E[\mathbf{X}]\),

\[
\mathbf{\Sigma}
=E[(\mathbf{X}-\boldsymbol{\mu})(\mathbf{X}-\boldsymbol{\mu})^T].
\]

For three variables,

\[
\mathbf{\Sigma}=
\begin{bmatrix}
\operatorname{Var}(X_1)&\operatorname{Cov}(X_1,X_2)&\operatorname{Cov}(X_1,X_3)\\
\operatorname{Cov}(X_2,X_1)&\operatorname{Var}(X_2)&\operatorname{Cov}(X_2,X_3)\\
\operatorname{Cov}(X_3,X_1)&\operatorname{Cov}(X_3,X_2)&\operatorname{Var}(X_3)
\end{bmatrix}.
\]

The diagonal contains variances; off-diagonal entries contain covariances. A covariance matrix is symmetric and positive semidefinite because

\[
\mathbf{a}^T\mathbf{\Sigma}\mathbf{a}
=\operatorname{Var}(\mathbf{a}^T\mathbf{X})\geq0
\]

for every vector \(\mathbf{a}\). Thus its eigenvalues are non-negative, subject to numerical tolerance. A matrix with materially negative eigenvalues cannot be a valid covariance matrix.

A positive-definite covariance matrix is invertible and has strictly positive eigenvalues. A positive-semidefinite matrix may be singular, for example when one variable is an exact linear combination of others. Ordinary Cholesky factorisation requires positive definiteness, not merely positive semidefiniteness.

The correlation matrix standardises each covariance by the product of the relevant standard deviations. It has ones on the diagonal and allows comparison across different units, but it does not preserve physical scales.

## 5. Linear transformations

For a deterministic matrix \(\mathbf{A}\), constant vector \(\mathbf{b}\), and

\[
\mathbf{Y}=\mathbf{A}\mathbf{X}+\mathbf{b},
\]

\[
E[\mathbf{Y}]=\mathbf{A}E[\mathbf{X}]+\mathbf{b},
\qquad
\operatorname{Cov}(\mathbf{Y})=\mathbf{A}\mathbf{\Sigma}\mathbf{A}^T.
\]

For a scalar combination \(Z=\mathbf{a}^T\mathbf{X}\),

\[
\operatorname{Var}(Z)=\mathbf{a}^T\mathbf{\Sigma}\mathbf{a}.
\]

These relationships are fundamental in coordinate transformations, error propagation, linear estimation and sensor fusion. Ignoring off-diagonal covariance terms can overstate or understate the resulting uncertainty. A transformation changes the representation and scale of uncertainty; it does not automatically reduce uncertainty or improve measurement quality.

## 6. Multivariate normal distribution

A random vector is multivariate normal if every linear combination of its components has a univariate normal distribution. Write

\[
\mathbf{X}\sim N_p(\boldsymbol{\mu},\mathbf{\Sigma}),
\]

where \(\boldsymbol{\mu}\) is the mean vector and \(\mathbf{\Sigma}\) the covariance matrix. When \(\mathbf{\Sigma}\) is positive definite, the density is

\[
f(\mathbf{x})=
\frac{1}{(2\pi)^{p/2}|\mathbf{\Sigma}|^{1/2}}
\exp\left[-\frac12(\mathbf{x}-\boldsymbol{\mu})^T
\mathbf{\Sigma}^{-1}(\mathbf{x}-\boldsymbol{\mu})\right].
\]

The covariance matrix controls the orientation and scale of the joint distribution. In two dimensions, equal-density contours are ellipses when the covariance matrix is positive definite.

For a multivariate normal vector, zero covariance between components implies independence. This equivalence is special to the joint normal model; it is not true for arbitrary distributions.

For a jointly normal pair \((X,Y)\),

\[
Y\mid X=x\sim N\left(
\mu_Y+\frac{\sigma_{XY}}{\sigma_X^2}(x-\mu_X),
\ \sigma_Y^2-\frac{\sigma_{XY}^2}{\sigma_X^2}
\right).
\]

The conditional mean shifts with the observed value of \(X\). This result is model-specific, not a universal rule for every conditional distribution.

## 7. Worked spatial example: two coordinate-error components

Suppose a hypothetical survey point has east and north error components \(E\) and \(N\), in metres. Assume for teaching purposes

\[
\begin{bmatrix}E\\N\end{bmatrix}
\sim N_2\left(
\begin{bmatrix}0\\0\end{bmatrix},
\begin{bmatrix}4&1.2\\1.2&9\end{bmatrix}
\right).
\]

This is synthetic, not a survey result. The marginal standard deviations are \(\sigma_E=2\) m and \(\sigma_N=3\) m. Correlation is

\[
\rho_{EN}=\frac{1.2}{2\times3}=0.2.
\]

For \(D=E-N\),

\[
\begin{aligned}
\operatorname{Var}(D)
&=\operatorname{Var}(E)+\operatorname{Var}(N)-2\operatorname{Cov}(E,N)\\
&=4+9-2(1.2)=10.6\text{ m}^2.
\end{aligned}
\]

If covariance were incorrectly set to zero, the result would be \(13\text{ m}^2\). The dependence term changes the uncertainty of the combination.

Because the pair is assumed jointly normal,

\[
N\mid E=e\sim N(0.3e,\ 8.64).
\]

For \(e=2\) m, conditional mean is 0.6 m and conditional variance is 8.64 m². The covariance matrix is positive definite: determinant \(4(9)-1.2^2=34.56>0\), with positive diagonal entries.

A real coordinate uncertainty statement must define coordinate frame, point and observation model, reference quality, component order, units, covariance estimation method and coverage convention. This synthetic matrix establishes none of those for a real survey.

## 8. Spatial dependence: related, not identical

For a spatial random field \(Z(\mathbf{s})\), covariance may depend on location:

\[
C(\mathbf{s}_1,\mathbf{s}_2)
=\operatorname{Cov}(Z(\mathbf{s}_1),Z(\mathbf{s}_2)).
\]

Under second-order stationarity it may depend only on separation \(\mathbf{h}=\mathbf{s}_2-\mathbf{s}_1\). Under isotropy it may depend only on distance \(\|\mathbf{h}\|\). These are assumptions to investigate, not properties guaranteed by a map.

Distinguish:

- **Cross-variable covariance:** association between different variables, possibly at the same site.
- **Spatial covariance:** association between values of a process at different locations.
- **Temporal covariance:** association between values at different times.
- **Spatiotemporal covariance:** association depending on spatial and temporal separation.

Sample correlation between nearby cells can be affected by spatial autocorrelation, unequal sampling, shared trends and boundary effects. Independent-observation formulas may then give misleading uncertainty. Spatial covariance functions and variograms receive deeper treatment in spatial statistics; this module establishes the probability and matrix language they require.

## 9. Common errors

- Assuming marginal distributions determine a joint distribution.
- Treating zero correlation as proof of independence.
- Treating correlation as evidence of causation.
- Comparing covariance magnitudes without considering units and scale.
- Omitting covariance terms when propagating uncertainty.
- Accepting a covariance matrix with materially negative eigenvalues.
- Treating sample covariance as population covariance.
- Assuming every measurement vector is multivariate normal.
- Confusing cross-variable covariance with spatial covariance across locations.
- Ignoring spatial or temporal dependence in independent-sample methods.
- Reporting coordinate standard deviations without covariance when joint error matters.

## 10. Exercises

**A — Covariance and correlation.** Suppose standard deviations are 2 and 5 units, and covariance is -4 unit-squared. Calculate correlation and interpret its sign. Does this establish independence?

*Worked guidance:* \(\rho=-4/(2\times5)=-0.4\). This is a negative linear association; it does not establish independence.

**B — Linear combination.** Let \(\operatorname{Var}(X)=9\), \(\operatorname{Var}(Y)=16\) and \(\operatorname{Cov}(X,Y)=3\). Find \(\operatorname{Var}(2X-Y)\).

*Worked guidance:* \(4(9)+16-4(3)=40\).

**C — Covariance matrix validity.** Is \(\begin{bmatrix}1&2\\2&1\end{bmatrix}\) a valid covariance matrix?

*Worked guidance:* eigenvalues are 3 and -1. The negative eigenvalue means it is not positive semidefinite and cannot be a valid covariance matrix.

**D — Spatial interpretation.** A team reports correlation 0.85 between building density and road density across grid cells. Give at least four reasons this does not prove that increasing roads causes building density to increase.

*Worked guidance:* common population or urbanisation drivers, spatial trends, grid resolution and zoning, temporal mismatch, spatial autocorrelation, study-area selection, aggregation effects and reciprocal relationships.

## 11. Connections and next steps

- Previous: [Random variables, distributions and probability models](random-variables-and-distributions.md).
- [Linear algebra and matrix methods](../linear-algebra/README.md): matrix operations, quadratic forms, eigenvalues and factorisation.
- [Measurement principles and field verification](../measurement-science/measurement-principles-and-field-verification.md): uncertainty budgets and measurement covariance.
- Next: sampling designs and sampling distributions, including what sample covariance estimates and how dependence affects inference.
- Later spatial-statistics connections: covariance functions, variograms, random fields, multivariate geostatistics and spatial cross-validation.

## References

- NIST/SEMATECH. *e-Handbook of Statistical Methods*, Section 6.5.4.2, “The Multivariate Normal Distribution.” [NIST reference](https://www.itl.nist.gov/div898/handbook/pmc/section5/pmc542.htm). Used for the multivariate normal density and covariance-matrix representation.
- Joint Committee for Guides in Metrology (JCGM). (2008). *Evaluation of measurement data — Guide to the expression of uncertainty in measurement*, JCGM 100:2008, Annex C on covariance matrices and correlation coefficients. [BIPM JCGM publications](https://www.bipm.org/en/committees/jc/jcgm/publications). Used for metrological interpretation of covariance and correlation.
- Diez, D. M., Çetinkaya-Rundel, M., and Barr, C. D. (2019). *OpenIntro Statistics*, 4th ed. [OpenIntro textbook](https://openintro.org/book/os/). Used for introductory probability context.

The mathematical development and coordinate-error example are original synthesis and synthetic illustration. No field observations are used.

## Evidence and review boundary

The NIST handbook section was inspected for the multivariate normal density and its mean-vector/covariance-matrix parameterisation. JCGM 100:2008 is registered in the source catalogue; Annex C defines covariance matrices and correlation coefficients in a measurement-uncertainty context. This module does not establish that a particular spatial dataset, survey network or measurement error is multivariate normal. Model choice, covariance estimation, reference-frame handling and coverage interpretation require application-specific evidence.
