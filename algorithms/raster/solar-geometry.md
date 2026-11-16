# Solar geometry and extraterrestrial irradiance

Solar geometry determines the position of the Sun relative to a location and
time. The reference implementation uses NOAA fractional-year approximations
for equation of time and solar declination, then derives hour angle, zenith,
elevation and azimuth. Azimuth is clockwise from true north.

Top-of-atmosphere normal irradiance is approximated using a day-of-year
Earth–Sun distance correction to the nominal solar constant. Horizontal
irradiance multiplies this by the positive sine of solar elevation; it is zero
when the Sun is below the horizon.

The implementation accepts decimal-degree latitude/longitude and timezone-
aware timestamps, normalizes time to UTC and returns explicit angular units.

It does not model atmospheric attenuation, clouds, diffuse radiation, terrain
horizon obstruction, slope incidence, albedo, vegetation, urban shading or
microclimate. Do not treat extraterrestrial irradiance as ground-level
shortwave radiation. The solar geometry package provides tests and usage.
