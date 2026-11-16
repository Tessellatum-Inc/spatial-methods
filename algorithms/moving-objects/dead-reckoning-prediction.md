# Moving-object dead-reckoning prediction

The state is ([x,y,v_x,v_y]^T). Under a constant-velocity model over interval (Delta t),

\[
F=\begin{bmatrix}
1&0&\Delta t&0\\
0&1&0&\Delta t\\
0&0&1&0\\
0&0&0&1
\end{bmatrix},
\qquad x_{t+1}=Fx_t.
\]

Covariance propagates as (P_{t+1}=FP_tF^T+Q). The implementation uses the standard white-acceleration process-noise block with caller-supplied acceleration standard deviation.

The 2D position covariance defines a Gaussian confidence ellipse. For confidence (p), the two-dimensional chi-square quantile is (-2\log(1-p)); multiplying this by the covariance eigenvalues gives squared ellipse radii. The update policy requests a new report when displacement from the last report, major-axis uncertainty radius or elapsed time reaches a declared threshold.

## Limits

The model assumes constant velocity between reports. It is not a full Kalman filter or moving-object database and does not provide map matching, road-network constraints, manoeuvre models, multi-object association or predictive spatial query execution.

## Verification

Tests compare state and covariance propagation with direct matrix equations, check the process-noise block analytically, verify confidence-ellipse axes, exercise each update trigger and validate invalid states/controls.

See the [implementation package](../../implementations/python/moving-object-prediction/README.md).
