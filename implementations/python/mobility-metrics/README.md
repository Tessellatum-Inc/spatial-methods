# Descriptive mobility metrics

Dependency-light descriptive metrics for projected planar movement trajectories and categorical visit sequences.

Implemented:
- Weighted or unweighted radius of gyration.
- Euclidean step lengths and signed turning angles.
- Shannon visit entropy in natural-log units and its effective number of states.
- Fano-inequality upper bound on maximum next-state predictability for a supplied number of states.

## Run

```bash
python -m pip install -r requirements.txt
python -m pytest -q
```

## Assumptions and limits

Coordinates are projected planar x/y values in common linear units and remain in time order. Radius of gyration weights are per observation, not elapsed-time weights unless the caller supplies them. Visit entropy requires a caller-defined discrete state sequence; spatial discretisation is not inferred. Predictability is an entropy-based upper bound, not an empirical forecast score. The package does not fit exploration/preferential-return models, Lévy flights, continuous-time random walks, Brownian bridges, step-selection functions or resource-selection functions.
