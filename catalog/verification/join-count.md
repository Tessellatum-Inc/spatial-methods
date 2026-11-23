# Source verification — binary join-count statistics

## Identity and bibliography

The method is the global binary join-count family for undirected spatial
weights, distinguishing black-black (BB), white-white (WW) and black-white
(BW) joins. A standard reference is Cliff, A. D. and Ord, J. K. (1981),
*Spatial Processes: Models & Applications*, Pion. Confirm edition and
publication metadata against a library or publisher record before marking
bibliography verification complete.

## Technical claims

For a fixed undirected graph with m edges and fixed class totals B and W,
random assignment of labels gives:

- E[BB] = m B(B-1) / [n(n-1)]
- E[WW] = m W(W-1) / [n(n-1)]
- E[BW] = 2mBW / [n(n-1)]

The expectations sum to m. The implementation counts each undirected edge
once and uses conditional label permutations that preserve the class totals.
Its upper- and lower-tail p-values are plus-one Monte Carlo estimates.

## Implementation and reproduction

A dependency-free reference implementation is available in
`implementations/python/join-count`. Tests cover analytic expected counts on
a path and complete graph, reproducible conditional permutations, a single
class, and invalid label/weight/permutation inputs. The implementation
requires a symmetric binary weights matrix with a zero diagonal.

Not implemented: local join-count statistics, multicolour join counts,
directed/weighted join-count variants, sparse production graph storage,
multiple-testing correction or a spatially varying class-probability null.
Repository CI must pass before recording the implementation as verified.

## Rights

The implementation and tests are original repository work. The algorithmic
concept and citation are described in original prose; no third-party source
code or figures are reproduced. Source-entry rights and bibliography review
remain separate from implementation status.
