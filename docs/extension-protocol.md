# Extension protocol: how the compendium grows

This repository is intended to keep growing after its initial completion. New work should extend the existing knowledge base without changing the meaning of the original 22-section intake or weakening its evidence standards.

## 1. Preserve the original source layer

The original 47-page compendium and its 22 section indexes are a historical intake layer. Do not silently rewrite source wording, merge distinct entries or renumber historical records.

When a new method comes from the original source:
- retain its exact source wording, original section and page;
- link it to one or more normalised child records;
- preserve parent/child and variant relationships;
- update the relevant section index and review dashboard only after evidence has been checked.

When a method is discovered later, add it as a **supplemental source entry**. Do not pretend it was in the original 47 pages. Record its source URL/DOI, date added, discovery context and the reason it belongs in the collection.

## 2. Stable identifiers

Use stable, readable slugs for canonical records: lowercase kebab-case, one concept per record. Do not encode a mutable section number in the ID.

For supplemental source entries, use `SUP-<topic>-<slug>` (for example, `SUP-ROUTING-time-dependent-shortest-paths`). IDs are permanent; if a title changes, keep the ID and record the old name as an alias.

For implementation packages, use a slug that names the method or bounded scope. Avoid vague names such as `misc`, `new-method` or `algorithm-2`.

## 3. Classify before implementing

Choose the primary record type using [record-types.md](../catalog/record-types.md): algorithm, operation, model, statistic, metric, data structure, software/system, standard, workflow, application or research family.

Do not force a standard, index, platform or workflow into a from-scratch algorithm implementation. For a named software system, a versioned integration may be the correct deliverable. For an uncertain method name, research identity before writing code.

## 4. Minimum canonical record

A new canonical lesson should state, as applicable:

- problem and use case;
- canonical name, aliases and variants;
- inputs, outputs, units, CRS and temporal/spatial scope;
- intuitive explanation and worked example;
- equations, defined symbols and derivation;
- algorithm steps or workflow;
- assumptions, correctness/guarantees and limitations;
- complexity, accuracy, memory and trade-offs;
- failure and edge cases;
- alternatives and related methods;
- primary references and versioned software sources;
- rights/attribution for every reused asset;
- links to implementations, tests, notebooks and exercises.

Short records are acceptable when the scope is genuinely small. Unsupported claims are not.

## 5. Implementation levels

Label every implementation as one of:

1. **Teaching baseline** — transparent, bounded and designed to explain the method.
2. **Reference reproduction** — attempts to reproduce a specified paper, algorithm or benchmark.
3. **Library integration** — wraps a maintained external implementation; state what is delegated.
4. **Production-oriented** — addresses operational scale, performance, errors, security and maintenance with evidence.

Never infer a higher level from a passing unit test. A package may contain more than one implementation level, but each implementation must state its own scope.

## 6. Tests and reproducibility

Use deterministic fixtures where possible. Include normal, boundary, degenerate, invalid and adversarial cases appropriate to the method. Prefer analytical or hand-checkable fixtures, differential tests against an independent oracle, property/invariant tests, and seeded stochastic tests.

Document:
- Python/runtime and dependency versions;
- installation and run commands;
- random seeds and tolerances;
- CRS, units and geometry validity assumptions;
- data provenance and licence;
- known unsupported cases.

Benchmarks must state hardware/software, data size, warm-up, repetitions, metric and baseline. Do not generalise beyond the tested workload.

## 7. Notebook and exercise rules

Add a notebook when it improves visual understanding, parameter exploration, reproducibility or method comparison. It must run top-to-bottom from a clean environment. Not every algorithm needs a notebook.

Exercises should test understanding or application rather than merely repeat code. Worked solutions may be a companion learning asset, but essential correctness information and public API behaviour must remain in the public repository.

## 8. Update order for a new addition

1. Open or update an issue describing the method and its source.
2. Add the source record and verify identity/bibliography.
3. Create the canonical lesson and technical evidence.
4. Add implementation, tests and walkthrough if appropriate.
5. Add notebook/exercise only where useful.
6. Add or update cross-links, topic indexes and learning paths.
7. Update the supplemental source index and coverage matrix.
8. Run link, catalogue, CI-coverage, package and notebook checks.
9. Record exact commit and validation evidence in the change log.

Do not mark a source row fully verified just because a lesson or package exists. Follow the [verification protocol](../catalog/verification-protocol.md).

## 9. Avoiding duplicate and drifting content

Before creating a new page, search canonical records, aliases and variants. If two pages overlap, document the relationship and choose a canonical home only after comparing scope and evidence. Do not delete the original intake label.

The canonical lesson is the source of truth for technical content. Learning paths, notebooks, Patreon companion notes and newsletters should link to it rather than maintaining competing definitions. When the canonical record changes, update affected derivatives.

## 10. Release and maintenance

A new addition is complete when its claims match its evidence, its stated implementation level is honest, its tests and reproducibility steps pass, its rights are clear, and its navigation is connected.

The repository is never "finished" in the sense of no future additions. Completion means the foundation, conventions, tests, source traceability and maintenance process are stable enough that new work can be added without structural redesign.
