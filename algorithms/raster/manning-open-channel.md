# Manning open-channel flow

For steady uniform flow, Manning's equation is

    Q = (1/n) A R^(2/3) S^(1/2)

where A is wetted area, R is hydraulic radius, S is energy slope and n is
Manning roughness. For a trapezoidal section with bottom width b, depth y and
side slope z:1 (horizontal:vertical),

    A = y (b + z y)
    P = b + 2 y sqrt(1 + z^2)
    R = A / P

The reference implementation calculates discharge and uses bracketed
bisection to invert for normal depth. SI-compatible units are assumed when
lengths are metres, slope is dimensionless and n is in SI units.

This is a steady uniform-flow model. It does not calculate backwater,
gradually varied profiles, unsteady Saint-Venant flow, hydraulic jumps or
2D inundation. See the Python package for tests and usage.
