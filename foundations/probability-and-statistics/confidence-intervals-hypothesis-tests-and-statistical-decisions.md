# Confidence intervals, hypothesis tests and statistical decisions

**Subject:** \`SM-FND-004\` — Probability and statistical inference  
**Module:** 06  
**Status:** Initial researched teaching resource; independent technical review and learner testing pending.

## 1. From an estimate to an uncertainty statement

An estimate is rarely the whole answer. A spatial analyst may estimate a mean travel time, a change in vegetation index, a difference in mapped class proportions, or a positional-error parameter. The next questions are:

- How variable would the estimator be under the stated sampling or probability model?
- Which parameter values remain compatible with the data and procedure?
- How surprising are the observed data under a specified null hypothesis?
- What kinds of errors could the decision procedure make?
- Is the estimated effect large enough to matter for the intended use?

Confidence intervals and hypothesis tests are inferential procedures. They depend on a probability model, sampling design, estimator, variance calculation and assumptions. They do not repair biased sampling, incomplete frames, measurement error, model misspecification or spatial dependence.

This module uses frequentist inference. A Bayesian credible interval and posterior probability are different objects; they are introduced in Module 07.

## 2. Standard errors and confidence intervals

A standard error (SE) describes the sampling variability of an estimator under a specified model or design. It is not the standard deviation of individual observations, although the two are related in simple settings. For an independent random sample with sample standard deviation \(s\), the standard error of the sample mean is \(s/\sqrt n\).

A confidence interval is produced by a procedure that, under its assumptions, covers the fixed target parameter at a stated long-run rate. A \(100(1-\alpha)\%\) confidence procedure has coverage probability \(1-\alpha\) over repeated samples generated under the model or design.

For a realised 95% confidence interval, the frequentist interpretation is not that there is a 95% probability that the fixed parameter lies inside this particular interval. The parameter is treated as fixed; the interval is random before sampling. The confidence statement describes the long-run coverage of the procedure.

### A basic normal interval

If observations are independent and identically distributed from a normal population with unknown mean \(\mu\) and unknown standard deviation, then

\[
\bar Y\ \pm\ t_{1-\alpha/2,n-1}\frac{s}{\sqrt n}
\]

is the usual two-sided \(100(1-\alpha)\%\) confidence interval for \(\mu\). The \(t\) critical value accounts for estimating the population standard deviation. If the population standard deviation is known, the corresponding normal \(z\) critical value is used.

The interval's validity depends on the sampling model. For small samples, strong departures from normality, outliers or dependence can make the standard formula unreliable. Large samples do not automatically neutralise selection bias or spatial clustering.

### Example — hypothetical site-level change

Suppose a probability sample of 25 independent sites produces paired before–after differences in a continuous environmental indicator. The sample mean difference is 2.4 units and the sample standard deviation of differences is 3.0 units. Assume the paired differences are independent across sampled sites and sufficiently compatible with the normal model for this small-sample \(t\) procedure.

\[
SE=\frac{3.0}{\sqrt{25}}=0.6.
\]

With 24 degrees of freedom, the 95% critical value is approximately 2.064, so

\[
2.4\pm2.064(0.6)
=[1.162,\ 3.638].
\]

The interval is in the original indicator units. Under the stated model and sampling procedure, the data support a positive mean change. This does not establish that every site changed, that the change was caused by a particular intervention, or that 2.4 units is practically important. The example is synthetic, not field evidence.

### Interval width and interpretation

An interval becomes narrower when estimator variability decreases, all else equal. This can occur through more informative observations, a larger effective sample, better measurement or a more efficient design. The effective sample size may be much smaller than the number of mapped pixels or records when observations are strongly dependent.

A narrow interval can still be misleading if the model omits important uncertainty, the sample frame is biased, the measurements are systematically wrong, or the target parameter is poorly defined. Precision is not the same as validity.

## 3. Confidence intervals from likelihood and other procedures

The \(t\)-interval is one construction, not a universal template.

- **Wald intervals** use an estimate and an approximate standard error, often from the inverse observed or expected information. They can perform poorly for small samples, parameters near boundaries, weakly identified models or strongly asymmetric likelihoods.
- **Likelihood-ratio intervals** retain parameter values whose likelihood-ratio statistic does not exceed an appropriate reference cutoff. They can reflect likelihood asymmetry better than a symmetric Wald interval, subject to the model and calibration assumptions.
- **Profile-likelihood intervals** optimise over nuisance parameters for each value of the parameter of interest.
- **Bootstrap intervals** use resampling to approximate an estimator's sampling distribution. The resampling scheme must reflect the actual sampling units, clusters, spatial blocks or design; resampling individual pixels from a spatially dependent raster is generally not a valid shortcut.
- **Design-based intervals** use the sample selection design and corresponding variance estimator. Unequal inclusion probabilities, stratification, clustering and spatially balanced designs require compatible methods.

The method should match the estimator, sampling process and data structure. Do not select an interval method solely because a software package makes it convenient.

## 4. Hypothesis testing

A hypothesis test evaluates data relative to a specified null model. It begins with:

- a **null hypothesis** \(H_0\), which defines the reference condition;
- an **alternative hypothesis** \(H_A\), which defines the departure of interest;
- a test statistic and its reference distribution under \(H_0\);
- a decision rule or significance level \(\alpha\).

For a two-sided test of a mean,

\[
H_0:\mu=\mu_0,\qquad H_A:\mu\ne\mu_0.
\]

A one-sided alternative may be appropriate when the direction is justified before examining the results and is relevant to the question. Choosing the direction after seeing the data changes the inferential procedure and can inflate false-positive risk.

A test statistic standardises the observed departure from the null value relative to its estimated uncertainty. For the one-sample \(t\)-test,

\[
t=\frac{\bar Y-\mu_0}{s/\sqrt n}.
\]

The p-value is the probability, assuming the null model and its assumptions, of obtaining a test statistic at least as extreme as the observed statistic, with extremeness defined by the test. A p-value is not the probability that the null hypothesis is true, nor the probability that the result occurred "by chance alone."

### Example — testing a mean difference

For the synthetic site-change example above, test

\[
H_0:\mu_d=0,\qquad H_A:\mu_d\ne0.
\]

The test statistic is \(t=2.4/0.6=4.0\) with 24 degrees of freedom. The two-sided p-value is approximately 0.00053. Under the specified independent normal-difference model, this is strong evidence against a zero mean difference. The estimated difference and its interval remain important: the p-value alone does not describe effect magnitude or operational importance.

## 5. Type I error, Type II error and power

A test procedure can make two kinds of error:

| Reality | Reject \(H_0\) | Fail to reject \(H_0\) |
|---|---|---|
| \(H_0\) is true | Type I error | Correct non-rejection |
| \(H_A\) is true | Correct rejection | Type II error |

- **Type I error:** reject a true null hypothesis. Its probability under the null is the test's size; a level-\(\alpha\) test controls this probability at or below \(\alpha\), under its assumptions.
- **Type II error:** fail to reject the null under a particular alternative. Its probability is denoted \(\beta\) and depends on the actual parameter value and test procedure.
- **Power:** probability of rejecting the null under a specified alternative; \(1-\beta\).

Power is not a single universal property of a test. It varies with effect size, sample size, variability, design, significance level, dependence and the alternative parameter value.

A useful sample-size plan specifies the smallest effect that would matter, the desired Type I error rate, the desired power at that effect, the variance or event-rate assumptions, and the sampling design. A formula based on independent observations is not a valid spatial survey design if clustering or unequal inclusion probabilities materially change the variance.

Failure to reject \(H_0\) is not proof that the null is true. If the interval is wide, the data may be compatible with both negligible and important effects. To support equivalence or non-inferiority, define an appropriate margin in advance and use a procedure designed for that question; a non-significant difference test is not an equivalence test.

## 6. Confidence intervals and tests are connected

For a two-sided test and a confidence interval constructed using the same model, estimator and standard error procedure, the null value is rejected at significance level \(\alpha\) exactly when it lies outside the corresponding \(100(1-\alpha)\%\) confidence interval.

This duality is useful, but only when the interval and test genuinely match. Different variance estimators, tail definitions, multiplicity adjustments or small-sample corrections can break the apparent correspondence.

Intervals often communicate more than a binary reject/fail-to-reject label because they show the range of parameter values compatible with the procedure. They still require context and do not replace a decision about practical consequences.

## 7. Multiple comparisons and spatial maps

Spatial analysis often involves many tests: thousands of raster cells, many land-cover classes, multiple time periods, candidate covariates, neighbourhood sizes or model variants. If each test is conducted at level \(\alpha\), the probability of at least one false positive can become much larger than \(\alpha\).

For \(m\) independent tests, each with Type I error probability \(\alpha\), the probability of at least one false positive is

\[
1-(1-\alpha)^m.
\]

For example, with 100 independent null tests at \(\alpha=0.05\), this probability is approximately 0.994. Spatial tests are rarely independent, so this expression is an illustration rather than a universal map-level false-positive probability.

Common approaches include:

- **Bonferroni:** test each of \(m\) hypotheses at \(\alpha/m\), or adjust p-values by multiplying by \(m\). This controls family-wise error under general dependence, though it can be conservative.
- **Holm procedure:** a step-down family-wise error procedure that is generally at least as powerful as simple Bonferroni while retaining strong family-wise error control under arbitrary dependence.
- **False discovery rate (FDR):** controls the expected proportion of false rejections among all rejections under the method's conditions. It addresses a different error criterion from family-wise control; it does not mean that a fixed percentage of the displayed significant cells are certainly false.
- **Permutation or simulation procedures:** can provide spatially appropriate reference distributions when the null-generation scheme preserves relevant dependence and design structure. The permutation scheme must be justified; arbitrary shuffling destroys spatial structure.

Define the family of hypotheses before examining the results. Report the number of tests, the adjustment method, the dependence assumptions and whether the analysis was confirmatory or exploratory. A visually compelling cluster on an unadjusted significance map may reflect multiplicity, spatial dependence or selective analysis.

## 8. Statistical significance versus practical significance

Statistical significance concerns compatibility with a specified null model under a procedure. Practical significance concerns whether the magnitude of an effect matters for the scientific, operational, environmental, economic or policy question.

A tiny effect can produce a small p-value in a very large sample. A consequential effect can produce a large p-value when data are sparse or noisy. Therefore, report at least:

- the estimated effect in interpretable units;
- an uncertainty interval;
- the sample size and effective sampling structure;
- the test statistic and p-value when a test is relevant;
- the analysis and multiplicity plan;
- the assumptions and diagnostics;
- the practical threshold or decision consequence, if one exists.

For a map, distinguish statistical evidence of a non-zero effect from the magnitude, spatial extent, persistence and operational relevance of that effect. A statistically significant pixel is not automatically a meaningful hotspot, and a non-significant pixel is not proof of no change.

## 9. From inference to decisions

A statistical decision is not identical to a statistical test. A real decision may involve costs of false alarms, missed events, delayed action, unequal consequences across locations, legal constraints and uncertainty about the model itself.

A decision threshold should be chosen with the consequences of errors in view, not inherited automatically from a conventional p-value. In spatial risk mapping, for example, a threshold that triggers field inspection may differ from one that triggers evacuation, regulatory action or capital investment. Those decisions require domain-specific loss functions, operational constraints and accountable review.

Keep separate:
1. **Estimation:** what magnitude is supported by the data?
2. **Uncertainty:** how variable or uncertain is that estimate under the procedure?
3. **Testing:** how compatible are the data with a specified null model?
4. **Decision:** what action is justified given benefits, harms, costs and uncertainty?

A statistical result informs a decision; it does not make the decision automatically.

## 10. Exercises

**A — Confidence interval.** A random sample of 25 independent sites has a mean paired change of 2.4 units and standard deviation 3.0 units. Under the normal paired-difference model, construct a 95% \(t\)-interval.

*Worked guidance:* \(SE=3/\sqrt{25}=0.6\), \(t_{0.975,24}\approx2.064\), giving \([1.162,3.638]\) units. State that the interval relies on the sample and model assumptions.

**B — Hypothesis test.** For the same sample, test \(H_0:\mu_d=0\) against a two-sided alternative. Interpret the result.

*Worked guidance:* \(t=4.0\), \(df=24\), two-sided \(p\approx0.00053\). This is evidence against a zero mean under the model, not a probability that \(H_0\) is true and not a measure of practical importance.

**C — Error types.** A monitoring programme tests whether a wetland's mean seasonal water level has changed. Describe Type I and Type II errors in this context.

*Worked guidance:* Type I: declare a change when the mean has not changed under the defined model. Type II: fail to detect a real change. Their consequences depend on the monitoring and management purpose.

**D — Power planning.** List the information needed before calculating sample size for detecting a meaningful change in a spatial field survey.

*Worked guidance:* Define the target population and estimand; minimum meaningful effect; variance; sampling design and inclusion probabilities; clustering or spatial dependence; significance level; desired power; nonresponse and measurement error; and the planned analysis.

**E — Multiple testing.** A change-detection analysis performs 500 cell-level tests. Explain why interpreting every unadjusted \(p<0.05\) as a confirmed change is unsafe and name two possible controls.

*Worked guidance:* Multiplicity raises the chance of false discoveries; spatial dependence also changes the joint behaviour of tests. Bonferroni or Holm can control family-wise error; an appropriately justified FDR procedure controls a different criterion. The spatial null and dependence structure still need consideration.

**F — Practical significance.** A very large sample produces a mean difference of 0.02 units with \(p<0.001\). What else is needed before calling the difference important?

*Worked guidance:* Report the interval and measurement scale, compare the magnitude with a pre-defined practical threshold, assess measurement validity and design, and explain operational or scientific consequences. A small p-value does not establish importance.

## 11. Connections and next steps

- Previous: [Likelihood and statistical estimation](likelihood-and-statistical-estimation.md).
- [Sampling designs and sampling distributions](sampling-designs-and-sampling-distributions.md): design-based standard errors and inference.
- [Joint distributions, covariance and dependence](joint-distributions-covariance-and-dependence.md): dependence and multivariate uncertainty.
- [Spatial cross-validation](../../methods/spatial-cross-validation.md): validation under spatial structure.
- [Forecast verification](../../methods/forecast-verification.md): uncertainty and evaluation of predictive results.
- [Photogrammetric checkpoint QA](../../implementations/python/photogrammetry-odm/checkpoint_qa.py): descriptive residual statistics are not, by themselves, inferential confidence intervals.
- Next: Bayesian inference and predictive distributions (Module 07).

## References

- Penn State Department of Statistics. [STAT 415 — Introduction to Mathematical Statistics](https://online.stat.psu.edu/stat415/), especially Lessons 9 and 10 on hypothesis tests, p-values, power, confidence intervals and their connection. Open educational course notes; licence and reuse conditions are described by Penn State.
- Wasserstein, R. L., and Lazar, N. A. (2016). “The ASA's Statement on p-Values: Context, Process, and Purpose.” *The American Statistician*, 70(2), 129–133. [https://doi.org/10.1080/00031305.2016.1154108](https://doi.org/10.1080/00031305.2016.1154108). Used for interpretation and limitations of p-values, effect size, transparency and the need to consider study design and context.
- Benjamini, Y., and Hochberg, Y. (1995). “Controlling the False Discovery Rate: A Practical and Powerful Approach to Multiple Testing.” *Journal of the Royal Statistical Society: Series B*, 57(1), 289–300. [JSTOR record](https://www.jstor.org/stable/2346101). Foundational reference for false discovery rate control.

The numerical site-change example and exercises are original synthetic teaching illustrations. No real spatial dataset has been tested and no operational threshold is recommended.

## Evidence and review boundary

Penn State STAT 415 Lessons 9 and 10 were inspected for hypothesis-test structure, p-values, Type I and Type II errors, power, sample-size planning and the connection between confidence intervals and tests. The American Statistical Association statement was inspected for its principles on p-value interpretation, effect size, transparency and the limits of threshold-based decisions. The Benjamini–Hochberg paper is cited as the foundational source for FDR; the module gives an introductory description rather than a full derivation of dependence conditions or procedures.

This is an introductory synthesis, not a comprehensive treatment of survey variance estimation, spatial multiplicity, randomisation inference, equivalence testing or decision theory. No empirical analysis was performed. Spatial dependence, sampling design, measurement quality and the consequences of decisions must be addressed in each real application.
