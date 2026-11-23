# Thermal land-surface temperature retrieval

Thermal infrared sensors measure radiance at the sensor, not land-surface
temperature directly. Retrieval requires sensor calibration, atmospheric
transmission/emission treatment and surface emissivity.

## Planck brightness temperature

For at-sensor spectral radiance L and band-specific Planck constants K1 and
K2, brightness temperature is

\[
T_b = \frac{K_2}{\ln(1+K_1/L)}.
\]

This is the blackbody-equivalent temperature at the sensor. It is not yet
surface temperature because atmospheric effects and emissivity have not been
removed.

## Single-channel radiative-transfer inversion

A simplified single-band radiative-transfer equation is

\[
L_{sensor}=\tau[\epsilon B(T_s)+(1-\epsilon)L_{\downarrow}]+L_{\uparrow},
\]

where tau is atmospheric transmittance, epsilon is surface emissivity,
L-down is downwelling atmospheric radiance reflected by the surface, and
L-up is upwelling atmospheric radiance. Solving for surface-leaving
blackbody radiance gives

\[
B(T_s)=\frac{L_{sensor}-L_{\uparrow}
-\tau(1-\epsilon)L_{\downarrow}}{\tau\epsilon}.
\]

The inverse Planck function then yields surface temperature. The implemented
kernel requires all atmospheric and emissivity terms as caller-supplied
inputs; it does not retrieve them from ancillary data.

## Generalized split-window correction

Two nearby thermal bands have different atmospheric absorption. A common
generalized polynomial form is

\[
T_s=T_{10}+c_1\Delta T+c_2(\Delta T)^2+c_0
+(c_3+c_4w)(1-\bar\epsilon)
+(c_5+c_6w)(\epsilon_{10}-\epsilon_{11}),
\]

where Delta-T is the brightness-temperature difference, w is column water
vapour, and the emissivity terms summarize the band pair. Coefficients depend
on sensor, spectral response, atmospheric training profiles and water-vapour
units. They must not be transferred indiscriminately between sensors.

## Implementation and limits

The [thermal LST reference package](../../implementations/python/thermal-lst/README.md)
contains Planck conversion, single-channel inversion and the generalized
split-window kernel with input validation and synthetic round-trip tests.
These functions do not replace complete sensor-specific workflows such as
radiometric calibration, cloud masking, emissivity retrieval, atmospheric
profile estimation or validation. Temperatures are kelvin; all radiance and
coefficient units must be consistent.

## References

- Jiménez-Muñoz, J. C. and Sobrino, J. A. (2003). A generalized single-channel
  method for retrieving land surface temperature from remote sensing data.
  *Journal of Geophysical Research: Atmospheres*, 108(D22), 4688.
  https://doi.org/10.1029/2003JD003480
- Jiménez-Muñoz, J. C. et al. (2014). Land surface temperature retrieval
  methods from Landsat-8 thermal infrared sensor data. *IEEE Geoscience and
  Remote Sensing Letters*, 11(10), 1840–1843.
  https://doi.org/10.1109/LGRS.2014.2312032
