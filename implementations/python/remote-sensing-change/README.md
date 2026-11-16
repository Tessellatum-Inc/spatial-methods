# Bitemporal remote-sensing change detection

This dependency-light package implements two classical change-detection
baselines from the Section 5 source inventory:

- **Change Vector Analysis (CVA):** per-pixel after-minus-before spectral
  difference vectors, Euclidean magnitudes and covariance-standardized
  Mahalanobis magnitudes.
- **Post-classification comparison:** an ordered from-class/to-class
  transition matrix and a pixel-level change mask.

## Run

```bash
python -m pip install -r requirements.txt
python -m pytest -q
```

## Data contract and interpretation

CVA expects two aligned numeric arrays shaped
`(rows, columns, bands)`. A pixel is valid only when all bands in both
dates are finite. The Euclidean magnitude is the norm of the spectral
difference vector. The Mahalanobis magnitude uses either a caller-supplied
band covariance matrix or a sample covariance estimated from valid change
vectors, stabilized by a positive diagonal ridge.

Post-classification comparison expects matching 2D numeric class rasters.
Non-finite values are NoData and excluded from the transition counts. Matrix
rows represent the earlier date; columns represent the later date. The
default class order is the sorted union of observed classes; pass
`class_values` to impose a stable external order.

Neither method performs atmospheric correction, co-registration, cloud
masking, radiometric normalization, threshold calibration or accuracy
assessment. CVA magnitudes are not automatically statistically significant,
and post-classification disagreement can reflect classification error as
well as real land-cover change. Validate thresholds and class transitions
against independent reference data and preserve class definitions between
dates.

See [the canonical lesson](../../../algorithms/remote-sensing/change-vector-analysis.md).
