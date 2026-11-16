# Coastal empirical processes and shoreline change rates

## Stockdon wave runup

Stockdon et al.'s empirical parameterization estimates the 2% exceedance vertical runup statistic from deep-water significant wave height, peak period and foreshore slope:

\[
R_{2\%}=1.1\left[0.35\beta_f\sqrt{H_0L_0}
+0.5\sqrt{H_0L_0(0.563\beta_f^2+0.004)}\right],
\qquad L_0=\frac{gT^2}{2\pi}.
\]

The package also exposes R1 and mean scaled summaries and the low-runup expression based on setup minus swash. These empirical summaries are not independent fitted quantiles. It is an empirical screening model, not a coupled tide-surge-wave inundation solver.

## CERC longshore transport

The implemented CERC-style bulk estimate uses breaking wave height (H_b), angle (alpha) from shore-normal and a shallow-water group velocity approximation (C_g=\sqrt{gH_b}):

\[
P_{ls}=\frac{\rho_w g H_b^2 C_g}{8}\sin\alpha\cos\alpha,
\qquad Q=\frac{K P_{ls}}{(\rho_s-\rho_w)g(1-p)}.
\]

The sign follows wave-angle sign. Coefficients and breaking-wave transformation are site-sensitive; Kamphuis' alternative is not represented by this formula.

## Shoreline change statistics

For transect positions (y_i) at survey years (t_i), EPR is ((y_n-y_1)/(t_n-t_1)). OLS fits (y_i=a+bt_i+\epsilon_i). Optional WLR minimizes weighted squared residuals using (w_i=1/\sigma_i^2). These are rate estimators only, not the full Digital Shoreline Analysis System workflow.

## Reference implementation

See [coastal-processes](../../implementations/python/coastal-processes/README.md). All methods state their units, inputs and scope; tests use analytic sign, scaling and regression cases.


## Bruun rule

The idealized Bruun relation estimates cross-shore recession as R = S W / (B + h*), where S is sea-level rise, W is active-profile width, B is berm height and h* is closure depth. The implementation is a direct calculation with explicit input constraints. Its equilibrium, two-dimensional sediment-conservation assumptions are strong; it is not suitable as a stand-alone site forecast.

## Dean equilibrium beach profile

Dean's idealized profile is h(x)=A x^(2/3), with analytic integral from x0 to x1 equal to (3A/5)(x1^(5/3)-x0^(5/3)). The package evaluates both. A has units length to the one-third power when x and h use the same length unit.


## Empirical satellite-derived bathymetry and multibeam gridding

The package includes a linear calibration baseline for depth as a function of a supplied log-band ratio, fitted from paired known depths, and a prediction function with optional calibrated-domain masking. It does not perform atmospheric correction, water-column inversion or bottom-type correction. Multibeam soundings can be aggregated to regular cells by mean or median, with counts and cell-centre coordinates returned; this is not a CUBE estimator or a hydrographic uncertainty model.


## Six-variable coastal vulnerability index

For six ordinal variable ranks (r_i\in\{1,2,3,4,5\}), the conventional index is (\mathrm{CVI}=\sqrt{\prod_{i=1}^{6}r_i}\). The implementation validates the six-rank axis and supports arrays of sites. The choice of variables and local rank thresholds are study-specific; the output is an ordinal composite, not an annual probability or calibrated risk estimate.
