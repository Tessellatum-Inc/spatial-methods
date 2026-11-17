# Implementation walkthrough: kriging variants

1. Build the data covariance matrix from pairwise sample distances and the
   selected permissible covariance family.
2. Add nugget and observation noise to the observation diagonal. The target
   remains the latent field, so its marginal variance is the partial sill.
3. Build the data-to-target covariance matrix for all prediction locations.
4. For simple kriging, solve the covariance system directly and add the
   known mean back to the predicted residual.
5. For ordinary kriging, augment the covariance matrix with a constant drift
   column and its unbiasedness constraint.
6. For universal kriging, augment it with the intercept and normalized x/y
   drift columns. Reject a rank-deficient drift design.
7. Solve the systems for all targets together. Calculate prediction variance
   from the same weights and Lagrange multipliers.
8. Reject singular/non-finite systems and materially negative variances;
   clip only small negative round-off to zero.

The implementation deliberately avoids a pseudo-inverse. A singular system
usually signals duplicate locations, a rank-deficient drift design or
inappropriate covariance parameters that need diagnosis.



## Sequential Gaussian simulation

The simulator uses simple kriging as its conditional distribution engine.
At each randomised grid location it builds the covariance matrix for all
observations and previously simulated latent cells, adds measurement noise
only to original observations, solves for conditional weights and samples a
normal draw with the corresponding conditional variance. The new simulated
cell is then added to the conditioning set. This is sequential conditional
simulation, not an unconditional field draw and not an indicator or
multiple-point simulator.
