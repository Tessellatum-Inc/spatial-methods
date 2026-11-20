# Statistical diagnostics, calibration and model criticism

**Module:** 08  
**Domain:** Probability and statistical inference (\`SM-FND-004\`)  
**Level:** Intermediate undergraduate to postgraduate  
**Status:** Initial researched synthesis

## 1. Why model checking is part of modelling

A fitted model is not automatically an adequate model. An optimisation routine can converge, coefficients can be finite, a classifier can achieve high accuracy and a regression can report a large \(R^2\), while the model still fails to represent important structure in the data or gives unreliable predictions.

This module brings together three related but distinct activities:

1. **Diagnostics:** inspect the fitted model, its residuals, assumptions and computational behaviour to identify possible deficiencies.
2. **Calibration:** assess whether predicted probabilities, quantiles or predictive distributions agree with the frequencies and outcomes that materialise.
3. **Model criticism:** decide whether the model's structure, data assumptions and predictive behaviour are adequate for the intended scientific or operational use.

These activities overlap, but none replaces the others. A model can be well calibrated on average yet fail to distinguish locations with different risk. It can discriminate well but systematically overstate probabilities. It can fit observed data closely but predict poorly outside the training sample.

The central discipline is to ask **what claim is being checked, against which data, at what spatial and temporal support, and under which assumptions?**

## 2. In-sample fit, residuals and out-of-sample performance

Let observations be \(y_i\), predictors be \(x_i\), and fitted predictions be \(\hat y_i\). For a regression model, the raw residual is

\[
e_i=y_i-\hat y_i.
\]

A residual is an observed response minus a fitted value. It is not the unobservable model error itself. Residuals are constrained by the fitting procedure and may have different variances across observations.

For a binary classifier, the outcome \(y_i\) may be 0 or 1 while the model predicts a probability \(\hat p_i\). The probability residual \(y_i-\hat p_i\) is useful in some diagnostics, but classification models also need diagnostics appropriate to their likelihood and probability outputs.

**In-sample fit** describes agreement with the data used to estimate the model. **Out-of-sample performance** describes how well predictions perform on observations not used to fit or select the model. A model with many parameters can fit training data extremely well and still generalise poorly.

Keep three datasets or roles distinct where the workflow requires them:

- **Training data:** fit model parameters.
- **Validation or calibration data:** select model settings, compare candidates or fit a calibration transformation.
- **Final test data:** estimate performance after modelling decisions are complete.

When data are scarce, resampling can support these roles, but all preprocessing, feature selection, imputation, hyperparameter tuning and calibration must occur inside the appropriate training folds. The final test data must not influence the fitted model or its calibration.

For spatial data, random row-wise splitting can leak information when nearby observations share spatial structure, overlapping imagery, common acquisition conditions or duplicated source features. Choose spatial, temporal or grouped splits that match the intended transfer: to new locations, new regions, new times, new sensors or another clearly defined deployment setting.

## 3. Regression diagnostics

No single statistic can certify a regression model. Residual plots are useful because they expose structure that a compact score can hide.

### 3.1 Functional form and omitted structure

Plot residuals against:

- fitted values;
- each predictor;
- plausible omitted predictors;
- time or acquisition order;
- spatial coordinates or mapped locations;
- groups, sensors, platforms or collection campaigns.

A systematic curve can indicate a missing nonlinear term or an inappropriate functional form. A cluster or step can indicate an omitted group effect, regime change or data-processing issue. A spatial pattern can indicate unmodelled spatial structure, missing geographic predictors or a support mismatch.

A structureless residual plot is reassuring for the feature being examined, but it does not prove the model is correct. A plot can have low power when the sample is small or the fitted model is highly flexible.

### 3.2 Non-constant variance

A funnel-shaped residual plot may indicate heteroscedasticity: residual variance changes with predictors or fitted values. Consequences depend on the model and objective. In ordinary least squares, heteroscedasticity can make conventional standard errors and tests unreliable even when coefficient estimates remain unbiased under the relevant exogeneity assumptions. Prediction intervals can also be poorly scaled.

Possible responses include modelling the variance, using a justified transformation, weighted least squares when weights represent the variance structure, or robust uncertainty estimates. Do not select a transformation merely to make a diagnostic plot look tidy; preserve interpretability and validate predictive performance.

### 3.3 Dependence and spatial residual structure

Residual autocorrelation across time or space can indicate that the conditional-independence assumptions are inadequate. For spatial data, map residuals and inspect them against distance, neighbourhood or spatial support. Depending on the problem, use a variogram, a spatial autocorrelation statistic, residual correlograms or model-specific simulation diagnostics.

A residual spatial pattern is evidence that something remains structured; it does not uniquely identify the cause. Possible causes include omitted covariates, spatially varying coefficients, an unsuitable covariance model, nonstationarity, measurement artefacts, sampling design or mismatched spatial units.

Do not automatically add a spatial random effect. First establish what spatial process and prediction target the model is meant to represent.

### 3.4 Distributional assumptions and influential observations

A normal Q–Q plot can help assess whether Gaussian residual assumptions are plausible for a model that relies on them. Normality is not a universal requirement for useful prediction, and a Q–Q plot should not be used as a generic pass/fail test for every model.

Inspect leverage and influence where appropriate. High leverage describes unusual predictor configurations; influence describes how much a fitted result changes when an observation is removed or perturbed. Cook's distance and related measures are diagnostics, not automatic deletion rules. An unusual observation may be a data error, a rare but valid event, a boundary case or evidence that the model is incomplete.

Check data provenance and the physical context before removing or downweighting observations. Report sensitivity to influential records when they materially affect conclusions.

### 3.5 Model-family-specific residuals

Raw residuals are not equally appropriate for every likelihood. Generalised linear models may use Pearson, deviance or other residuals; count models may require checks for overdispersion and excess zeros; survival models require diagnostics that respect censoring; hierarchical models may require conditional and marginal checks.

The diagnostic must correspond to the fitted model and the question. A normality test on raw binary outcomes, for example, is not a meaningful validation of a Bernoulli likelihood.

## 4. Classification: discrimination is not calibration

A classifier may return a class label or a probability. These are different outputs.

**Discrimination** concerns whether the model tends to assign higher scores to positive cases than to negative cases. ROC curves and AUC are common discrimination summaries.

**Calibration** concerns whether predicted probabilities agree with observed event frequencies. If a model assigns probability near 0.8 to a sufficiently large group of comparable cases, roughly 80% of those cases should experience the event for the forecasts to be calibrated at that level.

A model can have good AUC and poor calibration, or reasonable calibration and weak discrimination. A classification threshold such as 0.5 converts probabilities into labels for a particular decision rule; it does not determine whether the probabilities themselves are reliable.

### 4.1 Reliability diagrams

A reliability diagram groups predictions into bins and compares the mean predicted probability in each bin with the observed event fraction.

| Mean predicted probability | Observed event fraction | Number of cases |
|---:|---:|---:|
| 0.10 | 0.08 | 100 |
| 0.30 | 0.25 | 100 |
| 0.50 | 0.48 | 100 |
| 0.70 | 0.75 | 100 |
| 0.90 | 0.92 | 100 |

These are **synthetic teaching values**, not model results. The points lie near the ideal diagonal, with slight under- or over-prediction in different ranges. A real diagram should show bin counts and, where possible, uncertainty bands. Sparse bins can produce unstable observed fractions. Different binning choices can change the appearance.

A global reliability diagram may conceal local miscalibration. For spatial applications, examine calibration across meaningful regions, environmental conditions, classes, seasons, sensor types and risk ranges when sample size permits. Subgroup analysis itself can be unstable when the number of independent spatial units is small.

### 4.2 Proper scoring rules

For binary outcomes \(y_i\in\{0,1\}\) and predicted probabilities \(p_i\), the Brier score is

\[
\operatorname{BS}=\frac{1}{n}\sum_{i=1}^{n}(p_i-y_i)^2.
\]

Lower values are better for the evaluated sample and event definition. Log loss is

\[
\operatorname{LogLoss}
=-\frac{1}{n}\sum_{i=1}^{n}
\left[y_i\log(p_i)+(1-y_i)\log(1-p_i)\right].
\]

Log loss strongly penalises confident wrong predictions. In practice, probabilities may need numerical clipping for computation, but clipping must be documented and should not conceal model failures.

Brier score and log loss are **proper scoring rules**: in expectation, they reward reporting honest probabilities under the relevant conditions. They combine aspects of calibration, discrimination or resolution, and outcome uncertainty. A single overall score does not isolate calibration. Pair scores with reliability diagrams and suitable discrimination measures.

Accuracy, precision, recall and F-scores depend on a selected class threshold and class prevalence. They may be useful for operational decisions, but they do not evaluate probability calibration.

### 4.3 Calibration methods

A calibration model transforms the scores or probabilities from an existing model. Common approaches include:

- **Sigmoid / logistic calibration:** fits a logistic mapping from model scores to observed outcomes.
- **Isotonic regression:** fits a non-decreasing flexible mapping and can capture non-linear calibration patterns.
- **Other model-specific methods:** may be appropriate when the prediction structure and data volume justify them.

Calibration is another fitted model. Fit it using a dedicated calibration set or cross-validation within the training data. Do not fit a calibrator on the final test set and then report performance on that same set as independent evaluation. Flexible calibrators can overfit, particularly with few independent events.

Calibration does not fix poor discrimination, missing predictors, biased sampling, class-label errors or spatial leakage. It adjusts probability mapping under the conditions represented by its calibration data. If deployment conditions change, calibration may drift.

## 5. Predictive distributions: calibration, sharpness and coverage

A probabilistic forecast is more than a point estimate. It may be a predictive distribution, a set of quantiles, an ensemble or a prediction interval.

Two important properties are:

- **Calibration:** statistical agreement between the predictive distributions and the outcomes that occur.
- **Sharpness:** concentration of the predictive distributions; it is a property of the forecasts themselves.

A very wide interval can achieve high empirical coverage but be uninformative. A very narrow interval can be sharp but systematically miss observations. The goal is useful sharpness subject to adequate calibration, not narrow intervals at any cost.

### 5.1 Interval coverage and width

For nominal \(100(1-\alpha)\%\) prediction intervals \([L_i,U_i]\), empirical coverage is

\[
\widehat C=
\frac{1}{n}\sum_{i=1}^{n}
\mathbb{1}(L_i\le y_i\le U_i).
\]

Mean interval width is

\[
\overline W=
\frac{1}{n}\sum_{i=1}^{n}(U_i-L_i).
\]

Suppose 100 independent held-out cases are evaluated with nominal 90% prediction intervals. If 84 observations fall inside their intervals, empirical coverage is 84%, below the nominal level. This is a **synthetic illustration**. It is not enough to conclude that the model is miscalibrated without considering sampling uncertainty, dependence, the evaluation design and subgroup behaviour.

Coverage should be assessed at more than one nominal level where possible. Also inspect conditional coverage by predicted magnitude, location, time, class or other meaningful strata. Marginal coverage can hide severe local failures.

### 5.2 Probability integral transform

For a continuous predictive cumulative distribution function \(F_i\) and observed outcome \(y_i\), the probability integral transform is

\[
u_i=F_i(y_i).
\]

Under ideal probabilistic calibration and the relevant regularity conditions, PIT values should be approximately uniform. Systematic deviations can indicate bias or dispersion errors. For discrete outcomes, the ordinary PIT is not continuous-uniform; use a randomized PIT or rank-based diagnostics appropriate to the forecast representation.

A PIT histogram is a diagnostic, not a complete model test. Aggregated PIT values can hide conditional or spatial miscalibration. Inspect them alongside maps, time plots, subgroup diagnostics and proper scores.

### 5.3 Scoring predictive distributions

For continuous outcomes, common measures include the continuous ranked probability score (CRPS), log score, quantile or pinball loss, interval score and proper scoring rules for ensembles. Choose scores that match the target functional and decision.

For a predictive distribution \(F\) and observation \(y\), CRPS can be expressed as

\[
\operatorname{CRPS}(F,y)=
\int_{-\infty}^{\infty}
\left(F(z)-\mathbb{1}(z\ge y)\right)^2\,dz.
\]

Lower CRPS is better for the evaluated forecasts. It rewards distributions that place probability near the observed outcome while accounting for their spread. For a quantile forecast \(\hat q_\tau\), pinball loss is

\[
\rho_\tau(y-\hat q_\tau)
=(y-\hat q_\tau)\left(\tau-\mathbb{1}(y<\hat q_\tau)\right).
\]

Do not compare scores across different target variables, units, event definitions or evaluation samples without a defensible normalisation and explanation.

## 6. Spatial and temporal validation

Validation design determines what kind of generalisation a score can support.

- Random holdout estimates performance on randomly withheld records under that sampling mechanism.
- Spatial block validation assesses transfer to withheld geographic blocks, with block size and geometry chosen for the spatial dependence and deployment question.
- Leave-region-out validation asks about transfer to new regions.
- Temporal validation tests future periods using only information available at forecast time.
- Grouped validation can hold out entire campaigns, sensors, sites, platforms or source entities to prevent related observations crossing partitions.

There is no universal best split. A split that is appropriate for interpolation within a well-sampled region may be inappropriate for extrapolation to a new region. Spatial block size is a design decision, not a magic distance.

### Leakage and preprocessing

Any transformation that learns from data must be fitted within the training portion of each validation fold. This includes normalisation, imputation, feature selection, dimensionality reduction, resampling, hyperparameter tuning and probability calibration.

If a raster is tiled into overlapping patches, random patch splitting can place near-duplicates or overlapping source pixels in both training and test sets. Split by the original scene, acquisition, site or geographic block when that matches the deployment target.

A validation score is only interpretable when the held-out units are sufficiently independent for the uncertainty calculation or when the dependence is explicitly accounted for. Treating thousands of correlated pixels as thousands of independent test cases can produce misleadingly narrow confidence intervals.

## 7. A practical model-criticism workflow

A defensible review is iterative and records the reason for each change.

1. **Define the target:** population, spatial support, time horizon, outcome, prediction target and intended decision.
2. **Audit the data:** labels, units, CRS, spatial alignment, missingness, sampling frame, measurement error, provenance and duplicates.
3. **Establish a baseline:** compare with a simple reference model, climatology, majority class or operational baseline appropriate to the problem.
4. **Fit the candidate:** document features, likelihood, loss, priors, hyperparameters, software and random seeds where relevant.
5. **Inspect fit diagnostics:** residual patterns, functional form, variance, dependence, leverage, influence and model-family-specific checks.
6. **Evaluate held-out performance:** use spatial, temporal or grouped validation that matches the intended transfer.
7. **Check calibration:** reliability diagrams, probability scores, interval coverage, PIT or rank diagnostics as appropriate.
8. **Inspect conditional behaviour:** map errors and scores; examine regions, classes, times, exposure levels and relevant subgroups.
9. **Conduct sensitivity analysis:** test reasonable alternative specifications, priors, features, block sizes and data exclusions.
10. **Record limitations and decision implications:** state where the model is supported, where it is uncertain, what it cannot establish and when it must be re-evaluated.

Model refinement should respond to evidence, not to a desire to improve a leaderboard score. Changes made after inspecting a test set turn that test set into development data; a new independent test or appropriately nested evaluation is then required.

## 8. Spatial application examples

### Remote-sensing classification

A land-cover classifier produces per-pixel class probabilities. Check confusion matrices and class-specific discrimination, but also calibrate probabilities using independent reference data. If the reference sample is stratified or otherwise unequal-probability, use design-aware estimates when reporting population-level accuracy or calibration. Inspect spatial clusters of errors, class boundaries, acquisition conditions and uncertainty in reference labels. A visually smooth probability map is not evidence of calibrated probabilities.

### Environmental interpolation

A spatial regression predicts air temperature or soil moisture. Inspect residuals against predictors, time, elevation and coordinates; examine residual spatial dependence; and compare predictive distributions against withheld stations or spatial blocks. Pointwise RMSE alone does not show whether prediction intervals are calibrated or whether errors are concentrated in particular terrain or climate zones.

### Flood or hazard forecasting

A model estimates probabilities of exceedance or predictive distributions of water level. Define the event threshold and forecast horizon precisely. Check reliability by lead time and region, discrimination, proper scores, interval coverage and sharpness. A model can be well calibrated for common low-impact events and poor for rare extremes; the evaluation should reflect the decision consequences and scarcity of extreme observations.

These examples describe evaluation logic, not validated models or operational recommendations.

## 9. Exercises

**A — Residual interpretation.** A regression residual plot shows a curved pattern against elevation and a funnel shape against fitted values. Identify two possible model problems and describe a responsible next step.

*Worked guidance:* The curve suggests functional-form misspecification or omitted structure; the funnel suggests non-constant variance. Inspect the data and model specification, then consider a scientifically defensible nonlinear mean or variance model and re-evaluate on held-out data. Do not choose a transformation solely to make the plot look random.

**B — Calibration versus discrimination.** Two classifiers have similar AUC, but one assigns probabilities that are systematically too high. Which diagnostics would reveal the issue?

*Worked guidance:* A reliability diagram and probability scoring rules such as Brier score or log loss assess probabilistic performance. AUC primarily measures ranking/discrimination and cannot establish calibration.

**C — Reliability table.** Interpret the five synthetic probability bins in Section 4.1. Why should bin counts and uncertainty be shown?

*Worked guidance:* The observed event fractions broadly track predicted probabilities, but individual bins show small deviations. Counts reveal support; uncertainty bands help distinguish stable departures from sampling noise. Binning can conceal within-bin variation and results depend on bin construction.

**D — Prediction interval review.** A nominal 90% interval covers 84 of 100 independent test observations. State what can and cannot be concluded.

*Worked guidance:* Empirical coverage is 84% in this sample, below nominal. It raises a calibration concern but does not by itself prove systematic undercoverage; assess sampling uncertainty, conditional coverage, the evaluation design and interval widths.

**E — Spatial leakage.** An image classifier is evaluated by randomly splitting overlapping image patches. Explain why its reported test score may be optimistic and propose a stronger split.

*Worked guidance:* Overlapping patches or patches from the same scene may share pixels, objects and acquisition artefacts across train and test. Split by original scene, acquisition or geographic block to match the intended transfer.

**F — PIT interpretation.** A continuous predictive model produces a strongly non-uniform PIT histogram. What might this indicate, and what should be inspected next?

*Worked guidance:* Potential bias, dispersion error or other predictive-distribution misspecification. Inspect forecast magnitudes, time and space, subgroup behaviour, data quality and the predictive model. PIT is not a unique diagnosis.

**G — Influence.** A high-leverage observation strongly changes a regression coefficient. Should it be deleted?

*Worked guidance:* Not automatically. Verify the record, understand its physical context, assess whether it belongs to the target population and report sensitivity. It may be valid evidence of a model limitation or rare condition.

**H — Model review.** A spatial model has low random-holdout RMSE but much higher leave-region-out RMSE. Explain the difference.

*Worked guidance:* The model may interpolate well among nearby observations but transfer poorly to new regions. The relevant score depends on deployment; report both only with clear interpretations and do not claim regional generalisation from random holdout alone.

## 10. Connections and next steps

- Previous: [Bayesian inference and predictive distributions](bayesian-inference-and-predictive-distributions.md).
- [Spatial cross-validation](../../methods/spatial-cross-validation.md): validation under spatial dependence and geographic transfer.
- [Forecast verification](../../methods/forecast-verification.md): probabilistic and deterministic forecast evaluation.
- [Classification, regression, retrieval and calibration metrics](../../implementations/python/accuracy-assessment/README.md): existing computational metrics and stated boundaries.
- [Measurement uncertainty and Type A/Type B evaluation](../measurement-science/standard-uncertainty-type-a-type-b.md): distinguish model prediction uncertainty from measurement uncertainty.
- [Spatial statistics and stochastic processes](../spatial-statistics/README.md): specialised spatial dependence and stochastic-process models.

## References

- NIST/SEMATECH. [How can I tell if a model fits my data?](https://itl.nist.gov/div898/handbook/pmd/section4/pmd44.htm). Engineering Statistics Handbook, Process Modeling, Section 4.4.4. Inspected for residual analysis, the limits of \(R^2\), and graphical model validation.
- scikit-learn developers. [Probability calibration](https://scikit-learn.org/stable/modules/calibration.html). Official documentation. Inspected for reliability diagrams, calibration methods and the interpretation of proper scores.
- Gneiting, T., Wolffram, D., Resin, J., Kraus, K., Bracher, J., et al. (2023). [Model Diagnostics and Forecast Evaluation for Quantiles](https://doi.org/10.1146/annurev-statistics-032921-020240). *Annual Review of Statistics and Its Application*, 10, 597–621. Used for calibration, conditional calibration, sharpness and forecast evaluation.

The examples and reliability table are synthetic teaching illustrations. No empirical dataset was fitted or evaluated for this module. The module does not certify a model, dataset, map, forecast or operational decision.

## Evidence and review boundary

The NIST handbook material was inspected for residual-based model validation, limitations of \(R^2\), non-constant variance and model refinement. The scikit-learn documentation was inspected for probability calibration, reliability diagrams and the interpretation of Brier and log-loss scores. The 2023 review was inspected for probabilistic calibration, conditional calibration, sharpness and forecast evaluation.

This module is an introductory synthesis. Diagnostic plots and metrics are not automatic pass/fail tests. Their interpretation depends on the model family, data-generating process, sample design, spatial and temporal dependence, and intended use. Spatial validation and design-based accuracy assessment require methods suited to the target population and sampling design. Independent technical review, learner testing and application-specific validation remain outstanding.
