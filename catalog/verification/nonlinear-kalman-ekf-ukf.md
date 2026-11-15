# Source verification — nonlinear Kalman filters (EKF and UKF)

## Identity and bibliography
- Julier & Uhlmann (1997), “A New Extension of the Kalman Filter to Nonlinear Systems,” Proceedings of SPIE 3068.
- Julier & Uhlmann (2004), “Unscented Filtering and Nonlinear Estimation,” Proceedings of the IEEE 92(3), 401–422, DOI 10.1109/JPROC.2003.823141.
- Wan & van der Merwe (2000), “The Unscented Kalman Filter for Nonlinear Estimation,” IEEE Adaptive Systems for Signal Processing, Communications, and Control Symposium, pp. 153–158, DOI 10.1109/ASSPCC.2000.882463.

- Godsill, S. J., Doucet, A., & West, M. (2004), “Monte Carlo smoothing for nonlinear time series,” *Journal of the American Statistical Association*, 99(465), 156–168, DOI 10.1198/016214504000000151. The forward-filtering backward-simulation construction and its transition-density weighting were cross-checked against the article and standard particle-smoothing derivations.

## Technical claims
- EKF applies local first-order linearization to nonlinear process and observation models.
- UKF propagates deterministic sigma points through nonlinear transformations to approximate transformed moments, rather than requiring model Jacobians.
- Both retain a Gaussian mean/covariance approximation and are not exact general nonlinear Bayesian filters.
- Scaled UKF uses alpha, beta and kappa parameters; tuning and covariance numerical behavior matter.

## Implementation/reproduction
Implemented: discrete additive-noise EKF with supplied analytic Jacobians and Joseph update; scaled UKF with 2n+1 state sigma points; single-step and sequence APIs; innovation diagnostics. Tests are authored for linear-model agreement, nonlinear observation behavior, sequence shapes and invalid inputs.

Implemented in companion modules: bootstrap/SIR particle filtering with weighted particle histories and FFBSi backward simulation using supplied transition log densities. Tests cover deterministic supported paths, filtering-weight contribution to backward probabilities, end-to-end use of bootstrap-filter history, trajectory/moment shapes and invalid transition/history inputs. Not implemented: FFBSm, particle Gibbs/MCMC, ancestor sampling, nonlinear RTS smoothing, non-additive/correlated noise, control inputs, angular residual handling, adaptive noise, gating, square-root UKF or constraints. Repository CI is still required to establish passing tests.

## Rights
Original explanatory text and bibliographic metadata only; no source figures, code or datasets reproduced.
