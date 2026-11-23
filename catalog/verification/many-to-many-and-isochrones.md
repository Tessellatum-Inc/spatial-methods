# Verification record: many-to-many paths and network isochrones

## Source identity
- Compendium: *Spatial Analysis Algorithms: Complete Compendium*
- Original location: Section 1, Network analysis, page 2
- Source entries: many-to-many routing; service areas and isochrones

## Implemented scope
- Repeated single-source Dijkstra for requested source-target pairs.
- Cutoff Dijkstra for inclusive cost-budget network isochrones.
- Directed frontier arcs whose cumulative traversal cost exceeds the budget.

## Tests
- Directed path and cost reconstruction.
- Identity and unreachable pairs.
- Default target enumeration.
- Exact-budget inclusion and frontier reporting.
- Zero budget and invalid budgets.
- Negative and non-finite edge rejection.

## Boundaries
This is a bounded static-graph baseline. It is not a contraction-hierarchy or hub-label many-to-many engine; it does not handle time-dependent, stochastic, transit or turn-expanded routing, and it does not polygonize the returned network region. The corresponding grouped source entry remains partial until those variants and the source bibliography/claims/rights are separately reviewed.
