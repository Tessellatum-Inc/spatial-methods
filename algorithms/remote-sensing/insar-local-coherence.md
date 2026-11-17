# Local interferometric coherence

## Definition

For coregistered complex master and slave SLC images, local magnitude coherence over a window W is

γ = |mean_W(master × conjugate(slave))| / sqrt(mean_W(|master|²) × mean_W(|slave|²)).

The estimator is bounded in [0, 1] up to floating-point error. It measures local phase consistency, not displacement by itself. The package also provides a signed after-minus-before difference for aligned coherence maps.

## Assumptions

The images must be coregistered, finite, same-grid complex arrays. A square odd-sized moving window is used without padding; therefore the output is smaller than the input. Windows with insufficient mean power return NaN.

## Scope limits

This is only a local coherence estimator. It is not a complete InSAR processor and does not implement orbit refinement, TOPS handling, precise co-registration, flattening, phase filtering, unwrapping, atmospheric correction, geocoding, PS/SBAS time series, offset tracking, tomography or autofocus.