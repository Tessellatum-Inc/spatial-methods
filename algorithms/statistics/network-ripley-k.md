# Network Ripley's K and shortest-path point-pattern distances

## 1. Why network point patterns differ

Events constrained to roads, rivers, paths or utility networks do not interact through straight-line Euclidean distance. Two points that are close in the plane may be far apart along the network, while two points separated by a river or disconnected network component may have no finite network path.

Represent the study network as an undirected weighted graph whose edge weights are physical or impedance lengths. A point event is attached to an edge and an offset measured from that edge's first endpoint.

## 2. Point-to-point network distance

For an event p on edge (u,v) of length L_p at offset s_p, its distances to the two endpoints are s_p and L_p-s_p. For another event q on edge (a,b), compute the minimum over endpoint pairs:

\[
d_N(p,q)=\min_{x\in\{u,v\},\;y\in\{a,b\}}
\{d(p,x)+d_G(x,y)+d(y,q)\}.
\]

When both events lie on the same edge, also consider the direct segment distance. The graph distances d_G are shortest-path distances over the entire network, so cycles and parallel links can provide shorter alternate routes. Disconnected pairs have infinite distance.

## 3. Network K estimator

For n observed events and total network length |L|, the implementation reports the uncorrected descriptive estimator

\[
\widehat K_N(r)=\frac{|L|}{n(n-1)}
\sum_{i\ne j} I\{d_N(x_i,x_j)\le r\}.
\]

Pairs are ordered in the sum. The output has units of network length. It is not the planar Ripley K estimator and does not use Euclidean disks. The expression is a simple finite-network pair-count summary; boundary and junction effects matter for inferential interpretation.

## 4. Python implementation

The [point-process package](../../implementations/python/point-process/README.md) implements:

- Event-to-event shortest-path distance matrices.
- Direct same-edge and alternate cycle-route comparisons.
- Parallel links and disconnected components.
- Network K curves at user-supplied distance thresholds.

Run the package tests from its directory with `python -m pytest -q`.

## 5. Limitations and responsible use

- Network edges are undirected and have strictly positive finite lengths.
- Each event must be attached to one edge with an offset within its length.
- Total network length is the sum of input edge lengths; do not duplicate edges unless they are genuinely distinct network links.
- No endpoint, junction or network observation-window edge correction is applied.
- No intensity reweighting, inhomogeneous network K, simulation envelope or CSR test is included.
- The shortest-path model assumes the graph and edge lengths adequately represent movement or interaction.
- This implementation is a transparent reference method; all-pairs graph shortest paths are not suitable for very large networks without indexing or specialized network-distance algorithms.

## References and further reading

- Okabe, A., and Yamada, I. (2001). The K-function method on a network and its computational implementation. *Geographical Analysis*, 33(3), 271–290.
- Baddeley, A., Rubak, E., and Turner, R. (2015). *Spatial Point Patterns: Methodology and Applications with R*. Chapman and Hall/CRC.
