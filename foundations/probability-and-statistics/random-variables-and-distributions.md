# Random variables, distributions and probability models

**Subject:** \`SM-FND-004\` — Probability and statistical inference  
**Module:** 02  
**Status:** Initial researched teaching resource; independent technical review and learner testing pending.

## 1. From events to numerical random quantities

A random variable maps outcomes in a sample space to real numbers:

\[
X:\Omega\rightarrow\mathbb{R}.
\]

The variable \(X\) is the numerical quantity; \(x\) denotes a possible value. Examples in spatial work include the number of buildings in a selected cell, a signed survey residual, travel time for a selected trip, or the number of detected events in a defined observation window.

Define the variable before choosing a model. A count per cell, count per square kilometre and count per administrative area are different variables. A variable may be random because of a sampling design, an underlying stochastic process, measurement uncertainty, or a model for an unknown quantity. State which interpretation applies.

## 2. Discrete and continuous variables

A **discrete** variable takes values from a finite or countably infinite set: counts, category indicators, or numbers of detected objects. A **continuous** variable takes values on a continuum: distance, time, height or a measurement residual.

This is a mathematical distinction, not merely a data-storage distinction. Coordinates stored to millimetres do not thereby become intrinsically discrete random variables. A count remains discrete even if software stores it as a floating-point value.

## 3. Probability functions

### Probability mass function

For a discrete variable, the probability mass function is

\[
p_X(x)=P(X=x),\quad p_X(x)\geq0,\quad\sum_xp_X(x)=1.
\]

Probabilities over a set of values are sums of the corresponding masses.

### Probability density function

For a continuous variable with density \(f_X(x)\),

\[
f_X(x)\geq0,\quad \int_{-\infty}^{\infty}f_X(x)\,dx=1,
\]

and

\[
P(a\leq X\leq b)=\int_a^b f_X(x)\,dx.
\]

A density height is not a probability and can exceed one. For a continuous variable, \(P(X=x)=0\) at any single exact value, while an interval may have positive probability.

### Cumulative distribution function

For discrete, continuous and mixed variables,

\[
F_X(x)=P(X\leq x).
\]

It is non-decreasing and right-continuous. For \(a<b\),

\[
P(a<X\leq b)=F_X(b)-F_X(a),\qquad P(X>x)=1-F_X(x).
\]

For discrete variables, endpoint conventions matter because an individual value can have positive probability.

### Model distribution versus observed distribution

A theoretical distribution specifies possible values and their probabilities under a model. An empirical distribution summarises observed data, for example using relative frequencies or an empirical CDF. A histogram is not automatically a probability model: it depends on sample size, binning, sampling design, measurement and dependence. A theoretical model must be assessed against evidence rather than inferred from a histogram's appearance alone.

## 4. Expectation, variance and transformations

For a discrete variable,

\[
E[X]=\sum_x xp_X(x);
\]

for a continuous variable,

\[
E[X]=\int_{-\infty}^{\infty}xf_X(x)\,dx,
\]

when the expectation exists. Expectation is the probability-weighted mean implied by the model; it need not be a value the variable can attain.

Variance is

\[
\operatorname{Var}(X)=E[(X-\mu)^2]=E[X^2]-E[X]^2,
\]

where \(\mu=E[X]\). Standard deviation is \(\sigma_X=\sqrt{\operatorname{Var}(X)}\). Variance has squared units; standard deviation has the units of the variable.

For \(Y=a+bX\),

\[
E[Y]=a+bE[X],\qquad \operatorname{Var}(Y)=b^2\operatorname{Var}(X).
\]

For two variables,

\[
E[X+Y]=E[X]+E[Y]
\]

when expectations exist, but

\[
\operatorname{Var}(X+Y)=\operatorname{Var}(X)+\operatorname{Var}(Y)+2\operatorname{Cov}(X,Y).
\]

Do not discard the covariance term without justification. Independence implies zero covariance when second moments exist; zero covariance does not generally imply independence.

## 5. Common probability models

A named distribution has a support, parameters and assumptions. Select it from the data-generating or sampling mechanism, not from software convenience.

### Bernoulli

For one binary outcome,

\[
X\sim\operatorname{Bernoulli}(p),\quad P(X=1)=p,\quad P(X=0)=1-p.
\]

Here \(E[X]=p\) and \(\operatorname{Var}(X)=p(1-p)\). A spatial example is whether a building selected under a defined design is exposed under a stated reference definition. The probability refers to that population and selection mechanism, not automatically to land-area proportion.

### Binomial

For \(n\) independent Bernoulli trials with common success probability \(p\),

\[
X\sim\operatorname{Binomial}(n,p),\quad
P(X=k)=\binom nkp^k(1-p)^{n-k}.
\]

Its mean is \(np\), variance \(np(1-p)\). It may model exposed buildings among sampled buildings only if common probability and independence are defensible. Spatial clustering, unequal selection probabilities, repeated observations or complex sampling may invalidate the simple model. A raster count is not automatically binomial.

### Poisson

For a non-negative integer count,

\[
X\sim\operatorname{Poisson}(\lambda),\quad
P(X=k)=e^{-\lambda}\frac{\lambda^k}{k!},\quad k=0,1,\ldots
\]

Its mean and variance are both \(\lambda\). In a homogeneous Poisson process with constant intensity \(\rho\) per unit area, expected count in area \(A\) is \(\lambda=\rho A\). A Poisson count model alone does not establish spatial homogeneity, spatial randomness or independence between regions.

### Normal

For \(X\sim N(\mu,\sigma^2)\), the density is

\[
f_X(x)=\frac{1}{\sigma\sqrt{2\pi}}
\exp\left[-\frac{(x-\mu)^2}{2\sigma^2}\right].
\]

The standardised variable \(Z=(X-\mu)/\sigma\) follows \(N(0,1)\). The normal model is symmetric and continuous; it can be useful for measurement errors, aggregated quantities and sampling distributions under appropriate conditions. It is not a universal model for coordinates, distances, counts or residuals.

A one-dimensional signed residual may be approximated by a normal model after examining bias, reference quality, heterogeneity and dependence. Two-dimensional positional error requires a joint model for both components, including covariance; assuming independent components without checking is not justified.

### Other useful distributions

- **Geometric:** number of independent Bernoulli trials up to and including the first success; assumes constant success probability.
- **Negative binomial:** failures before a specified number of successes, or certain overdispersed count models; state the parameterisation.
- **Uniform:** constant density over a specified interval; this is a strong assumption, not a default for unknown position.
- **Exponential:** waiting times in a constant-rate Poisson process; its memoryless property is substantive.

Counts, waiting times, binary outcomes and signed residuals have different supports and mechanisms; their distributions are not interchangeable.

## 6. Worked spatial examples

All values below are **synthetic teaching assumptions**, not estimates from a real region.

### A. Binary exposure

A selected building has modelled exposure probability \(p=0.30\). Let \(X=1\) if exposed and \(0\) otherwise:

\[
E[X]=0.30,\qquad \operatorname{Var}(X)=0.30(0.70)=0.21.
\]

The standard deviation is approximately \(0.4583\). The expected value is a probability, not a fraction of one building.

### B. Events in a fixed cell and time window

Suppose service requests in one defined 1 km² cell during one hour follow a Poisson model with \(\lambda=2.5\):

\[
P(X=0)=e^{-2.5}\approx0.0821,
\]

\[
P(X\leq2)=e^{-2.5}\left(1+2.5+\frac{2.5^2}{2}\right)\approx0.5438.
\]

The model mean and variance are 2.5; standard deviation is \(\sqrt{2.5}\approx1.581\). If requests cluster near a hub, arrive in bursts or have time-varying intensity, the homogeneous Poisson model may be inadequate.

### C. Signed measurement residual

Suppose a hypothetical residual component is modelled as \(X\sim N(0,2^2)\) metres. An observed residual of 3 m has standardised value

\[
z=\frac{3-0}{2}=1.5.
\]

This is 1.5 model standard deviations above the assumed mean. It does not establish a positional accuracy standard or a two-dimensional confidence region; those require an appropriate joint error model, covariance, reference quality and accuracy definition.

## 7. Choosing and checking a model

Ask:

1. What is the variable, its unit, support, spatial footprint and time window?
2. What sampling, measurement or event mechanism generates it?
3. Are parameters assumed, externally specified or estimated?
4. Are observations independent, clustered, repeated or spatially/temporally dependent?
5. Do the model's mean, variance, support, tails and zero frequency resemble the evidence?
6. What happens to the decision if the model is misspecified?

Diagnostics may include empirical distributions, probability plots, residual analysis, dispersion comparisons, spatial plots and out-of-sample checks. No single diagnostic proves a model correct.

## 8. Common errors

- Treating a histogram as a known probability model.
- Confusing a density height with a point probability.
- Forgetting discrete CDF endpoint mass.
- Confusing variance with standard deviation or their units.
- Assuming expectation must be attainable.
- Selecting Poisson merely because the data are counts.
- Treating spatial cells as independent binomial trials without evidence.
- Assuming normality because it is familiar.
- Ignoring covariance when combining variables.
- Fitting a model in one region and assuming it transfers unchanged elsewhere.

## 9. Exercises

**A — Discrete expectation and variance.** A count variable has \(P(X=0)=0.2\), \(P(X=1)=0.5\), \(P(X=2)=0.3\). Calculate \(E[X]\), \(E[X^2]\) and variance.

*Worked guidance:* \(E[X]=1.1\), \(E[X^2]=1.7\), and \(\operatorname{Var}(X)=1.7-1.1^2=0.49\).

**B — Poisson probability.** For \(X\sim\operatorname{Poisson}(3)\), calculate \(P(X=0)\) and \(P(X\leq1)\).

*Worked guidance:* \(P(X=0)=e^{-3}\approx0.0498\); \(P(X\leq1)=e^{-3}(1+3)\approx0.1991\). Interpret these as probabilities for the defined count window, not evidence by themselves that a Poisson process generated the events.

**C — Linear transformation.** If \(E[X]=10\), \(\operatorname{Var}(X)=4\), and \(Y=5+3X\), find the mean, variance and standard deviation of \(Y\).

*Worked guidance:* \(E[Y]=35\), \(\operatorname{Var}(Y)=36\), \(\sigma_Y=6\).

**D — Critique.** A researcher fits a Poisson distribution to landslide reports in 1 km² cells. Identify at least four questions before interpreting the fit.

*Worked guidance:* consider equal cell area, observation period, reporting effort, spatial clustering, terrain/rainfall variation, duplicated events and the mean-variance relationship. Distinguish a Poisson count distribution from a homogeneous spatial Poisson process.

## 10. Connections

- Previous: [Probability models, events and conditioning](probability-models-events-and-conditioning.md).
- Next: sampling designs and sampling distributions, where random variables describe statistics calculated from repeated samples.
- [Linear algebra](../linear-algebra/README.md): covariance matrices and multivariate models.
- [Measurement science](../measurement-science/measurement-principles-and-field-verification.md): measurement models and uncertainty evaluation.
- Future SM-FND-005: spatial dependence, point processes and random fields.
- Applications: [empirical semivariogram](../../methods/empirical-semivariogram.md), [point-pattern second-order statistics](../../methods/point-pattern-second-order-statistics.md), [spatial cross-validation](../../methods/spatial-cross-validation.md), [forecast verification](../../methods/forecast-verification.md).

## References

Diez, D. M., Çetinkaya-Rundel, M., and Barr, C. D. (2019). *OpenIntro Statistics*, 4th ed. Chapter 3, Sections 3.4–3.5, and Chapter 4. [OpenIntro textbook and companion resources](https://openintro.org/book/os/). The book is listed under CC BY-SA 3.0; consult the [licence page](https://openintro.org/license/) for exceptions and conditions. This is an original synthesis with original synthetic spatial examples; no textbook figures or exercises are reproduced.

## Evidence and review boundary

The fourth-edition table of contents and chapter resources were inspected for random variables, continuous distributions, normal, geometric, binomial, negative binomial and Poisson distributions. The source is an introductory applied-statistics reference, not a complete probability theory treatment. No empirical spatial dataset was fitted, no model was validated against field observations, and no spatial-independence assumption is established by the textbook.
