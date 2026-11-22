# Gaussian random-field inference and conditional simulation

**Subject identity:** \`SM-FND-005\` — Spatial statistics and stochastic processes  
**Module:** 04  
**Status:** Initial researched teaching resource; independent technical review and learner testing pending.

## 1. A Gaussian random field

A Gaussian random field is a collection of random variables for which every finite vector of field values has a multivariate normal distribution. For locations \(\mathbf s_1,\ldots,\mathbf s_n\),

\[
\mathbf Z=
\begin{bmatrix}
Z(\mathbf s_1)&\cdots&Z(\mathbf s_n)
\end{bmatrix}^{\mathsf T}
\sim\mathcal N(\mathbf m,\Sigma).
\]

The mean vector contains \(m(\mathbf s_i)\), and the covariance matrix contains \(C(\mathbf s_i,\mathbf s_j)\). The covariance function must be valid: every finite covariance matrix must be symmetric positive semidefinite.

Gaussianity is a distributional assumption, not a synonym for spatial continuity. It makes conditional distributions analytically tractable, but may be unsuitable for strongly skewed, bounded, heavy-tailed, zero-inflated or multimodal quantities unless an appropriate transformation or alternative model is justified.

## 2. Conditioning a joint Gaussian distribution

Partition a jointly Gaussian vector into observed and target components:

\[
\begin{bmatrix}
\mathbf Z_o\\
\mathbf Z_* 
\end{bmatrix}
\sim
\mathcal N\left(
\begin{bmatrix}\mathbf m_o\\\mathbf m_*\end{bmatrix},
\begin{bmatrix}
K_{oo}&K_{o*}\\
K_{*o}&K_{**}
\end{bmatrix}
\right).
\]

If \(K_{oo}\) is nonsingular, the conditional target distribution is

\[
\mathbf Z_*\mid\mathbf Z_o=\mathbf z_o
\sim\mathcal N(\boldsymbol\mu_{*|o},K_{*|o}),
\]

with

\[
\boldsymbol\mu_{*|o}
=\mathbf m_*+
K_{*o}K_{oo}^{-1}(\mathbf z_o-\mathbf m_o),
\]

\[
K_{*|o}
=K_{**}-K_{*o}K_{oo}^{-1}K_{o*}.
\]

In computation, solve linear systems using Cholesky factorisation where the matrix is positive definite; do not explicitly form \(K_{oo}^{-1}\). Numerical jitter may stabilise a solve, but it changes the effective covariance and must be reported rather than treated as a physical measurement-error term.

The conditional mean is the minimum mean-square-error predictor under the specified Gaussian model. The conditional covariance describes residual uncertainty after conditioning on the observations and fixed model parameters. It does not automatically include uncertainty in estimated mean, covariance parameters, data quality, support mismatch or model choice.

## 3. Observation noise and the latent target

Measurements often include noise:

\[
\mathbf Y_o=\mathbf Z_o+\boldsymbol\epsilon,
\qquad
\boldsymbol\epsilon\sim\mathcal N(\mathbf 0,R),
\]

with noise independent of the latent field in this basic model. Then the observation covariance is \(K_{oo}+R\), while the latent target cross-covariance remains \(K_{*o}\). Therefore,

\[
\operatorname E[\mathbf Z_*\mid\mathbf Y_o=\mathbf y_o]
=\mathbf m_*+
K_{*o}(K_{oo}+R)^{-1}(\mathbf y_o-\mathbf m_o),
\]

\[
\operatorname{Cov}(\mathbf Z_*\mid\mathbf Y_o)
=K_{**}-K_{*o}(K_{oo}+R)^{-1}K_{o*}.
\]

The target here is the latent field, not a future noisy measurement. To predict a future observation, add its observation-noise covariance to the latent predictive covariance, with any relevant cross-covariance model stated explicitly.

A nugget can represent microscale field variation, measurement error, or a combination, depending on the model and sampling support. It should not be assigned a measurement interpretation without evidence. Replicates, calibration information or a separate observation model may be needed to distinguish these components.

## 4. Kriging is a conditional expectation under the model

For a Gaussian field with known mean and covariance, the conditional mean above is also the simple-kriging predictor. Its conditional variance is the corresponding simple-kriging variance.

Ordinary and universal kriging instead treat an unknown mean or drift as an unknown fixed component and impose unbiasedness constraints. Their block systems are best linear unbiased prediction systems. They are not identical to simply inserting an estimated trend into the known-mean Gaussian conditional formula: uncertainty and constraints associated with the unknown drift affect the predictor and variance.

Under Gaussian assumptions, universal-kriging predictors coincide with appropriate Gaussian conditional calculations under a diffuse/improper prior treatment of the regression coefficients, subject to the model's rank and identifiability conditions. Keep the chosen inferential interpretation explicit.

A kriging variance is conditional on the supplied model and parameters. A small value is not proof that the covariance family, trend, sampling design or data are correct.

## 5. Prediction and conditional simulation answer different questions

**Prediction** summarises the conditional distribution, commonly through its mean and variance. It gives a central estimate and a measure of uncertainty at each target.

**Conditional simulation** generates complete realisations from the joint conditional distribution. A realisation preserves spatial dependence among target cells; it is not a collection of independent draws from each cell's marginal predictive distribution.

Use prediction when a central estimate and local uncertainty summary are the required outputs. Use conditional realisations when decisions depend on spatial configurations, connected regions, threshold exceedance, volumes, gradients, extremes or other nonlinear summaries of the whole field.

For a threshold \(c\), an ensemble can estimate

\[
\Pr\{Z(\mathbf s)>c\mid\mathbf y_o\}
\approx
\frac{1}{M}\sum_{m=1}^{M}
\mathbb 1\{Z^{(m)}(\mathbf s)>c\}.
\]

For a region \(A\), each realisation can be used to calculate a spatial functional \(g(Z^{(m)}_A)\), such as exceedance area or connected-component size. The resulting ensemble approximates the conditional distribution of that functional, which generally cannot be recovered from cellwise means and variances alone.

## 6. Sequential Gaussian simulation

A basic sequential simulator visits target nodes in an order and samples each node from its Gaussian conditional distribution given the observations and all previously simulated nodes. If each conditional distribution is calculated from the same valid joint Gaussian model, the resulting vector has the desired joint conditional distribution, apart from numerical approximation.

At step \(k\), let \(S_k\) contain the observations and previously simulated values. The next value is drawn as

\[
Z(\mathbf s_k)\mid Z(S_k)=\mathbf z(S_k)
\sim
\mathcal N\left(
m_{k|S_k},v_{k|S_k}
\right).
\]

The algorithm appends the simulated value to the conditioning set and continues. A seeded random path makes a run reproducible; it does not remove Monte Carlo uncertainty or model dependence.

A dense implementation that conditions on all prior nodes becomes expensive as the grid grows. Local neighbourhoods, sparse precision matrices, spectral methods, FFT-based methods, low-rank approximations, SPDE representations and other scalable methods introduce additional approximations or structural assumptions that must be evaluated.

## 7. Parameter uncertainty and model uncertainty

The conditional distribution above treats mean and covariance parameters as fixed. In practice, these may be estimated from the same data. Plug-in prediction can understate uncertainty, especially with sparse sampling, weak identifiability, strong trend-covariance confounding or flexible covariance families.

A fuller predictive distribution integrates over parameter uncertainty:

\[
p(\mathbf z_*\mid\mathbf y)
=\int p(\mathbf z_*\mid\mathbf y,\boldsymbol\theta)
\,p(\boldsymbol\theta\mid\mathbf y)\,d\boldsymbol\theta,
\]

where \(\boldsymbol\theta\) denotes model parameters. This can be approached with Bayesian inference, parametric bootstrap or other calibrated procedures. Alternative covariance families and mean structures add model uncertainty that is not represented merely by widening a plug-in Gaussian interval.

Do not confuse:
- conditional field uncertainty given fixed parameters;
- uncertainty in estimated parameters;
- measurement uncertainty in observations;
- uncertainty from the sampling design;
- structural uncertainty from model misspecification.

An uncertainty budget or predictive statement should identify which components are included and which are not.

## 8. Diagnostics and validation

A credible Gaussian-field workflow should examine:

1. the scientific meaning, units and support of the random quantity;
2. the mean/trend model and residual structure;
3. the sampling design, spatial coverage and observation-error model;
4. covariance validity and parameter identifiability;
5. numerical conditioning, duplicate locations and near-singular systems;
6. residual spatial structure and directional diagnostics;
7. predictive calibration, interval coverage and proper scoring rules;
8. spatial and temporal holdouts matched to the deployment task;
9. sensitivity to covariance family, range, smoothness and anisotropy;
10. parameter and model uncertainty not represented by the plug-in conditional distribution.

Simulation diagnostics should additionally inspect ensemble means, variances, variograms, cross-location dependence, reproduction of conditioning data under the stated noise model, and relevant spatial functionals. Matching cellwise histograms is not enough to validate spatial structure.

## 9. Repository connections and implementation boundaries

- [Simple, ordinary and universal kriging](../../algorithms/geostatistics/kriging-variants.md) explains the repository's covariance-based predictors and their mean assumptions.
- [Kriging implementation](../../implementations/python/kriging-variants/README.md) includes dense simple, ordinary and planar universal kriging plus seeded sequential Gaussian simulation. It is a small-grid reference implementation; it uses supplied covariance parameters and does not propagate hyperparameter uncertainty.
- [Variogram model fitting](../../algorithms/geostatistics/variogram-model-fitting.md) and [variogram models implementation](../../implementations/python/variogram-models/README.md) estimate covariance structures; fitting does not establish that the chosen family is scientifically appropriate.
- [Spatial cross-validation](../../methods/spatial-cross-validation.md) describes validation designs. Choose folds to represent the actual prediction geography and time.
- [Separable spatiotemporal Gaussian-process regression](../../algorithms/geostatistics/separable-spatiotemporal-gp.md) and [nonseparable space-time covariance](../../implementations/python/nonseparable-space-time-covariance/README.md) extend dependence across time. Separable and nonseparable are different covariance assumptions; neither is automatically nonstationary.
- [Anisotropic and nonstationary spatial fields](anisotropic-and-nonstationary-spatial-fields.md) develops spatially varying and directional dependence, which the basic stationary sequential simulator does not estimate.

The presence of runnable code is evidence of an executable computational example, not independent validation of its scientific assumptions or suitability for a particular field campaign.

## 10. Check your understanding

1. Derive the conditional mean and covariance of a partitioned multivariate Gaussian vector.
2. Why does observation noise enter the data covariance but not automatically the latent target variance?
3. Under what assumptions is simple kriging the Gaussian conditional expectation?
4. Why are ordinary and universal kriging not simply known-mean conditioning with an arbitrary fitted trend?
5. Why can independent cellwise draws not replace a joint conditional simulation?
6. Give an example of a spatial decision that depends on a complete realisation rather than cellwise means.
7. What changes when covariance parameters are estimated rather than known?
8. Why does a seeded simulation not establish that the model is valid?
9. Which diagnostics would reveal a simulation that matches marginal distributions but not spatial dependence?
10. What additional variance is needed when predicting a future noisy observation rather than the latent field?
