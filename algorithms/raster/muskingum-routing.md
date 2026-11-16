# Muskingum channel routing

The Muskingum method approximates reach storage with a weighted combination
of inflow and outflow:

    S = K [X I + (1-X) O]

For equally spaced inflow samples, the finite-difference continuity equation
gives

    O[t] = C0 I[t] + C1 I[t-1] + C2 O[t-1]

with

    C0 = (delta_t/2 - KX) / (K(1-X) + delta_t/2)
    C1 = (delta_t/2 + KX) / (K(1-X) + delta_t/2)
    C2 = (K(1-X) - delta_t/2) / (K(1-X) + delta_t/2)

The reference implementation enforces 0 <= X <= 0.5 and the conventional
non-negative coefficient interval 2 K X <= delta_t <= 2 K (1-X). K and
delta_t must use the same time units.

This is a lumped linear routing method, not a substitute for dynamic-wave
Saint-Venant solvers, 2D shallow-water equations or spatially distributed
hydrodynamics. See the Python package for API and tests.
