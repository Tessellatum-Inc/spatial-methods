# Source verification — weighted head-banging

## Identity and bibliography
The NCI Head-Bang software documentation describes weighted two-dimensional median-based smoothing. Primary references include Hansen (1991), “Head-banging: Robust smoothing in the plane,” *IEEE Transactions on Geoscience and Remote Sensing*, 29(3), 369–378; and Mungiole, Pickle and Simonson (1999), “Application of a weighted head-banging algorithm to mortality data maps,” *Statistics in Medicine*, 18(23), 3201–3209, DOI 10.1002/(SICI)1097-0258(19991215)18:23%3C3201::AID-SIM310%3E3.0.CO;2-U.

## Technical claims
The documented algorithm uses nearest neighbours, nearly collinear triples, low/high endpoint screens based on medians, and a median update of the target. The weighted extension uses weighted medians and allows target weight to determine whether a screen overrides its current value. Parameters include neighbour count, angular tolerance, maximum triples and iteration limit.

## Implementation and reproduction
Implemented: k-nearest neighbour selection, angular triple filtering, low/high weighted median screens, weighted target update, synchronous iteration and convergence reporting. Tests cover spike clipping, screen retention, weighted target resistance, endpoint dominance, no-triple fallback, deterministic ties and invalid input.

Not implemented: complete Head-Bang software corner-point rules, parameter optimization, age adjustment, rate uncertainty or all software interface options. Repository CI is required to establish committed tests pass.

## Rights
The algorithm is independently implemented from published descriptions and public NCI documentation; no source code or figures are copied.
