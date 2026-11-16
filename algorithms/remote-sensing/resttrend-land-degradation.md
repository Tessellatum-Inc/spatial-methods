# RESTREND land-degradation screening

RESTREND (residual trend) first estimates the relationship between vegetation response and precipitation at each pixel,

\[
NDVI_t=\alpha+\beta P_t+\epsilon_t,
\]

then examines the temporal trend in residuals \(\epsilon_t\). A negative residual trend can indicate vegetation decline not explained by the fitted rainfall relationship, but confounding processes and model misspecification can produce the same signal.

The reference implementation fits the rainfall response by ordinary least squares per pixel and reports the residual temporal slope, R-squared and p-value. It omits nonlinear rainfall response, lagged precipitation, temperature and soil covariates, sensor harmonization, land-cover stratification, NPP and soil-salinity models, and causal attribution.

## Verification

Seeded synthetic fixtures recover a known rainfall coefficient and residual trend, test pixel-specific missing data and constant rainfall, and validate shapes and time order.

See the [implementation package](../../implementations/python/land-degradation/README.md).
