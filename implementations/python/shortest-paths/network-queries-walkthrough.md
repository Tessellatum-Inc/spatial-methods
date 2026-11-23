# Walkthrough: many-to-many paths and network isochrones

## Many-to-many

The key optimization in this baseline is modest but useful: compute one Dijkstra predecessor tree per source, rather than rerunning a fresh source-to-target query for every pair. Each requested target is then reconstructed by walking predecessor links backwards. Unreachable targets have no predecessor chain and return `(None, inf)`.

For very large source sets, this is still expensive. More advanced routing systems share work across queries through preprocessing or specialised data structures.

## Isochrones

A cutoff is integrated into Dijkstra. A candidate label is inserted only when its cumulative cost is at most the budget. After the search, each outgoing edge from a reached node is checked; an edge whose cumulative traversal cost exceeds the budget is a frontier arc. This makes the boundary explicit without pretending that a set of graph nodes is already a geographic polygon.

## Run

```bash
python -m pytest -q test_network_queries.py
```
