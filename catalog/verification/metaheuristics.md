# Verification record — metaheuristics in spatial optimisation

**Source entry:** Section 6, page 10  
**Original label:** Heuristics: genetic algorithms, simulated annealing, NSGA-II, particle swarm, ant colony, tabu search, GRASP, variable neighborhood search, matheuristics  
**Canonical record:** [Metaheuristics for spatial optimisation](../../algorithms/optimization/metaheuristics.md)  
**Review date:** 18 November 2026

## Independent review dimensions

| Dimension | Current status | Evidence and boundary |
|---|---|---|
| Capture | captured | Original label and page are preserved in the Section 6 index and 47-page source transcription |
| Identity | confirmed for named families | The nine named items resolve to established method families or a named multi-objective algorithm; GA and matheuristics are broad families rather than one implementation |
| Bibliography | selected references confirmed | Original/publisher or author/institutional records were checked for Holland, Kirkpatrick et al., Deb et al., Kennedy & Eberhart, Dorigo et al., Glover, Feo & Resende, Mladenović & Hansen, and the Maniezzo/Stützle/Voß edited volume |
| Technical claims | partially checked | The canonical record gives a bounded taxonomy and explicit distinctions. It is not a full derivation or variant-by-variant technical review |
| Implementation | not_started for this grouped family | Existing location/routing heuristics in the repository are problem-specific. This record does not claim generic implementations of the nine families |
| Tests/validation | not_applicable to this taxonomy page | Future method-specific implementations require their own independent tests and comparison baselines |
| Rights | link_only for papers/books | Bibliographic links are provided; no third-party paper text, figures or tables are reproduced in the new page |
| Canonicalisation | created | One canonical overview links the nine method families without collapsing them into a single algorithm |

## Research checks

- Holland's book record was checked against MIT Press and its DOI landing page; the 1975 University of Michigan Press original and 1992 MIT Press reprint are distinguished.
- Simulated annealing was checked against the *Science* publisher record and DOI.
- NSGA-II was checked against the IEEE bibliographic record and an institutional research record.
- Particle swarm optimisation was checked against IEEE Xplore and the conference proceedings record.
- Ant System was checked against the article metadata and DOI.
- Tabu Search Part I was checked against the INFORMS publisher record and DOI.
- GRASP was checked against the journal DOI and the authors' publication bibliography; page-end metadata varies across secondary exports, so the canonical record uses the publisher/journal citation and does not reproduce article content.
- VNS was checked against the publisher's journal record and DOI.
- The matheuristics entry was checked against the Springer edited-volume record; it is treated as a hybridisation family, not an algorithm.

## Remaining work

1. Research the technical details and modern variants relevant to spatial optimisation separately.
2. Decide whether any named method merits a dedicated method page or implementation, based on a concrete spatial problem.
3. Add problem-specific examples and exact small-instance baselines before benchmarking stochastic methods.
4. Do not promote the source row to fully verified until the technical-claim and intended implementation/reproduction dimensions have been reviewed.
