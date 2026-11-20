# Bayesian inference and predictive distributions

**Module:** 07  
**Domain:** Probability and statistical inference (`SM-FND-004`)  
**Level:** Intermediate undergraduate to postgraduate  
**Status:** Initial researched synthesis

## 1. Why Bayesian inference?

Modules 01–06 developed probability models, random variables, dependence, sampling, likelihood, estimation and frequentist inference. Bayesian inference brings these pieces together by representing uncertainty about unknown parameters with probability distributions and updating those distributions when observations arrive.

This is especially useful in spatial work where evidence is uneven, observations are sparse, several information sources must be combined, and decisions depend on the probability of future or unobserved conditions. Examples include small-area environmental rates, habitat suitability, flood-risk scenarios, land-cover classification and probabilistic forecasts.

Bayesian inference does not make weak data strong. The result remains conditional on the likelihood, prior, sampling process, spatial structure and measurement assumptions.

## 2. The Bayesian model

Let:

- \(\theta\) denote an unknown parameter or vector of parameters;
- \(y\) denote observed data;
- \(p(\theta)\) denote the **prior distribution**, representing uncertainty about \(\theta\) before conditioning on the current data;
- \(p(y\mid\theta)\) denote the **sampling model** or likelihood contribution;
- \(p(\theta\mid y)\) denote the **posterior distribution**, representing uncertainty about \(\theta\) after observing \(y\).

Bayes' theorem gives

\[
p(\theta\mid y)=
\frac{p(y\mid\theta)p(\theta)}{p(y)}
\propto p(y\mid\theta)p(\theta).
\]

For a continuous parameter,

\[
p(y)=\int_{\Theta}p(y\mid\theta)p(\theta)\,d\theta
\]

is the marginal likelihood, also called the prior predictive density of the observed data. For a discrete parameter, the integral is replaced by a sum. The denominator normalises the posterior so that it integrates or sums to one.

The likelihood is a function of \(\theta\) with the observed data held fixed. It is not itself a probability distribution over \(\theta\): it need not integrate to one over parameter space. The posterior is a probability distribution over \(\theta\).

A useful verbal summary is:

**posterior ∝ likelihood × prior**

The data update the prior through the likelihood. Sequential updating is valid when the likelihood correctly represents the new data conditional on the information already used. Reusing the same observations as if they were new independent evidence double-counts information.

### Prior information is not automatically external evidence

A prior may encode previous studies, expert elicitation, physical constraints, established process knowledge or a deliberately weak regularisation choice. The origin and rationale should be stated. If previous data are used to construct a prior, explain how overlap with the current dataset was prevented. A prior is not a licence to treat unverified assumptions as observations.

## 3. Priors and prior predictive reasoning

A prior distribution must place probability only on values allowed by the parameter's meaning. A probability parameter lies in \([0,1]\); a positive rate lies above zero; a regression coefficient may be positive or negative unless the model or science imposes a constraint.

Common descriptions include:

- **Informative prior:** represents substantial defensible information before the current data.
- **Weakly informative prior:** constrains implausible extremes while leaving a broad range of values plausible.
- **Regularising prior:** stabilises estimation or discourages implausibly large or complex parameter values.
- **Conjugate prior:** belongs to a distribution family that yields a posterior in the same family for a specified likelihood.

“Non-informative” is not a guarantee of neutrality. Diffuse or improper priors can have unintuitive implications, depend on parameterisation, or produce an improper posterior. Prior choice is part of model specification.

### Prior predictive distribution

Before seeing the observations, the prior and likelihood imply a distribution for possible data:

\[
p(y)=\int p(y\mid\theta)p(\theta)\,d\theta.
\]

A prior predictive check asks whether data simulated from this distribution are plausible for the application. For a spatial event-rate model, for example, it is worth asking whether the prior allows implausibly high event counts, impossible rates, or spatial patterns inconsistent with the scale and process being modelled.

Prior predictive checks can reveal priors that are too concentrated, too diffuse, poorly scaled or inconsistent with known constraints. They do not validate the likelihood or prove that the prior is scientifically correct.

## 4. Worked example: updating a spatial detection proportion

Suppose a hypothetical field-screening programme records whether a target feature is detected at each sampled location. Let \(\theta\) be the probability of detection for the population and conditions represented by the sampling model.

Assume, for teaching purposes:

\[
Y\mid\theta\sim\operatorname{Binomial}(n=60,\theta),
\qquad
\theta\sim\operatorname{Beta}(2,2).
\]

The prior mean is

\[
E(\theta)=\frac{2}{2+2}=0.5.
\]

The prior is symmetric and puts more mass near moderate probabilities than at the extremes. It is an illustrative prior, not a claim about real detection rates.

Suppose 18 of the 60 sampled locations record a detection. The likelihood kernel is

\[
L(\theta;y)\propto\theta^{18}(1-\theta)^{42}.
\]

The Beta prior density is proportional to \(\theta^{2-1}(1-\theta)^{2-1}\). Multiplying prior and likelihood gives

\[
p(\theta\mid y)\propto
\theta^{18+2-1}(1-\theta)^{42+2-1},
\]

so

\[
\theta\mid y\sim\operatorname{Beta}(20,44).
\]

The posterior mean is

\[
E(\theta\mid y)=\frac{20}{20+44}=0.3125.
\]

The equal-tail 95% credible interval is approximately

\[
[0.206,\ 0.430].
\]

**Interpretation:** under this model and prior, the posterior probability that the represented population detection probability lies between approximately 0.206 and 0.430 is 0.95.

This is a model-based statement about \(\theta\), not a statement that 95% of sampled locations have detection probabilities in that range. It does not establish that the 60 locations represent the target population. If nearby locations are dependent, the binomial likelihood may be inappropriate; if the sampling frame excludes inaccessible areas, the posterior does not repair that coverage error.

The prior matters. With a different prior, the posterior changes. A useful analysis should justify the prior and examine whether conclusions are sensitive to reasonable alternatives.

## 5. Posterior summaries and credible intervals

A posterior distribution contains more information than a single estimate. Common summaries include:

- posterior mean, useful under squared-error loss;
- posterior median, useful under absolute-error loss;
- maximum a posteriori (MAP) estimate, a posterior mode that can depend on parameterisation and density scale;
- posterior quantiles and credible intervals;
- posterior probabilities of scientifically or operationally meaningful events.

An equal-tail \(100(1-\alpha)\%\) credible interval \([a,b]\) satisfies

\[
P(a\leq\theta\leq b\mid y)=1-\alpha
\]

with posterior tail probability \(\alpha/2\) on each side. A highest-posterior-density interval is another construction, but may be non-unique for multimodal or irregular posteriors.

A 95% credible interval has a direct posterior probability interpretation conditional on the model, prior and observed data. This differs from a 95% frequentist confidence interval, whose coverage statement concerns the long-run behaviour of a procedure under repeated sampling. Neither interval is automatically a guarantee of practical accuracy.

For decisions, a probability such as

\[
P(\theta>0.30\mid y)
\]

may be more useful than a point estimate if 0.30 is a meaningful threshold. The threshold must come from the application and its consequences, not from a statistical convention alone.

## 6. Posterior predictive distributions

Parameter inference and prediction are different tasks. A posterior describes uncertainty about model parameters. A posterior predictive distribution describes uncertainty about a future or unobserved observation:

\[
p(\tilde y\mid y)
=
\int p(\tilde y\mid\theta)\,p(\theta\mid y)\,d\theta.
\]

It averages the future-data model over posterior uncertainty in the parameters. It therefore includes both uncertainty about \(\theta\) and the variability of new observations conditional on \(\theta\).

For the Beta–Binomial example, suppose we want the number \(K\) of detections in 20 additional comparable locations. Integrating over the posterior gives a Beta–Binomial predictive distribution:

\[
K\mid y\sim\operatorname{BetaBinomial}(20,20,44).
\]

Its predictive mean is

\[
E(K\mid y)=20\frac{20}{64}=6.25.
\]

The predictive standard deviation is larger than it would be if \(\theta\) were known and fixed, because it also reflects posterior uncertainty about \(\theta\). The predictive distribution is not a confidence interval for the parameter. It concerns future observations.

### Posterior predictive checks

A posterior predictive check compares observed data with replicated datasets generated from the fitted model:

1. draw parameter values from the posterior;
2. generate replicated data under the observation model;
3. compare useful summaries or patterns in the replicated data with those in the observed data.

For spatial applications, comparisons may include count distributions, zero frequencies, residual patterns, spatial clustering, edge behaviour, temporal structure and variation across relevant subregions. The discrepancy measures must be selected for the scientific question. Matching a global mean does not demonstrate that a model reproduces local spatial structure.

A model can have a well-behaved sampler and still fit the data poorly. Computational diagnostics and model criticism answer different questions.

## 7. A second conjugate example: Poisson counts and a Gamma rate prior

Suppose counts \(Y_i\) are conditionally Poisson with rate \(\lambda\) per unit of exposure \(e_i\):

\[
Y_i\mid\lambda\sim\operatorname{Poisson}(e_i\lambda).
\]

Use a Gamma prior in the **shape–rate** parameterisation:

\[
\lambda\sim\operatorname{Gamma}(a,b),
\qquad E(\lambda)=a/b.
\]

For conditionally independent observations, the posterior is

\[
\lambda\mid y\sim
\operatorname{Gamma}\left(a+\sum_i y_i,\ b+\sum_i e_i\right).
\]

For an illustrative prior \(\operatorname{Gamma}(2,1)\), 14 events across 10 exposure units produce

\[
\lambda\mid y\sim\operatorname{Gamma}(16,11),
\qquad E(\lambda\mid y)=16/11\approx1.455.
\]

The rate unit is events per exposure unit. If exposure is site-months, the rate is events per site-month. Do not mix counts and rates without retaining exposure.

This simple model assumes a common rate and conditional independence given that rate. It is not automatically appropriate for spatially clustered counts, unequal population at risk, overdispersion, changing observation effort or spatially varying exposure. Those features require an appropriate likelihood and potentially hierarchical or spatial structure.

## 8. Hierarchical and spatial Bayesian models

A hierarchical model introduces parameters that describe variation across groups or locations. A simple schematic structure is

\[
y_i\mid\theta_i\sim p(y_i\mid\theta_i),
\qquad
\theta_i\mid\phi\sim p(\theta_i\mid\phi),
\qquad
\phi\sim p(\phi).
\]

Here \(\theta_i\) may represent a local event rate, class probability or environmental response, while \(\phi\) controls the distribution of local effects.

**Partial pooling** allows local estimates to share information through a common higher-level model. It can stabilise estimates for locations with sparse observations, but it can also oversmooth genuine local differences if the hierarchy is misspecified.

Spatial models may add dependence through adjacency structures, spatial random effects, Gaussian processes, conditional autoregressive models, spatially varying coefficients or spatiotemporal processes. The probability and statistical inference foundation introduces the Bayesian logic; detailed spatial stochastic-process theory and model construction belong with **SM-FND-005 — Spatial statistics and stochastic processes**.

A spatial Bayesian model still needs:
- a defensible spatial support and neighbourhood or distance definition;
- an explicit observation and sampling model;
- a reasoned spatial dependence structure;
- appropriate treatment of exposure, missingness and measurement error;
- prior predictive checks and prior sensitivity analysis;
- posterior predictive checks that inspect spatial as well as marginal behaviour;
- validation against genuinely held-out information where possible.

A map of posterior means alone hides uncertainty. Show posterior intervals, exceedance probabilities or predictive distributions where they are relevant, and explain what each map represents.

## 9. Computation and MCMC diagnostics

Conjugate models can sometimes be solved analytically. More complex models require numerical integration, approximation or simulation. Markov chain Monte Carlo (MCMC) produces dependent draws intended to represent the posterior distribution.

A trace plot is a useful first inspection, but no single diagnostic proves convergence. For MCMC workflows, examine at least:

- multiple chains and whether they explore compatible regions;
- rank-normalised split \(\hat R\), with values near 1 and commonly below 1.01 as a practical target in modern Stan workflows;
- bulk and tail effective sample sizes (ESS);
- Monte Carlo standard errors for quantities being reported;
- divergent transitions and other sampler warnings;
- trace plots, marginal distributions and pairwise relationships;
- sensitivity to parameterisation, initialisation and model specification.

A divergence is not a cosmetic warning: it can indicate that the sampler has failed to explore important posterior geometry and that estimates may be biased. Increasing iterations alone is not a universal remedy. Reconsider model structure, parameterisation, scaling and identifiability.

These diagnostics address computation, not whether the model is scientifically adequate. A sampler can accurately explore the posterior of a bad model.

## 10. Prior sensitivity, identifiability and model criticism

A responsible Bayesian analysis should ask:

1. **Prior sensitivity:** do important conclusions change under other defensible priors?
2. **Identifiability:** can the available data distinguish the parameters that the model attempts to estimate?
3. **Likelihood adequacy:** does the observation model reflect the actual sampling and measurement process?
4. **Predictive adequacy:** can the fitted model reproduce features relevant to the application?
5. **Spatial adequacy:** does the model capture the dependence, scale and heterogeneity that matter?
6. **Decision relevance:** are posterior summaries aligned with the consequences of acting or not acting?

A posterior may be narrow because the prior is strong, not because the data are informative. Report that distinction. A posterior probability is conditional on the complete model; it is not an objective probability detached from assumptions.

## 11. Exercises

**A — Identify the model components.** A land-cover validation study uses prior information about a class prevalence and new reference observations. Identify the parameter, prior, likelihood, posterior and target population.

*Worked guidance:* The parameter is the population prevalence or class-specific probability of interest; the prior describes uncertainty before the current validation data; the likelihood models the observed sample conditional on that parameter; the posterior updates uncertainty. The target population and sampling frame must be defined before interpreting the result.

**B — Beta–Binomial update.** With prior \(\operatorname{Beta}(2,2)\), observe 18 detections in 60 trials. Derive the posterior and its mean.

*Worked guidance:* \(\operatorname{Beta}(20,44)\), with posterior mean \(20/64=0.3125\).

**C — Credible interval.** Explain the meaning of the 95% equal-tail credible interval \([0.206,0.430]\) from the worked example, and contrast it with a 95% confidence interval.

*Worked guidance:* Conditional on the prior, likelihood and observed data, posterior probability in the interval is 0.95. A frequentist confidence interval instead has a repeated-sampling coverage interpretation.

**D — Posterior prediction.** For 20 additional comparable locations in the worked example, calculate the expected number of detections.

*Worked guidance:* \(20\times0.3125=6.25\). This is the predictive mean; a prediction interval must also account for posterior parameter uncertainty and future Bernoulli variation.

**E — Prior sensitivity.** Repeat the Beta–Binomial update using a uniform \(\operatorname{Beta}(1,1)\) prior. Compare the posterior mean with the worked example and explain why this comparison is not a substitute for prior justification.

*Worked guidance:* The posterior is \(\operatorname{Beta}(19,43)\), with mean \(19/62\approx0.3065\). The numerical difference is small in this example, but prior choice should still be justified and examined in relation to plausible alternatives.

**F — Spatial dependence.** A study records detections at 60 nearby raster cells and treats them as independent Bernoulli trials. Explain the risk and suggest what a more defensible model might need.

*Worked guidance:* Nearby cells may share environmental conditions, image artefacts or spatial processes. An independent binomial likelihood can overstate effective information. Consider the sampling support, spatial dependence, clustered design or a spatial/hierarchical model, and validate the resulting structure.

**G — Poisson–Gamma update.** A prior \(\operatorname{Gamma}(2,1)\) is used for an event rate. Fourteen events are observed over 10 exposure units. Give the posterior and its mean, using shape–rate notation.

*Worked guidance:* \(\operatorname{Gamma}(16,11)\), with mean \(16/11\approx1.455\) events per exposure unit.

**H — Model criticism.** A Bayesian spatial model has \(\hat R\) values near 1 and no reported divergences, but posterior predictive simulations fail to reproduce observed clustering. What can be concluded?

*Worked guidance:* The sampler diagnostics provide some evidence about computation, not model adequacy. The fitted model does not reproduce an important feature of the data and needs substantive revision or a narrower stated purpose.

## 12. Connections and next steps

- Previous: [Confidence intervals, hypothesis tests and statistical decisions](confidence-intervals-hypothesis-tests-and-statistical-decisions.md).
- [Likelihood and statistical estimation](likelihood-and-statistical-estimation.md): likelihood is the data contribution to the posterior.
- [Joint distributions, covariance and dependence](joint-distributions-covariance-and-dependence.md): multivariate and conditional probability structures.
- [Sampling designs and sampling distributions](sampling-designs-and-sampling-distributions.md): the sampling frame and design remain central to the likelihood.
- [Spatial cross-validation](../../methods/spatial-cross-validation.md): validation under spatial structure.
- [Forecast verification](../../methods/forecast-verification.md): evaluation of predictive distributions.
- Next: [Statistical diagnostics, calibration and model criticism](README.md) — Module 08.

## References

- Powell, B. (2026). [Bayesian Statistics: notes to accompany the lectures](https://www-users.york.ac.uk/~bp787/Bayes_notes.html). Department of Mathematics, University of York. Inspected sections on Bayes' theorem, binomial and Poisson models, conjugacy, prediction, priors, Monte Carlo methods, MCMC and hierarchical models.
- Stan Development Team. [Stan User's Guide](https://mc-stan.org/docs/stan-users-guide/). Consult the sections on posterior prediction and posterior predictive checks. Used for predictive distributions and model-checking workflow.
- Stan Development Team. [How to Diagnose and Resolve Convergence Problems](https://mc-stan.org/learn-stan/diagnostics-warnings.html). Used for current guidance on \(\hat R\), effective sample size and divergent transitions.

The numerical examples are original synthetic teaching illustrations. The Beta credible interval was calculated from the stated Beta posterior. No real spatial dataset was fitted, no MCMC model was run, and no operational risk or accuracy claim is made.

## Evidence and review boundary

The University of York lecture notes were inspected for Bayesian updating, the prior/likelihood/posterior distinction, marginal likelihood, Beta–Binomial and Gamma–Poisson conjugacy, predictive distributions, prior sensitivity, Monte Carlo, MCMC and hierarchical models. Stan documentation was inspected for posterior predictive checking and current sampler diagnostics, including \(\hat R\), effective sample size and divergences.

This module is an introductory synthesis. It does not derive advanced Bayesian computation, prove convergence of MCMC algorithms, prescribe a universal prior, or provide a complete spatial hierarchical modelling guide. Spatial dependence, sample selection, measurement error, exposure and model adequacy must be handled explicitly in each real application.
