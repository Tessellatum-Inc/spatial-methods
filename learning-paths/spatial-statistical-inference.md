# Spatial statistical inference: from real-world question to defensible result

**Purpose:** Connect probability and statistical inference to the design, collection, analysis, validation and communication of spatial evidence.

**Status:** Initial applied pathway published. It links existing foundations, methods, collection guidance, recipes and implementations; it is not yet a completed end-to-end empirical case study.

## Why this path exists

A spatial analysis is not defensible merely because a statistical function ran or a map looks plausible. The conclusion depends on what was measured, which places and times could enter the study, how observations were selected, what spatial units they represent, which model was used and how the result was checked.

This pathway connects the eight modules in [Probability and statistical inference](../foundations/probability-and-statistics/README.md) to the wider Spatial Methods collection. It follows the logic of a study rather than treating statistical techniques as a menu of independent tools. This is consistent with the geospatial production perspective in the UNECE [Geospatial View of the Generic Statistical Business Process Model](https://statswiki.unece.org/spaces/GSBPM/pages/312476034/GeoGSBPM) and with the staged geospatial analysis workflow described by the [Interstate Technology & Regulatory Council (ITRC)](https://gro-1.itrcweb.org/geospatial-analysis-work-flow-overview/).

You do not have to follow every branch. Choose the route that matches the question and return to shared stages when needed.

## What you should be able to do

By the end of a completed project through this path, you should be able to:

- turn a broad geographic question into a defined population, spatial support, estimand and decision;
- explain how observations were generated, selected, measured and filtered;
- distinguish sampling uncertainty, measurement uncertainty, model uncertainty and predictive uncertainty;
- select an inferential method that matches the response, design, dependence and intended use;
- diagnose model limitations and validate against the geographic and temporal task the result is meant to support;
- communicate estimates, uncertainty, assumptions and evidence boundaries without overstating what the map proves;
- preserve enough provenance and computational detail for another person to reproduce and challenge the analysis.

## The shared workflow

### 1. Define the question before choosing a statistic

Write a short study specification before opening a modelling tool.

1. **Question:** What do you want to describe, estimate, explain, predict or decide?
2. **Target population:** Which places, objects, people, events or time periods does the conclusion concern?
3. **Unit and support:** Is the observation a point, pixel, plot, building, road segment, event, grid cell or administrative area? What is its spatial footprint and time window?
4. **Estimand:** What population quantity is wanted—a mean, total, proportion, rate, contrast, spatial intensity, regression parameter or prediction at an unsampled location?
5. **Decision context:** Who may use the result, what action could follow, and what error would matter?
6. **Geography and time:** Define the study boundary, coordinate reference system, spatial resolution, temporal coverage and relevant boundaries.

Do not confuse a statistic calculated from the available rows with an estimand for the target population. A map aggregation can change the question: point, pixel and area-level quantities are not interchangeable.

**Foundation:** [Module 01 — probability models, events and conditioning](../foundations/probability-and-statistics/probability-models-events-and-conditioning.md), [Module 02 — random variables and distributions](../foundations/probability-and-statistics/random-variables-and-distributions.md), and [Module 04 — sampling designs and sampling distributions](../foundations/probability-and-statistics/sampling-designs-and-sampling-distributions.md).

**Checkpoint:** Can you state the target population, unit, spatial support, time window and estimand in one paragraph? If not, the analysis question is not yet ready.

### 2. Understand how the observations came to exist

Treat data acquisition as part of the statistical model, not as a preliminary administrative task.

Record:

- the source, instrument, sensor, platform or reporting process;
- the sampling frame and how it covers—or fails to cover—the target population;
- the selection mechanism and inclusion probabilities, where applicable;
- measurement procedures, calibration, control, geolocation and reference systems;
- spatial and temporal resolution, aggregation and positional support;
- missing observations, nonresponse, inaccessible locations, detection limits and exclusions;
- transformations, joins, geocoding and processing applied before analysis.

A large dataset can still be biased. A probability sample from an incomplete frame does not represent omitted units automatically. More nearby pixels do not necessarily provide the information of more independent locations. Convenience replacements can alter the sampling design.

**Collection and measurement links:**
- [Spatial Data Collection](../collection/README.md)
- [Photogrammetric image acquisition](../collection/photogrammetry/image-acquisition.md)
- [Measurement science and survey adjustment](measurement-science-and-survey-adjustment.md)
- [Measurement models and measurand definition](../foundations/measurement-science/measurement-models-and-measurand-definition.md)
- [Standard uncertainty: Type A and Type B evaluation](../foundations/measurement-science/standard-uncertainty-type-a-type-b.md)

**Checkpoint:** Could another analyst explain which real-world units had a chance to be observed, which did not, and how the recorded values were produced?

### 3. Design collection and validation for the intended inference

Sampling design and model validation are related but distinct.

- **Collection design** determines which units are observed and supports inference to a target population.
- **Model validation design** determines which observations are withheld to assess performance for a specified prediction or deployment task.
- **Independent reference data** support an external assessment only when they were not used to fit, tune, calibrate or select the model being evaluated.

Choose the design to match the estimand and practical constraints. Consider stratification, spatial balance, clustering, unequal inclusion probabilities, nonresponse, travel cost, safety, temporal repetition and the precision needed for important subgroups. Define validation geography and time before model fitting.

Do not assume that random row splitting is appropriate for spatial data. Equally, do not use spatial blocks automatically: the split must represent the intended prediction task. Interpolation within a sampled region, transfer to a new region and forecasting a future period are different tasks.

**Relevant material:**
- [Module 04 — sampling designs and sampling distributions](../foundations/probability-and-statistics/sampling-designs-and-sampling-distributions.md)
- [Spatial cross-validation](../methods/spatial-cross-validation.md)
- [Photogrammetric mapping recipe](../recipes/photogrammetric-mapping/README.md)
- [Survey-to-spatial-dataset recipe](../recipes/survey-to-spatial-dataset/README.md)

**Checkpoint:** Is the collection design capable of supporting the population claim, and does the validation design reproduce the intended use of the model?

### 4. Audit and explore before fitting

Start with data integrity and the observation process, then explore both statistical and geographic structure.

**Data and geometry checks**
- row counts, unique identifiers, duplicate and conflicting records;
- missingness, impossible values, units and category definitions;
- geometry validity, coordinate reference system, axis order and distance units;
- temporal alignment, spatial joins, boundary effects and support mismatch;
- source lineage, processing history and reproducible filters.

**Exploratory checks**
- maps of observations and missingness;
- distributions, quantiles, outliers and subgroup summaries;
- relationships with candidate predictors;
- trends over space and time;
- clustering, neighbourhood structure and spatial dependence;
- sample density and gaps relative to the target geography.

An unusual value may be a data error, a real extreme event or a meaningful local condition. Investigate it before excluding it. A normal-looking histogram does not establish independence, and exploratory patterns do not by themselves establish a causal explanation.

**Methods to explore:**
- [Spatial autocorrelation and hotspots](global-spatial-autocorrelation.md)
- [Point-pattern foundations](point-pattern-foundations.md)
- [Empirical semivariogram](../methods/empirical-semivariogram.md)

**Checkpoint:** Can you describe what the sample contains, where it is sparse or unrepresentative, and which features of the data may challenge the proposed model?

### 5. Choose the inferential model to match the estimand

Do not select a model because it is familiar or because it produces a visually smooth map. Match the method to the response, target, observation process and assumptions.

| Question or data structure | Candidate approach | Important boundary |
|---|---|---|
| Population mean, total or proportion from a probability sample | Design-based estimation and design-consistent variance | Respect inclusion probabilities, strata, clusters and nonresponse adjustments |
| Continuous response with predictors | Regression and likelihood-based estimation | Examine functional form, residual dependence, heteroscedasticity and confounding |
| Correlated measurement observations | Covariance modelling and generalized least squares | The covariance model must reflect the observation process; a successful solver does not validate it |
| Values at unsampled locations | Interpolation or geostatistical prediction | Distinguish deterministic estimates from model-based uncertainty |
| Areal values with neighbourhood structure | Spatial regression or spatial statistics | Weights, support, scale and dependence assumptions are part of the model |
| Event locations | Point-pattern summaries or point-process models | Define the observation window, event process, intensity variation and null model |
| Counts by area or time | Count models with exposure and observation effort | Check overdispersion, excess zeros, clustering and varying exposure |
| Binary or multiclass map predictions | Classification evaluation and probability calibration | Class balance, sampling design, spatial leakage and calibration all matter |
| Uncertain parameters or predictive quantities | Frequentist or Bayesian inference | State the model, prior or repeated-sampling interpretation and sensitivity checks |

**Foundations:**
- [Module 03 — joint distributions, covariance and dependence](../foundations/probability-and-statistics/joint-distributions-covariance-and-dependence.md)
- [Module 05 — likelihood and statistical estimation](../foundations/probability-and-statistics/likelihood-and-statistical-estimation.md)
- [Module 06 — confidence intervals, hypothesis tests and statistical decisions](../foundations/probability-and-statistics/confidence-intervals-hypothesis-tests-and-statistical-decisions.md)
- [Module 07 — Bayesian inference and predictive distributions](../foundations/probability-and-statistics/bayesian-inference-and-predictive-distributions.md)
- [Covariance, correlated observations and generalized least squares](../foundations/measurement-science/covariance-correlated-observations-and-gls.md)

**Computational companions:**
- [Covariance and GLS implementation](../implementations/python/covariance-gls/README.md)
- [Matrix factorization companion and integrated case](../implementations/python/matrix-factorizations/README.md)
- [Accuracy-assessment metrics](../implementations/python/accuracy-assessment/README.md)

**Checkpoint:** Can you explain why this model answers the stated question better than a simpler alternative, and list the assumptions that would change the conclusion if they failed?

### 6. Diagnose, compare and validate

Use several forms of evidence. No single diagnostic or score proves that a model is correct.

1. **Numerical and structural checks:** convergence, rank, conditioning, parameter boundaries, residual degrees of freedom and reproducibility.
2. **In-sample diagnostics:** residual patterns, influential observations, heteroscedasticity, dependence, spatial structure and model misspecification.
3. **Predictive evaluation:** holdout errors, proper scoring rules, calibration, interval coverage and sharpness where relevant.
4. **Geographic and temporal evaluation:** compare performance across regions, classes, scales, seasons, acquisition campaigns and deployment conditions.
5. **Sensitivity analysis:** vary defensible modelling choices, spatial weights, block sizes, buffers, covariance structures, thresholds and priors.
6. **External checks:** use independent reference observations or domain knowledge where available; record what is and is not independent.

Keep all learned preprocessing, feature selection, imputation, calibration and tuning inside the training data. If validation results influence model selection, they are no longer an untouched final test. Report failed fits and unstable results rather than silently discarding them.

**Relevant material:**
- [Module 08 — statistical diagnostics, calibration and model criticism](../foundations/probability-and-statistics/statistical-diagnostics-calibration-and-model-criticism.md)
- [Spatial cross-validation](../methods/spatial-cross-validation.md)
- [Forecast verification](../methods/forecast-verification.md)
- [Photogrammetric checkpoint QA implementation](../implementations/python/photogrammetry-odm/README.md)

**Checkpoint:** Does the validation design answer the deployment question, and are the reported uncertainties and scores appropriate to that design?

### 7. Interpret the result at the scale of the evidence

A result should communicate more than a colour ramp or a p-value.

Report, as appropriate:
- the estimand and estimate, with units and target geography;
- uncertainty intervals or predictive distributions and what they mean;
- effect sizes and practical consequences, not only significance;
- sample sizes, inclusion weights and design limitations;
- spatial and temporal variation in performance;
- model assumptions, diagnostics, sensitivity and known failure regions;
- the distinction between association, prediction and causal effect;
- what the model cannot support.

For maps of local tests, consider multiple comparisons and spatial dependence. For classification maps, distinguish pixel-count metrics from design-based, area-adjusted estimates. For interpolation, distinguish model-based prediction variance from observed prediction error. For survey measurements, distinguish formal covariance from external accuracy evidence.

**Checkpoint:** Could a decision-maker understand what is known, how uncertain it is, where it may fail and what additional evidence would change the decision?

### 8. Preserve the analysis as a reproducible study

A defensible project record should preserve:

- question, target population, estimand and decision context;
- source versions, licences, dates and raw-data fingerprints;
- coordinate and vertical reference systems, units and spatial support;
- collection and sampling protocol, inclusion probabilities and nonresponse;
- data cleaning, exclusions, transformations and feature construction;
- model specification, parameters, software versions and random seeds;
- training, tuning, calibration and validation splits;
- diagnostics, sensitivity analyses, uncertainty and limitations;
- outputs, figures, interpretation and unresolved questions.

Keep original observations immutable where possible. Separate source data, derived data, code, configuration and final outputs. A notebook that only runs on one person's machine is not a complete reproducibility record.

## Choose an applied route

The shared workflow above is adapted to three different kinds of spatial evidence. Choose one route for a first project; the routes are alternatives, not consecutive levels.

### Route A — Field measurements and survey-derived spatial data

**Question type:** How well do measured positions, elevations or reconstructed surfaces represent the real-world quantities of interest?

1. Define the measurand, reference system, spatial extent and fitness-for-purpose requirement.
2. Understand acquisition geometry, instruments, control and independent checks.
3. Model measurement uncertainty and correlation where justified.
4. Adjust or process observations using a method appropriate to the observation equations and covariance.
5. Assess residuals and numerical conditioning.
6. Compare final products with independent checkpoints or reference observations.
7. Report coordinate and height reference, residual convention, sample distribution and limits.

Start with [Measurement science and survey adjustment](measurement-science-and-survey-adjustment.md), [photogrammetric image acquisition](../collection/photogrammetry/image-acquisition.md) and the [survey-to-spatial-dataset recipe](../recipes/survey-to-spatial-dataset/README.md). For a concrete processing companion, inspect the [ODM runner and checkpoint QA](../implementations/python/photogrammetry-odm/README.md). The [matrix-factorization integrated case](../implementations/python/matrix-factorizations/integrated-case.md) demonstrates affine control, terrain-plane estimation, GLS and SVD diagnostics using synthetic values.

**Evidence boundary:** the integrated matrix case is synthetic. The ODM companion has not been demonstrated on a real image dataset in this repository. Neither is field accuracy evidence or a substitute for competent survey design and review.

### Route B — Map accuracy and classification assessment

**Question type:** How accurately does a classified map represent a defined target population and geography?

1. Define the map date, class definitions, target area and population quantity to estimate.
2. Design a reference sample that supports the intended overall and class-specific estimates.
3. Preserve reference labels, interpretation rules, spatial and temporal matching and uncertainty.
4. Calculate confusion-matrix metrics and class-level performance.
5. Where the sample design requires it, use design-consistent weights and area-adjusted estimation rather than treating raw sample proportions as map-area proportions.
6. Examine classwise calibration if the map provides probabilities.
7. Report sampling uncertainty, class imbalance, reference limitations and geographic variation.

Use [Module 04 — sampling designs](../foundations/probability-and-statistics/sampling-designs-and-sampling-distributions.md), the [count-based accuracy-assessment metrics](../implementations/python/accuracy-assessment/README.md), the new [area-adjusted map accuracy method](../methods/area-adjusted-map-accuracy.md) and its [Python implementation and tests](../implementations/python/area-adjusted-accuracy/README.md), plus [spatial cross-validation](../methods/spatial-cross-validation.md). Complete the [learner exercise](../implementations/python/area-adjusted-accuracy/exercise.md) and use the [assessment report template](../implementations/python/area-adjusted-accuracy/report-template.md) to communicate the result.

**Evidence boundary:** the new implementation supports only independent simple random sampling within mapped-class strata. It does not support arbitrary unequal-probability, cluster, general systematic or spatially balanced designs. Its reference labels are treated as correct, and its intervals are normal-approximation teaching baselines.

### Route C — Spatial prediction and environmental patterns

**Question type:** What values or risks are expected at unsampled locations, and how well do predictions transfer across space or time?

1. Define the prediction target, support, prediction horizon and decision use.
2. Examine the observation process, spatial coverage, covariates and missingness.
3. Explore trends, clustering, anisotropy and dependence.
4. Compare an appropriate baseline with spatially structured alternatives.
5. Estimate model parameters and spatial covariance where required.
6. Validate using folds or independent data that reflect the prediction geography and time.
7. Map predictions and uncertainty separately, and identify areas beyond the evidence.

Choose the relevant branch:
- [Interpolation and geostatistics](interpolation-and-geostatistics.md) for continuous values and unsampled locations.
- [Spatial autocorrelation and hotspots](global-spatial-autocorrelation.md) for areal patterns and neighbourhood relationships.
- [Point-pattern foundations](point-pattern-foundations.md) for event locations and spatial intensity.
- [Forecast verification](../methods/forecast-verification.md) for probabilistic and time-indexed predictions.

**Evidence boundary:** descriptive spatial patterns do not establish causal effects. Prediction uncertainty is conditional on the model and available data; it does not automatically include sampling-frame, measurement, source or structural uncertainty.

## Integrated project: design, analyse and defend a spatial study

Use a real dataset with documented provenance if one is available and suitable. If not, use a clearly labelled synthetic dataset to practise the workflow. Do not present synthetic results as empirical findings.

### Project brief

Choose one question from Route A, B or C. Prepare four linked deliverables:

1. **Study protocol:** question, target population, estimand, unit, support, time, data source, collection design and validation design.
2. **Analysis record:** data audit, exploratory maps and summaries, method choice, assumptions, fitted results and computational details.
3. **Validation record:** diagnostics, independent or held-out evaluation, sensitivity checks and limitations.
4. **Decision brief:** concise findings, uncertainty, geographic applicability, recommended next evidence and what the analysis does not establish.

### Minimum review questions

- Is the target population explicit and covered by the available frame?
- Is the sampling unit consistent with the estimand and spatial support?
- Are measurement and sampling uncertainties distinguished?
- Does the model respect dependence and the observation process?
- Was validation designed before results were inspected?
- Is any data used for fitting or tuning being incorrectly called independent?
- Are maps, metrics and uncertainty statements consistent with the actual validation design?
- Can another analyst reproduce the result from the documented inputs and code?

### Suggested assessment rubric

| Criterion | Points |
|---|---:|
| Question, population, support and estimand | 4 |
| Collection and sampling design | 4 |
| Data audit and exploratory analysis | 3 |
| Method choice and assumptions | 4 |
| Diagnostics, validation and sensitivity | 4 |
| Interpretation, reproducibility and limitations | 4 |
| **Total** | **23** |

A technically sophisticated model cannot compensate for a poorly defined target population or an unsuitable validation design. Reward justified decisions and honest limits, not model complexity.

## How this path connects the four pillars

| Pillar | Contribution to the study |
|---|---|
| **Theoretical Foundations** | Probability, sampling, inference, measurement uncertainty, dependence and model criticism |
| **Spatial Data Collection** | Instruments, sensors, observation processes, sampling frames, field protocols and reference data |
| **Spatial Algorithms** | Estimation, spatial weights, interpolation, point-pattern analysis, regression and validation metrics |
| **Spatial Recipes** | Reproducible end-to-end workflows, quality gates, project records and decision-ready outputs |

The pathway is a connective layer. It does not replace the canonical foundation modules, algorithm pages, collection guidance, implementations or recipes.

## References and review boundary

- United Nations Economic Commission for Europe (UNECE). *Geospatial View of the Generic Statistical Business Process Model (GeoGSBPM)*, version 1.0, May 2021. [Official publication (PDF)](https://statswiki.unece.org/spaces/GSBPM/pages/312476034/GeoGSBPM). Used for integrating geospatial considerations across needs specification, design, build, collection, processing, analysis, dissemination and evaluation.
- Interstate Technology & Regulatory Council (ITRC). *Geospatial Analysis Work Flow Overview*. [Official guidance](https://gro-1.itrcweb.org/geospatial-analysis-work-flow-overview/). Used for the sequence from project goals and exploratory analysis through method selection, model building, validation, results and use.

This is an initial synthesis and navigation pathway, not an independently peer-reviewed course or a completed empirical case study. The linked implementations and examples have different evidence states; follow each item's own limitations. The ITRC material is grounded in environmental-site applications and should not be treated as a universal regulatory standard. The UNECE framework is a process model for geospatially enabled official statistics, not a substitute for study-specific statistical design. No new field data have been collected or analysed for this pathway.
