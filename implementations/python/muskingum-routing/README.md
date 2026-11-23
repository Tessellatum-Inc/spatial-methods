# Muskingum channel routing

Dependency-free implementation of the linear Muskingum storage-routing
method for equally spaced inflow hydrographs.

The method represents reach storage as

    S = K [X I + (1-X) O]

and routes inflow using

    O[t] = C0 I[t] + C1 I[t-1] + C2 O[t-1]

The implementation returns the routed outflow, corresponding storage and
the three coefficients. K and the time step must use the same time unit.
The weighting factor X is constrained to [0, 0.5]. The conventional
non-negative-coefficient stability interval is enforced:

    2 K X <= delta_t <= 2 K (1-X)

The initial outflow defaults to the first inflow value, but can be supplied.

## Limitations

This is a lumped, linear reach-routing model. It does not estimate K or X,
represent lateral inflows, nonlinear storage, backwater, floodplain exchange,
sediment, channel geometry or spatially distributed Saint-Venant dynamics.
It assumes equally spaced samples and non-negative flow values. Check units,
initial conditions and calibration before operational use.

## Tests

    python -m pytest -q
