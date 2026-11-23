# Mean radiant temperature from a globe thermometer

Mean radiant temperature (MRT) is the uniform enclosure temperature that
would produce the same net radiant heat exchange with a person or sensor as
the actual radiant environment. It is not air temperature and is not a
complete thermal-comfort index.

## Globe heat balance

For a spherical globe at steady state, radiative exchange balances convective
exchange. With globe temperature Tg, air temperature Ta, emissivity epsilon,
Stefan–Boltzmann constant sigma and convective coefficient hc:

    epsilon * sigma * (Tr^4 - Tg^4) = hc * (Tg - Ta)

Therefore:

    Tr = [Tg^4 + hc * (Tg - Ta) / (epsilon * sigma)]^(1/4)

All temperatures in the fourth-power expression are kelvin. The teaching
implementation accepts Celsius and performs conversion internally.

The ISO 7726 empirical globe correlations are:

    hc,n = 1.4 * (abs(tg - ta) / D)^(1/4)
    hc,f = 6.3 * va^0.6 / D^0.4

where D is globe diameter in metres and va is air speed in m/s. The larger
coefficient is selected for the mixed-convection estimate. Defaults are
emissivity 0.95 and diameter 0.15 m, representing a standard matte-black globe.

## Implementation

- Python implementation: ../implementations/python/mean-radiant-temperature/mean_radiant_temperature.py
- Tests: ../implementations/python/mean-radiant-temperature/test_mean_radiant_temperature.py
- Package contract: ../implementations/python/mean-radiant-temperature/README.md
- Implementation walkthrough: ../implementations/python/mean-radiant-temperature/implementation-walkthrough.md
- Exercise: ../exercises/mean-radiant-temperature.md
- Lab: ../notebooks/mean-radiant-temperature-lab.ipynb

The implementation supports broadcast-compatible arrays and reports the
controlling convection regime. It rejects invalid temperatures, negative
velocity, nonpositive diameter and invalid emissivity.

## Interpretation and limits

A globe thermometer integrates radiative exchange over its surface, but its
temperature also depends on convection. The correction is sensitive to globe
diameter and local air speed. Allow the sensor to approach thermal equilibrium
and measure air speed close to the globe. This method does not calculate
directional plane radiant temperatures, solar exposure from first principles,
or a human heat-balance index such as UTCI or PET. Those require additional
meteorological, radiative and physiological inputs.

## References

- ISO 7726:1998, Ergonomics of the thermal environment — Instruments for
  measuring physical quantities. The standard gives the globe heat balance
  and natural/forced convection correlations.
- ISO 7726:1985, Thermal environments — Instruments and methods for measuring
  physical quantities. Earlier edition containing the classic globe correction.
- NIST, Thermal Analysis—Human Comfort—Indoor Environments, for the steady-state
  globe energy balance and convective heat-transfer discussion.
