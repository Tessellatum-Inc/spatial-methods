# Network node-failure and attack resilience

Dependency-free undirected-graph baselines:

- Largest connected component size.
- Static degree-targeted removal order.
- Seeded random removal order.
- Node-removal resilience curve tracking the largest connected component and remaining-node fractions relative to the original graph.

Run with `python -m pytest -q` from this directory.

The implementation treats every edge as undirected and unweighted. It recomputes connectivity after each node removal and is intended for small teaching graphs. It does not model flow/capacity, travel-time accessibility, dynamic betweenness attacks, edge failures, cascading overload, recovery, spatial distance, stochastic ensembles or uncertainty. A large connected component is only one aspect of infrastructure service resilience.
