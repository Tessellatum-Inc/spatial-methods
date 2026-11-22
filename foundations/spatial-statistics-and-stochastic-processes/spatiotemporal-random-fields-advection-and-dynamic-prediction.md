# Spatiotemporal random fields, advection and dynamic prediction

## Purpose

A spatial field observed repeatedly is not merely a stack of independent maps. Values at different locations and times may be coupled by persistence, transport, diffusion, growth, decay, movement of sources, changing environmental conditions or human activity.

This module develops the stochastic language for those relationships. It distinguishes three questions that are often conflated:

1. **Interpolation:** what is the field at an unobserved location or time inside the domain represented by observations?
2. **Prediction:** what distribution does a specified statistical model assign to an unobserved value, including values at later times?
3. **Forecasting:** what may happen in the future under an explicit account of system evolution, available information at forecast issue time, and any assumed or modelled future drivers?

A Gaussian-process conditional distribution can answer a prediction question at a future timestamp. That alone does not make the model a physical forecast system.

## 1. A field indexed by space and time

Let

\[
Z(\mathbf{s},t), \qquad \mathbf{s}\in D\subseteq\mathbb{R}^{d},\quad t\in\mathcal{T},
\]

be a real-valued random field. Its mean is

\[
m(\mathbf{s},t)=\mathbb{E}[Z(\mathbf{s},t)]
\]

and its covariance is

\[
C\bigl((\mathbf{s},t),(\mathbf{s}',t')\bigr)
=\operatorname{Cov}\left[Z(\mathbf{s},t),Z(\mathbf{s}',t')\right].
\]

A valid covariance must produce a symmetric positive-semidefinite matrix for every finite collection of space-time points. For any locations and times \((\mathbf{s}_i,t_i)\), and any real coefficients \(a_i\),

\[
\sum_{i=1}^{n}\sum_{j=1}^{n}
a_i a_j C\bigl((\mathbf{s}_i,t_i),(\mathbf{s}_j,t_j)\bigr)\geq 0.
\]

This finite-dimensional condition is the central constraint. A covariance formula is not valid merely because it is smooth, non-negative at each lag, or visually plausible.

A second-order stationary space-time field has constant mean and covariance depending only on spatial and temporal lags:

\[
C\bigl((\mathbf{s},t),(\mathbf{s}',t')\bigr)
=C(\mathbf{h},u),\qquad
\mathbf{h}=\mathbf{s}-\mathbf{s}',\quad u=t-t'.
\]

Stationarity is a modelling assumption, not a default property of environmental or social processes. Boundaries, trends, seasonality, changing regimes, moving sources and evolving variance can violate it.

## 2. Separability: a useful baseline with a strong restriction

A covariance is separable when it can be written as a product of a spatial and a temporal covariance:

\[
C(\mathbf{h},u)=C_s(\mathbf{h})C_t(u).
\]

For example, the repository's exact separable GP uses

\[
C(\mathbf{h},u)=\sigma^2
\exp\left(-\frac{\|\mathbf{h}\|}{a_s}\right)
\exp\left(-\frac{|u|}{a_t}\right).
\]

The spatial scale \(a_s\) and temporal scale \(a_t\) control different dimensions, but the spatial dependence shape does not change with temporal lag. At every time lag, the spatial correlation is the same spatial correlation multiplied by one temporal attenuation factor.

This can be reasonable for a field whose temporal persistence acts similarly across spatial scales. It can be restrictive when, for example, nearby values decorrelate quickly while broad spatial structures persist, or when a moving phenomenon changes the apparent spatial relationship through time.

The separable implementation is a small-data exact GP baseline with a zero prior mean and fixed user-supplied scales. Its dense factorisation has quadratic memory and cubic factorisation cost in the number of training observations. Do not infer that its assumptions or computational limits apply to every spatiotemporal GP.

## 3. Nonseparability: temporal lag changes spatial dependence

A nonseparable covariance allows the spatial dependence structure to vary with temporal lag. One repository implementation uses a Gneiting-class construction. Define

\[
q(u)=1+\left(\frac{|u|}{a_t}\right)^{2\alpha},
\]

then

\[
C(\mathbf{h},u)
=
\sigma^2 q(u)^{-\beta d/2}
\exp\left(
-\frac{\|\mathbf{h}\|^2}{a_s^2q(u)^\beta}
\right),
\]

with \(0<\alpha\leq1\), \(0\leq\beta\leq1\), positive scales, and Euclidean spatial dimension \(d\).

The temporal lag changes both the amplitude factor and the effective spatial scale. For this parameterisation, \(\beta=0\) removes temporal decay; positive \(\beta\) couples the temporal and spatial dependence. This is one valid family, not a universal model for all dynamics.

The companion implementation constructs covariance matrices from Euclidean coordinates and linear time. Its finite-matrix eigenvalue diagnostic is a useful numerical check, not a proof of validity beyond the mathematical construction. Its distance contract must not be silently replaced with great-circle, ellipsoidal, graph or road-network distance.

## 4. Advection: distinguish fixed-space change from moving-with-the-flow change

Suppose a field pattern is transported by a constant velocity vector \(\mathbf{v}\). A simple advective coordinate is

\[
\mathbf{s}^{*}=\mathbf{s}-\mathbf{v}t.
\]

A covariance stationary in the moving frame can be written

\[
C\bigl((\mathbf{s},t),(\mathbf{s}',t')\bigr)
=
C_0\left(
(\mathbf{s}-\mathbf{v}t)-(\mathbf{s}'-\mathbf{v}t'),
t-t'
\right).
\]

Equivalently, its spatial lag in the moving frame is

\[
\mathbf{h}^{*}=\mathbf{h}-\mathbf{v}u.
\]

This is a coordinate transformation for a specified transport model. It is not a claim that every observed field is frozen and translated unchanged. It assumes a meaningful velocity, a compatible coordinate frame and a transport-dominated structure over the interval considered.

A constant velocity is often only a local approximation. Real flows may vary with position, depth and time. If \(\mathbf{v}=\mathbf{v}(\mathbf{s},t)\), a trajectory \(\boldsymbol{\phi}_{t_0\rightarrow t}(\mathbf{s}_0)\) is defined by

\[
\frac{d\boldsymbol{\phi}}{dt}
=
\mathbf{v}(\boldsymbol{\phi}(t),t),
\qquad
\boldsymbol{\phi}(t_0)=\mathbf{s}_0.
\]

The relevant moving-frame separation then depends on the flow map, not simply on \(\mathbf{s}-\mathbf{v}t\). Uncertain velocity fields also contribute uncertainty and can induce non-Gaussian or nonstationary behaviour. A deterministic coordinate shift must not be presented as if it had propagated velocity uncertainty.

### Interpretation

- A fixed sensor asks how the field changes at its fixed location.
- A moving platform samples along its trajectory and may confound spatial gradients with temporal change.
- A transported feature may remain coherent along a flow trajectory even when fixed-location temporal correlation is short.
- A forecast that advects observations forward needs a velocity field and an account of its uncertainty or error.

Advection is relevant to oceanographic sound-speed and current fields, atmospheric variables, smoke and plume transport, river conditions, moving fronts, animal movement and traffic congestion. The appropriate transport law differs across applications.

## 5. Evolving anisotropy and nonstationarity

Anisotropy means dependence varies with direction. A geometric anisotropy model can transform spatial lag by a matrix \(A\):

\[
r_A(\mathbf{h})=\sqrt{\mathbf{h}^{\mathsf T}A^{\mathsf T}A\mathbf{h}},
\qquad
C(\mathbf{h})=c(r_A(\mathbf{h})).
\]

For a time-invariant \(A\), the preferred directions and relative scales remain fixed. If orientation or scale changes with time, one might write a local metric \(A(t)\), but simply inserting \(A(t)\) into a stationary lag covariance does not automatically define a valid covariance for arbitrary pairs of times. Pairwise symmetry and positive definiteness must still hold.

Safer constructions include:
- a process defined in a physically justified moving coordinate system;
- valid nonstationary covariance constructions, such as process convolutions with location- and time-varying kernels;
- hierarchical or state-space models whose transitions explicitly evolve latent structure;
- locally stationary approximations with a stated domain and scale of validity.

A varying mean, variance, directional metric, correlation range and transport velocity are different kinds of nonstationarity. Diagnose and model them separately where possible. A trend-removal step does not by itself solve changing covariance, and a spatially varying covariance model does not automatically account for an evolving mean.

## 6. Dynamic models: encode evolution rather than only correlation

A dynamic model specifies how a latent state evolves. A generic linear state-space model is

\[
\mathbf{x}_{k}=F_k\mathbf{x}_{k-1}+B_k\mathbf{u}_k+\mathbf{w}_k,
\]

\[
\mathbf{y}_k=H_k\mathbf{x}_k+\mathbf{v}_k,
\]

where \(\mathbf{x}_k\) is the latent state, \(\mathbf{u}_k\) represents known inputs, \(\mathbf{w}_k\) is process noise, and \(\mathbf{v}_k\) is observation error. Their covariance assumptions must be stated, including any temporal or cross-component dependence.

This formulation separates:
- the physical or statistical evolution law \(F_k\);
- external forcing \(B_k\mathbf{u}_k\);
- process uncertainty;
- the observation operator \(H_k\);
- measurement error.

A continuous field may instead be represented by a stochastic partial differential equation. For example, a schematic advection-diffusion-reaction model is

\[
\frac{\partial Z}{\partial t}
+\mathbf{v}\cdot\nabla Z
=
\nabla\cdot(\kappa\nabla Z)
+r(Z,\mathbf{s},t)+\eta(\mathbf{s},t),
\]

where \(\kappa\) describes diffusion, \(r\) represents sources, sinks or reactions, and \(\eta\) is a stochastic forcing term. This equation is a model template, not a complete specification: boundary conditions, initial conditions, coefficient fields, forcing covariance and a solution method are required.

A covariance model describes dependence. A dynamic model describes an evolution mechanism. They can be connected, but neither automatically supplies the other's physical interpretation.

## 7. Interpolation, conditional prediction and forecasting

These tasks differ by target and information set.

| Task | Target | Essential question |
|---|---|---|
| Spatial interpolation | Unobserved location at an observed or specified time | What does the spatial model imply between samples? |
| Temporal interpolation | Unobserved time between observations | What temporal structure is assumed between measurements? |
| Spatiotemporal prediction | Unobserved space-time point | What conditional distribution follows from the fitted joint model? |
| Forecasting | Future state after an issue time | What evolution law and future inputs propagate the current information forward? |

A stationary GP may condition on observations and return a distribution at \(t_*>t_{\max}\). This is a valid model-based prediction under its covariance assumptions. It is not necessarily a physical forecast: the model may omit advection, forcing, boundary changes, regime shifts and the mechanism that generates future observations.

Forecast evaluation must also respect information availability. At forecast origin \(t_0\), training and feature construction may use only information available at or before \(t_0\). Randomly splitting space-time rows can leak future information into training. Use rolling-origin or otherwise target-aligned validation for forecast claims. Leave-location-and-time-out validation instead tests transfer to held-out location/time combinations; it is not a substitute for chronological forecast evaluation.

Report the forecast horizon, issue time, observation cut-off, data latency, baseline, uncertainty calibration and performance by horizon and relevant regime. A model that performs well at short horizons may fail at longer horizons as process uncertainty accumulates.

## 8. Observation design and moving platforms

A space-time dataset is shaped by how it was collected. Fixed stations, repeated transects, satellite overpasses, mobile sensors, autonomous vehicles, aircraft and opportunistic reports produce different observation geometries and missingness patterns.

For a moving platform with trajectory \(\mathbf{s}(t)\), observations are

\[
Y_i=Z(\mathbf{s}(t_i),t_i)+\epsilon_i.
\]

If the platform moves with the phenomenon, samples may cluster along trajectories and fail to represent the full spatial domain. If collection times depend on observed conditions, the observation process may be informative. Sampling design, platform motion, data latency, sensor footprint and measurement error should be represented separately from the latent field whenever they materially affect inference.

A dense set of observations along one trajectory is not equivalent to dense coverage of the space-time domain. Replication at the same place and time, revisits at different times, and simultaneous observations at separated locations answer different inferential questions.

## 9. Model criticism and validation

Before accepting a spatiotemporal model, test whether its structure is compatible with the application.

1. Plot observations and residuals against both space and time; inspect trends, seasonality and regime changes.
2. Examine spatial dependence at multiple temporal lags and temporal dependence at multiple spatial separations.
3. Test whether directional structure or apparent velocity changes through time.
4. Compare separable and nonseparable alternatives using target-aligned validation, not only in-sample fit.
5. Check residual space-time dependence and predictive interval calibration.
6. Evaluate forecast performance using chronological origins and realistic data latency.
7. Check sensitivity to coordinate reference system, temporal units, aggregation windows and missing-data assumptions.
8. Separate uncertainty from observation error, process variation, parameter estimation, forcing and model discrepancy where the application supports that decomposition.

A better score on one finite split does not prove that a covariance is valid, that a transport mechanism is correct, or that a model will generalise to a new regime.

## 10. Connections across Spatial Methods

- [Random fields, covariance functions and variograms](random-fields-covariance-and-variograms.md) establishes the spatial stochastic language.
- [Anisotropic and nonstationary spatial fields](anisotropic-and-nonstationary-spatial-fields.md) develops directional and location-varying dependence.
- [Gaussian random-field inference and conditional simulation](gaussian-random-field-inference-and-conditional-simulation.md) derives conditional distributions and simulation.
- [Separable spatiotemporal GP algorithm](../../algorithms/geostatistics/separable-spatiotemporal-gp.md) and [implementation](../../implementations/python/spatiotemporal-gaussian-process/README.md) provide an exact dense baseline.
- [Nonseparable space-time covariance method](../../methods/nonseparable-space-time-covariance.md) and [implementation](../../implementations/python/nonseparable-space-time-covariance/README.md) provide a Gneiting-class alternative.
- [Spatiotemporal validation implementation](../../implementations/python/spatiotemporal-validation/README.md) implements strict leave-location-and-time-out fold construction; use a chronological design for forecast evaluation.
- [Spatiotemporal point-process methods](../../implementations/python/point-process/README.md) address event processes rather than continuous-valued fields.
- Collection methods and recipes determine where, when and how observations are acquired; their sampling geometry is part of the inferential problem.

## 11. Limits and unresolved work

This module establishes concepts and model distinctions; it does not provide a universal spatiotemporal covariance or a production forecasting system. The repository's current separable GP and Gneiting covariance implementations are deliberately limited baselines. Neither estimates all parameters, models arbitrary advection, handles evolving anisotropy, nor guarantees forecast skill under regime change.

Further development should include dynamic-model implementations with explicit process and observation models, advection-aware covariance or state-space examples, parameter uncertainty, scalable inference, and independent domain review. Application-specific physical equations and boundary conditions must be reviewed by the relevant scientific discipline.

## References

- Cressie, N. and Wikle, C. K. (2011). *Statistics for Spatio-Temporal Data*. Wiley.
- Gneiting, T. (2002). Nonseparable, Stationary Covariance Functions for Space-Time Data. *Journal of the American Statistical Association*, 97(458), 590–600. https://doi.org/10.1198/016214502760047113
- Wikle, C. K., Zammit-Mangion, A. and Cressie, N. (2019). * Spatial Statistics for Remote Sensing*. CRC Press.

## Check your understanding

1. What restriction does separability impose on the spatial correlation shape as temporal lag changes?
2. Why does a positive covariance value at every lag not establish positive definiteness?
3. Under what assumptions is \(\mathbf{s}^{*}=\mathbf{s}-\mathbf{v}t\) a meaningful advective coordinate?
4. Why does a time-varying anisotropy matrix require more than substituting \(A(t)\) into a stationary covariance?
5. Give an example where a GP prediction at a future time is not a defensible physical forecast.
6. Which validation design would you use for future-time forecasting, and why is leave-location-and-time-out validation a different target?
7. How could a moving sensor's trajectory create apparent temporal change even when part of the field variation is spatial?
