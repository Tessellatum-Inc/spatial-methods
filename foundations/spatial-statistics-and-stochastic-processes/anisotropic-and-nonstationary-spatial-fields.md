# Anisotropic and nonstationary spatial fields

**Subject identity:** \`SM-FND-005\` — Spatial statistics and stochastic processes  
**Module:** 03  
**Status:** Initial researched teaching resource; independent technical review and learner testing pending.

## 1. Why direction and location matter

The simplest stationary isotropic model assumes that dependence is unchanged when a field is translated or rotated. Many spatial processes violate one or both assumptions.

Examples include:
- a contaminant plume whose correlation extends farther downwind than across the wind;
- geological structures with continuity along bedding or fracture directions;
- rainfall fields shaped by prevailing circulation and terrain;
- soil properties whose variance and correlation scale change across soil or landform boundaries;
- urban environmental fields whose structure changes between dense centres, industrial corridors and rural edges.

Two distinct departures must be separated:

- **Anisotropy:** dependence changes with the direction of separation. In geometric anisotropy, the same covariance shape is stretched or compressed along principal directions. In zonal anisotropy, the sill or other structural components also differ by direction.
- **Nonstationarity:** the mean, variance, dependence structure, or some combination changes with absolute location. A field can be nonstationary without being anisotropic, and anisotropic without being nonstationary.

A model should describe the phenomenon and the intended prediction domain. More flexible mathematics is not automatically better: extra spatially varying parameters need enough data and physical justification.

## 2. Directional dependence and geometric anisotropy

Let \(\mathbf h=\mathbf u-\mathbf s\) be the separation vector in a suitable projected coordinate system. An isotropic covariance depends only on \(\|\mathbf h\|\). A stationary geometrically anisotropic covariance instead uses a transformed distance:

\[
C(\mathbf h)=\sigma^2\,\rho\!\left(
\sqrt{\mathbf h^{\mathsf T}A\mathbf h}
\right),
\]

where \(A\) is symmetric positive definite and \(\rho\) is a valid isotropic correlation model in the transformed metric.

For a two-dimensional field with principal axes rotated by angle \(\theta\), one convenient parameterisation is

\[
A=R(\theta)
\begin{bmatrix}
a_1^{-2}&0\\
0&a_2^{-2}
\end{bmatrix}
R(\theta)^{\mathsf T},
\qquad
R(\theta)=
\begin{bmatrix}
\cos\theta&-\sin\theta\\
\sin\theta&\cos\theta
\end{bmatrix}.
\]

Here \(a_1\) and \(a_2\) are directional distance scales under this parameterisation. The angle convention and coordinate axis convention must be stated. If \(a_1>a_2\), dependence decays more slowly along the first principal axis for a common monotone radial correlation family.

The transformed distance is dimensionless only if the scale parameters carry the same units as the coordinate axes. Use coordinates whose distance metric is meaningful for the study region; applying Euclidean anisotropy directly to longitude and latitude in degrees is generally not defensible.

### Geometric versus zonal anisotropy

Geometric anisotropy changes the distance scale by direction while retaining a common sill and covariance family. Zonal anisotropy allows directional structures or sills to differ. A single distance transformation cannot generally represent zonal anisotropy.

Nested structures may also have different principal directions and ranges. A model can therefore be anisotropic at one scale and nearly isotropic at another. Report the model components rather than compressing all behaviour into one ratio.

## 3. Directional variograms as evidence

An empirical directional semivariogram restricts pairs to selected orientations and angular tolerances. For direction unit vector \(\mathbf d\), lag \(r\), and tolerance set \(N(r,\mathbf d)\),

\[
\widehat\gamma(r,\mathbf d)=
\frac{1}{2|N(r,\mathbf d)|}
\sum_{(i,j)\in N(r,\mathbf d)}
\left\{z(\mathbf s_i)-z(\mathbf s_j)\right\}^{2}.
\]

In practice, the pair set also uses a lag-width tolerance and may use a bandwidth perpendicular to the direction. The estimator can be unstable when few pairs support a direction or when sampling geometry is strongly irregular.

A defensible diagnostic sequence is:

1. inspect the spatial distribution and sampling design before interpreting directional curves;
2. remove or model a defensible mean trend before attributing its structure to covariance;
3. compare directional variograms using comparable lag support and pair counts;
4. examine multiple nested scales and uncertainty in the empirical estimates;
5. check whether the inferred principal direction is stable under reasonable binning choices;
6. validate the resulting model for the intended spatial transfer task.

An elongated cloud of sample locations can create apparent directional differences simply because some directions have little pair support. Directional variograms are diagnostics, not proof of a physical mechanism.

## 4. Nonstationarity: separate the mean, variance and dependence

A useful decomposition is

\[
Z(\mathbf s)=m(\mathbf s)+\sigma(\mathbf s)X(\mathbf s),
\]

where \(m(\mathbf s)\) is a mean or trend, \(\sigma(\mathbf s)>0\) is a location-dependent standard-deviation scale, and \(X(\mathbf s)\) is a zero-mean unit-variance process with a valid correlation function \(R(\mathbf s,\mathbf u)\).

Then

\[
\operatorname{Cov}\{Z(\mathbf s),Z(\mathbf u)\}
=\sigma(\mathbf s)\sigma(\mathbf u)R(\mathbf s,\mathbf u).
\]

If \(R\) is a valid correlation function and the scale function is finite, this covariance is valid: it is obtained by scaling the rows and columns of a positive-semidefinite covariance matrix. This provides a safe way to model spatially varying variance without inventing an arbitrary pairwise covariance formula.

The components answer different questions:

- A changing \(m(\mathbf s)\) describes systematic expected variation, often associated with covariates or a broad trend.
- A changing \(\sigma(\mathbf s)\) describes local variability after accounting for the mean.
- A changing \(R(\mathbf s,\mathbf u)\) describes how residual dependence varies with location and pair geometry.

A trend can produce an increasing empirical semivariogram even when residual dependence is stationary. Conversely, removing a trend does not guarantee stationary residual covariance. Diagnose these components separately.

## 5. Constructing valid nonstationary dependence

A common mistake is to replace the stationary range \(a\) in a covariance formula with an arbitrary location-dependent value \(a(\mathbf s)\), then evaluate the formula using one endpoint or an average of both endpoints. Symmetry may be retained, but positive definiteness is not guaranteed. A covariance must be valid jointly for every finite set of locations, not merely plausible for each pair.

Several principled approaches exist.

### 5.1 Covariate-dependent covariance parameters

A spatially varying parameter model can be useful when the covariance construction is known to remain valid. The model must specify how parameters at both endpoints jointly determine covariance and must establish positive definiteness. A convenient interpolation of local ranges is not, by itself, such a proof.

### 5.2 Spatial deformation

A deformation maps the original domain through a transformation \(\mathbf f:D\to\mathbb R^d\), then applies a valid stationary covariance in transformed space:

\[
C(\mathbf s,\mathbf u)
=C_0\!\left(\mathbf f(\mathbf s)-\mathbf f(\mathbf u)\right).
\]

If \(C_0\) is a valid covariance and \(\mathbf f\) is a well-defined mapping, the pullback covariance is valid. Deformation can represent spatially varying effective distances, but it may distort geography, be difficult to identify, and require regularisation. The deformed coordinates are a statistical device, not a replacement for the authoritative CRS or physical distance.

### 5.3 Process convolution

Let \(W\) be spatial white noise and let \(K_{\mathbf s}(\mathbf v)\) be a square-integrable kernel that may vary with the target location. Define

\[
X(\mathbf s)=\int_D K_{\mathbf s}(\mathbf v)\,W(d\mathbf v).
\]

The induced covariance is

\[
C(\mathbf s,\mathbf u)=
\int_D K_{\mathbf s}(\mathbf v)
K_{\mathbf u}(\mathbf v)\,d\mathbf v.
\]

This is positive semidefinite because for any coefficients \(a_i\),

\[
\sum_i\sum_j a_i a_j C(\mathbf s_i,\mathbf s_j)
=
\int_D\left\{
\sum_i a_i K_{\mathbf s_i}(\mathbf v)
\right\}^{2}d\mathbf v
\geq 0.
\]

Location-varying kernels can encode local orientation, scale and shape while preserving covariance validity by construction. Kernel design, boundary treatment, computational cost and parameter identifiability remain substantive modelling choices.

### 5.4 Locally stationary approximations

A local model estimates dependence within neighbourhoods or moving windows. It can be useful descriptively and computationally, but independently fitted local covariance models do not automatically combine into one globally valid covariance function. Predictions near window boundaries and in sparse regions need explicit treatment.

## 6. Intrinsic models, trends and universal kriging

Some fields are better described through increments than through a stationary covariance. Intrinsic random-function models and generalized covariances extend the variogram framework, but require their own assumptions and valid estimation equations.

For a trend represented by known basis functions,

\[
m(\mathbf s)=\mathbf f(\mathbf s)^{\mathsf T}\boldsymbol\beta,
\]

the residual dependence model should be assessed after accounting for the trend. Universal kriging estimates the trend jointly with prediction under its specified covariance or generalized covariance assumptions. It does not make an arbitrary trend or residual model correct.

Covariates can include terrain, elevation, land cover, distance to a source, sensor geometry or physical drivers. Avoid using covariates that leak the target or would be unavailable at prediction time. Check extrapolation when prediction locations fall outside the covariate range represented by training data.

## 7. Consequences for prediction and validation

An anisotropic model changes which observations are informative for a target location. A nonstationary model may have different prediction uncertainty and effective support across the domain. Consequently:

- a single global range or block size may be inappropriate;
- a random split can conceal poor transfer across environmental or structural boundaries;
- validation blocks should represent the regions, directions and scales where the model will be deployed;
- uncertainty should reflect parameter estimation and model choice where those are material;
- extrapolation beyond observed covariate or process regimes should be reported separately from interpolation.

Compare candidate models using spatially meaningful holdouts, residual diagnostics, predictive calibration and sensitivity to model assumptions. A lower fitting error alone does not establish better transfer or more credible uncertainty.

## 8. Repository connections

| Concept | Related repository resource | Relationship |
|---|---|---|
| Empirical directional and omnidirectional variograms | [Empirical semivariogram method](../../methods/empirical-semivariogram.md) and [implementation](../../implementations/python/empirical-semivariogram/README.md) | Pair construction and empirical diagnostics; model assumptions remain explicit |
| Fitting and comparing covariance structures | [Variogram model fitting](../../algorithms/geostatistics/variogram-model-fitting.md) | Parameter fitting is distinct from proving stationarity or selecting the correct physical model |
| Kriging under alternative structures | [Kriging variants](../../algorithms/geostatistics/kriging-variants.md) and [implementation](../../implementations/python/kriging-variants/README.md) | Prediction methods depend on the specified mean and covariance assumptions |
| Spatial validation | [Spatial cross-validation](../../methods/spatial-cross-validation.md) | Holdout geometry should reflect intended spatial transfer |
| Nonseparable space-time dependence | [Nonseparable space-time covariance implementation](../../implementations/python/nonseparable-space-time-covariance/README.md) | Extends dependence beyond separable space/time factors; it is not automatically a nonstationary spatial model |

These connections identify reusable repository assets. They do not imply that each implementation currently estimates every model family discussed here.

## 9. Practical modelling checklist

Before adopting an anisotropic or nonstationary field model, record:

1. the random quantity, units and observation support;
2. the spatial domain, coordinate reference, distance metric and epoch where relevant;
3. the sampling frame, observation effort and spatial coverage;
4. the mean/trend model and the covariates available at deployment;
5. whether variance and dependence are expected to vary with location;
6. directional pair counts, lag support and uncertainty in empirical variograms;
7. the mathematical construction that guarantees covariance validity;
8. parameter identifiability and sensitivity to neighbourhood or basis choices;
9. the validation design and target transfer distance or region;
10. limitations, extrapolation conditions and uncertainty components not represented.

## 10. Further reading

- Chilès, J.-P., and Delfiner, P. (2012). *Geostatistics: Modeling Spatial Uncertainty*, 2nd ed. Wiley.
- Cressie, N. (1993). *Statistics for Spatial Data*, revised ed. Wiley.
- Sampson, P. D., and Guttorp, P. (1992). Nonparametric estimation of nonstationary spatial covariance structure. *Journal of the American Statistical Association*, 87(417), 108–119.
- Paciorek, C. J., and Schervish, M. J. (2006). Spatial modelling using a new class of nonstationary covariance functions. *Environmetrics*, 17(5), 483–506.
- Higdon, D. (2002). Space and space-time modeling using process convolutions. In *Quantitative Methods for Current Environmental Issues*. Springer.

The references provide routes for deeper study; the module remains an initial synthesis pending independent review.

## 11. Check your understanding

1. What distinguishes geometric anisotropy from zonal anisotropy?
2. Why must the coordinate metric and units be stated before estimating directional ranges?
3. How can an unmodelled mean trend be mistaken for long-range spatial dependence?
4. Why does multiplying a valid correlation function by \(\sigma(\mathbf s)\sigma(\mathbf u)\) preserve covariance validity?
5. Why is substituting a location-varying range into an isotropic covariance formula not automatically valid?
6. Show why the process-convolution covariance is positive semidefinite.
7. What does spatial deformation change, and what must it not be confused with?
8. Why can a collection of locally fitted covariance models fail to define a valid global model?
9. How should validation change when the intended use is transfer across a structural boundary?
10. Which model limitations would matter most when predicting beyond the observed environmental regime?
