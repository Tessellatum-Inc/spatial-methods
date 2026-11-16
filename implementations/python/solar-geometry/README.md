# Solar geometry

Dependency-free NOAA fractional-year solar-position approximation.

## API

- solar_position(latitude, longitude, timestamp): geometric solar elevation, zenith, azimuth clockwise from true north, equation of time and declination.
- extraterrestrial_irradiance(...): top-of-atmosphere normal and horizontal irradiance using a day-of-year Earth–Sun distance factor.

Coordinates are decimal degrees; timestamps must be timezone-aware and are normalized to UTC. Elevation is geometric and no atmospheric refraction correction is applied.

## Scope and limitations

This is a solar geometry and top-of-atmosphere baseline, not a complete surface-radiation model. It does not estimate atmospheric transmittance, clouds, aerosols, diffuse irradiance, terrain horizon obstruction, slope/aspect incidence, albedo, canopy, urban shading, wind exposure or cold-air drainage. Use a radiative-transfer or validated clear-sky model for surface irradiance, and combine with a DEM/horizon model for terrain effects.

## Tests

    python -m pytest -q
