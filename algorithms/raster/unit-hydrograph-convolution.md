# Discrete unit-hydrograph convolution

## Purpose

A discrete unit hydrograph maps effective rainfall depth per interval to a discharge response. For rainfall excess e and discrete ordinates u, the direct-runoff hydrograph is the full linear convolution q = e * u.

## Implementation

unit_hydrograph_convolution(rainfall_excess, unit_hydrograph, time_step=1.0) returns the full convolution and its time coordinate. Rainfall excess is depth per interval (commonly mm); unit-hydrograph ordinates must be discharge per matching unit depth (for example m3/s/mm). Both series share the supplied positive time step.

## Limitations

The function performs routing only. It does not derive a unit hydrograph from catchment geomorphology, estimate duration or base time, separate baseflow, calibrate parameters, or account for nonlinear/time-varying catchment response. The user must ensure consistent units and interval duration.

See the terrain-derivatives package and tests.