# Spatial cellular automata: synchronous B/S rules and Schelling relocation

## What this covers

A cellular automaton represents a spatial field as cells whose states change through local rules. A simple binary automaton has state (x_{i,j}^{(t)} \in \{0,1\}), a neighborhood (N(i,j)), and a transition rule that maps the previous generation to the next:

\[
x_{i,j}^{(t+1)} = f\left(x_{i,j}^{(t)}, \sum_{(u,v)\in N(i,j)}x_{u,v}^{(t)}\right).
\]

For a B/S rule, a dead cell is born when its live-neighbor count is in the birth set (B), while a live cell survives when its count is in the survival set (S). Conway's Life is B3/S23.

A Moore neighborhood has eight adjacent cells. A von Neumann neighborhood has four orthogonal cells. Boundary treatment is part of the model: fixed-dead boundaries omit cells outside the raster; periodic boundaries wrap the grid into a torus.

## Synchronous update

A synchronous step computes every new cell from the same old grid. It must not mutate cells in place while iterating, because that would make the result depend on scan order. The reference implementation in [spatial-simulation](../../implementations/python/spatial-simulation/README.md) computes neighbor counts, evaluates the B/S sets, and returns a new array.

## Schelling-style relocation

A Schelling model represents agents from two or more groups on a lattice with vacant cells. For agent (i), define the same-group share among occupied neighbors:

\[
s_i = \frac{\#\{j\in N(i): x_j=x_i,\ x_j\ne0\}}
{\#\{j\in N(i):x_j\ne0\}}.
\]

An agent is unhappy when (s_i < \tau), where (	au\) is a tolerance parameter. The implementation evaluates unhappiness on the current state, then processes unhappy agents in a seeded random order and relocates them to distinct cells that were vacant at the start of the step. It preserves group counts and makes the random order reproducible.

This is one deliberately specified relocation variant. Other Schelling models differ in how agents search, whether moves are sequential or simultaneous, whether agents can swap, how vacancies are chosen, and whether preferences vary by household or context.

## Complexity and interpretation

A B/S automaton step is (O(RC|N|)) for an (R\times C) grid and a fixed-size neighborhood. The transparent Schelling implementation evaluates local neighborhoods directly and is intended for small and medium teaching grids; it is not optimized for large agent populations.

A simulation is not a forecast merely because its output resembles a map. Results depend on initial conditions, transition rules, neighborhood definition, boundary conditions, time step, parameter calibration and validation. A stylized Schelling model demonstrates how local preferences can produce aggregate spatial patterns; it does not establish a causal explanation for real-world segregation.

## Scope boundary

This lesson and package do **not** implement or reproduce SLEUTH, ANN-CA, logistic-CA, Markov-CA, CLUE-S, FLUS, PLUS, Dinamica EGO or Land Change Modeler. Those are distinct land-change models and software systems requiring separate identity, data, calibration and validation work. The source entry remains partial.

## Tests

The independent tests cover Moore and von Neumann counts, fixed and periodic boundaries, a Life blinker oscillator, zero-step copying, input validation, occupied-neighbor share, group-count preservation, seeded reproducibility and stopping behaviour.


## Site percolation

In site percolation, each lattice site is independently occupied with probability (p). A finite-grid crossing test asks whether occupied sites connect one designated boundary to another under a specified adjacency rule. The reference package samples Bernoulli occupancy and uses graph traversal to test a top-to-bottom crossing. Four-neighbor and eight-neighbor connectivity are different models and can produce different thresholds and finite-size outcomes.

## Stochastic forest-fire automaton

The forest-fire teaching model uses three states: empty, tree and burning. In one synchronous update, burning cells become empty, trees ignite through neighboring fire or a lightning event, and empty cells may grow trees. Growth and lightning probabilities are explicit inputs; a seed makes a run reproducible.

This is a stochastic cellular automaton, not a physical fire-behaviour model. It omits wind, fuel moisture, topography, spotting, suppression and calibrated spread rates.

## Remaining source family

The source entry also names Sugarscape, diffusion-limited aggregation, sandpile dynamics and spatial game theory. They are separate model families and are not implemented by this package. The source row remains partial rather than complete.
