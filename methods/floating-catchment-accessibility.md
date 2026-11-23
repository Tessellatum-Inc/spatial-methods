# Two-step floating catchment area accessibility

The 2SFCA family measures potential spatial access to facilities while accounting for supply and competing demand. It is commonly used for healthcare, education and public-service accessibility.

For each facility \(j\), the first step calculates

\[
R_j=\frac{S_j}{\sum_{i:d_{ij}\le d_0}P_i},
\]

where \(S_j\) is facility capacity, \(P_i\) is population or demand, and \(d_{ij}\) is the selected distance or travel time. The second step calculates

\[
A_i=\sum_{j:d_{ij}\le d_0}R_j.
\]

E2SFCA replaces the binary catchment membership with a distance-decay weight \(w_{ij}\), commonly piecewise constant across travel-time bands:

\[
R_j=\frac{S_j}{\sum_i P_iw_{ij}},\qquad A_i=\sum_jR_jw_{ij}.
\]

This repository implements the equations over an explicit distance matrix. 2SFCA includes observations exactly at the radius. E2SFCA includes each upper boundary in its corresponding zone and assigns zero weight beyond the final break.

The result depends on the chosen catchment, impedance measure, facility capacity, demand definition and decay weights. It is not a measure of realised utilisation, quality, affordability or causal health outcomes. Zero-demand catchments return zero ratios; this convention is explicit and should be reviewed for each application.

Run tests from `implementations/python/floating-catchment`.

## References

- Luo, W. & Wang, F. (2003). Measures of spatial accessibility to health care in a GIS environment: synthesis and a case study in the Chicago region. *Environment and Planning B*, 30(6), 865–884. https://doi.org/10.1068/b29120.
- Luo, W. & Qi, Y. (2009). An enhanced two-step floating catchment area (E2SFCA) method for measuring spatial accessibility to primary care physicians. *Health & Place*, 15(4), 1100–1107. https://doi.org/10.1016/j.healthplace.2009.06.002.

## Common travel-time decay functions

Three reusable non-negative impedance kernels are implemented:

- Gaussian: \(w(d)=\exp[-\tfrac12(d/\sigma)^2]\).
- Regularised power: \(w(d)=(1+d/s)^{-\beta}\).
- Epanechnikov compact-support kernel: \(w(d)=\max(0,1-(d/h)^2)\) for \(d<h\), and zero otherwise.

All accept finite non-negative distances and strictly positive scale/bandwidth parameters. The regularised power form remains finite at zero distance. These functions provide weights only; parameter calibration, multimodal transfer impedance, mode choice and observed-utilisation validation are not inferred by the package.
