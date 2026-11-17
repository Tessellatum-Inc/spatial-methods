# Contraction hierarchies — static directed routing

This NumPy-free Python teaching implementation preprocesses a directed graph by contracting vertices in a supplied order, adding an unpruned set of shortcut edges for every potentially shortest two-edge path through each contracted vertex. Queries use bidirectional upward Dijkstra searches and recursively unpack shortcuts to original edges.

## API

`ContractionHierarchy(n_nodes, edges, order=None)` accepts integer node IDs and finite nonnegative edge weights. An explicit permutation is recommended. If omitted, a deterministic static degree order is used as a basic baseline, not a road-network importance heuristic.

`query(source, target)` returns distance, the unpacked node path, original input edge IDs and the meeting node. `return_path=False` skips unpacking.

## Test

Run `python -m pytest -q` from this directory.

Tests compare all-pairs queries against an independent Dijkstra implementation on seeded random directed graphs, verify shortcut creation and direct-edge dominance, and check path unpacking, parallel edges, zero weights, disconnected nodes and invalid inputs.

## Limits

This is a correctness-oriented static reference implementation. Witness-based shortcut pruning is deliberately disabled: shortcut growth can be large, so this exactness-oriented baseline is for small graphs only. The static degree order is not an advanced contraction-order heuristic. It does not implement nested-dissection orders, witness-search limits, priority updates, stall-on-demand, customizable contraction hierarchies, dynamic edge-weight updates, turn costs, time-dependent weights or multimodal transfer edges. It is not intended for continental-scale road networks.
