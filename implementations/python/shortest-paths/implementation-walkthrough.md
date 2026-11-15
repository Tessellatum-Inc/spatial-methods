# Intern walkthrough: Dijkstra and A*

## Objective

Implement a reliable shortest-path baseline on a weighted directed graph, then introduce A* without changing the graph model.

## Step 1 — State the graph contract

The graph maps each node to outgoing (neighbour, cost) pairs. Direction is explicit: if travel is allowed both ways, both arcs must be present. Edge costs must be finite and non-negative.

## Step 2 — Maintain best-known labels

The best mapping stores the cheapest discovered cost to each node. The priority queue stores candidate labels. When an outdated queue entry is popped, skip it.

## Step 3 — Reconstruct the path

Whenever a cheaper route to a neighbour is found, store its predecessor. When the goal is removed with its current best label, walk backward through predecessors and reverse the result.

## Step 4 — Add A*

A* changes queue priority from g to g+h. The path cost g remains the value used for relaxation. The heuristic must never overestimate the true remaining cost if an optimal result is required.

## Step 5 — Validate with an oracle

A* with a zero heuristic must return the same result as Dijkstra. Add fixtures for unreachable goals, zero-cost edges, equal-cost paths and directed asymmetry.

## Step 6 — Do not overgeneralise

Real routing may require edge-based state for turn restrictions, time-dependent costs, vehicle profiles and network snapping. These concerns belong in the graph model and search state, not in a map drawing layer.

## 8. Pareto label-setting for multiple route criteria

A scalar shortest-path algorithm assumes that all edge costs can be added into one number. A weighted sum can hide trade-offs: a route that is faster but longer may be incomparable with one that is slower but shorter.

The Pareto algorithm stores multiple labels at each node. A label contains the accumulated cost vector and the path that produced it. Label A dominates label B when A is no worse in every objective and strictly better in at least one. Dominated labels can be discarded because every continuation adds the same nonnegative edge-cost vector to both.

The implementation orders the queue lexicographically, removes dominated labels, and prevents repeated nodes in a path. Nonnegative costs mean a cycle cannot improve a path. The returned frontier contains every nondominated source-to-target cost vector. The optional per-node label cap raises an error if exceeded; it never returns a silently truncated frontier.

The worst-case number of nondominated paths can be exponential. This is an exact multi-criteria baseline, not a polynomial-time replacement for Dijkstra. It does not choose one preferred route; a downstream decision-maker must select among the trade-offs.
