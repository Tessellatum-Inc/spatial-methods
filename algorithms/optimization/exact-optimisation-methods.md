# Exact optimisation methods and network-flow models

"Exact method" is not one algorithm. This source group combines a general search framework, mathematical relaxations and decomposition, network-flow models, special cases of those models, and an experimental quantum approximate algorithm. Their guarantees and use cases must be kept separate.

## Methods and problem classes

| Name | What it is | Role in optimisation | Key distinction |
|---|---|---|---|
| Branch-and-bound | General exact search framework | Splits a discrete search space into subproblems and uses valid bounds to prune regions that cannot improve the incumbent | Exactness depends on valid bounds, exhaustive branching and correct termination; performance can be exponential |
| Lagrangian relaxation | Mathematical relaxation and bounding technique | Moves selected complicating constraints into the objective with multipliers, producing a bound and often a decomposable subproblem | It is not by itself a complete solver; multiplier optimisation, primal recovery and bound interpretation matter |
| Benders decomposition | Decomposition framework | Separates complicating variables from a tractable subproblem and iteratively adds feasibility/optimality cuts | Classical guarantees rely on assumptions about the master/subproblem structure and valid cuts |
| Minimum-cost flow | Network optimisation model | Routes flow through a directed network at minimum total arc cost subject to conservation, supply/demand and capacity constraints | It is a problem class with multiple exact algorithms, not one unique algorithm |
| Transportation problem | Structured supply-to-demand flow model | Assigns shipments from origins to destinations while satisfying supply and demand at minimum cost | It is a special network-flow/linear-programming structure; balanced and unbalanced formulations differ |
| Assignment problem | One-to-one matching optimisation model | Assigns each agent/item to one task/slot under a cost or score matrix | It is a special case of bipartite matching and can be solved by several methods |
| Hungarian method | Exact algorithm for the assignment problem | Finds an optimal one-to-one assignment for the classical cost-matrix formulation | It is not a general solver for every facility-location or routing problem |
| Quantum annealing | Quantum optimisation approach | Encodes a problem into an energy landscape for hardware or simulated annealing-like quantum processes | Hardware, embedding, noise, formulation and sampling effects are central; it is not a general classical exact solver |
| QAOA | Parameterised quantum approximate optimisation algorithm | Alternates problem and mixing operators with classically optimised parameters to sample candidate solutions | It is a variational approximate method; the original paper does not establish general practical quantum advantage |

## How these methods relate

Branch-and-bound is a search framework that can use linear-programming bounds, Lagrangian bounds or problem-specific relaxations. Benders decomposition is useful when the mathematical structure can be split into a master problem and a subproblem. Lagrangian relaxation can expose separable structure and produce bounds, but a dual bound alone is not a feasible primal solution.

Minimum-cost flow, transportation and assignment are models rather than interchangeable solver names. A spatial allocation problem may be formulated as a network flow only if its decision structure and constraints fit the network model. For example, a simple supply-to-demand transportation model does not automatically capture facility-opening decisions, contiguity, route sequencing, equity floors or nonlinear congestion.

The Hungarian method addresses the classical assignment model. It should not be described as a generic location-allocation solver. Similarly, QAOA and quantum annealing belong in an experimental quantum-computing branch of the catalogue, not in a list of established classical exact algorithms.

## Spatial applications

These model families can support:
- assigning field crews, sensors, jobs or facilities to tasks;
- distributing commodities from depots to demand locations;
- routing divisible flow through capacitated transport or utility networks;
- decomposing large location-allocation or planning models;
- deriving lower bounds for spatial integer programmes.

The spatial formulation must state what is being assigned or routed, whether flow is divisible, how capacity is measured, what costs represent, and whether geometry or network constraints are embedded in the model. A network model is not automatically spatially valid merely because its nodes have coordinates.

## Reproducibility and validation

For exact optimisation, report the formulation and solver status, not only the returned objective value:

1. Define variables, objective, constraints, units, and integrality requirements.
2. State whether the instance is feasible, infeasible, unbounded or stopped early.
3. Distinguish an optimality proof from a feasible incumbent or a best-known heuristic solution.
4. Record primal objective, dual/best bound, optimality gap, termination condition and time limit where the solver exposes them.
5. Validate every constraint independently on the returned solution.
6. Compare small instances with exhaustive enumeration or a second solver.
7. For decomposition methods, retain cut validity, convergence assumptions and subproblem status.
8. For quantum methods, report circuit depth, encoding, hardware/simulator, shots, optimiser, seeds and classical baseline.

## What this repository currently provides

This page is a source-linked taxonomy, not a claim that all methods in the source group have been implemented. The repository contains exact small-instance teaching solvers for selected location models and other problem-specific methods. Those implementations do not constitute general branch-and-bound, Lagrangian-relaxation, Benders, min-cost-flow, Hungarian or QAOA engines.

The next implementation should be chosen around a concrete spatial problem and a clear model contract. A small exact solver with an independent oracle is preferable to a generic abstraction that cannot demonstrate correctness.

## Primary and authoritative references

1. Land, A. H., & Doig, A. G. (1960). An automatic method of solving discrete programming problems. *Econometrica*, 28(3), 497–520. [https://doi.org/10.2307/1910129](https://doi.org/10.2307/1910129).
2. Geoffrion, A. M. (1974). Lagrangean relaxation for integer programming. In M. L. Balinski (Ed.), *Approaches to Integer Programming* (Mathematical Programming Studies 2, pp. 82–114). North-Holland. [Springer record](https://doi.org/10.1007/BFb0120686).
3. Benders, J. F. (1962). Partitioning procedures for solving mixed-variables programming problems. *Numerische Mathematik*, 4, 238–252. [https://doi.org/10.1007/BF01386316](https://doi.org/10.1007/BF01386316).
4. Ahuja, R. K., Magnanti, T. L., & Orlin, J. B. (1993). *Network Flows: Theory, Algorithms, and Applications*. Prentice Hall. [Publisher catalogue](https://www.pearson.com/en-us/subject-catalog/p/network-flows-theory-algorithms-and-applications/P200000003456).
5. Hitchcock, F. L. (1941). The distribution of a product from several sources to numerous localities. *Journal of Mathematics and Physics*, 20(1–4), 224–230. [https://doi.org/10.1002/sapm1941201224](https://doi.org/10.1002/sapm1941201224).
6. Kuhn, H. W. (1955). The Hungarian method for the assignment problem. *Naval Research Logistics Quarterly*, 2(1–2), 83–97. [https://doi.org/10.1002/nav.3800020109](https://doi.org/10.1002/nav.3800020109).
7. Farhi, E., Goldstone, J., & Gutmann, S. (2014). A quantum approximate optimization algorithm. [arXiv:1411.4028](https://arxiv.org/abs/1411.4028).

These sources establish a bibliographic starting point for the named families. They do not validate every modern solver variant, spatial formulation or claim of computational advantage. See the [verification record](../../catalog/verification/exact-optimisation.md).
