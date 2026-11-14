# Verification record: network edge failure and reliability

## Identity and scope
- Canonical record: network edge-failure curves, independent-edge Monte Carlo reliability, and small-graph minimal edge cut sets.
- Implementation: implementations/python/network-resilience/edge_reliability.py.
- Classification: original teaching/reference baselines, not a reproduction of one published reliability solver.

## Bibliographic checks
- Brown, Kolokolnikov & Kooij (2024), New approximations for network reliability, Networks 84, DOI 10.1002/net.22215. The paper discusses Monte Carlo reliability and the difficulty of exact reliability-polynomial evaluation. This repository implements direct Bernoulli edge-state sampling, not the paper's edge-removal-process estimator or its approximations.
- Chaturvedi (2016), Network Reliability: Measures and Evaluation, Wiley. Its cut-set chapter defines minimal terminal cut sets. This repository uses exhaustive subset enumeration, not the book's specialized enumeration algorithms.
- Bashan et al. (2013), The extreme vulnerability of interdependent spatially embedded networks, Nature Physics 9, 667–672, DOI 10.1038/nphys2727. Context only; spatial embedding and interdependence are not implemented.

## Technical checks
- Graph must be nonempty, simple, undirected and symmetrically encoded.
- Attack curves require a complete permutation of the undirected edge set.
- Reliability assumes independent, identical edge survival and explicit seeded pseudorandom sampling.
- Standard error is the Bernoulli plug-in estimate; interval is a clipped normal approximation.
- Minimal cuts are inclusion-minimal, not necessarily minimum-cardinality. Enumeration is exponential and guarded by a maximum edge count.
- Edge betweenness is ranked on the intact graph, not recalculated after removals.

## Reproduction and rights
- Original repository implementation; no source code or figures copied.
- Unit tests cover path/triangle cuts, deterministic random seeds, edge curves, reliability boundary probabilities and k-terminal reliability.
- Full repository pytest and CI have not been run in this authoring session.
