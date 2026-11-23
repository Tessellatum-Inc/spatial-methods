# Source verification — Pareto multi-criteria shortest paths

## Identity and bibliography
Martins, E. Q. V. (1984). “On a multicriteria shortest path problem.” *European Journal of Operational Research*, 16(2), 236–245. DOI 10.1016/0377-2217(84)90077-8.

## Technical claims
Each path accumulates a vector of additive edge costs. At a node, a label is retained only if no existing label is componentwise no worse. Nonnegative edge costs permit removal of cycles without improving a path. The algorithm returns the nondominated source-to-target cost vectors.

## Implementation/reproduction
Implemented: arbitrary fixed objective dimension; lexicographic label queue; componentwise dominance; stale-label pruning; equal-cost deduplication; cycle avoidance; optional explicit per-node label cap that raises rather than truncates. Tests cover two- and three-objective trade-offs, intermediate dominance, zero-cost cycles, unreachable targets, source-equals-target, invalid costs and cap behaviour.

Not implemented: negative costs, multimodal timetable integration, turn-expanded graph construction, stochastic route choice, skyline services, route diversity or a polynomial bound on frontier size. Worst-case frontier growth is exponential. Repository CI is required to establish passing status.

## Rights
Only the published algorithmic concepts and bibliographic metadata are paraphrased; no source code or figures are reproduced.
