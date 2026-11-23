# Network edge failure and reliability

## Why this family matters

Node-removal robustness is only one view of infrastructure vulnerability. Roads, bridges, cables, pipes and communication links can fail while their endpoint facilities remain. Bond percolation models link failure; reliability analysis asks for the probability that specified terminals remain connected when components fail probabilistically. A minimal cut set is an inclusion-minimal set of components whose simultaneous failure disconnects the requested terminals.

## Implemented teaching baselines

The companion Python module provides:
1. Edge attack curves, with seeded random order and static edge-betweenness ranking.
2. Monte Carlo all-terminal or selected-terminal reliability under independent identical edge survival, including a Bernoulli standard error and clipped normal-approximation 95% interval.
3. Exhaustive inclusion-minimal edge cut sets for small graphs, protected by a maximum-edge guard.

For a graph G=(V,E) and independent edge survival probability p, all-terminal reliability is the probability that the surviving graph is connected. For a terminal set T, k-terminal reliability is the probability that every node in T lies in one connected component. The estimator is R-hat=s/N, where s of N sampled networks satisfy the event; its plug-in standard error is sqrt(R-hat(1-R-hat)/N).

A cut set C is a set of edges whose removal breaks the requested connectivity event. It is minimal when no proper subset is also a cut set. Minimal does not mean minimum-cardinality: minimal cuts may have different sizes.

## Learning workflow

1. Identify whether the question concerns all-terminal or selected-terminal connectivity.
2. Compare node-attack and edge-attack curves and state each denominator.
3. Estimate reliability across several probabilities and seeds; report trial count and Monte Carlo uncertainty.
4. Enumerate minimal cuts only on small graphs, then map abstract edges to physical assets.
5. Challenge the independent-identical failure assumption: geographically clustered infrastructure often experiences common-cause hazards.

## Scope boundary

This is not a full reliability package. It does not implement exact reliability-polynomial evaluation, specialized minimal-path algorithms, Karger-style approximation schemes, directed or capacitated reliability, common-cause failures, spatial hazard fields, interdependent networks, cascading overload, or post-disaster repair. The reported interval is not an exact interval and can be poor for rare events. Static edge betweenness is not a causal criticality measure.

## References

- Brown, J. I., Kolokolnikov, T., & Kooij, R. (2024). New approximations for network reliability. Networks, 84. DOI: 10.1002/net.22215.
- Chaturvedi, S. K. (2016). Network Reliability: Measures and Evaluation. Wiley. Chapter 4 covers terminal cut-set enumeration and minimal cut sets.
- Bashan, A., Berezin, Y., & Havlin, S. (2013). The extreme vulnerability of interdependent spatially embedded networks. Nature Physics, 9, 667–672. DOI: 10.1038/nphys2727.
