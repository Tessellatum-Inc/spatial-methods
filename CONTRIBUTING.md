# Help make spatial analysis easier to understand

You don't have to be an expert to make this collection better.

Maybe you spotted an error. Maybe you know a useful paper, found an edge case, built a small example or have a question that the explanation didn't answer. Those are all good reasons to get involved.

## You can help by…

- suggesting a method or topic we have missed;
- asking a question or pointing out something that isn't clear;
- sharing a paper, documentation page or other useful reference;
- correcting an explanation or adding an example;
- contributing code, tests, notebooks or visualisations;
- trying an exercise and telling us where you got stuck;
- sharing a dataset or benchmark result that others can reproduce;
- translating or improving learning materials.

Small contributions matter. A clear issue report can be just as useful as a large code change.

## Before you send a change

1. Check whether the topic or issue is already in the collection.
2. Tell us what you changed and why.
3. Include a primary or authoritative source for technical claims; check title, authors, venue, year and DOI/URL against that source.
4. If a source entry is uncertain or only partly checked, say so explicitly instead of marking it verified.
5. If you share code, include versions and reproducible run steps.
6. For spatial examples, state the coordinate reference system, units, spatial/temporal scope and important assumptions.
7. Only share data, code and images that you have permission to redistribute.
8. Distinguish original work from AI-assisted drafting, generated content and third-party source material; a human contributor remains responsible for checking the submitted work.

## Contribution workflow

Use the [extension protocol](docs/extension-protocol.md) when adding a new algorithm, variant, model, dataset or implementation. It explains stable IDs, source traceability, record types, expected deliverables and the update order for indexes and coverage.

For each new method:

- preserve the exact source label and provenance if it comes from the original compendium;
- if it is a new addition, record it as a supplemental source with its own reference and date;
- split grouped methods into separately reviewable child records;
- create or update the canonical lesson before linking it from indexes;
- include tests and a notebook only when they add meaningful evidence or learning value;
- state whether the deliverable is a teaching baseline, reproduction, library integration or production-oriented implementation;
- record rights separately from technical verification.

If you're unsure, open an issue and describe the idea before preparing a full change.

## Run the checks

From the repository root:

```bash
python scripts/check_internal_links.py
python scripts/check_catalogue_dashboard.py
python scripts/check_ci_coverage.py
```

For a Python package:

```bash
cd implementations/python/<package-name>
python -m pip install -r requirements.txt
python -m pytest -q
```

The GitHub Actions workflow currently covers 321 Python implementation packages in 48 isolated shards, executes all 180 learning notebooks, checks catalogue/dashboard consistency and internal links, and runs Clipper2 C# smoke checks. Counts change as packages and notebooks are added; the coverage checker should pass before a pull request is ready.

## Licensing and sign-off

Read [LICENSES.md](LICENSES.md) and [licensing and reuse](docs/licensing-and-reuse.md). Original code is Apache-2.0; original learning material is CC BY 4.0. Third-party assets retain their own terms.

Human-authored contribution commits must include a DCO sign-off. Configure your Git identity, then use:

```bash
git config user.name "Your Name"
git config user.email "you@example.com"
git commit -s -m "Describe your contribution"
```

The resulting commit message includes `Signed-off-by: Your Name <you@example.com>`. Sign off every commit in your contribution. Do not sign off on behalf of another person. The DCO is a provenance certification, not a copyright assignment.

### AI-assisted and agent-generated contributions

AI tools and autonomous coding agents may prepare changes, but they cannot truthfully provide a human DCO certification. Never add a human's sign-off to a commit they did not create or personally certify.

An AI-assisted pull request must:

1. Be clearly disclosed in its pull request description, identifying the tool or agent and summarising its role.
2. Preserve normal commit authorship and provenance; do not impersonate a human contributor or fabricate a DCO trailer.
3. Be reviewed by a human maintainer for correctness, security, licensing, source attribution, tests and scope.
4. Receive the repository's `agent-reviewed` label from a human maintainer only after that review is complete.

The `agent-reviewed` label is the maintainer's explicit attestation that the review above has occurred. For a pull request carrying that label, CI records the DCO check as not applicable to the agent-generated commits and requires the label to be present when the check runs. Applying the label triggers CI again. Without the label, the normal DCO check remains mandatory for every contribution commit.

This exception does not waive review, licensing, attribution, testing or legal responsibilities. Human-authored commits in mixed contributions must still carry their own DCO sign-offs.

## Help us keep it trustworthy

- Tell readers when a method is exact, approximate, heuristic or stochastic.
- Separate mathematical guarantees from software behaviour.
- Explain dependence on data, coordinate systems, precision and software versions.
- Do not present one benchmark as proof that a method is always faster.
- Never invent a source, result or test.
- A passing test suite does not verify a literature claim; a citation does not establish permission to reproduce an asset.

## Credit and reuse

Contributors retain copyright in their contributions. Substantial contributions will be credited in the relevant material or project notes. We may ask for corrections or decline material that cannot be independently checked or lawfully redistributed.

Thanks for helping make spatial analysis clearer, more useful and easier to explore.
