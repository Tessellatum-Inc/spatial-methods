# Exact p-dispersion for small candidate sets

The max-min p-dispersion problem selects exactly `p` sites from a finite candidate set to maximise the minimum pairwise distance among selected sites.

```python
import numpy as np
from p_dispersion import solve_p_dispersion

coordinates = np.array([[0, 0], [1, 0], [4, 0], [8, 0], [10, 0]])
distances = np.linalg.norm(coordinates[:, None, :] - coordinates[None, :, :], axis=2)
selected, minimum_separation = solve_p_dispersion(distances, p=3)
```

## Contract

- Input is a finite, symmetric, non-negative square pairwise distance matrix with zero diagonal.
- Exactly `p` distinct candidate indices are selected, with `2 <= p <= n`.
- Objective is the minimum pairwise distance among selected sites; larger is better.
- Equal optima are resolved lexicographically by candidate index.
- Duplicate candidate locations are permitted and have zero mutual distance.

## Limits

The package uses exhaustive enumeration of `n choose p` subsets and is intended for small instances and exact teaching/oracle use. It does not model demand, facility capacity, assignment cost, uncertainty, geographic barriers or network travel time; those are represented by the caller's distance matrix if appropriate. It is not a scalable heuristic or mixed-integer solver.

Run `pip install -r requirements.txt` and `pytest -q`.
