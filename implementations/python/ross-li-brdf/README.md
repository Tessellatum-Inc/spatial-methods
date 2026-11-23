# RossThick-LiSparseR BRDF normalization

Fits the isotropic, Ross-Thick volumetric and Li-Sparse-Reciprocal geometric
kernel coefficients independently for each spectral band. Each observation
is scaled to caller-selected reference solar/view geometry using the ratio of
fitted reference and observation BRDF values.

Angles are radians. Reflectance has shape (observations,) or
(observations, bands); each geometry vector has one value per observation.
The observation design matrix must have rank three. Crown-shape ratios are
explicit parameters; defaults are conventional baselines, not sensor-specific
coefficient tables.

Install numpy and pytest, then run python -m pytest -q. Synthetic tests recover
known coefficients and check reference-geometry normalization.

This is not the operational MODIS MCD43 processing chain. Atmospheric
correction, cloud screening, temporal angular sampling, quality flags,
uncertainty propagation, terrain correction and sensor-specific calibration
remain outside scope. Sparse or poorly distributed view geometries can make
the fit unstable; inspect coefficient plausibility, residuals and angular
coverage before use.
