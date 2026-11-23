# Likelihood and statistical estimation

**Subject:** \`SM-FND-004\` — Probability and statistical inference  
**Module:** 05  
**Status:** Initial researched teaching resource; independent technical review and learner testing pending.

## 1. From probability models to parameter estimation

A probability model describes how data could arise under specified assumptions. In many applications, the model contains unknown quantities. A spatial analyst may know the form of a regression model but not its coefficients; a mapping team may posit a Poisson model for event counts but not know the event intensity; a geostatistician may specify a covariance family but need to estimate its range and variance parameters.

Let observations be represented by \(y\), and let \(\theta\) denote an unknown parameter or parameter vector. A statistical model specifies a probability mass function or density \(f(y\mid\theta)\), together with the support and assumptions under which it applies.

An **estimator** is a rule that maps observed data to an estimate of an unknown quantity. An estimate is the realised value produced by that rule for a particular dataset. Keep these distinct:

- \(\theta\): the unknown model parameter;
- \(\hat\theta=T(Y)\): an estimator, viewed as a random variable before data are observed;
- \(\hat\theta(y)\): the numerical estimate after observing \(y\).

Estimation does not make the model true. It selects parameter values within a chosen model. Model form, data quality, sampling design and assumptions still require scrutiny.

## 2. The likelihood function

For observed data \(y\), the likelihood is the model's probability mass or density evaluated at those data, regarded as a function of the unknown parameter:

\[
L(\theta\mid y)=f(y\mid\theta).
\]

The same mathematical expression has a different role depending on what is held fixed. In a probability distribution, \(\theta\) is fixed and the expression varies over possible data. In likelihood analysis, the observed data \(y\) are fixed and the expression is examined over possible parameter values.

**Likelihood is not the probability that a parameter has a particular value.** In ordinary frequentist likelihood, the parameter is not assigned a probability distribution. Bayesian inference introduces a prior and posterior distribution; that is a different inferential framework.

For independent observations \(y_1,\ldots,y_n\) from a common model,

\[
L(\theta\mid y_1,\ldots,y_n)
=\prod_{i=1}^{n}f(y_i\mid\theta).
\]

Independence is essential to this product factorisation. If observations are dependent, the joint likelihood must represent their dependence, for example through a multivariate distribution or an explicit conditional factorisation. Multiplying marginal densities as if observations were independent does not become valid merely because the observations are stored in separate rows.

The log-likelihood is

\[
\ell(\theta\mid y)=\log L(\theta\mid y).
\]

For independent observations,

\[
\ell(\theta)=\sum_{i=1}^{n}\log f(y_i\mid\theta).
\]

Because the logarithm is strictly increasing, maximising log-likelihood gives the same maximiser as maximising likelihood. The sum is usually easier and more numerically stable to work with than a product of many small probabilities or densities. Terms that do not depend on \(\theta\) may be dropped when locating the maximiser, but not when computing quantities that require the full likelihood value.

## 3. Maximum likelihood estimation

The maximum likelihood estimator (MLE) is

\[
\hat\theta_{\mathrm{MLE}}
=\operatorname*{arg\,max}_{\theta\in\Theta}
L(\theta\mid y)
=\operatorname*{arg\,max}_{\theta\in\Theta}
\ell(\theta\mid y),
\]

where \(\Theta\) is the permitted parameter space.

For a differentiable scalar parameter, an interior maximum may satisfy the score equation

\[
U(\theta)=\frac{\partial\ell(\theta)}{\partial\theta}=0.
\]

For a vector parameter, the score is the gradient

\[
\mathbf U(\boldsymbol\theta)
=\nabla_{\boldsymbol\theta}\ell(\boldsymbol\theta).
\]

A zero score is a candidate stationary point, not proof of a maximum. Check the parameter space, curvature, boundaries and competing solutions. Some MLEs occur at a boundary; some models have no finite MLE; some likelihoods have multiple local maxima or are flat in particular parameter directions.

### Example A — Bernoulli detection probability

Suppose \(n\) independent sampling units each produce a binary result \(Y_i\in\{0,1\}\), with \(P(Y_i=1)=p\). Let \(s=\sum_i y_i\) be the number of positive outcomes.

\[
L(p)=p^s(1-p)^{n-s},\qquad 0\leq p\leq1.
\]

Ignoring terms independent of \(p\),

\[
\ell(p)=s\log p+(n-s)\log(1-p).
\]

Differentiating and solving the score equation gives

\[
\frac{s}{p}-\frac{n-s}{1-p}=0
\quad\Longrightarrow\quad
\hat p=\frac{s}{n}.
\]

If 18 of 60 hypothetical sampled units are positive, \(\hat p=0.30\). This is a model-based estimate for the defined sampling units and process. If the 60 units were selected through a complex unequal-probability design, clustered selection, or spatially dependent process, the simple independent Bernoulli likelihood and its standard error may not be appropriate. The number 0.30 is not automatically an area-adjusted map accuracy or a population prevalence estimate.

### Example B — Poisson event rate

Suppose independent counts \(Y_i\) follow a Poisson distribution with common rate parameter \(\lambda>0\):

\[
P(Y_i=y_i\mid\lambda)
=\frac{e^{-\lambda}\lambda^{y_i}}{y_i!}.
\]

For \(n\) observations,

\[
\ell(\lambda)
=-n\lambda+\left(\sum_i y_i\right)\log\lambda
-\sum_i\log(y_i!).
\]

The score equation gives

\[
-\;n+\frac{\sum_i y_i}{\lambda}=0
\quad\Longrightarrow\quad
\hat\lambda=\bar y.
\]

For hypothetical counts \(4,2,3,1,5\), the estimate is \(\hat\lambda=3\) events per defined observation window. A spatial interpretation requires the window, exposure or area, observation process and sampling frame to be specified. A constant-rate Poisson model is not established by the arithmetic mean; clustering, varying exposure and spatially varying intensity may require a different model.

## 4. Normal models and least squares

Suppose observations satisfy

\[
Y_i=\mu_i(\boldsymbol\beta)+\varepsilon_i,
\qquad
\varepsilon_i\overset{\mathrm{ind}}{\sim}N(0,\sigma^2),
\]

with common variance and independent errors. The likelihood is proportional to

\[
(\sigma^2)^{-n/2}
\exp\left[-\frac{1}{2\sigma^2}
\sum_{i=1}^n(y_i-\mu_i(\boldsymbol\beta))^2\right].
\]

For a fixed \(\sigma^2\), maximising this likelihood over \(\boldsymbol\beta\) is equivalent to minimising the sum of squared residuals. Thus ordinary least squares (OLS) estimates of the regression coefficients are also MLEs under the independent, equal-variance Gaussian error model.

For the linear model \(\mathbf y=\mathbf X\boldsymbol\beta+\boldsymbol\varepsilon\), when \(\mathbf X\) has full column rank,

\[
\hat{\boldsymbol\beta}_{\mathrm{OLS}}
=(\mathbf X^T\mathbf X)^{-1}\mathbf X^T\mathbf y.
\]

This expression describes the solution mathematically; in numerical work, solve the least-squares problem with a stable QR or SVD method rather than explicitly forming a matrix inverse.

The Gaussian MLE of the error variance is

\[
\hat\sigma^2_{\mathrm{MLE}}
=\frac{1}{n}\sum_{i=1}^n
(y_i-\mathbf x_i^T\hat{\boldsymbol\beta})^2.
\]

The familiar residual variance estimator with denominator \(n-p\), where \(p\) coefficients were fitted, is unbiased under the classical full-rank linear model assumptions; it is not the MLE of \(\sigma^2\). The distinction matters when reporting fitted variance and uncertainty.

### Correlated errors and generalized least squares

If

\[
\boldsymbol\varepsilon\sim N(\mathbf 0,\boldsymbol\Sigma)
\]

with known positive-definite covariance matrix \(\boldsymbol\Sigma\), the Gaussian log-likelihood leads to minimising

\[
(\mathbf y-\mathbf X\boldsymbol\beta)^T
\boldsymbol\Sigma^{-1}
(\mathbf y-\mathbf X\boldsymbol\beta).
\]

The resulting generalized least-squares (GLS) estimator is

\[
\hat{\boldsymbol\beta}_{\mathrm{GLS}}
=(\mathbf X^T\boldsymbol\Sigma^{-1}\mathbf X)^{-1}
\mathbf X^T\boldsymbol\Sigma^{-1}\mathbf y,
\]

when the required inverses exist. GLS is therefore a Gaussian maximum-likelihood estimator for the coefficients when the covariance is known and the Gaussian model is correctly specified. If covariance parameters are also unknown, they must be estimated jointly or through a justified staged procedure; treating an estimated covariance matrix as known understates uncertainty in some settings.

Least squares and maximum likelihood are not synonyms. Their equivalence depends on the error distribution, covariance structure and parameterisation. Non-Gaussian errors, heteroscedasticity, censoring, count outcomes and robust loss functions lead to different objectives and estimators.

## 5. Estimator properties

An estimator is a random quantity because it depends on random data. Its properties describe how it behaves over repeated samples under a specified model or sampling design.

### Bias

The bias of \(\hat\theta\) is

\[
\operatorname{Bias}(\hat\theta)
=E[\hat\theta]-\theta.
\]

An estimator is unbiased if its expected value equals the target parameter for every parameter value in the stated model. Unbiasedness is not the only criterion: a biased estimator may have lower mean squared error or better practical behaviour.

### Variance and mean squared error

\[
\operatorname{Var}(\hat\theta)
=E[(\hat\theta-E[\hat\theta])^2],
\]

and

\[
\operatorname{MSE}(\hat\theta)
=E[(\hat\theta-\theta)^2]
=\operatorname{Var}(\hat\theta)+\operatorname{Bias}(\hat\theta)^2.
\]

A lower variance alone does not guarantee a better estimator if bias differs. Compare estimators against the same target, model and loss criterion.

### Consistency

An estimator is consistent if it converges in probability to the target parameter as the amount of information grows:

\[
\hat\theta_n\xrightarrow{P}\theta.
\]

Consistency is an asymptotic property. It does not guarantee good performance for a small sample, and it depends on conditions such as identifiability, the data-generating process and the estimator's construction.

### Efficiency and information

For regular models, Fisher information describes how much information the likelihood contains about a parameter. In a scalar model, the expected Fisher information for \(n\) observations is

\[
I_n(\theta)
=E\left[\left(\frac{\partial\ell}{\partial\theta}\right)^2\right]
=-E\left[\frac{\partial^2\ell}{\partial\theta^2}\right],
\]

when the regularity conditions allowing these equivalent forms hold. For vector parameters, information is a matrix.

Under suitable regularity conditions, the MLE is often consistent and asymptotically normal:

\[
\hat{\boldsymbol\theta}
\ \dot\sim\
N\left(\boldsymbol\theta,\ I_n(\boldsymbol\theta)^{-1}\right).
\]

This is an approximation for sufficiently informative samples under a correctly specified, identifiable and regular model. It is not a universal finite-sample guarantee. Boundary parameters, weak identification, small samples, mixtures, highly correlated observations and model misspecification can invalidate or degrade the approximation.

The observed information is often computed from the negative Hessian of the log-likelihood at the estimate. Its inverse may provide an approximate covariance matrix for the MLE. A numerical optimiser's convergence flag is not evidence that the model is appropriate, the maximum is global, or the uncertainty approximation is reliable.

## 6. Identifiability and model criticism

A parameter is identifiable when distinct parameter values imply distinct probability distributions for the observable data. If different parameter values produce exactly the same observable distribution, the data cannot distinguish them under that model. Near-non-identifiability occurs when different parameter values produce very similar distributions; estimates may then be unstable and uncertainty large.

Common warning signs include:

- a flat or nearly flat likelihood surface;
- highly correlated parameter estimates;
- estimates that change greatly with starting values;
- parameters driven to imposed bounds;
- a singular or ill-conditioned information matrix;
- multiple local optima;
- large sensitivity to a small number of observations;
- a model whose assumptions conflict with the data-collection process.

Outliers can strongly affect ordinary least squares and many likelihood estimators. Robust estimation may be useful, but a robust objective defines a different estimator and requires its own interpretation and uncertainty treatment.

Model criticism should examine residual structure, distributional assumptions, dependence, influential observations, calibration and predictive performance. A good numerical fit is not proof of causal explanation or external validity.

## 7. Spatial applications and dependence

Likelihood methods appear throughout spatial analysis:

- **Spatial regression:** estimate relationships between spatial predictors and responses. Spatial trend, clustered sampling, heteroscedasticity and residual autocorrelation affect the likelihood and uncertainty.
- **Event counts:** Poisson or negative-binomial models may represent counts per area or time window. Exposure offsets and varying observation effort must be defined; overdispersion and clustering should be assessed.
- **Geostatistics:** covariance parameters such as sill, range and nugget may be estimated through likelihood or restricted maximum likelihood (REML). The assumed mean structure, covariance family, sampling geometry and likelihood approximation matter.
- **Classification:** likelihood-based models can estimate class probabilities, but probability calibration, class imbalance, sampling design and spatial transferability remain separate questions.
- **Measurement adjustment:** Gaussian observation models lead to least-squares or GLS estimates, while the stochastic model must be supported by measurement design and covariance evidence.

For spatially dependent observations, a joint spatial likelihood may be required. A product of independent marginal likelihood contributions is generally not the correct joint likelihood when the observations are dependent. Composite likelihoods and pseudo-likelihoods are specialised approximations with their own variance corrections and limitations; they should not be presented as ordinary full likelihood without explanation.

Sampling design and likelihood answer related but different questions. A probability sample supports design-based inference through known selection probabilities. A model-based likelihood supports inference through a probability model for the observations. Model-based estimation does not automatically repair an incomplete sampling frame, nonresponse, selection bias or poor measurement.

## 8. Worked interpretation: a spatial event-rate estimate

A team counts hypothetical service incidents in five equal observation windows: \(4,2,3,1,5\). Under an independent, identically distributed Poisson model, the maximum-likelihood rate is

\[
\hat\lambda=\frac{4+2+3+1+5}{5}=3
\]

incidents per window. The fitted model's likelihood is maximised at this value, but the estimate alone does not answer:

- whether windows have equal area, duration and exposure;
- whether all incidents were detected and recorded;
- whether counts are independent;
- whether the rate is constant across space and time;
- whether the windows represent the target area;
- whether a Poisson variance equal to the mean is plausible.

If windows differ in exposure \(e_i\), a rate model may instead use \(Y_i\sim\operatorname{Poisson}(e_i\lambda)\), giving \(\hat\lambda=\sum_i y_i/\sum_i e_i\) under the independent common-rate model. If event counts cluster spatially or vary with covariates, a constant-rate model may be inadequate. These are model-design questions, not arithmetic corrections.

## 9. Exercises

**A — Bernoulli likelihood.** A hypothetical independent sample contains 24 positive outcomes among 80 binary observations. Write the likelihood kernel and calculate the MLE of \(p\).

*Worked guidance:* \(L(p)\propto p^{24}(1-p)^{56}\). The MLE is \(24/80=0.30\). State the independent Bernoulli assumption and define the sampling unit.

**B — Poisson likelihood.** Counts are \(2,0,4,3,1\) from equal observation windows. Derive the MLE of the common Poisson mean.

*Worked guidance:* \(\hat\lambda=\bar y=(2+0+4+3+1)/5=2\) events per window.

**C — Likelihood versus probability.** Explain why \(L(\theta\mid y)\) is not the probability that \(\theta\) is true.

*Worked guidance:* In frequentist likelihood, the observed data are fixed and the expression varies over parameter values. A probability distribution over parameters requires an additional framework, such as a Bayesian prior and posterior.

**D — Least squares.** State the assumptions under which minimising squared residuals for regression coefficients is equivalent to maximising a Gaussian likelihood.

*Worked guidance:* The response model is correctly specified with independent Gaussian errors having common variance; the coefficient estimates minimise the residual sum of squares. Correlated Gaussian errors instead lead to a covariance-weighted GLS objective.

**E — Estimator comparison.** Estimator A has bias 0 and variance 9. Estimator B has bias 2 and variance 4. Calculate each MSE and compare under squared-error loss.

*Worked guidance:* A has MSE \(9\). B has MSE \(4+2^2=8\). B has lower MSE despite being biased. This comparison is meaningful only for the same target and model.

**F — Spatial model criticism.** A Poisson model is fitted to incident counts in adjacent grid cells. List at least five checks before interpreting its rate estimates.

*Worked guidance:* Define cell area and time window; check completeness and detection; examine exposure differences; investigate overdispersion and excess zeros; assess spatial autocorrelation or clustering; consider covariates and nonstationarity; inspect residuals; verify that the grid represents the target population and that the assumed count process is plausible.

## 10. Connections and next steps

- Previous: [Sampling designs and sampling distributions](sampling-designs-and-sampling-distributions.md).
- [Joint distributions, covariance and dependence](joint-distributions-covariance-and-dependence.md): the joint model needed when observations or errors are dependent.
- [Linear algebra and matrix methods](../linear-algebra/README.md): least squares, QR/SVD, covariance matrices and information matrices.
- [Covariance, correlated observations and generalized least squares](../measurement-science/covariance-correlated-observations-and-gls.md): a measurement-focused treatment of GLS and stochastic models.
- [Spatial cross-validation](../../methods/spatial-cross-validation.md): spatially structured validation and limits of random splits.
- Next: [Confidence intervals, hypothesis tests and statistical decisions](confidence-intervals-hypothesis-tests-and-statistical-decisions.md).

## References

- NIST/SEMATECH. *e-Handbook of Statistical Methods*, “How are estimates of the unknown parameters obtained?” [NIST handbook section](https://www.itl.nist.gov/div898/handbook/pmd/section4/pmd43.htm). Used for parameter estimation, maximum likelihood and least-squares equivalence under normally distributed errors.
- NIST/SEMATECH. *e-Handbook of Statistical Methods*, “Maximum likelihood estimation.” [NIST handbook section](https://www.itl.nist.gov/div898/handbook/apr/section4/apr412.htm). Used for likelihood construction, log-likelihood maximisation and examples with censored data; reliability-specific censoring details are not generalised to spatial data.
- University of Washington, STAT 512. “Introduction to Statistical Inference,” Lecture 6: Estimators. [Lecture notes](https://faculty.washington.edu/yenchic/20A_stat512/Lec6_MLE.html). Used for score functions, Fisher information, asymptotic normality and Bernoulli/Poisson MLE examples.

The spatial examples and exercises in this module are original synthetic teaching illustrations. No empirical spatial dataset has been fitted.

## Evidence and review boundary

The NIST/SEMATECH parameter-estimation section was inspected for its distinction between least squares and maximum likelihood and its stated equivalence under normally distributed errors. The NIST reliability section was inspected for likelihood construction, log-likelihood maximisation, censoring examples and large-sample cautions; its specialised reliability-data formulas are not treated as general spatial methods. University of Washington STAT 512 lecture notes were inspected for the likelihood/log-likelihood distinction, score equations, Fisher information, asymptotic behaviour and elementary Bernoulli and Poisson examples.

This is an introductory synthesis, not a complete theory of likelihood inference. It does not cover full Bayesian inference, REML derivations, survival analysis, latent-variable models, complex survey pseudo-likelihoods or advanced spatial likelihood computation. No empirical model was fitted, no real spatial process was validated and no field or operational accuracy claim is made.
