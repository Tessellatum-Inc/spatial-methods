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
