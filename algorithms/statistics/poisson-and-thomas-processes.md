# Homogeneous Poisson and Thomas point-process models

Stable IDs: SA-STAT-HOMOGENEOUS-POISSON, SA-STAT-THOMAS · Source compendium section 2, page 3

## Homogeneous Poisson point process

A homogeneous planar Poisson process (HPPP) with intensity λ has independent counts in disjoint regions. For a region B of area |B|:

\[
N(B)\sim\operatorname{Poisson}(\lambda |B|).
\]

Conditional on N(B)=n, the n locations are independent and uniformly distributed in B. The intensity has units of events per squared coordinate unit. Under the homogeneous Poisson model, the pair-correlation function is one and Ripley's K is πr².

This model is a useful baseline for complete spatial randomness (CSR), but CSR is a model assumption, not a universal description of randomness. Spatially varying intensity, barriers, sampling effort and dependence can all make a homogeneous model unsuitable.

## Thomas cluster process

The Thomas process is a Gaussian Neyman–Scott Poisson cluster process:

1. Generate latent parent locations from a homogeneous Poisson process with intensity κ.
2. For each parent, draw a Poisson number of offspring with mean μ.
3. Displace each offspring independently from its parent by an isotropic bivariate Gaussian vector with standard deviation σ along each coordinate axis.
4. Observe the offspring only; parent locations are latent construction variables.

The stationary mean offspring intensity is:

\[
\lambda=\kappa\mu.
\]

Small σ produces tight clusters; larger σ spreads offspring around their parents. The process is stationary and isotropic under the homogeneous parent process and isotropic Gaussian displacement specification. It is a model of aggregation around latent centres, not a model for every form of clustering.

## Simulation details and boundary handling

The homogeneous simulator draws the event count exactly from a Poisson distribution using exponential inter-arrival times, then samples uniform coordinates in the rectangular window.

The Thomas simulator generates parent points in a buffer-expanded rectangle, generates offspring, and retains only offspring inside the target window. This avoids the obvious edge depletion caused by forcing all parents to lie inside the target window. Gaussian displacement has unbounded support, so a finite buffer necessarily truncates a small tail. The default buffer is four σ; the user can increase it and should assess sensitivity when edge accuracy matters.

Both functions use a fixed integer seed for reproducibility. They are simulation tools, not parameter estimators or goodness-of-fit tests.

## Interpretation and diagnostics

- Compare observed patterns with simulations under a scientifically justified null or fitted model.
- A CSR rejection says the chosen homogeneous Poisson model is inadequate; it does not prove a Thomas process.
- A Thomas-like cluster pattern does not identify the latent parents uniquely.
- Similar first-order intensity can coexist with very different second-order structure.
- Use K/L, pair correlation and nearest-neighbour summaries as descriptive diagnostics, then use simulation envelopes or a model-based test appropriate to the fitted model.
- Parameter uncertainty and model selection are not included in this simulator.

## Implementation scope

This page documents the homogeneous Poisson and Thomas simulators. The same dependency-free point-process package also provides separate, explicitly bounded simulators documented in their own canonical records:

- [Matérn disc-cluster process](matern-cluster-process.md): exact finite parent-buffer construction for its compact-support disc offspring kernel.
- [Log-Gaussian Cox process](log-gaussian-cox-process.md): a small-grid, piecewise-constant approximation using a dense exponential-covariance Cholesky factorisation.
- [Strauss interaction process](strauss-point-process.md): finite-window birth-death Metropolis–Hastings simulation for a repulsive Gibbs model.

These are generative teaching baselines, not fitted models. The LGCP grid approximation is not an exact continuous-field simulation; the Strauss chain is a finite-run approximate MCMC draw whose convergence is not diagnosed. General Gibbs potentials, broader inhomogeneous point-process models, parameter estimation, likelihood inference and formal goodness-of-fit procedures remain outside this implementation scope. See the package [README](../../implementations/python/point-process/README.md) for the complete module inventory and limitations.

## References

- Thomas, M. (1949). A generalisation of Poisson's binomial limit for use in ecology. *Biometrika*, 36(1/2), 18–25.
- Neyman, J., & Scott, E. L. (1958). Statistical approach to problems of cosmology. *Journal of the Royal Statistical Society: Series B*, 20(1), 1–43.
- Møller, J., & Waagepetersen, R. P. (2004). *Statistical Inference and Simulation for Spatial Point Processes*. Chapman & Hall/CRC.
- Baddeley, A., Rubak, E., & Turner, R. (2015). *Spatial Point Patterns: Methodology and Applications with R*. CRC Press.
- spatstat.random documentation for the Thomas process (rThomas).
