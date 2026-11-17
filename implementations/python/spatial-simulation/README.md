# Spatial simulation: cellular automata and Schelling segregation

Teaching implementations for two bounded spatial-simulation patterns:

- synchronous binary B/S cellular automata with Moore or von Neumann neighborhoods;
- a seeded Schelling-style relocation model for categorical agents on a 2D lattice.

## Install and test

```bash
python -m pip install -r requirements.txt
python -m pip install pytest
python -m pytest -q
```

## Cellular automata

```python
import numpy as np
from spatial_simulation import simulate_life_like

seed = np.zeros((30, 30), dtype=np.uint8)
seed[14:17, 14:17] = 1
result = simulate_life_like(seed, 20, birth=(3,), survive=(2, 3))
```

The rule is evaluated synchronously: every next-generation cell is derived from the same prior grid. Edges are fixed-dead by default; set `periodic=True` for a toroidal lattice. This is a generic binary automaton, not an implementation of SLEUTH, CLUE-S, FLUS, PLUS or a calibrated land-change model.

## Schelling-style segregation

Use 0 for empty cells and positive integers for group labels:

```python
from spatial_simulation import simulate_schelling

result = simulate_schelling(
    initial_grid,
    tolerance=0.4,
    max_iterations=100,
    seed=7,
)
final_grid = result.grid
```

Agents compare their group with occupied neighbors. Agents below the tolerance relocate to distinct cells that were empty at the beginning of that iteration. Unhappiness is evaluated before moves, and relocation order is seeded. The implementation preserves group counts but is a deliberately simple one-pass relocation baseline; it is not a full agent-based simulation framework or an empirical model of segregation.

## Contracts and limitations

- Grids are non-empty 2D integer arrays. Cellular automata accept only 0/1.
- Moore neighborhoods have eight offsets; von Neumann neighborhoods have four.
- Periodic boundaries wrap across both axes. Non-periodic boundaries omit off-grid neighbors.
- Schelling's share is defined over occupied neighbors; no occupied neighbors means share 1.
- The model does not include heterogeneous preferences, household units, transport costs, land markets, vacancy search, or empirical calibration.
- Complexity is proportional to grid cells times neighborhood size per automaton step. The transparent Schelling baseline currently evaluates local neighborhoods directly and is intended for small/medium teaching grids.


## Site percolation

`sample_site_percolation(shape, probability, seed=...)` draws independent occupied sites with the requested Bernoulli probability. `percolates(grid)` checks whether occupied cells form a top-to-bottom path using four-neighbor connectivity by default; pass `neighborhood="moore"` to allow diagonal links.

This is a finite-lattice connectivity experiment, not a fitted model of a particular material or landscape. The finite grid, boundary definition and connectivity convention affect the result.

## Forest-fire automaton

`forest_fire_step` uses 0=empty, 1=tree and 2=burning. At each synchronous step, burning cells become empty; trees ignite if adjacent to fire or struck by lightning; empty cells grow trees with the supplied probability. Growth and lightning are independently parameterized and the random seed is explicit.

The model is a compact stochastic cellular automaton, not a calibrated wildfire spread model. It omits wind, fuel moisture, topography, spotting, fire suppression and physical spread rates.


## Spatial random graphs

The package also provides two seeded graph generators:

- `distance_decay_preferential_attachment` starts with an `m+1` clique and attaches each later node to `m` predecessors using degree preference multiplied by exponential Euclidean distance decay.
- `watts_strogatz_graph` constructs a ring lattice and rewires clockwise edges with probability `beta`, preserving the edge count and avoiding self-loops/duplicate edges.

Both return dense Boolean adjacency matrices. The spatial generator assumes finite coordinates in one consistent Euclidean coordinate system; the small-world generator does not guarantee connectivity after rewiring. These are small-instance reference generators, not large-network engines or empirical network fits.


## Network SIR

`sir_step` and `simulate_sir` implement a discrete-time SIR process on a static undirected contact graph. States are 0=susceptible, 1=infected and 2=recovered. A susceptible with (k) infected neighbors becomes infected with probability (1-(1-\beta)^k); infected nodes recover with probability (\gamma). The simulator returns S/I/R counts at the initial state and after each step.

The update is synchronous: newly infected nodes transmit only in the following step. The model assumes homogeneous probabilities and a fixed contact graph; it is not a spatial diffusion or mobility-driven epidemic model and is not calibrated for forecasting.
