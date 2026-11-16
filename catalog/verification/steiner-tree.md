# Verification record: Steiner tree

## Source identity
- Compendium: *Spatial Analysis Algorithms: Complete Compendium*
- Original location: Section 1, page 2
- Source entry: flows and trees — Steiner tree

## Implemented scope
- Exact Dreyfus–Wagner subset dynamic program with shortest-path closure.
- Undirected positive finite edge weights, parallel-edge reduction, self-loop omission.
- Parent reconstruction into a minimum terminal-spanning subgraph.
- Explicit terminal-count guard (default 12).

## Tests
- Two-terminal shortest-path equivalence.
- Three-terminal star with a non-terminal Steiner vertex.
- Three-terminal triangle.
- One-terminal zero-cost case.
- Parallel edges, self-loops, disconnected terminals and invalid inputs.

## Limits
The method is exponential in terminal count and is deliberately capped. It is not a large-network heuristic, Euclidean geometric Steiner tree, directed arborescence or Steiner forest solver.
