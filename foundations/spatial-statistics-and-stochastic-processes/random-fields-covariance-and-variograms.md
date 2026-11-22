# Random fields, covariance functions and variograms

**Subject identity:** `SM-FND-005` — Spatial statistics and stochastic processes  
**Module:** 01  
**Status:** Initial researched teaching resource; independent technical review and learner testing pending.

## 1. Why spatial randomness needs its own model

A conventional random sample is often introduced as a collection of independent observations from one distribution. Spatial observations rarely satisfy that simplification automatically. Measurements close together may share geology, land cover, weather, infrastructure, acquisition conditions or unobserved causes.

A spatial statistical model therefore needs to describe not only the distribution at one location, but also how values at different locations vary together. This is the role of a **random field** and its dependence structure.

Examples include:

- soil moisture varying across a catchment;
- elevation errors shared by neighbouring raster cells;
- rainfall measured at a network of gauges;
- habitat suitability varying over a landscape;
- sound-speed anomalies evolving through a water column and across survey epochs.

The random field is a model for a specified quantity and support. A pixel average, point measurement, parcel total and line-segment average are not interchangeable random variables.

## 2. A random field

Let (D) be a spatial domain and let (Z(mathbf{s})) be a real-valued random variable associated with location (mathbf{s}in D). The collection

[
{Z(mathbf{s}):mathbf{s}in D}
]

is a spatial random field. At any fixed location, (Z(mathbf{s})) has a marginal distribution. For multiple locations, the field has joint distributions that describe dependence.

The mean function is

[
m(mathbf{s})=operatorname{E}[Z(mathbf{s})].
]

The covariance function is

[
C(mathbf{s},mathbf{u})
=operatorname{Cov}(Z(mathbf{s}),Z(mathbf{u}))
=operatorname{E}left[
{Z(mathbf{s})-m(mathbf{s})}
{Z(mathbf{u})-m(mathbf{u})}
ight].
]

The variance at location (mathbf{s}) is (C(mathbf{s},mathbf{s})). The covariance between two locations measures their joint linear variation; it is not itself a distance or a causal influence.

For any finite set of locations (mathbf{s}_1,ldots,mathbf{s}_n), the covariance matrix

[
Sigma_{ij}=C(mathbf{s}_i,mathbf{s}_j)
]

must be symmetric positive semidefinite. In other words, for every real vector (mathbf{a}),

[
mathbf{a}^{T}Sigmamathbf{a}geq 0.
]

This condition is essential: the variance of every linear combination of field values must be non-negative. A formula that looks like a plausible correlation curve is not automatically a valid covariance function in every dimension.

## 3. Stationarity: what is assumed not to change?

Stationarity is a family of assumptions about how a field behaves under shifts in location. It is not a claim that the observed map looks visually uniform.

### Strict stationarity

A field is strictly stationary if all its finite-dimensional distributions are invariant under a common translation of their locations, whenever the translated locations remain in the domain. This is a strong distributional condition.

### Second-order stationarity

A field is second-order stationary when:

1. its mean is constant, (m(mathbf{s})=m);
2. its covariance depends only on the separation vector (mathbf{h}=mathbf{u}-mathbf{s}):

[
C(mathbf{s},mathbf{u})=C(mathbf{h}).
]

The variance is then constant across the domain. Second-order stationarity concerns first and second moments; it does not imply strict stationarity unless additional distributional conditions hold.

### Isotropy

A covariance is isotropic when it depends on the separation distance (r=|mathbf{h}|), rather than the direction of separation:

[
C(mathbf{h})=C(r).
]

An anisotropic field may have different dependence ranges or strengths along different directions. For example, a pollutant plume aligned with a prevailing wind or a geological formation may not be isotropic.

Stationarity and isotropy are modelling assumptions that need evidence and a defensible domain. A single empirical map cannot establish them by inspection alone.

## 4. Covariance and correlation

The correlation function standardises covariance:

[
ho(mathbf{s},mathbf{u})
=rac{C(mathbf{s},mathbf{u})}
{sqrt{C(mathbf{s},mathbf{s})C(mathbf{u},mathbf{u})}},
]

provided both marginal variances are positive. Correlation is dimensionless and lies between -1 and 1. Covariance retains the squared units of the measured quantity.

For a second-order stationary field with variance (sigma^2),

[
ho(mathbf{h})=rac{C(mathbf{h})}{sigma^2}.
]

A covariance function must produce a positive-semidefinite covariance matrix for every finite selection of locations. This requirement constrains the shapes and parameter combinations that can be used. It is why covariance models are not chosen solely by drawing a curve through empirical points.

### A valid exponential covariance model

A common isotropic model in Euclidean space is

[
C(mathbf{h})=sigma^2
expleft(-rac{|mathbf{h}|}{a}ight),
qquad a>0.
]

Here (sigma^2) is the marginal variance and (a) is a distance scale controlling the decay. At zero separation, (C(mathbf{0})=sigma^2); as distance increases, covariance approaches zero.

The parameter (a) is not automatically the practical range, and its interpretation depends on the chosen covariance family. Parameters should be reported with coordinate units and the exact model definition.

## 5. The semivariogram

For a second-order stationary field, the semivariogram is related to covariance by

[
gamma(mathbf{h})=C(mathbf{0})-C(mathbf{h}).
]

More generally, under intrinsic stationarity, the semivariogram is defined through stationary increments:

[
gamma(mathbf{h})
=rac{1}{2}operatorname{E}
left[
{Z(mathbf{s}+mathbf{h})-Z(mathbf{s})}^{2}
ight].
]

Intrinsic stationarity requires the expected increment to be zero and the increment variance to depend only on (mathbf{h}). It does not require a constant marginal variance or a covariance function to exist.

For observations (z(mathbf{s}_1),ldots,z(mathbf{s}_n)), the classical Matheron estimator in lag class (N_k) is

[
widehat{gamma}_k=
rac{1}{2|N_k|}
sum_{(i,j)in N_k}
{z(mathbf{s}_i)-z(mathbf{s}_j)}^{2}.
]

(N_k) is the set of pairs assigned to lag class (k), and (|N_k|) is its number of pairs. The empirical estimator is noisy and depends on lag width, maximum lag, sampling geometry, direction, outliers and trend.

See the repository's [empirical semivariogram method](../../methods/empirical-semivariogram.md) for pair construction, lag bins and an implemented estimator.

## 6. Nugget, sill and range are model features, not universal truths

A fitted semivariogram is often described using:

- **Nugget:** a discontinuity at the origin, which may represent measurement error, microscale variation below the sampling resolution, or both. The empirical data alone do not identify which cause applies.
- **Sill:** the value approached by a bounded semivariogram as separation increases. Under second-order stationarity, it corresponds to the marginal variance for a covariance model that decays to zero.
- **Range:** a distance at which a model reaches or approaches its sill according to the model's convention. Some models have a finite range; others approach the sill asymptotically, so a practical range threshold must be stated.

A trend, changing variance, anisotropy, irregular sampling or mixed populations can produce an empirical variogram that is difficult to interpret. Fitting a familiar curve does not repair a misspecified mean or sampling design.

## 7. Spatial dependence changes validation

Randomly splitting nearby observations between training and test sets can make a model appear more transferable than it is. Nearby observations may share the same latent field structure, image footprint, survey session or environmental conditions.

The validation design must match the intended use:

- predicting gaps within a sampled region;
- predicting at new locations in the same region;
- transferring to a new region;
- predicting a future period;
- transferring to a new region and future period.

The [spatial cross-validation method](../../methods/spatial-cross-validation.md) describes spatial blocking, buffers and leakage controls. A block size should be chosen for the deployment question and supported by the dependence scale and sampling design—not selected merely to improve a score.

## 8. From spatial fields to spatiotemporal fields

A spatiotemporal field is indexed by both location and time:

[
Z(mathbf{s},t).
]

Its covariance may depend on spatial separation, temporal lag, direction, and potentially their interaction:

[
Cig((mathbf{s},t),(mathbf{u},t')ig).
]

A **separable** model factors the covariance into spatial and temporal terms, for example

[
Cig((mathbf{s},t),(mathbf{u},t')ig)
=sigma^2 R_s(mathbf{s},mathbf{u})R_t(t,t').
]

This is convenient and interpretable, but restrictive: the temporal relationship does not change the shape of the spatial dependence, and vice versa. Advection, propagation, evolving anisotropy and nonstationary dynamics generally require richer models.

The repository's [separable spatiotemporal Gaussian-process algorithm](../../algorithms/geostatistics/separable-spatiotemporal-gp.md) implements a bounded model and states its assumptions.

### Example: an OU temporal correlation model

For temporal anomalies (A(t)), a stationary Ornstein–Uhlenbeck correlation model is

[
R(t,t')=expleft(-rac{|t-t'|}{	au}ight),
qquad 	au>0.
]

The parameter (	au) is a correlation time in the same units as (t). If a vector of vertical layer anomalies has covariance (C_p), a separable temporal-layer model is

[
operatorname{Cov}(A_k(t_i),A_ell(t_j))
=R(t_i,t_j)(C_p)_{kell}.
]

This preserves dependence both between epochs and between layers. It is a model for temporal anomalies around an explicitly specified mean or reference profile; it does not itself represent advection or predict a changing physical mean field.

The [hydrographic ray-tracing implementation](../../implementations/python/hydrographic-ray-tracing/README.md) demonstrates deterministic profile interpolation and a separate OU conditional profile model. It is a bounded computational example, not evidence that one correlation time or separable covariance is universally appropriate for oceanographic sound speed.

## 9. Model choice and diagnostics

Before fitting or using a spatial covariance model, document:

1. **Random quantity and support:** what is random, and is it a point value, cell average, area total or another support?
2. **Mean structure:** is a constant mean defensible, or is a trend or covariate model needed?
3. **Sampling design:** how were locations selected, and are there clustered or preferential observations?
4. **Coordinate system and metric:** what distance is used, and are its units appropriate?
5. **Stationarity and anisotropy:** what evidence supports the assumptions, and which alternatives were considered?
6. **Measurement error:** is the nugget being used as a measurement-error term, a microscale term, or an unresolved combination?
7. **Fit and residual diagnostics:** are the fitted model and residual assumptions plausible across distance and direction?
8. **Validation target:** does the holdout design represent the locations and times where predictions will be used?
9. **Uncertainty:** are parameter uncertainty, mean-model uncertainty and model discrepancy represented, or is only conditional prediction uncertainty reported?

A model can interpolate well and still be unsuitable for extrapolation or transfer to another region. A fitted variogram is not a physical explanation.

## 10. What this module does not claim

This module introduces second-order spatial dependence and the basic variogram language. It does not provide a complete treatment of:

- point-process theory and event interaction;
- design-based spatial sampling and preferential sampling;
- intrinsic random functions and generalized covariance;
- likelihood and restricted maximum-likelihood variogram fitting;
- anisotropic and nonstationary covariance construction;
- conditional and unconditional spatial simulation;
- nonseparable spatiotemporal models, transport and advection;
- uncertainty in estimated covariance parameters.

These topics require separate modules and application-specific evidence.

## Further reading

- Cressie, N. (1993). *Statistics for Spatial Data*, revised edition. Wiley.
- Chiles, J.-P., and Delfiner, P. (2012). *Geostatistics: Modeling Spatial Uncertainty*, 2nd edition. Wiley.
- Gelfand, A. E., Diggle, P., Fuentes, M., and Guttorp, P. (eds.) (2010). *Handbook of Spatial Statistics*. CRC Press.
- Stein, M. L. (1999). *Interpolation of Spatial Data: Some Theory for Kriging*. Springer.
- Rasmussen, C. E., and Williams, C. K. I. (2006). *Gaussian Processes for Machine Learning*. MIT Press.

These references are foundational texts, not claims that every result or model in this module has been independently reviewed against every edition.

## Check your understanding

1. Why does a spatial random field require joint distributions, rather than only one marginal distribution?
2. What is the difference between strict stationarity and second-order stationarity?
3. Why must a covariance function generate positive-semidefinite matrices for arbitrary finite sets of locations?
4. Under which assumptions can the semivariogram be written as (C(mathbf{0})-C(mathbf{h}))?
5. Why does a nugget not automatically identify measurement error?
6. Why might random train/test splitting be optimistic for spatial prediction?
7. What modelling restriction is introduced by a separable spatiotemporal covariance?
8. What additional physical information would be needed before interpreting an OU conditional sound-speed profile as a forecast?
