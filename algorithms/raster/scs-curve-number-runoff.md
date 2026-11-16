# SCS curve-number event runoff

## Purpose

The SCS curve-number method estimates direct-runoff depth from event precipitation and a catchment curve number. Potential retention is S = 25400/CN - 254 mm when CN uses the conventional 0–100 scale; initial abstraction is Ia = lambda S. For P > Ia, runoff is Q = (P-Ia)^2/(P-Ia+S), otherwise Q=0.

## Implementation

scs_curve_number_runoff(precipitation, curve_number, abstraction_ratio=0.2) broadcasts inputs and returns event runoff depth in the same units as precipitation. The standard lambda=0.2 is configurable. scs_curve_number_antecedent(curve_number_ii) applies conventional empirical conversions to dry and wet antecedent conditions.

## Limitations

This is an event lumped abstraction model. It does not produce a hydrograph, route flow through a channel, model spatially distributed infiltration, estimate parameters from local data, or replace a continuous catchment water balance. The antecedent conversions are empirical and should be checked against local standards and calibration.

## Tests and code

See the terrain-indices implementation and unit tests.