# Height Above Nearest Drainage (HAND)

Dependency-free HAND calculation from a conditioned D8 direction raster and
an explicit stream mask. Each valid non-stream cell follows its D8 receiver
until it reaches the first downstream stream cell. HAND is the cell elevation
minus that drainage-cell elevation. Stream cells have HAND 0.

Paths that terminate at a sink, raster boundary or NoData before reaching a
stream return None. The implementation validates shape, direction codes,
strictly downhill receiver links and cycles. Iterative path compression
avoids recursion-depth limits.

Run `pytest -q` from this directory. Tests cover paths, branching,
NoData/edge termination, cycles, invalid receivers and a seeded grid oracle.

Scope: this does not extract streams, condition DEM depressions, resolve
flats, model channel stages or determine flood inundation. Results depend on
the supplied stream threshold and D8 flow network.
