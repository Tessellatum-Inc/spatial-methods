# Learning-unit template

Use this template to develop a coherent body of learning material around a spatial concept, method, technology, measurement practice or applied problem.

The template is modular. **Do not create every component by default.** Select the components that genuinely improve understanding, reproducibility or practice. A short foundational concept may need only a theory page; a computational method may need theory and implementation; a field method may need collection and application material; a substantial teaching unit may use all four.

## The four components

| Component | Main question | Typical home |
|---|---|---|
| Theory | What is it, why does it work, and under what assumptions? | Relevant pillar directory, often `foundations/` or `algorithms/` |
| Implementation | How can it be computed or reproduced? | `implementations/<language>/<topic>/` |
| Application | How does it behave in a real operational or scientific context? | Relevant application, workflow or experiment directory |
| Assessment | Can a learner explain, use, test and critique it independently? | Beside the lesson or implementation it assesses |

These are connected views of one subject, not four copies of the same explanation. Give each component a clear purpose and link to the others.

## Start here

1. **Define the subject.** Identify the question, intended audience, scope and stable subject IDs from the [master subject index](../../catalog/master-subject-index.md).
2. **Choose the pillar or pillars.** Spatial Algorithms, Spatial Recipes, Spatial Data Collection and Theoretical Foundations are complementary lenses. Do not force a subject into only one.
3. **Map what already exists.** Search the repository before creating new canonical material. Extend or connect existing work where possible.
4. **Choose components.** Use the templates in this directory selectively.
5. **Build from evidence.** Distinguish established theory, documented software behaviour, reasoned interpretation, synthetic demonstration and field evidence.
6. **Connect the unit.** Link prerequisites, related methods, data, implementations, applications, learning paths and sources.
7. **Review before promotion.** Check technical accuracy, reproducibility, licensing, accessibility, rendered presentation and stated limitations.

## Suggested unit structure

A compact unit may use this layout:

```text
<canonical-topic>/
├── README.md                 # learner entry point and navigation
├── theory.md                 # optional: theory and method explanation
├── implementation/           # optional: runnable code and tests
├── application.md             # optional: operational or scientific context
└── assessment.md              # optional: exercises and marking guidance
```

Adapt the layout to existing repository conventions. Do not create empty placeholder files just to match this diagram.

## Quality gates

Before describing a unit as complete, confirm the relevant items:

- [ ] The reader's question and learning outcomes are explicit.
- [ ] Terms, notation, units, inputs and outputs are defined.
- [ ] Assumptions and scope are visible where they affect interpretation.
- [ ] Claims are supported by traceable sources or clearly labelled as interpretation.
- [ ] Examples are reproducible and their data provenance is stated.
- [ ] Code has meaningful tests or another explicit verification method.
- [ ] Synthetic examples are never presented as field evidence.
- [ ] Real-world application identifies operational constraints and validation needs.
- [ ] Known failure modes, uncertainty and limitations are discussed.
- [ ] Related repository material is linked rather than duplicated.
- [ ] Licences, attribution and reuse permissions are checked.
- [ ] The rendered pages and any notebooks are checked for accessibility and usability.

Not every unit needs code, a dataset, a field exercise or a formal assessment. Explain why a component is absent when a reader might reasonably expect it.

## Evidence and status language

Use precise status language. A working example is not automatically validated; passing tests do not establish suitability for field use; a plausible application scenario is not an implemented operational system.

Keep these distinctions explicit:

- **Synthetic demonstration:** generated or constructed data used to explain behaviour.
- **Reproducible experiment:** a documented procedure and data that another person can rerun.
- **External evidence:** published research, official specifications, authoritative documentation or documented field observations.
- **Field evidence:** observations collected under a stated real-world protocol, with provenance and quality controls.
- **Validated for a use:** tested against appropriate independent evidence and acceptance criteria for that specific use.

## Worked example in this repository

The [matrix-factorization unit](../../implementations/python/matrix-factorizations/README.md) demonstrates how a topic can connect foundational explanations, runnable examples, an integrated synthetic spatial case and a learner exercise. It is a useful structural example, not a mandatory format for every topic.

## Relationship to existing standards

This template complements rather than replaces the [learning experience standard](../../docs/learning-experience-standard.md), [compendium completion standard](../../docs/compendium-completion-standard.md), [source provenance rules](../../docs/compendium-provenance.md), catalogue conventions and subject-specific technical standards. Where requirements differ, follow the more specific technical, licensing or repository standard.
