# Robust contextual thermal-hotspot screening

A small anomaly-screening baseline for a 2-D thermal brightness-temperature
or temperature-like image. A local median estimates background; the median
absolute deviation (MAD) of local residuals estimates robust neighbourhood
variability. A cell is flagged only when it passes both an absolute threshold
and a minimum local-excess threshold.

## Output

The result contains a Boolean hotspot mask plus local background, local MAD
and positive excess diagnostics. NaN cells remain unclassified.

## Run

Install with python -m pip install -r requirements.txt, then run
python -m pytest -q.

## Limits

This is not the MODIS active-fire algorithm, MCD64A1 burned-area product,
volcanic thermal retrieval, or a calibrated sensor-specific detection model.
It does not use multi-band contextual tests, scan-angle correction,
cloud/smoke screening, saturation flags, day/night thresholds, temporal
confirmation or geolocation uncertainty. Set thresholds in the correct
sensor units and validate omission/commission errors against independent
reference observations.
