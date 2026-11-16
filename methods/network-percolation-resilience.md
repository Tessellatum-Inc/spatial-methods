# Network percolation and node-attack resilience

A network's connectivity can be tested by removing nodes or edges and tracking how the remaining graph fragments. A simple diagnostic is the fraction of original nodes in the largest connected component after a removal fraction \(q\):
\[
S(q)=\frac{|C_{\max}(q)|}{N_0}.
\]
Random failures and targeted attacks are different experiments. A degree-targeted attack removes high-degree nodes first; a random-failure experiment samples nodes without targeting. Their curves can reveal structural vulnerability, but neither alone measures service continuity.

## Implemented baseline

The [Python package](../implementations/python/network-resilience/README.md) computes largest-component size, static degree attack order, seeded random order and node-removal curves. It validates undirected graph structure and normalizes the giant-component fraction by the original node count.

## Spatial infrastructure cautions

For roads, transit or utilities, topological connectivity is not the same as functional accessibility. A connected component may still be disconnected in practice by capacity, direction, travel time, hazard exposure, service frequency or mode restrictions. A more realistic assessment should track origin-destination accessibility, flow/capacity, critical demand and recovery, and should model spatially correlated failures rather than assuming independent random removal.

## Source

- Albert, R., Jeong, H., & Barabási, A.-L. (2000). “Error and Attack Tolerance of Complex Networks.” *Nature*, 406, 378–382. [DOI](https://doi.org/10.1038/35019019). The 2001 corrigendum corrected part of the reported error-tolerance curves; see [Nature correction](https://doi.org/10.1038/35054111).

No source text or figures are reproduced.
