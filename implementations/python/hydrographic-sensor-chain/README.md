# Hydrographic multi-stage sensor-chain geometry

Dependency-free first-order geometry from a GNSS antenna reference point through
an IMU and mounted transducer to an acoustic detection point.

## Frames and static model

Let \(n\), \(i\), and \(t\) be navigation, IMU, and transducer frames.
\(\mathbf l_{i,g}\) and \(\mathbf l_{i,t}\) are vectors from the IMU origin to
the GNSS antenna and transducer origins, both expressed in IMU axes.
\(\mathbf s_t\) runs from transducer origin to acoustic detection in transducer
axes. \(\mathbf R_{n\leftarrow i}\) maps IMU to navigation and
\(\mathbf R_{i\leftarrow t}\) maps transducer to IMU.

\[
\mathbf p_n=\mathbf r_{n,g}+
\mathbf R_{n\leftarrow i}(-\mathbf l_{i,g}+\mathbf l_{i,t}+
\mathbf R_{i\leftarrow t}\mathbf s_t).
\]

The negative antenna lever-arm term follows from solving for the IMU origin.
The supplied GNSS position must refer to the antenna. If the navigation
solution already reports the IMU origin, do not apply this correction again.

## Static Jacobian

For \(\mathbf q=\mathbf R_{i\leftarrow t}\mathbf s_t\) and
\(\mathbf v_n=\mathbf R_{n\leftarrow i}(-\mathbf l_{i,g}+\mathbf l_{i,t}+\mathbf q)\),
the static input order is
\([\mathbf r_{n,g},\delta\boldsymbol\theta_n,\mathbf l_{i,g},
\mathbf l_{i,t},\delta\boldsymbol\phi_i,\mathbf s_t]\), and

\[
\mathbf J=[\mathbf I,-[\mathbf v_n]_\times,
-\mathbf R_{n\leftarrow i},\mathbf R_{n\leftarrow i},
-\mathbf R_{n\leftarrow i}[\mathbf q]_\times,
\mathbf R_{n\leftarrow i}\mathbf R_{i\leftarrow t}].
\]

Both attitude perturbations are left-multiplicative; their angular derivatives
are per radian.

## Time-aligned pose interpolation

The time-aligned module evaluates the chain at
\(t_e=t_{ping}+\Delta t\). GNSS position is linearly interpolated between two
bracketing navigation epochs, and attitude is interpolated along the shortest
SO(3) geodesic. Extrapolation is rejected rather than silently extending a
trajectory beyond its support.

The returned Jacobian is 3 by 19: the static 18 columns followed by the
time-offset sensitivity \(\partial\mathbf p/\partial\Delta t\), in
coordinate-units per second. Under the segment's constant-velocity and
constant-body-angular-rate interpolation assumptions,

\[
\frac{\partial\mathbf p_n}{\partial\Delta t}
=\frac{\mathbf r_{n,g,1}-\mathbf r_{n,g,0}}{t_1-t_0}
+\mathbf R_{n\leftarrow i}
\left[\frac{\boldsymbol\phi}{t_1-t_0}\right]_\times
\mathbf v_i,
\]

where \(\boldsymbol\phi=\log(\mathbf R_{n\leftarrow i,0}^{T}
\mathbf R_{n\leftarrow i,1})\) and
\(\mathbf v_i=-\mathbf l_{i,g}+\mathbf l_{i,t}+
\mathbf R_{i\leftarrow t}\mathbf s_t\).
Positive \(\Delta t\) means evaluating navigation later than the ping timestamp.
This is a local timing derivative for the chosen interpolation model, not an
estimate of actual sensor latency.

The 3 by 19 Jacobian can be combined with a joint covariance whose final
parameter is the time offset in seconds. If timing is correlated with
trajectory or calibration parameters, retain those off-diagonal covariance
terms; do not add timing variance as though it were automatically independent.

## Run and test

    python -m pip install -r requirements.txt
    python -m pytest -q

Tests cover identity and composed rotations, lever-arm signs, all static
Jacobian blocks by finite differences, time interpolation, time sensitivity
by finite differences, extrapolation rejection and invalid inputs.

## Scope

The temporal model uses only two bracketing states, linear position and
constant-rate geodesic attitude interpolation. It does not model higher-order
trajectory dynamics, asynchronous sensor filtering, latency estimation,
clock drift, time-varying lever arms, heave/draft/squat, vessel flexure,
acoustic ray tracing, beamforming, bottom detection, vertical datum reduction,
calibration estimation or full hydrographic TPU. It is not a substitute for
instrument-specific calibration or field validation.
