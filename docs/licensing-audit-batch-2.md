# Licensing and release-risk audit — Batch 2

**Date:** 18 November 2026  
**Scope:** Policy documents and top-level licensing records reviewed on the completion branch. This is a document-level consistency audit, not a full asset-by-asset copyright review or legal opinion.

## Review result

The selected split-license policy is internally consistent at the high level: code and executable examples are Apache-2.0, original learning prose is CC BY 4.0, and third-party material is excluded unless a specific reuse basis is documented. The provenance record correctly distinguishes the owner's compilation/authorship claim from rights in embedded third-party material.

The policy should not be treated as operationally complete until every asset and mixed-content file has an explicit scope and reuse record.

## Findings

| ID | Risk | Finding | Recommended closure |
|---|---|---|---|
| LIC-01 | High | The 47-page source transcription is excluded from blanket licensing, but remains part of the public repository. Exclusion notices and page-level review are critical to avoid implying permission to redistribute incorporated material. | Maintain page/asset provenance; remove, replace or link-only any content without a reuse basis. |
| LIC-02 | High | A lesson/notebook may contain both original explanatory text, executable code, and third-party figures or excerpts. A single repository-level licence may be ambiguous for mixed files. | Add front matter or adjacent file notices for mixed content; identify code blocks and third-party assets separately. |
| LIC-03 | Medium | Project-level licence files are present, but individual files may not visibly carry SPDX identifiers or scope notices. Downstream users can misinterpret the licence when files are copied without the root context. | Add file-level SPDX metadata where practical (SPDX-License-Identifier: Apache-2.0 for original code; CC-BY-4.0 for original prose), and explicit exception/third-party notices where mixed. |
| LIC-04 | Medium | DCO sign-off is intended to apply prospectively. Historical completion commits are not retroactively certified, and PR #3 is explicitly exempt from retroactive sign-off. | Keep the exemption transparent; require signed-off commits on new contributions and maintain the DCO check. |
| LIC-05 | Medium | Visual-source register entries indicate licence and rights-check dates, but a repository-wide asset inventory may not be complete. | Generate an asset inventory and cross-check every image, SVG, notebook embedded asset, dataset and copied code fragment against a source record. |
| LIC-06 | Medium | The public GitHub archive and paid Patreon model is correctly distinguished in policy, but paid material may still incorporate external assets. | Use the same rights gate for free and paid derivatives; do not assume paid status changes permission scope. |
| LIC-07 | Low | The project policy is not legal advice and may need professional review before institutional/commercial distribution. | Obtain qualified review for high-risk third-party content, substantial redistribution or unclear ownership. |

## Recommended mechanical controls

1. A reusable file-header template for original code and documentation.
2. A third-party asset register with required fields: file path, asset type, source, creator, exact licence/version, attribution text, modification, access date and reviewer.
3. A check that image and notebook-asset paths resolve to an asset register entry or are explicitly marked project-created.
4. A check that new contribution commits satisfy DCO policy, while clearly documenting the historical exemption.
5. A mixed-file policy for notebooks and tutorials: code licence, narrative licence, and third-party content are scoped separately.
6. A release checklist that blocks publication if rights are unknown for any copied figure, excerpt, dataset or code.

## Limits of this audit

- No exhaustive asset tree scan was performed in this document.
- No external rights-holder or legal consultation was performed.
- The source compendium was not reviewed page by page for third-party inclusions.
- This audit does not certify that all files comply with the selected licences.

## Next rights batch

Prioritize: (1) all embedded figures and SVGs, (2) notebooks with image or dataset assets, (3) copied or adapted code samples, (4) substantial excerpts in the preserved source inventory, and (5) files with ambiguous or absent scope notices.

Rights status should remain not_checked or in_progress until the individual asset's evidence is recorded.
