# Pixel-wise optical image compositing

Temporal compositing reduces a time series of co-registered observations to one representative spectrum per pixel. The repository implementation provides three distinct selection rules rather than treating “best pixel” and medoid as interchangeable.

- **Best-pixel selection:** maximize a supplied quality score over valid observations. This supports sensor-specific cloud, view-angle, aerosol and temporal quality scoring, but the score definition is external.
- **Spectral medoid:** compute the per-band temporal median and select the actual observed spectrum with minimum squared Euclidean distance to that median. Unlike a per-band median composite, the result is an observed spectrum. Unscaled Euclidean distance makes band units and scaling important.
- **Maximum-NDVI selection:** compute NDVI for each valid date and select the complete spectrum from the date with the highest value. It can preferentially select peak vegetation conditions and is not a neutral all-purpose composite.

All methods preserve the selected date index and valid-observation count. Ties choose the earliest observation; pixels with no eligible observation return NaN bands and index -1. Inputs must already be co-registered and harmonized. These functions do not perform cloud masking, atmospheric correction, BRDF correction or sensor harmonization.
