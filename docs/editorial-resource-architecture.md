# Spatial Methods — Editorial and resource architecture

This document defines how Spatial Methods curates knowledge for learners, educators, researchers, developers and professionals.

## Organising principle

Organise the collection primarily by subject and method, then describe each resource's depth, audience relevance, prerequisites and format. Do not create isolated beginner, PhD and professional silos. A single method can serve all of these audiences through layered explanations and clearly labelled resources.

## Audience needs

| Audience | Typical need | Useful resource forms |
|---|---|---|
| Students and independent learners | Build understanding and capability | Foundations, learning paths, worked examples, exercises and solutions |
| Educators and instructors | Teach accurately and efficiently | Lesson plans, demonstrations, diagrams, exercises, assessment prompts and references |
| PhD candidates and postdocs | Investigate methods and identify research directions | Formal definitions, literature maps, variants, correctness, complexity, benchmarks and open questions |
| Researchers and research groups | Compare, reproduce and extend methods | Reproducible experiments, comparative studies, datasets, code, limitations and research briefs |
| Professionals and practitioners | Make sound method and implementation decisions | Selection guidance, case studies, tradeoffs, performance, failure modes and operational constraints |
| Developers and technical teams | Build reliable spatial systems | Specifications, APIs, reference implementations, tests, benchmarks and integration notes |

## Depth labels

Resources may carry multiple labels:

- **FOUNDATIONS:** concepts, intuition, terminology and visual explanation.
- **METHOD:** formal problem definition, mathematics and algorithmic reasoning.
- **IMPLEMENTATION:** code, tests, reproducibility, notebooks and practical usage.
- **ANALYSIS:** correctness, complexity, assumptions, precision, limitations and comparisons.
- **RESEARCH:** literature, variants, benchmarks, unresolved questions and research directions.
- **TEACHING:** instructional sequence, demonstrations, exercises, assessment and adaptation guidance.

Labels describe content dimensions, not the status or ability of the reader. State prerequisites explicitly.

## Canonical resource record

Every substantial method entry should capture, as applicable:

1. Title and stable identifier.
2. Subject and related methods.
3. Problem statement and motivation.
4. Definitions, notation and terminology.
5. Prerequisites and depth labels.
6. Conceptual and visual explanation.
7. Formal formulation and algorithm.
8. Correctness reasoning and complexity.
9. Implementation language, environment and tests.
10. Data assumptions, coordinate reference system and precision model.
11. Edge cases, limitations and failure modes.
12. Comparisons, alternatives and selection guidance.
13. Applications and case studies.
14. References, provenance and attribution.
15. Exercises, worked solutions and teaching guidance.
16. Licence, version, date and correction history.
17. Open questions and possible extensions.

Not every entry requires every field. Mark unavailable, out-of-scope or not-yet-investigated dimensions honestly.

## Publication surfaces

### GitHub
Canonical home for technical explanations, equations, code, tests, notebooks, reproducibility instructions, references and version history. Public archive remains independently useful.

### Patreon
Membership and editorial interface. Publish accessible introductions, context, learning outcomes, resource navigation, release notes, discussions, polls and event information. Avoid relying on Patreon to render complex mathematics, code or notebooks.

### Downloadable assets
Use typeset PDFs, diagrams, worksheets, answer keys, teaching packs and bundles when portability or printability adds value. State reuse rights on each asset.

### External publishing
Adapt selected insights into articles, newsletters, talks and social posts. Link back to canonical resources; avoid maintaining conflicting copies.

## Editorial workflow

1. Select a meaningful question or method.
2. Define scope, intended outcomes and audience needs.
3. Review primary and authoritative sources.
4. Work through the method independently.
5. Implement and test when code is relevant.
6. Identify assumptions, edge cases, alternatives and limitations.
7. Build appropriate depth layers and teaching/research extensions.
8. Review citations, licensing, technical correctness and reproducibility.
9. Publish the canonical resource and companion assets.
10. Create the Patreon editorial post and distribution adaptations.
11. Collect questions and corrections; update the canonical resource with a version history.

## Quality gates

- Technical claims are sourced or clearly identified as original reasoning.
- Code examples are run and tests pass before being described as tested.
- Mathematical notation is consistent and checked.
- Examples match stated assumptions.
- Coordinate systems, units and precision policies are stated when relevant.
- Complexity claims identify the relevant input size and assumptions.
- Teaching material distinguishes simplification from general truth.
- Research notes distinguish established consensus, contested claims and open questions.
- Licences and third-party attribution are respected.
- Scope and limitations are explicit.

## Initial subject map

This is a navigational starting point, not a fixed taxonomy.

- Computational geometry
- Spatial data structures and indexing
- Spatial graphs and networks
- Raster, grids and fields
- Spatial statistics and geostatistics
- Spatial databases and query processing
- Remote sensing and image analysis
- Spatial optimization and operations research
- Simulation, agent-based models and cellular systems
- Spatial machine learning and AI
- Cartography, visualization and visual analytics
- Spatial data quality, uncertainty and provenance

Methods may belong to multiple subjects. Maintain cross-links rather than forcing artificial exclusivity.

## Creator development loop

The creator uses each release as a structured mastery cycle: research, derive, implement, test, compare, explain, teach and revisit. The public resource is the durable output; the creator's developing skill is a parallel benefit, not a substitute for evidence, review or technical quality.
