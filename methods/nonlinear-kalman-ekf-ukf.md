# Nonlinear state estimation: EKF and scaled UKF

## State-space model

Consider a discrete-time additive-noise model:

\[
x_{k+1}=f(x_k)+w_k,\qquad z_k=h(x_k)+v_k,
\]

where the process and observation noises have zero means and covariances Q and R. The filters propagate an approximate state mean and covariance; they do not propagate the complete posterior density.

## Extended Kalman filter

The EKF linearizes the process and observation functions locally. With prior estimate (x, P), prediction uses the Jacobian F of f:

\[
x^- = f(x),\quad P^- = FPF^T+Q.
\]

At the predicted state, the observation Jacobian H gives innovation r, innovation covariance S, and gain K:

\[
r=z-h(x^-),\quad S=HP^-H^T+R,\quad K=P^-H^TS^{-1}.
\]

The state update is x+ = x- + Kr. The implementation uses the Joseph covariance form
\[
P^+=(I-KH)P^-(I-KH)^T+KRK^T,
\]
which is preferable to the simplest subtractive form for numerical symmetry/positive-semidefinite behavior. Jacobians are supplied by the caller; finite differences and automatic differentiation are not silently substituted.

## Scaled unscented Kalman filter

The UKF uses a deterministic set of sigma points representing the state mean and covariance. Each point is propagated through the nonlinear transition. Weighted transformed moments form the predicted mean and covariance; transformed sigma points are then passed through the observation model. Cross-covariance gives the gain and the innovation updates the state.

The scaled transform uses alpha, beta and kappa to control sigma-point spread and weights. These are modelling/numerical choices, not universal constants. The code uses 2n+1 state sigma points and additive Q/R; it does not augment the state with noise variables.

## Implemented baseline

The [NumPy package](../implementations/python/state-estimation/README.md) provides EKF and scaled-UKF single-step and sequence functions for finite vector states, finite observation vectors, additive uncorrelated process/measurement noise, and time-invariant Q/R matrices. Tests include agreement with a linear Kalman update, a nonlinear scalar observation, sequence output shapes and input validation.

## Spatial applications and cautions

Examples include fusing GNSS/IMU observations, tracking moving objects, estimating vehicle motion, and smoothing noisy trajectories. Coordinate systems, units, map projections, angular variables and sensor timing must be handled consistently. Latitude/longitude should not be treated as an ordinary Euclidean state without an appropriate local or geodetic model. Bearing residuals require wrap-aware differences; this baseline intentionally does not provide them. A filter can be confidently wrong when its dynamics or noise covariances are misspecified.

## Limitations and adjacent methods

This is not an ensemble square-root filter or an RTS nonlinear smoother. The companion particle-filter module provides a bootstrap/SIR filter and an offline forward-filtering backward-simulation (FFBSi) particle smoother. FFBSi requires the complete stored filtering-particle history and a callable transition log density consistent with the forward transition sampler. It samples complete state trajectories by choosing the final particle from its filtering weights, then sampling each previous particle with probability proportional to its filtering weight times the transition density to the already selected next state. It is not an online smoother; its work is O(M T N) for M trajectories, T time steps and N particles, plus the cost of evaluating transition densities. It does not implement FFBSm, particle MCMC, ancestor sampling or a particle Gibbs smoother. The EKF/UKF still omit controls, non-additive/correlated noise, angle-aware statistics, gating, adaptive noise, square-root formulations, nonlinear RTS smoothing and state constraints. EKF performance depends on local linearity and Jacobian quality; UKF performance depends on sigma-point scaling and model/noise assumptions. Neither is generally an exact Bayesian solution for nonlinear systems.

## Sources

- Julier, S. J., & Uhlmann, J. K. (1997). “A New Extension of the Kalman Filter to Nonlinear Systems.” *Proceedings of SPIE*, 3068. [Paper](https://www.robots.ox.ac.uk/~cvrg/hilary2003/Julier1997_SPIE_KF.pdf).
- Julier, S. J., & Uhlmann, J. K. (2004). “Unscented Filtering and Nonlinear Estimation.” *Proceedings of the IEEE*, 92(3), 401–422. DOI: 10.1109/JPROC.2003.823141.
- Wan, E. A., & van der Merwe, R. (2000). “The Unscented Kalman Filter for Nonlinear Estimation.” *Proceedings of the IEEE 2000 Adaptive Systems for Signal Processing, Communications, and Control Symposium*, 153–158. DOI: 10.1109/ASSPCC.2000.882463.
- Godsill, S. J., Doucet, A., & West, M. (2004). “Monte Carlo smoothing for nonlinear time series.” *Journal of the American Statistical Association*, 99(465), 156–168. DOI: 10.1198/016214504000000151.

No source figures, code or datasets are reproduced.
