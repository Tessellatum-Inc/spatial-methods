# Road-network stroke generation

A dependency-free good-continuation baseline that partitions an undirected embedded road graph into edge-disjoint strokes.

At each junction, the method computes the deflection from straight continuation for every pair of incident edges. Candidate pairs within a caller-supplied angular threshold are sorted from straightest to least straight and greedily selected, with each incident edge paired at most once at that junction. The resulting edge-adjacency graph has maximum degree two; its connected components are emitted as open strokes or closed cycles.

## Run

```bash
python -m pip install -r requirements.txt
python -m pytest -q
```

## Input contract

Nodes map stable identifiers to projected planar x/y coordinates. Edges are unique (edge_id, u, v) tuples and are treated as undirected. The default maximum deviation from a 180-degree continuation is 45 degrees. A larger threshold permits more angular bends.

## Limits

This is a transparent greedy stroke-construction baseline, not a full road-network generalisation system. It does not simplify stroke geometry, preserve network topology under scale change, classify road hierarchy, detect dual carriageways, resolve grade-separated crossings, infer missing links, or optimise global stroke pairings. Results depend on graph segmentation, coordinate projection, angular threshold and deterministic tie-breaking. Split roads at true junctions before use; do not connect grade-separated crossings merely because they share coordinates.
