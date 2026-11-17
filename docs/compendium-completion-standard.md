# Compendium completion standard

This document defines what it means to develop the supplied *Spatial Analysis Algorithms: Complete Compendium* into a useful, reproducible technical and learning resource. It supplements—not replaces—the preserved [47-page source transcription](../source-inventory/README.md), the [22 section indexes](../catalog/sections/README.md), the [coverage matrix](../catalog/coverage-matrix.md), and the [source-entry verification protocol](../catalog/verification-protocol.md).

## 1. The source compendium remains the master specification

The source transcription is the scope-preserving record. Do not shrink it to match the current repository, silently discard awkward or unfamiliar entries, or substitute the index for the source. Preserve original page, section, wording, cautions and grouped relationships.

The section indexes and coverage matrix are navigation and project-management layers. They are not the compendium itself and do not prove that a method has been researched, explained or implemented.

Every source entry must remain traceable to:
- its original page and section;
- its preserved source wording;
- one or more normalised child records where the source groups distinct methods;
- the canonical lesson, research dossier, implementation or external maintained tool that addresses it;
- an explicit development and review status.

## 2. Develop each entry according to its actual kind

Do not force every entry into a Python algorithm. First classify it using [the record-type taxonomy](../catalog/record-types.md).

| Record kind | Appropriate technical treatment | Executable treatment |
|---|---|---|
| Algorithm | Problem, inputs/outputs, assumptions, derivation, steps, correctness or guarantees, complexity, failure modes and variants | From-scratch teaching implementation where meaningful; tests and comparison baseline |
| Statistical model or estimator | Mathematical model, estimand, assumptions, identification, inference, uncertainty, diagnostics and validation | Numerical example, tests against known or trusted results, sensitivity notebook |
| Metric or index | Definition, units, range, interpretation, invariance, edge cases and misuse | Calculation, hand-checkable fixtures, tests and a worked notebook where useful |
| Data structure or index | Invariants, operations, complexity, memory/update behaviour and workload fit | Data structure, invariant/property tests and workload experiment |
| Software, framework or platform | Purpose, architecture, supported methods, version, dependencies, licence, maturity and reproducibility | Minimal documented integration or reproducible example; do not reimplement the platform |
| Standard, format or data model | Normative source, schema, semantics, coordinate/time conventions, interoperability and version | Parser/validator or interoperability fixture where useful |
| Workflow or applied method | Inputs, stages, decisions, data provenance, spatial/temporal scale, calibration and validation | Reproducible end-to-end case with synthetic or licensed data |
| Research family or unresolved name | Identity investigation, competing interpretations, primary sources and explicit uncertainty | No code until the method is identified and its contract can be stated |

A row that names six different algorithms is not one implementation task. Split it into child records, retain the parent grouping, and track the children separately.

## 3. Canonical lesson standard

A lesson should include the parts relevant to its record kind:

1. **The question:** what problem is being solved and why it matters.
2. **Inputs and outputs:** data model, units, coordinate reference, spatial and temporal scope.
3. **Core idea:** intuitive explanation and a worked example.
4. **Mathematics:** rendered notation, defined symbols, derivation or model definition where appropriate.
5. **Algorithm or workflow:** clear steps, pseudocode or process diagram.
6. **Correctness and limits:** assumptions, guarantees, edge cases, failure modes and what the method does not do.
7. **Complexity and trade-offs:** time, memory, accuracy, scale and alternatives where meaningful.
8. **Practical use:** when to choose it, when not to, and how it relates to adjacent methods.
9. **Evidence:** primary references, official documentation, versioned sources and attribution.
10. **Learning activities:** prediction, tracing, experiments, exercises and further questions where useful.

Not every method needs a long chapter. It does need enough substance for a reader to understand what the method does, how to use it responsibly and how to investigate it further.

## 4. Implementation standard

Every implementation must state which of these it is:

- **Teaching implementation:** transparent, deliberately bounded and designed to expose the algorithm.
- **Reference reproduction:** a documented reproduction of a published method or benchmark.
- **Library integration:** a reproducible wrapper around a maintained specialist implementation.
- **Production-oriented implementation:** designed and tested for operational constraints, with performance and failure behaviour documented.

Do not call a teaching baseline production-ready. Do not claim an algorithm is implemented merely because a package with a similar name is imported.

Where code is appropriate, include:
- explicit input, output, units, coordinate and numerical contracts;
- validation and useful errors;
- deterministic behaviour or documented randomness;
- tests for ordinary, boundary, degenerate, invalid and adversarial cases as relevant;
- differential/property tests or comparison with an authoritative implementation where possible;
- complexity and performance notes;
- dependencies and reproducible setup;
- a step-by-step walkthrough.

For wrappers, state exactly what is delegated to the dependency and what this repository contributes. For a software product or standard, a reproducible integration can be the correct deliverable; a from-scratch clone is not required.

## 5. Notebook standard

A notebook is appropriate when it materially improves understanding, comparison, visual inspection or reproducibility. It should:
- run from a clean environment using documented dependencies;
- use small, reproducible or clearly licensed data;
- explain the experiment and expected observation;
- expose meaningful parameters and intermediate results;
- include interpretation, not just code output;
- avoid relying on hidden local files, manual state or network access unless explicitly documented.

A notebook does not replace the canonical explanation or automated tests. Not every source entry needs a separate notebook: related methods can share a lab if each remains traceable.

## 6. Diagrams, data and reuse

Prefer a clear original diagram or a permitted, accurately attributed source figure when it improves the lesson. Record the exact source, creator, licence, modifications and access date. A citation is not permission to reproduce. Check the rights of code, figures, text, datasets, model weights and notebook assets separately.

Use synthetic data when it makes an experiment reproducible and avoids implying that illustrative data are observations. For real datasets, document provenance, licence, spatial/temporal coverage, resolution and known limitations.

## 7. Independent review dimensions

Track these separately; do not collapse them into one generic completion badge:

- **Identity:** the name refers to the intended method, model, software or standard.
- **Bibliography:** primary or authoritative references and version details are correct.
- **Technical claims:** equations, assumptions, guarantees, complexity and limitations are checked.
- **Implementation/reproduction:** code or integration matches the stated contract and is reproducible.
- **Tests/validation:** meaningful edge cases and comparison evidence exist.
- **Rights:** every reused artefact has a documented basis for use.
- **Learning/publishing:** explanation, notebook, exercises, accessibility and navigation are fit for the intended edition.

A source row is complete only when its child records have the applicable dimensions reviewed. A research-only record can be complete without original code if the record kind does not call for it and the reason is explicit. An implementation is not a substitute for bibliography, technical review or rights review.

## 8. Release gates before Patreon

The compendium is ready to move into the publishing/membership phase only when:

- all 47 source pages and 22 original sections remain preserved and accounted for;
- every source entry has been triaged, ambiguities and grouped families split, and cross-links resolved;
- every in-scope child record has a canonical treatment and an explicit rationale for implementation, integration or research-only status;
- all promised implementations have tests, and all notebooks designated as executable have been run in CI;
- primary references, technical claims, dependencies and reuse rights have been reviewed;
- the coverage matrix, source dashboard, road map and README agree with the actual repository;
- full validation passes on the exact release commit;
- the public learning experience has been checked for navigation, rendering, accessibility and mobile use.

The first public edition can be curated from completed material before every research question is exhausted, but the project must distinguish that edition from completion of the full source compendium. Patreon planning must not redefine or reduce the underlying technical scope.

## 9. Current baseline

The repository preserves the 47-page source transcription and indexes all 22 sections. The source review dashboard, recounted from the 22 section indexes on 17 November 2026, contains **695 grouped source-entry rows: 221 partial, 474 intake-only and zero fully verified**. These are review-state counts, not a measure of implementation completion. A grouped row may contain multiple distinct methods; an implementation link does not complete identity, bibliography, technical-claim or rights review. The 695 rows are therefore a minimum source-entry workload, not a guaranteed count of all child records required.

At the recursive-tree audit snapshot on 17 November 2026, `main` contained 287 Python implementation packages, 777 Python files under the implementation tree, 379 Python test files, 180 notebooks, 327 algorithm Markdown files, 157 verification records and 153 walkthrough files. The roadmap audit found 282 of 356 checklist items checked and 74 open. These are inventory and task-list measurements only: they are not a project-completion percentage and do not establish that every test, notebook, method or source entry is complete.

At that same audit snapshot, `main` was at commit `3c23de925d89bc2c1c1659b12d7d0765a5a9da11`. Its GitHub Actions run [44025614505](https://github.com/geo-dev-hub/spatial-analysis/actions/runs/44025614505) contained 51 jobs, all queued when observed; **no passing CI result is claimed**. The workflow covers 48 isolated Python package shards, catalogue/link checks, notebook execution and Clipper2 C# checks. A queued workflow is not evidence that any of these checks passed.

Use the [coverage matrix](../catalog/coverage-matrix.md) for the section-level narrative, the [source-entry verification protocol](../catalog/verification-protocol.md) for independent evidence requirements, and the [repository roadmap](repository-roadmap.md) for the open work queue. Recount the actual tree and review records, inspect the exact-head workflow result, and complete the release gates before making a release or completion claim.

## Implementation reconciliation — random-hyperplane LSH

Section 1's approximate-search source row now links to a static multi-table random-hyperplane LSH implementation for cosine similarity. The package includes seeded projection generation, unique candidate collection, exact cosine reranking, input validation and tests; it is registered in the Python CI matrix. This covers only one LSH family. HNSW, IVF-PQ and ScaNN remain separate open systems, and no recall, latency or production-scale claim is made. The Section 1 source-entry status changes from 26 partial / 7 intake-only to 27 partial / 6 intake-only; the aggregate dashboard changes from 219 / 474 to 220 / 473, with 693 rows and zero fully verified. The repository inventory is now expected to include 284 Python implementation packages, 401 non-test Python source files, 370 Python test files and 318 algorithm lesson files (323 algorithm Markdown files including five README indexes); these are tree inventory counts, not evidence that all tests pass.

## Historical reconciliation — 17 November 2026 (06:33 UTC+3)

The live main inventory was recounted from the recursive Git tree: 321 algorithm lesson files, 83 method guides, 400 non-test Python source files, 369 Python test files, 283 Python implementation directories and 179 notebooks. The source-review dashboard currently reconciles to 693 grouped source-entry rows across 22 section indexes: 219 partial, 474 intake-only and zero fully verified. Section 7 now records 10 partial and 38 intake-only rows. Recent Section 7 additions include tested categorical landscape patch metrics (patch counts, mean patch area, largest-patch index, internal edge density and Shannon class diversity); the existing raster least-cost corridor method is now cross-linked to ecology connectivity; and the AIS gap/implied-speed screening baseline is cross-linked to maritime track analysis. These are bounded contributions to grouped entries, not full coverage of FRAGSTATS, Circuitscape/Omniscape, Conefor, SAR/AIS fusion or the other named research/software families.

The latest workflow run for this snapshot is [44011612911](https://github.com/geo-dev-hub/spatial-analysis/actions/runs/44011612911). It is queued, with no completed jobs observed. The new and modified tests therefore remain unverified by CI at this snapshot; do not describe the repository as fully tested or complete.


## Current reconciliation — 17 November 2026 (CI sharding and LSH)

The current recursive Git tree contains 324 algorithm Markdown files (319 lesson files and five README indexes), 83 method Markdown files (82 guides and one README), 401 non-test Python source files, 370 Python test files, 284 Python implementation directories and 179 notebooks. The source-review dashboard reconciles to 693 grouped source-entry rows across all 22 section indexes: 220 partial, 473 intake-only and zero fully verified. Section 1 is 27 partial and six intake-only; Section 7 remains 10 partial and 38 intake-only. The LSH implementation covers one bounded member of the Section 1 approximate-search row; HNSW, IVF-PQ and ScaNN remain open. Section 6 now also links a deterministic greedy VRPTW construction with stop schedules, waiting, service durations, capacity and depot-return checks; its verification record explicitly leaves exact and advanced VRPTW methods open.

A CI audit found that the former 258-entry GitHub Actions matrix exceeded GitHub's 256-job matrix limit, so its package-test job was not being expanded in the observed run. The workflow has now been restructured into 240 shard jobs, with a checked-in manifest enumerating all 284 implementation directories and a runner that creates a fresh virtual environment for each package before installing its dependencies and running pytest. This preserves per-package dependency isolation while staying within the workflow run limit: 240 package shards plus the links, notebook and Clipper2 jobs (243 jobs total). The coverage checker now compares the manifest against every Python implementation directory and the notebook executor manifest; a unit test checks that sharding partitions packages exactly once. The [GitHub Actions workflow history](https://github.com/geo-dev-hub/spatial-analysis/actions) shows the run state for each commit. The run triggered by this reconciliation was queued when it was written; no passing CI result is claimed. The repository is not complete: 473 grouped source-entry rows remain intake-only, all 693 still lack full verification, and tests/notebooks must pass on the current head before release claims.
