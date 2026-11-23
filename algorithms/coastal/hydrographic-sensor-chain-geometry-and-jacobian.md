# GNSS–IMU–transducer sounding-point geometry and Jacobian

## Frames and model

Let \(n,i,t\) denote navigation, IMU and transducer frames. The GNSS
position \(\mathbf r_{n,g}\) refers to the antenna reference point.
The lever arms \(\mathbf l_{i,g}\) and \(\mathbf l_{i,t}\) both point outward
from the IMU origin and are expressed in IMU axes. The acoustic vector
\(\mathbf s_t\) is expressed in transducer axes. Rotations map
\(\mathbf R_{n\leftarrow i}\) from IMU to navigation and
\(\mathbf R_{i\leftarrow t}\) from transducer to IMU.

\[
\mathbf r_{n,i}=\mathbf r_{n,g}-
\mathbf R_{n\leftarrow i}\mathbf l_{i,g}
\]

\[
\boxed{\mathbf p_n=\mathbf r_{n,g}+
\mathbf R_{n\leftarrow i}(-\mathbf l_{i,g}+\mathbf l_{i,t}+
\mathbf R_{i\leftarrow t}\mathbf s_t)}
\]

The negative GNSS lever-arm term follows from solving for the IMU origin.
If the navigation solution already reports the IMU origin, do not apply the
antenna correction a second time.

## Jacobian and conventions

Define \(\mathbf q=\mathbf R_{i\leftarrow t}\mathbf s_t\) and
\(\mathbf v_n=\mathbf R_{n\leftarrow i}(-\mathbf l_{i,g}+\mathbf l_{i,t}+\mathbf q)\).
For input order
\([\mathbf r_{n,g},\delta\boldsymbol\theta_n,\mathbf l_{i,g},
\mathbf l_{i,t},\delta\boldsymbol\phi_i,\mathbf s_t]\),

\[
\mathbf J=[\mathbf I,-[\mathbf v_n]_\times,
-\mathbf R_{n\leftarrow i},\mathbf R_{n\leftarrow i},
-\mathbf R_{n\leftarrow i}[\mathbf q]_\times,
\mathbf R_{n\leftarrow i}\mathbf R_{i\leftarrow t}].
\]

Attitude errors are left-multiplicative: navigation attitude error is in
navigation axes and transducer mounting error is in IMU axes. Angular
derivatives are per radian.

## Time dependence

A sounding must use the navigation pose at the ping epoch, with an explicit
sensor time offset. The [time-aligned sensor-chain method](hydrographic-time-aligned-sensor-chain.md)
defines two-state position and SO(3) attitude interpolation, rejects
extrapolation and appends a timing-sensitivity column to form a 3 by 19
Jacobian. This enables timing uncertainty and its correlations to be included
in joint covariance propagation.

## Covariance

For joint input covariance \(\mathbf C_x\), first-order output covariance is

\[
\mathbf C_p=\mathbf J\mathbf C_x\mathbf J^T.
\]

Preserve correlations among trajectory, installation, timing and calibration
parameters. Shared uncertain parameters across pings induce cross-ping
covariance; treating every ping independently discards that structure.

## Computational reference

The [Python sensor-chain implementation](../../implementations/python/hydrographic-sensor-chain/README.md)
contains static geometry and time-aligned interpolation, with finite-difference
tests for the geometric and timing sensitivities.

## Limits

These are bounded geometry and interpolation components, not a complete
navigation estimator or TPU engine. They do not model clock drift, latency
estimation, asynchronous filtering, heave/draft/squat, vessel flexure, water
column refraction, bottom detection or vertical datum reduction.
