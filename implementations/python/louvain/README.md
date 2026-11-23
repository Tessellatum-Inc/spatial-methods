# Louvain community detection

Dependency-free multilevel Louvain optimisation for undirected weighted graphs. It performs local modularity-improving node moves, aggregates communities into supernodes, and repeats. Seeded node order makes runs reproducible.

Run: `python -m pip install -r requirements.txt && python -m pytest -q`.

Reciprocal adjacency weights are averaged; iterable adjacency denotes unit edges. Self-loops and zero-weight edges are ignored; neighbour-only nodes are included. Resolution controls modularity scale. This is a reference implementation, not a claim of Leiden connectivity guarantees or production performance. Louvain is heuristic and subject to resolution-limit and degeneracy issues.
