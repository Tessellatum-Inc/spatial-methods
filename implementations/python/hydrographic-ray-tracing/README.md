# Temporally correlated sound-speed profile uncertainty

This module constructs a joint covariance for layered sound-speed-profile
errors observed at multiple survey epochs. It complements the ray tracer's
single-epoch profile covariance and the sensor-chain multi-ping Jacobian.

## Model

Let \(C_p\) be the covariance between layer sound-speed errors at one epoch.
Temporal dependence is represented by a stationary exponential kernel:

\[
R_{ij}=\exp\left(-\frac{|t_i-t_j|}{\tau}\right),
\]

where \(\tau>0\) is the temporal correlation time. The joint covariance is
separable:

\[
C_{(i,k),(j,\ell)}=R_{ij}(C_p)_{k\ell}.
\]

The state order is epoch-major: all layer errors at the first supplied
epoch, then all layer errors at the second epoch, and so forth. The supplied
epoch order is preserved. Repeated epochs are permitted and have unit
temporal correlation.

## API

\`build_temporally_correlated_sound_speed_covariance(
profile_epochs_s, single_epoch_profile_covariance, correlation_time_s)\`

The returned mapping contains the joint profile covariance, temporal
correlation matrix, epochs, correlation time, layer count and state-order
description. The single-epoch profile covariance must be finite, symmetric
and positive semidefinite. The exponential temporal kernel is positive
semidefinite, so its Kronecker/separable product with the profile covariance
is also positive semidefinite.

## Connecting to multi-ping ray tracing

For ping \(i\), evaluate the ray endpoint Jacobian with respect to its
epoch's layer speeds. Compose that profile block through the endpoint-to-
sounding sensor-chain Jacobian. Stack those per-ping profile sensitivities
in the same epoch-major order as the returned covariance, then include the
resulting temporal profile state block in the full multi-ping input
covariance. This retains both vertical cross-layer correlation and
cross-epoch correlation in the final sounding covariance.

Do not duplicate one profile state into independent ping blocks. Do not
interpret \(\tau\) as a universal oceanographic constant: estimate or
select it from the survey's environmental sampling cadence and observed
profile variability, and perform sensitivity analysis. The model describes
correlated anomalies around supplied epoch-specific mean profiles; it does
not evolve the mean profile, infer water-mass advection, or replace CTD,
SVP, XBT, MVP or other in-situ observations.

## Scope

This is a separable first-order covariance model. It assumes the same
vertical covariance structure at each epoch and one exponential temporal
correlation scale shared across layers. More complex depth-dependent
temporal scales, nonstationarity, horizontal variability, currents and
profile interpolation uncertainty require richer environmental models.
