# Contextual thermal-hotspot screening

A thermal hotspot detector can combine an absolute temperature threshold
with a local-background anomaly test. A robust local median estimates the
background, while the median absolute deviation (MAD) of local residuals
provides a robust scale estimate.

For pixel i, the reference baseline flags a hotspot when

    T_i >= T_absolute
    T_i - median(N_i) >= max(delta_min, k * 1.4826 * MAD(N_i)),

where N_i is the local neighbourhood, delta_min is a minimum excess and k is
a robust-scale multiplier. The 1.4826 factor makes MAD consistent with the
standard deviation for Gaussian noise under ideal conditions.

See [the Python implementation](../../implementations/python/thermal-hotspot-detection/README.md).
This is a generic contextual anomaly screen, not a reproduction of MODIS
active-fire or MCD64A1 algorithms. Sensor-specific quality flags, spectral
tests, cloud/smoke screening, temporal confirmation and validation remain
essential for operational products.
