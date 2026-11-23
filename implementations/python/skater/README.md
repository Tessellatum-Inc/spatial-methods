# SKATER spatial regionalization

A deterministic greedy regionalization baseline that builds a minimum
spanning tree (MST) from supplied spatial adjacency costs and prunes edges to
form k connected regions with low within-region feature variation.

## Run
```bash
python -m pip install -r requirements.txt
python -m pytest -q
```

## Example
```python
import numpy as np
from skater import skater
X = np.array([[0.], [1.], [10.], [11.]])
adjacency = [(0, 1, 1.), (1, 2, 1.), (2, 3, 1.)]
fit = skater(X, adjacency, k=2)
print(fit["labels"], fit["cuts"], fit["objective"])
```

The graph must be connected. Edge costs define the MST; feature vectors
define the within-region sum-of-squares objective. Every output region is
connected in the input graph because it is a component of the pruned MST.

This is a small-graph greedy baseline, not a full reproduction of every
SKATER implementation variant. It does not implement automatic selection of
k, contiguity constraints beyond supplied adjacency, regional minimum sizes,
multi-attribute scaling, or alternative regionalization objectives.
