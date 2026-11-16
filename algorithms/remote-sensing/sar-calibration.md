# SAR backscatter calibration and multilooking

## Radiometric scaling

Given complex digital number (DN), the detected intensity is (|DN|^2). With caller-supplied calibration factor (K), the reference model computes

\[
\sigma^0=\max(|DN|^2-N,0)K,
\]

where (N) is optional noise power. For incidence angle (	heta) measured from vertical, this teaching baseline uses

\[
\beta^0=\frac{\sigma^0}{\sin\theta},\qquad
\gamma^0=\frac{\sigma^0}{\cos\theta}.
\]

Sensor-specific conventions and LUTs must be verified before applying these conversions operationally.

## Multilooking

Non-overlapping azimuth-by-range blocks are averaged to reduce speckle variance at the expense of spatial resolution. The implementation crops incomplete trailing blocks and reports valid look counts. NoData can be omitted or propagated.

## Limits and verification

This is not radiometric terrain correction, geocoding, orbit refinement, speckle modelling or enhanced spectral diversity coregistration. Tests compare complex intensity/noise calculations, incidence-angle conversions, direct block means and NoData policies.

See the [implementation package](../../implementations/python/sar-calibration/README.md).
