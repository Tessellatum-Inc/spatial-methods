# Canonical knowledge records

This directory documents the metadata contract and operating rules for the canonical knowledge-record catalogue. The first records are maintained in the machine-readable [knowledge-records.jsonl](../knowledge-records.jsonl) file and validated against the [JSON Schema](../schemas/knowledge-record.schema.json).

## Identity

Canonical knowledge record IDs use the form `SM-KB-NNNNNN`. IDs identify the knowledge object, not its file path. Once assigned, an ID must not be recycled or changed merely because a title, path, subject mapping or taxonomy placement changes.

Subject IDs such as `SM-FND-011` identify subject territories; record IDs identify individual canonical resources. Do not substitute one for the other.

## Catalogue rules

- One JSON object per line; UTF-8; no enclosing JSON array.
- The schema validates metadata shape and controlled values, not technical correctness.
- Every canonical path must resolve to a repository file.
- Every subject ID must exist in the master subject index.
- Every relationship target must resolve to a subject ID or canonical record ID; external targets require a stable resolvable identifier and explicit source handling.
- Keep summaries concise, specific and limitation-aware.
- Status reflects the evidence actually present; implementation does not imply testing or validation.
- Do not duplicate the full article in the catalogue.
- Add records when a resource has a meaningful canonical identity and retrieval value; do not catalogue every file indiscriminately.

## Evidence and review

`evidence_refs` currently points to repository paths that support the mapping or contextual interpretation. It is not a substitute for claim-level citations inside the canonical resource. External bibliographic provenance should be added in a dedicated source model rather than squeezed into a path field.

The first eleven records are a pilot metadata slice for the reference, positioning and measurement cluster. Their subject assignments and summaries are editorial mappings and should be reviewed as the linked content receives deeper technical review.

## Change process

1. Inspect the canonical resource.
2. Confirm its primary record kind using [record types](../record-types.md).
3. Confirm subject mappings against the master index and subject alignment register.
4. Assign the next unused record ID.
5. Add concise metadata and only evidence-supported relationships.
6. Validate schema, file paths, subject IDs and relationship targets.
7. Update this catalogue and relevant navigation in the same change.
