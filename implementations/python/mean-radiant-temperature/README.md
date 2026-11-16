# Globe-based mean radiant temperature

This package estimates mean radiant temperature (MRT) from a steady-state
globe thermometer using the ISO 7726 heat-balance form.

## Inputs and outputs

- Globe and air temperature: degrees Celsius.
- Air speed: metres per second.
- Globe diameter: metres (default 0.15 m).
- Globe emissivity: dimensionless (default 0.95).
- Output: MRT in degrees Celsius, selected convective heat-transfer
  coefficient in W m-2 K-1, and the controlling convection regime.

The implementation compares natural convection,
1.4 * (abs(Tg - Ta) / D)**0.25, with forced convection,
6.3 * v**0.6 / D**0.4, and selects the larger coefficient. It then solves
the steady-state globe energy balance for equivalent radiant temperature.

## Scope and limitations

This is a globe-sensor calculation, not a full urban microclimate model. It
assumes steady state, a spherical sensor and the stated empirical convection
correlations. Sensor response time, solar absorption corrections, globe
orientation, directional radiance and measurement uncertainty are not
modelled. For spatially distributed MRT from radiative fluxes, use directional
shortwave/longwave radiation and view-factor methods; do not treat this
estimator as a substitute.

## Tests

Run python -m pytest -q from this directory with NumPy and pytest installed.
