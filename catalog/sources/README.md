# Source register and claim-evidence mapping

**Version:** 0.1  
**Status:** Active structured register; claim-level reviews completed for the VIM, legacy GUM core and NIST TN 1297 on 2026-11-20. Twenty-two source-to-claim links are now marked verified; other candidate links remain unverified.

## Purpose

This register gives external sources stable identifiers and separates bibliographic provenance from claims made in Spatial Methods resources. It complements, rather than replaces, the canonical knowledge-record catalogue.

- [Source register](source-register.jsonl): one JSON object per source.
- [Claim-evidence map](claim-evidence-map.csv): candidate links between specific claims and sources.
- [Source map](../surveying-field-measurement-source-map.md): broader discovery, authority hierarchy and subject coverage.
- [Knowledge records](../knowledge-records.jsonl): canonical Spatial Methods resources.

## Identifier policy

Source IDs use `SM-SRC-NNNNNN`. IDs are permanent and never recycled. A new edition, amendment or materially distinct version receives a new source ID and may be related to the prior record as a successor or amendment. Do not silently overwrite bibliographic identity when a standard or law changes.

## Minimum source metadata

Each record captures issuing body, title, identifier/edition, publication date where known, source class, jurisdiction, stable landing URL, access conditions, review state, relevance and cautions. Unknown values remain explicit rather than inferred.

## Evidence states

- `identified_not_inspected`: source discovered and bibliographic identity recorded; source content has not been checked for a particular claim.
- `metadata_checked`: issuer/title/edition/date checked against an authoritative catalogue or issuing body.
- `content_reviewed`: relevant passages or sections inspected and scope recorded.
- `claim_verified`: the cited passage directly supports the precisely worded claim.
- `superseded`, `withdrawn`, `historical`: lifecycle states; retain records for provenance.

The claim-evidence map distinguishes `candidate_support` from `verified_support`. Initial entries are candidate links only. A source being authoritative, relevant or listed in an existing source map does not itself verify a claim.

## Claim mapping rules

1. One row should express one independently reviewable proposition, not a whole paragraph or topic.
2. Identify the exact canonical resource and section/heading where the proposition appears.
3. Record the source ID, exact section/page/clause when known, and the relationship type.
4. Use `direct` only when the source directly addresses the proposition; use `contextual` for background or institutional context.
5. Record jurisdiction, edition and scope limits. A foreign national manual is not Kenyan law.
6. Do not claim support from a source's title, abstract, search snippet or catalogue listing alone.
7. Where sources disagree, preserve the disagreement and its context; do not flatten it into a single unqualified statement.
8. Record access date and reuse/licensing terms before republishing excerpts, figures, tables or substantial derived material.

## Copyright and reuse

A public URL does not imply permission to reproduce a document. Prefer original explanation, short properly attributed quotations where lawful, and links to the issuing source. Do not upload paywalled standards or reproduce substantial protected material. Record explicit licences and their scope; if terms are unclear, mark them as unknown and link rather than republish.

## Review workflow

1. Confirm source identity and current edition/status from the issuing body.
2. Inspect the full accessible source or the relevant licensed text.
3. Capture section/page/clause locators and relevant scope/limitations.
4. Draft a narrow, testable claim in the canonical resource.
5. Add or update its claim-evidence row and set the evidence state honestly.
6. Have technical content reviewed independently where consequences warrant it.
7. Re-run the catalogue validator and check that all source IDs resolve.

## Current boundary

The initial source set is deliberately small and concentrated on measurement science, field verification, GNSS practice, control surveying, levelling, reference frames and Kenyan regulatory context. The first technical review inspected the BIPM-hosted VIM3 and legacy GUM texts, and checked the BIPM's 2026 GUM suite overview and amendment listing. The GUM is a maintained suite, not merely JCGM 100:2008; source records for the suite and the 2026 nonlinearity amendment are retained separately. It is not a complete bibliography and does not establish the current legal or technical status of Kenya's national reference system. The existing source map records unresolved legal and KENREF questions; those must remain open until primary documents are inspected and reconciled.
