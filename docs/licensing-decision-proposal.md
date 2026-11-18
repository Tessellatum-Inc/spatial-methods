# Licensing decision record

**Decision date:** 18 November 2026  
**Decision owner:** Project owner  
**Status:** Selected; applied to original project material through the repository licence files.

## Decision

1. Original software code, tests, scripts and executable examples: **Apache License 2.0**.
2. Original explanatory prose, tutorials, exercises, narrative notebook content and project-created diagrams: **Creative Commons Attribution 4.0 International (CC BY 4.0)**.
3. Future contributions: **Developer Certificate of Origin 1.1**, using per-commit `Signed-off-by` sign-off.
4. Third-party material: retain its own licence and attribution; exclude it from project-wide licences unless a compatible reuse basis is documented.
5. Supplied 47-page compendium transcription: retain as source intake, outside the blanket licence until a page-level review identifies and resolves any incorporated third-party content.

## Rationale

Apache-2.0 makes the implementations practical to reuse in research, education and commercial products while providing an express patent grant. CC BY 4.0 makes the original learning archive genuinely reusable with attribution. DCO records contribution provenance without requiring copyright assignment.

This supports the intended model: the GitHub repository remains a complete, public and reusable archive; Patreon sells additional teaching, structure, curation, support and community—not exclusive access to material already openly licensed.

## Operational implementation

- Root `LICENSE`: Apache-2.0.
- Root `LICENSE-DOCUMENTATION`: CC BY 4.0.
- Root `LICENSES.md`: scope and exclusions.
- Root `DCO`: unmodified DCO 1.1 text.
- `CONTRIBUTING.md` and the pull-request template: require sign-off on future contribution commits.
- Source and visual registers: retain per-asset rights records.

The DCO process applies prospectively to new contributions. It does not retroactively certify historical commits.

## Review triggers

Revisit this decision only if the project changes ownership, accepts a contribution under incompatible terms, begins distributing a separately licensed product, or needs a different contribution arrangement. Do not change licences casually after public release: both Apache-2.0 and CC BY 4.0 grants are irrevocable for recipients who comply with their terms.
