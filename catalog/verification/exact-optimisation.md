# Verification record — exact optimisation and network-flow source group

**Source entry:** Section 6, page 10  
**Original label:** Exact methods: branch-and-bound, Lagrangian relaxation, Benders decomposition, min-cost flow, transportation and assignment problems, Hungarian algorithm; quantum annealing and QAOA (experimental)  
**Canonical record:** [Exact optimisation methods and network-flow models](../../algorithms/optimization/exact-optimisation-methods.md)  
**Review date:** 18 November 2026

## Independent review dimensions

| Dimension | Current status | Evidence and boundary |
|---|---|---|
| Capture | captured | Original grouped label and page retained in the Section 6 index |
| Identity | confirmed for named families/models | Branch-and-bound, Lagrangian relaxation, Benders decomposition, network-flow models, transportation, assignment, Hungarian method and QAOA are distinguished; quantum annealing is retained as a separate approach |
| Bibliography | selected references confirmed | Land–Doig, Geoffrion, Benders, Ahuja–Magnanti–Orlin, Hitchcock, Kuhn and Farhi–Goldstone–Gutmann records checked against publisher, institutional or author-hosted sources |
| Technical claims | partially checked | The overview distinguishes frameworks, relaxations, problem classes and quantum approximate methods; it is not a full derivation of every method |
| Implementation | not_started for this grouped family | Selected exact small-instance location solvers exist, but they are not general implementations of all named methods |
| Tests/validation | not_applicable to this taxonomy page | Any new solver needs its own formulation, independent feasibility checks, exact small-instance oracle and solver-status reporting |
| Rights | link_only for references | Bibliographic links are used; no paper text or third-party figures are reproduced |
| Canonicalisation | created | One overview record links the grouped families while retaining their distinct types |

## Research checks

- Land and Doig's branch-and-bound paper was checked against an institutional publication record and the DOI record.
- Geoffrion's Lagrangian-relaxation chapter was checked against the Springer volume record and the reproduced chapter.
- Benders' decomposition paper was checked against the original *Numerische Mathematik* bibliographic record and an institutional research record.
- Ahuja, Magnanti and Orlin's network-flow book was checked against the authors' institutional page and publisher catalogue; its chapters explicitly cover minimum-cost flows and assignments.
- Hitchcock's transportation paper was checked against Wiley's publisher record and DOI.
- Kuhn's Hungarian-method paper was checked against Wiley's publisher record and DOI.
- QAOA was checked against the original arXiv preprint by Farhi, Goldstone and Gutmann.

## Remaining work

1. Research technical claims and modern variants separately, especially branch-and-bound node selection/bounding, Lagrangian dual optimisation and primal recovery, Benders cut classes, and min-cost-flow algorithms.
2. Keep quantum annealing hardware claims separate from the QAOA paper and review current devices only when a concrete comparison is planned.
3. Decide whether one method merits a dedicated implementation based on a spatial use case.
4. Do not promote the source row to fully verified until the applicable technical, implementation and validation dimensions are complete.
