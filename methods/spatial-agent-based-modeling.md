# Spatial agent-based modeling

Agent-based modeling represents a system as interacting entities with state, behaviour and local or network-mediated interactions. In spatial applications, agents occupy locations or move through a spatial environment; their decisions can depend on nearby agents, environmental attributes, access, constraints and changing conditions.

## Model specification

A reproducible spatial ABM should define:

1. **Agents:** types, attributes, state variables and population generation.
2. **Space:** raster lattice, vector geometry, network or continuous coordinate domain.
3. **Environment:** static and dynamic fields, resources, barriers and capacities.
4. **Behaviour:** decision rules, information available to agents and behavioural heterogeneity.
5. **Interaction:** neighborhood, contact network, conflict or cooperation rules.
6. **Time:** synchronous or asynchronous updates, event ordering and time-step meaning.
7. **Stochasticity:** random processes, seed management and sensitivity to random streams.
8. **Outputs:** agent trajectories, aggregate indicators, spatial patterns and uncertainty.
9. **Validation:** empirical calibration, pattern-oriented checks, sensitivity analysis and comparison with simpler baselines.

## Cellular automata and ABMs

A cellular automaton updates cell states through local transition rules. An ABM gives individual agents explicit state and behaviour. The categories overlap: a lattice model can place one agent per cell, while a CA can encode aggregate land-cover states without representing individual decision-makers.

The [cellular automata lesson](../algorithms/domain-modeling/cellular-automata.md) and its [reference package](../implementations/python/spatial-simulation/README.md) provide several small examples: a synchronous binary B/S automaton, a finite-lattice site-percolation crossing test, a stochastic forest-fire automaton a Schelling-style relocation process, and a discrete-time SIR process on a static contact graph, and a first-order categorical Markov land-change baseline. The Schelling example is agent-like but remains a tightly constrained lattice model; SIR is a network process rather than a spatial-mobility model.

## Design and validation cautions

- Distinguish a generative demonstration from an empirically validated model.
- Specify whether updates are synchronous, sequential, random-sequential or event-driven.
- Report boundary effects, spatial resolution and the meaning of a cell or agent.
- Use multiple random seeds and parameter sensitivity analysis; a single run is not a stable result.
- Avoid calibrating only to one aggregate statistic when multiple spatial patterns are observable.
- Compare against simpler statistical or process baselines.
- Preserve the distinction between model assumptions and observed mechanisms.

## Scope

This page is a modeling framework overview, not a reproduction of a named land-use, disease, evacuation, ecological or economic model. Each named model family in the source compendium requires its own source and implementation review.
