# Knowledge graph model

**Status:** Initial relationship vocabulary  
**Parent architecture:** [Complete knowledge base and AI-readiness architecture](../docs/knowledge-base-and-ai-readiness-architecture.md)

This document defines the first controlled vocabulary for expressing relationships between Spatial Methods knowledge objects. It supplements, and does not replace, the [master subject index](master-subject-index.md) or [record types](record-types.md).

## Design rules

1. Relationships connect identifiable objects; they are not decorative tags.
2. Use directional relationships with an unambiguous subject and target.
3. Prefer an existing relationship type over inventing near-duplicates.
4. Record only relationships supported by the content.
5. A relationship does not imply that either endpoint has been technically verified.
6. Preserve the distinction between subject IDs, canonical record IDs and external resource identities.
7. Keep canonical explanations in their existing repository locations. Indexes point to them; they do not duplicate them.

## Initial relationship vocabulary

| Relationship | Directional meaning | Example |
|---|---|---|
| explains | Source explains target | A foundation record explains a method |
| depends_on | Source requires or assumes target | An algorithm depends on a data structure |
| implements | Source provides a concrete realisation of target | A software library implements an operation |
| uses | Source employs target as an input or component | A recipe uses a dataset |
| collects_with | Source describes acquisition using target | A survey workflow collects observations with GNSS |
| applies_to | Source is relevant to target context | A method applies to a monitoring problem |
| alternative_to | Source is an alternative to target | Two estimation methods solve a related task |
| validates | Source provides a check for target | An independent check validates a dataset |
| benchmarked_by | Source has performance assessed by target | An implementation is benchmarked by a test suite |
| derived_from | Source was derived or adapted from target | A worked example is derived from a published method |
| cites | Source explicitly cites target | A technical record cites a standard |
| part_of | Source belongs to target | A submethod is part of a workflow |
| supersedes | Source replaces an earlier target | A revised record supersedes an older record |

## Relationship record shape

When machine-readable relationships are introduced, each edge should minimally preserve:

- source_id: stable ID of the source object;
- relationship: one value from the controlled vocabulary;
- target_id: stable ID or resolvable external identifier of the target object;
- evidence: optional pointer to the section, source or decision supporting the relationship;
- note: optional short qualification where the relationship needs context.

Do not create a relationship edge if either endpoint cannot be identified reliably. A normal Markdown link can remain useful before both objects receive stable IDs.

## Example (illustrative only)

~~~json
{
  "source_id": "SM-REC-EXAMPLE",
  "relationship": "uses",
  "target_id": "SM-ALG-EXAMPLE",
  "evidence": "recipe section: processing steps",
  "note": "The recipe uses this algorithm for the stated processing stage."
}
~~~

The example IDs are placeholders, not assigned repository identifiers.

## Review checklist

Before accepting a relationship:
- Is the source object correctly identified?
- Is the target object correctly identified?
- Does the selected relationship express the actual direction and meaning?
- Is the relationship supported by the source content?
- Does the link resolve?
- Does the relationship need a short qualification?
- Would an ordinary link be more accurate than a semantic edge?

The vocabulary should evolve from real curation needs. Do not attempt to map the entire repository into a graph in one pass.
