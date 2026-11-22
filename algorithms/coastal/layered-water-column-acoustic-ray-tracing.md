

## Temporally correlated sound-speed profile uncertainty

A survey line may cross a changing water column. Treating one profile as
perfectly shared across every ping can understate temporal variability;
treating each ping's profile error as independent discards persistence
between nearby observations. The reference implementation
`build_temporally_correlated_sound_speed_covariance` in
`implementations/python/hydrographic-ray-tracing/temporal_sound_speed_covariance.py`
provides an intermediate model: epoch-specific profile errors with
cross-layer covariance and exponential temporal correlation.

For layer-error vector \(\mathbf c_i\) at epoch \(t_i\), let the same-epoch
profile covariance be \(C_p\), and let \(\tau\) be a positive correlation
time. Then

\[
R_{ij}=\exp\left(-\frac{|t_i-t_j|}{\tau}\right),
\qquad
C_{(i,k),(j,\ell)}=R_{ij}(C_p)_{k\ell}.
\]

The full state is epoch-major: all layer errors at one epoch, followed by
all layer errors at the next. This separable covariance retains vertical
cross-layer dependence and temporal persistence. It is positive
semidefinite when \(C_p\) is positive semidefinite because the exponential
kernel is a valid positive-semidefinite covariance kernel.

For multi-ping propagation, evaluate each ping's ray Jacobian against the
profile associated with that ping's environmental epoch, compose it through
the endpoint-to-sounding Jacobian, and stack the profile sensitivities in
the same epoch-major order. Use the resulting joint profile covariance as
one correlated state block in the full survey covariance. This is not the
same as a single static profile shared unchanged across the line, nor is it
a collection of independent per-ping profiles.

The correlation time is a model parameter to estimate or justify from
environmental observations and survey cadence; it is not a universal
constant. The model describes anomalies around epoch-specific mean
profiles. It does not advect or forecast the mean sound-speed field, model
horizontal gradients or currents, or replace direct SVP/CTD/XBT/MVP
observations. See the implementation README for the API and limitations.
