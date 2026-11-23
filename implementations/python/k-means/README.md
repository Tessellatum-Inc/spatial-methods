# Lloyd k-means

NumPy implementation of Lloyd's squared-Euclidean partitioning algorithm
with k-means++ initialization and deterministic empty-cluster repair.

## Run
```bash
python -m pip install -r requirements.txt
python -m pytest -q
```

## Example
```python
import numpy as np
from k_means import kmeans
X = np.array([[0, 0], [0, 1], [1, 0], [9, 9], [9, 10], [10, 9]], dtype=float)
fit = kmeans(X, 2, random_state=42, n_init=10)
print(fit["centers"], fit["labels"], fit["inertia"])
```

The caller chooses k and handles feature scaling. Multiple seeded starts retain
the lowest-inertia result. This is ordinary unconstrained Lloyd k-means; it
does not implement streaming, kernel/spherical variants, automatic k selection,
capacity/equal-size constraints, spatial contiguity or geodesic distance.
