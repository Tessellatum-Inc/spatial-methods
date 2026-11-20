# Probability and statistical inference

**Subject identity:** `SM-FND-004` — Probability and statistical inference.

This domain develops the probability language and inferential reasoning needed to describe uncertainty, learn from samples, compare models and make defensible claims from spatial data. It is a theory collection, not a catalogue of statistical tests or software recipes.

## Why this domain matters in Spatial Methods

Probability underlies uncertainty-aware surveying, spatial sampling, remote-sensing classification, point-pattern analysis, geostatistics, prediction, risk assessment, model validation and decision-making. A result from a statistical method is only interpretable when its random variables, sampling process, conditioning information and assumptions are understood.

The repository already contains applied statistical methods and implementations. This domain supplies their shared foundations without duplicating each method's computational procedure.

## Scope and boundaries

The domain will develop:

- probability spaces, events, probability rules and conditional probability;
- independence, dependence, joint and marginal distributions;
- random variables, probability mass/density functions and distribution functions;
- expectation, variance, covariance, correlation and moments;
- common discrete and continuous probability distributions;
- sampling designs, sampling distributions and the law of large numbers and central limit theorem;
- likelihood, estimation, bias, consistency and efficiency;
- confidence intervals, hypothesis tests, error rates, power and multiple comparisons;
- Bayesian inference, prior distributions, likelihoods, posterior distributions and predictive reasoning;
- model checking, calibration, predictive uncertainty and limits of statistical conclusions.

### Boundaries with neighbouring foundations

- **SM-FND-005 — Spatial statistics and stochastic processes:** spatial dependence, random fields, point processes and spatiotemporal stochastic models belong there. This domain introduces probability and dependence generally.
- **SM-FND-011 — Measurement science:** measurement models, traceability and uncertainty budgets belong there. Probability supplies mathematical tools used in uncertainty evaluation; it does not replace metrological definitions or decisions.
- **SM-FND-002 — Linear algebra:** matrix and vector structures used by multivariate distributions and covariance models are developed there.
- **SM-FND-016 — Numerical analysis:** computational approximation, numerical integration, random-number generation quality and numerical stability belong there.
- **SM-FND-018 — GIScience:** the meaning of spatial units, scale, representation and geographic inference must be considered alongside statistical models.

## Learning modules

| Module | Topic | Spatial connections | Status |
|---|---|---|---|
| 01 | [Probability models, events and conditioning](probability-models-events-and-conditioning.md) | Screening maps, classification prevalence, spatial sampling units, conditional evidence and Bayes' theorem | Initial public module |
| 02 | [Random variables, distributions and probability models](random-variables-and-distributions.md) | Measurement outcomes, event counts, detection and classification | Initial module published |
| 03 | [Joint distributions, covariance and dependence](joint-distributions-covariance-and-dependence.md) | Correlated measurements, multivariate spatial data and dependence structures | Initial module published |
| 04 | [Sampling designs and sampling distributions](sampling-designs-and-sampling-distributions.md) | Field sampling, ground truth, survey design and spatially representative inference | Initial module published |
| 05 | [Likelihood and statistical estimation](likelihood-and-statistical-estimation.md) | Parameter estimation, regression, geostatistics and model fitting | Initial module published |
| 06 | [Confidence intervals, hypothesis tests and statistical decisions](confidence-intervals-hypothesis-tests-and-statistical-decisions.md) | Accuracy assessment, change detection and model comparison | Initial module published |
| 07 | [Bayesian inference and predictive distributions](bayesian-inference-and-predictive-distributions.md) | Evidence updating, risk mapping and probabilistic prediction | Initial module published |
| 08 | Statistical diagnostics, calibration and model criticism | Prediction validation, classification calibration and uncertainty communication | Planned |

The sequence is a suggested route, not a compulsory order. Readers may enter through a concrete application and follow its prerequisites.

## Application anchors already in the repository

- [Spatial cross-validation](../../methods/spatial-cross-validation.md)
- [Empirical semivariogram](../../methods/empirical-semivariogram.md)
- [Point-pattern second-order statistics](../../methods/point-pattern-second-order-statistics.md)
- [Forecast verification](../../methods/forecast-verification.md)
- [Photogrammetric checkpoint QA](../../implementations/python/photogrammetry-odm/checkpoint_qa.py)
- [Measurement uncertainty and Type A/Type B evaluation](../measurement-science/standard-uncertainty-type-a-type-b.md)
- [Covariance and correlated observations](../measurement-science/covariance-correlated-observations-and-gls.md)

These are application anchors, not evidence that this foundation domain or every linked method has been independently reviewed.

## Development standard

Each module should define its random objects and notation; distinguish a probability model from observed relative frequencies; state the sampling unit and sampling design; derive the important rules; include spatially meaningful worked examples; identify dependence, selection and measurement assumptions; explain what can and cannot be inferred; and connect to canonical algorithms, implementations, collection methods and recipes.

A probability value is not self-explanatory. Record what is random, what population or process is represented, what information is conditioned upon, and which assumptions justify the model.

## Review status

This is an initial domain collection. Modules 01–07 are researched syntheses based on cited probability, metrology and sampling-design material and original spatial examples. Independent technical review, learner testing and further modules remain outstanding. No publication in this folder constitutes professional statistical certification or validation of a real spatial dataset.
