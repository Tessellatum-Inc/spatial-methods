# Ward hierarchical clustering

Exact dense agglomerative Ward clustering for finite Euclidean observations.

## Run
```bash
python -m pip install -r requirements.txt
python -m pytest -q
```

## Example
```python
import numpy as np
from ward_clustering import ward_clustering
X = np.array([[0, 0], [0, 1], [8, 8], [9, 8]], dtype=float)
fit = ward_clustering(X, k=2)
print(fit["labels"])
print(fit["linkage"])
```

At each step the algorithm merges the pair that produces the smallest
increase in within-cluster sum of squares. Linkage heights are
sqrt(2 * increase in SSE); ties use the smallest active cluster-id pair.

The implementation is an exact small-data baseline with O(n^3) straightforward
pair search. It does not implement Ward.D2 variants for arbitrary dissimilarity
matrices, sparse/large-scale nearest-neighbour-chain acceleration, other
linkage criteria, or spatial contiguity constraints.
