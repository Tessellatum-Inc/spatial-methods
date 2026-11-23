# HANTS: harmonic analysis of time series

HANTS represents a periodic signal with an intercept and Fourier
sine/cosine terms. It iteratively fits the current valid observations and
rejects the largest residual outside a user-selected low/high threshold.
The final harmonic curve can reconstruct values at missing and rejected
time steps.

The linked reference implementation uses least squares, explicit period
and harmonic count, optional irregular time coordinates, NaN missing values,
and a minimum-observation guard. It is a compact baseline; HANTS variants
differ in weighting, rejection policy and quality-flag integration. Period
selection, sampling irregularity, sensor quality masks and uncertainty
remain application-specific.
