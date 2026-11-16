# Exercise: mean radiant temperature from globe observations

## Given

A standard matte-black globe has diameter 0.15 m and emissivity 0.95. Its
measured temperature is 35 °C, air temperature is 28 °C and air speed is
0.2 m/s.

## Tasks

1. Calculate MRT with the package and record the selected convection regime.
2. Repeat at air speeds 0, 0.1, 0.5 and 1.0 m/s. Explain when forced convection
   controls the correction.
3. Repeat with a 40 mm globe. Explain why the same globe temperature does not
   imply the same MRT when sensor diameter changes.
4. Explain why this measurement correction alone cannot produce a defensible
   urban-canyon MRT map or a UTCI/PET surface.

## Acceptance checks

- Units are Celsius, metres and metres/second.
- Fourth-power temperatures are converted to kelvin.
- The natural and forced coefficients are compared explicitly.
- Conclusions distinguish a globe-sensor correction from a full radiation
  or human heat-balance model.
