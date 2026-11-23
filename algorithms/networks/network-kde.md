# Network kernel density estimation

Network kernel density estimation (NKDE) adapts kernel smoothing to a linear
network. Euclidean distance is replaced by shortest-path distance along the
network, preventing off-network shortcuts.

For event vertices x_i with non-negative weights w_i, target vertex s and
bandwidth h, the reference implementation evaluates

\[
\hat f(s)=\frac{1}{\sqrt{2\pi}h}
\sum_i w_i\exp\left(-\frac{d_N(s,x_i)^2}{2h^2}\right),
\]

where d_N is undirected weighted shortest-path distance. This is a
one-dimensional Gaussian kernel evaluated at graph vertices.

Dijkstra search is run for each target vertex. Parallel edges are reduced to
their shortest length; disconnected events contribute zero. Edge lengths
and bandwidth must share a projected linear unit.

## Limitations

This is a vertex-sampled teaching baseline, not a full continuous linear
network estimator. It does not integrate over edge interiors, locate events
inside edges, apply endpoint or network edge correction, estimate bandwidth,
or implement network K and SANET methods. Values depend on vertex sampling
and should not be interpreted as an edge-integrated intensity surface.

See the [Python implementation](../../implementations/python/network-kde/README.md)
and [tests](../../implementations/python/network-kde/test_network_kde.py).
