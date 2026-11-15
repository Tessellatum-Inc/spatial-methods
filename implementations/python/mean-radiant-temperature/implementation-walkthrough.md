# Implementation walkthrough: globe-based mean radiant temperature

## 1. Start with the measurement model

A globe thermometer does not measure air temperature. Its equilibrium temperature
is set by the balance of radiation absorbed/emitted by the globe and convection
between the globe and surrounding air. The correction therefore needs globe
temperature, air temperature, air speed, globe diameter and emissivity.

## 2. Compute both convection modes

The implementation computes the ISO 7726 natural-convection and forced-convection
coefficients independently. It uses the larger coefficient, corresponding to
the mixed-convection selection rule for the standard globe method. The forced
term is zero at zero air speed.

## 3. Solve the steady-state energy balance

The fourth-power calculation is performed in kelvin. Celsius is converted before
the radiative balance and restored only after the fourth root. This avoids the
common dimensional error of applying a fourth-power law directly to Celsius.

## 4. Inspect diagnostics

The return value includes the selected convective coefficient and the controlling
regime. These diagnostics matter: two measurements with identical globe and air
temperatures can receive different corrections when air speed or globe diameter
changes.

## 5. Validate before mapping

The function rejects non-finite observations, temperatures at/below absolute
zero, negative air speed, nonpositive diameter and emissivity outside (0, 1].
Array inputs broadcast, so a raster stack can be processed when its arrays are
shape-compatible. Check masks, units, sensor calibration and spatial alignment
before applying it to gridded observations.

## 6. Know what is not solved

The globe method does not infer directional radiation, solar geometry, sky
view factors or human posture. It does not calculate UTCI or PET. For urban
microclimate mapping, directional shortwave and longwave radiation and
view-factor calculations are separate required model components.
