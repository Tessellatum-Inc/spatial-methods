# Spatial statistics and stochastic processes

**Subject identity:** \`SM-FND-005\` — Spatial statistics and stochastic processes.

This domain develops the probability models for spatially indexed and time-evolving quantities. It explains how dependence, spatial structure and stochastic variation differ from independent sampling noise, and how those assumptions influence estimation, prediction, simulation and decisions.

## Scope

The domain covers:
- random fields and spatially indexed random variables;
- covariance functions, correlation functions and semivariograms;
- stationarity, isotropy, anisotropy and nonstationarity;
- spatial point processes and their first- and second-order properties;
- spatial sampling and design-based versus model-based inference;
- Gaussian random fields, Gaussian processes and conditional prediction;
- spatiotemporal processes, separability, advection and evolving dependence;
- conditional simulation, uncertainty decomposition and model criticism.

## Modules

1. [Random fields, covariance functions and variograms](random-fields-covariance-and-variograms.md) introduces random-field notation, second-order stationarity, isotropy, covariance validity and semivariograms. It connects to the [empirical semivariogram method](../../methods/empirical-semivariogram.md), [separable spatiotemporal Gaussian-process algorithm](../../algorithms/geostatistics/separable-spatiotemporal-gp.md), [spatial cross-validation method](../../methods/spatial-cross-validation.md) and [temporally conditioned hydrographic sound-speed profiles](../../implementations/python/hydrographic-ray-tracing/README.md).
2. [Spatial point processes and spatial sampling design](spatial-point-processes-and-sampling-design.md) develops point-process structure, observation-process limitations, inclusion probabilities, Horvitz–Thompson estimation and design-based versus model-based selection. It connects to point-process simulators, sampling-design implementations and collection planning.
3. [Anisotropic and nonstationary spatial fields](anisotropic-and-nonstationary-spatial-fields.md) distinguishes directional dependence from location-varying mean, variance and covariance. It develops valid geometric-anisotropy metrics, directional variogram diagnostics, spatial deformation and process-convolution constructions, then connects these assumptions to fitting, kriging and spatial validation.
4. [Gaussian random-field inference and conditional simulation](gaussian-random-field-inference-and-conditional-simulation.md) derives Gaussian conditioning, distinguishes latent prediction from noisy-observation prediction, explains kriging and sequential conditional simulation, and identifies parameter/model uncertainty and validation requirements.
5. [Spatiotemporal random fields, advection and dynamic prediction](spatiotemporal-random-fields-advection-and-dynamic-prediction.md) develops separable and nonseparable dependence, moving-frame coordinates, evolving anisotropy, state-space and transport models, observation trajectories, and the distinction between interpolation, conditional prediction and physical forecasting.

## Boundaries with neighbouring foundations

- **SM-FND-004 — Probability and statistical inference:** general probability, random variables, distributions, conditioning and inferential procedures. This domain specialises those ideas for spatial and spatiotemporal dependence.
- **SM-FND-002 — Linear algebra and matrix methods:** covariance matrices, matrix factorizations and multivariate transformations. This domain explains how covariance is indexed by space and time and what makes a covariance function valid.
- **SM-FND-011 — Measurement science:** measurands, traceability, measurement uncertainty and uncertainty budgets. A stochastic field model is not a substitute for a measurement model or metrological uncertainty budget.
- **SM-FND-016 — Numerical analysis:** numerical approximation, conditioning and stable computation. This domain states the stochastic model; numerical methods implement it.

## Development status

Five initial teaching modules are published. They establish the core vocabulary and connect to existing algorithms and implementations, but do not constitute a complete course or independent technical certification. Remaining work includes deeper Bayesian and likelihood-based inference, covariance-parameter uncertainty, preferential sampling, dynamic-model implementations, application-specific advection, scalable inference, independent technical review and learner testing.

## Reading route

1. Read the [probability foundation](../probability-and-statistics/README.md) for the general language of random variables and dependence.
2. Read [covariance matrices and multivariate structure](../linear-algebra/covariance-matrices-and-multivariate-structure.md) for matrix properties and linear uncertainty propagation.
3. Study the modules in the order that best fits the application, then follow each theory into a method, implementation, collection workflow or validation design. Do not infer that a model is suitable merely because its software can be run.
