# Measurement science and survey-network adjustment

**A practical learning path from defining a measurement to adjusting and evaluating a correlated survey network.**

This path connects the measurement-science foundations, synthetic experiments and dependency-free Python implementation already maintained in Spatial Methods. It is designed for learners who want to understand not only how an adjustment is computed, but why its stochastic model, datum, observations and quality decisions matter.

The path is useful to surveying and geospatial students, educators, researchers and practitioners. It is not a professional qualification, field procedure, instrument calibration guide or substitute for applicable standards and competent supervision.

## What you will learn

By working through the collection, you should be able to:

- define a measurand and express a measurement model;
- distinguish observations, corrections, uncertainty components and reported results;
- evaluate standard uncertainty using Type A and Type B methods;
- represent shared error sources with covariance;
- formulate weighted and generalized least-squares adjustments;
- recognise datum defects and apply an explicit inner constraint;
- interpret residuals, redundancy, reliability and robust-estimation results;
- compare stochastic models without assuming that a more complex model is automatically better;
- explain what a synthetic experiment does—and does not—demonstrate.

## Suggested route

### 1. Understand the measurement

Start with the foundations:

1. [Measurement principles and field verification](../foundations/measurement-science/measurement-principles-and-field-verification.md)
2. [Measurement models and measurand definition](../foundations/measurement-science/measurement-models-and-measurand-definition.md)
3. [Standard uncertainty: Type A and Type B evaluation](../foundations/measurement-science/standard-uncertainty-type-a-type-b.md)

Then work through [Exercise A: repeated distance and angle observations](../experiments/measurement/exercise-a-repeated-distance-and-angle.md). Pay attention to the assumptions behind repeated observations and the distinction between a calculated standard uncertainty and a claim about instrument performance.

Before the network exercises, read [Terrestrial surveying: total station and differential levelling](../collection/terrestrial-surveying-total-station-and-levelling.md). It describes the field observations and checks that give practical meaning to angles, distances, height differences, closures and stochastic assumptions. Its procedures are a learning synthesis, not a substitute for current instrument manuals or project specifications.

### 2. Move from observations to network adjustment

Read [Exercise B: differential levelling loop](../experiments/measurement/exercise-b-differential-levelling-loop.md) and [Exercise C: weighted control network](../experiments/measurement/exercise-c-weighted-control-network.md).

These introduce observation equations, weights, closure, redundancy, adjusted parameters and residuals. The datasets and uncertainty assumptions are synthetic teaching inputs.

### 3. Understand the datum and stochastic model

Read [Exercise D: stochastic control and correlation](../experiments/measurement/exercise-d-stochastic-control-and-correlation.md), then [Exercise E: minimally constrained vertical network](../experiments/measurement/exercise-e-minimally-constrained-vertical-network.md).

The key distinction is between:
- the relative geometry or height differences supported by observations;
- the datum convention used to select a unique coordinate representation; and
- external control that relates the network to a reference datum.

The sum-to-zero inner constraint in Exercise E selects an arbitrary vertical origin. It is not an external benchmark observation.

### 4. Evaluate quality and reliability

Work through:

- [Exercise F: network quality and blunder detection](../experiments/measurement/exercise-f-network-quality-and-blunder-detection.md)
- [Exercise G: reliability and network design](../experiments/measurement/exercise-g-reliability-and-network-design.md)
- [Exercise H: Monte Carlo reliability and design](../experiments/measurement/exercise-h-monte-carlo-reliability-and-design.md)
- [Exercise I: robust estimation and outlier identification](../experiments/measurement/exercise-i-robust-estimation-and-outlier-identification.md)
- [Exercise J: Monte Carlo comparison of robust estimators](../experiments/measurement/exercise-j-monte-carlo-comparison-of-robust-estimators.md)

Do not interpret a statistical flag as automatic proof of a blunder, or a robust estimator as permission to ignore the observation process.

### 5. Model correlated observations

Read the [covariance and generalized least-squares foundation](../foundations/measurement-science/covariance-correlated-observations-and-gls.md), then:

- [Exercise K: correlated errors and GLS](../experiments/measurement/exercise-k-correlated-errors-and-generalized-least-squares.md)
- [Exercise L: block-robust GLS](../experiments/measurement/exercise-l-block-robust-gls-with-correlated-observations.md)
- [Exercise M: multi-session adjustment and robustness](../experiments/measurement/exercise-m-multi-session-network-adjustment-and-robustness.md)
- [Exercise N: variance-component estimation](../experiments/measurement/exercise-n-variance-component-estimation-from-repeated-networks.md)
- [Exercise O: covariance-model selection and misspecification](../experiments/measurement/exercise-o-covariance-model-selection-and-misspecification.md)

These experiments show why covariance structure should be connected to plausible acquisition and processing mechanisms. Their simulated outcomes are conditional on their stated synthetic assumptions; they do not establish a universal best covariance model or estimator.

### 6. Reproduce the calculations in Python

Open the [covariance and GLS implementation](../implementations/python/covariance-gls/README.md).

It includes:
- covariance validation and session-common covariance construction;
- Cholesky-based unconstrained GLS;
- exact-constraint GLS using a KKT system;
- synthetic Exercise E and Exercise K examples;
- standard-library unit tests.

From the implementation directory, run:

```bash
python -m unittest -v
python example_exercise_k.py
python example_exercise_e.py
```

The solver requires positive-definite observation covariance. It does not implement singular-covariance generalized inverses, variance-component estimation, robust estimation or variance-factor rescaling. Read the implementation's limitations before adapting it to other networks.

## A useful study routine

For each experiment:

1. State the question and identify the quantities being estimated.
2. Draw or write the observation model before looking at the code.
3. Identify the stochastic assumptions and the source of each uncertainty component.
4. Predict what should happen when the datum, weights or covariance structure changes.
5. Run the example and compare your prediction with the output.
6. Change one assumption at a time.
7. Record what changed, what remained invariant and what the experiment cannot establish.

## How the collection maps to the four pillars

- **Theoretical Foundations:** measurement models, uncertainty, covariance, estimation and statistical testing.
- **Spatial Data Collection:** observation design, levelling, control, repeat sessions and the physical origin of error sources.
- **Spatial Algorithms:** weighted least squares, GLS, constrained adjustment, robust estimation and Monte Carlo analysis.
- **Spatial Recipes:** the reproducible sequence from observations and assumptions to adjustment, diagnostics and a documented result.

The pillars are connected, not a compulsory sequence. A learner may enter through field collection, computation, theory or a practical adjustment problem.

## Scope and evidence boundary

All Exercises A–O in this path use synthetic data or simulated scenarios. They are not observations from an actual survey, instrument calibration, certified accuracy assessment or evidence that a field method meets a legal or project specification. Some simulations deliberately simplify the observation process to isolate one modelling issue.

External sources, claim-level evidence and review states are maintained in the [source register](../catalog/sources/README.md). A source being authoritative does not automatically validate every claim associated with it.

## Further study and support

The public repository contains the canonical foundations, experiment descriptions and reusable implementation. A deeper learning companion can add original annotated derivations, answer walkthroughs, uncertainty-budget worksheets, additional exercises and guided implementation tasks. Those materials should extend the public collection rather than duplicate it.

[Support and follow the ongoing Spatial Methods curation on Patreon](https://www.patreon.com/c/SpatialMethods).
