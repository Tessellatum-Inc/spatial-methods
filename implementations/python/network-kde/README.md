# Network kernel density estimation

Dependency-free vertex-sampled network KDE reference implementation.

## Run

```bash
python -m pip install -r requirements.txt
python -m pytest -q
```

## Example

```python
from network_kde import network_kde
edges = [("a", "b", 400.0), ("b", "c", 250.0)]
fit = network_kde(edges, ["a", "c"], bandwidth=500.0)
print(list(zip(fit["nodes"], fit["density"])))
```

The estimator evaluates a one-dimensional Gaussian kernel using weighted
shortest-path distance on an undirected graph. Events and targets are vertices;
edge lengths and bandwidth must use the same linear unit. Optional event
weights are finite and non-negative.

This is a small-network vertex-sampled baseline. It does not integrate over
edge interiors, locate events inside edges, apply network edge correction,
estimate bandwidth, or implement network K / SANET methods. Disconnected
components do not influence one another.
