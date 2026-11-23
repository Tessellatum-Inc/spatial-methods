# Optical image compositing

NumPy reference implementations of three pixel-wise temporal compositors:

- Best-pixel: choose the valid observation with the highest caller-supplied quality score.
- Medoid: choose the observed spectrum closest to the per-pixel temporal spectral median.
- Maximum NDVI: choose the valid date with the highest NDVI and copy its complete spectrum.

Input shape is (time, rows, columns, bands). Optional valid_mask is boolean (time, rows, columns). Pixels without valid observations receive a NaN spectrum and selected_time_index -1. Ties select the earliest date. Medoid uses unscaled Euclidean distance, so band scaling is consequential.

Install NumPy and pytest, then run pytest -q. These compositors do not perform cloud detection, atmospheric correction, BRDF normalization, or sensor harmonization; quality scores and masks must be produced by an upstream workflow.
