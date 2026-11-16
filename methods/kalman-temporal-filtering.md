# Scalar Kalman filtering and RTS smoothing for temporal observations

The local-level model treats an evolving latent signal as a random walk observed with noise:

\[
x_t=x_{t-1}+w_t,\quad w_t\sim N(0,Q),\qquad
y_t=x_t+v_t,\quad v_t\sim N(0,R).
\]

The scalar Kalman filter alternates prediction and observation update. With predicted state mean/variance \((m_t^-,P_t^-)\), the gain is

\[
K_t=\frac{P_t^-}{P_t^-+R},\quad
m_t=m_t^-+K_t(y_t-m_t^-),\quad
P_t=(1-K_t)P_t^-.
\]

A missing observation skips the measurement update and retains the prediction. The implementation returns filtered means and variances.

The Rauch–Tung–Striebel (RTS) backward pass uses the full observation sequence to revise earlier estimates. This is smoothing, not causal filtering: it is appropriate for retrospective reconstruction, but it must not be used as if it were an online estimate available at time t.

## Implementation scope

The [temporal-models package](../implementations/python/temporal-models/README.md) includes a scalar random-walk filter and RTS smoother with optional missing observations. It does not implement a general vector/matrix Kalman filter, extended/unscented filters, data association, parameter estimation or a seasonal/trend state model. Process and observation variances must be supplied.

## Spatial and EO use

This baseline can smooth a single extracted pixel or station series. Before interpreting it, consider irregular acquisition intervals, sensor-specific observation noise, cloud/missingness mechanisms, seasonality and abrupt changes. A local-level model can oversmooth genuine abrupt transitions; a change-point or switching-state model may be more appropriate.

## Sources

- Kalman, R. E. (1960). “A New Approach to Linear Filtering and Prediction Problems.” *Journal of Basic Engineering*, 82(1), 35–45. DOI: [10.1115/1.3662552](https://doi.org/10.1115/1.3662552).
- Rauch, H. E., Tung, F., & Striebel, C. T. (1965). “Maximum Likelihood Estimates of Linear Dynamic Systems.” *AIAA Journal*, 3(8), 1445–1450. DOI: [10.2514/3.3166](https://doi.org/10.2514/3.3166).

No source text or figures are reproduced.
