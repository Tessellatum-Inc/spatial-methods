# Manning open-channel flow

Dependency-free Manning equation calculations for steady, uniform flow in
rectangular and trapezoidal channels.

The package computes discharge from flow depth and inverts discharge to
normal depth with bracketed bisection. Trapezoid side slope is horizontal
distance per unit vertical distance (z:1). The hydraulic radius is area
divided by wetted perimeter.

For SI use, provide channel geometry in metres, dimensionless energy slope
and Manning roughness n in compatible SI units.

## Assumptions and limitations

This is a uniform-flow calculation. It assumes a prismatic channel, steady
conditions, a representative roughness coefficient and energy slope. It does
not solve backwater profiles, gradually varied flow, hydraulic jumps,
unsteady Saint-Venant equations, compound sections, sediment transport,
vegetation drag or floodplain exchange. The normal-depth result is not a
water-surface profile or flood model.

## Tests

    python -m pytest -q
