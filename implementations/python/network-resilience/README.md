# Network resilience and reliability

Dependency-free, undirected, unweighted graph baselines:
- Largest connected component, static degree-targeted node attacks and seeded random node attacks (percolation.py).
- Seeded random edge removal, static edge-betweenness attack ordering and edge-attack curves (edge_reliability.py).
- Monte Carlo all-terminal and k-terminal reliability under independent, identical edge survival.
- Exhaustive inclusion-minimal edge cut-set enumeration for small graphs, with a hard edge-count guard.
- Motter–Lai-style node overload cascades using shortest-path betweenness load and capacity tolerance (`cascading_failures.py`).

Run `python -m pytest -q --import-mode=importlib` from this directory.

## Interpretation and limits

The reliability estimator samples each edge independently and reports a Bernoulli standard error plus a clipped normal-approximation 95% interval. The interval can be poor for rare events or estimates near zero/one; no variance-reduction scheme or rare-event guarantee is implemented. Minimal-cut enumeration is exponential subset enumeration and intended only for small teaching examples. Edge-betweenness attack is a static ranking on the intact graph, not an adaptive recalculation after every failure.

All routines assume a simple undirected graph. The cascade extension is a structural shortest-path load model, not a physical power-flow, hydraulic or traffic assignment simulator. It assumes instantaneous rerouting and synchronous overload removal; it does not model edge capacities, demand matrices, spatially dependent failures, interdependent layers, repair, restoration scheduling or hazard-specific fragility. Connectivity is a structural proxy, not a full measure of service delivered to users.
