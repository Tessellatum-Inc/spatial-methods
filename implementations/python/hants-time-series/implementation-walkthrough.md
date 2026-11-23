# HANTS implementation walkthrough

1. Build an intercept and sine/cosine columns for each requested harmonic.
2. Fit the current valid observations by least squares.
3. Calculate residuals for all finite observations.
4. Identify residuals outside the chosen low, high or two-sided thresholds.
5. Remove the single largest threshold exceedance and refit.
6. Stop when no residual exceeds its threshold, the iteration limit is
   reached, or removing another observation would violate the minimum
   sample-size guard.

The final harmonic curve reconstructs values at missing and rejected time
steps. A false convergence flag is an incomplete fit, not a successful
gap-fill.
