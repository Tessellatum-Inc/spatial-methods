# SKATER implementation verification

Implemented: deterministic Kruskal minimum spanning tree from supplied
non-negative adjacency costs; greedy edge pruning by reduction in
within-region sum of squares; connected-component labels for k regions.

Independent tests cover a chain with two feature groups, MST edge selection,
connected output regions, deterministic ties, k=1, k=n and invalid/disconnected
inputs.

Not implemented: automatic k selection, minimum region sizes, alternate
regional objectives or a complete reproduction of every SKATER variant.
