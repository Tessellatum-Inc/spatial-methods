# Green-Ampt infiltration stepping

## Governing relation

For cumulative infiltration F, wetting-front suction psi, moisture deficit delta-theta, and saturated hydraulic conductivity Ks, the Green-Ampt infiltration capacity is:

f(F) = Ks * (1 + psi * delta-theta / F).

For constant rainfall intensity r greater than Ks, ponding begins at Fp = (psi * delta-theta) / (r/Ks - 1). The ponded phase is integrated using the implicit Green-Ampt equation.

## Implementation

green_ampt_infiltration_step(F, rainfall_intensity, Ks, psi, moisture_deficit, duration) advances one step. Depths are millimetres, rates millimetres/hour, and duration hours. It returns step infiltration, cumulative infiltration, rainfall excess and ponding state.

## Scope and limitations

The implementation assumes a homogeneous one-dimensional soil column, constant rainfall intensity and constant soil parameters within a step. It does not model layered soils, macropores, water-table effects, spatial variability, runoff routing or a continuous catchment water balance. Treat output as a process-model baseline, not calibrated local prediction.

See the terrain-derivatives package and tests.