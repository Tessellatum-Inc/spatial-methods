# Source review dashboard

Snapshot: 17 November 2026. Counts below are recalculated from the current 22 item-level section indexes.

This dashboard tracks source-entry review state, not technical completion. An implementation-linked row is still partial until the complete grouped source entry has been independently reviewed.

## Current position

| Measure | Entries | Meaning |
|---|---:|---|
| Source-entry rows counted | 695 | Rows with a source-entry review status in the 22 section indexes |
| Partial | 183 | At least one related method has an implementation or canonical record, but the grouped source entry remains incompletely reviewed |
| Not checked — intake only | 512 | Source wording is preserved, but no adequate independent review is recorded |
| Fully verified | 0 | No row has passed all independent verification dimensions |

## By section

| Section | Source entries | Partial | Intake only |
|---:|---:|---:|---:|
| 1 — Core GIS | 33 | 26 | 7 |
| 2 — Spatial statistics | 27 | 13 | 14 |
| 3 — Geostatistics | 26 | 6 | 20 |
| 4 — Raster, terrain and hydrology | 27 | 20 | 7 |
| 5 — Remote sensing | 36 | 15 | 21 |
| 6 — Optimization, mobility and transport | 31 | 4 | 27 |
| 7 — Domain modeling | 48 | 1 | 47 |
| 8 — GeoAI | 54 | 2 | 52 |
| 9 — Geodesy, cartography and infrastructure | 39 | 1 | 38 |
| 10 — Classical statistical and computational additions | 30 | 22 | 8 |
| 11 — GeoAI and computer-vision additions | 26 | 0 | 26 |
| 12 — Signal, GNSS and regional science | 28 | 14 | 14 |
| 13 — GeoFM workflows, urban mobility and LLMs | 29 | 0 | 29 |
| 14 — Databases, graphics, morphology and hazards | 33 | 1 | 32 |
| 15 — Vision, registration and vector extraction | 33 | 3 | 30 |
| 16 — Flows, regions, deformation and marine | 25 | 25 | 0 |
| 17 — Geometry, scalability, design and siting | 27 | 8 | 19 |
| 18 — Moving objects, routing, transit and water | 32 | 4 | 28 |
| 19 — African applications, addressing and finance | 32 | 1 | 31 |
| 20 — Indices, microwave, events and information | 25 | 8 | 17 |
| 21 — Neural fields, climate accounting and robust geometry | 26 | 3 | 23 |
| 22 — Inference, covariance, spherical methods and asset monitoring | 28 | 6 | 22 |
| **Total** | **695** | **183** | **512** |

The totals include implementation-linked custom status descriptions in Sections 2, 17 and 20 as partial, and Section 4's storage/compression row as intake-only. Counts exclude lesson inventories, implementation inventories, explanatory tables and software lists.

## Interpretation and completion standard

- **Partial is not verified.** A source row may group several distinct methods; implementing one member does not complete the row.
- **Intake only is not incorrect.** It means the source wording has been preserved but not independently checked.
- **Fully verified requires evidence across dimensions:** source identity and decomposition, authoritative bibliography, technical claims and equations, implementation or justified unsupported status, independent tests/reproduction, documentation/examples, and rights/provenance.
- **CI is a separate gate.** A package being present in the workflow matrix is not a test pass. The current full workflow is pending/queued; repository-wide CI success is not established.

## Required completion sequence

1. Split grouped source rows into child entries wherever their methods, citations, software or rights differ.
2. Verify each child's identity and bibliographic metadata against primary or authoritative records.
3. Check equations, assumptions, edge cases, guarantees and known limitations.
4. Implement the method or record a defensible unsupported/not-applicable disposition with evidence.
5. Add independent tests, examples, documentation and provenance/rights notes.
6. Run the relevant package tests, notebook execution, link checks and full CI; record exact results.
7. Change the row label only after the underlying evidence is present.

No source row is currently labelled fully verified. The remaining 512 intake-only rows and the 183 partial rows remain in scope; this dashboard must not be read as a completion claim.
