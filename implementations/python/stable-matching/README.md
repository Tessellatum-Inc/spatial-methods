# Stable matching — resident-proposing deferred acceptance

This package implements the Gale–Shapley deferred-acceptance algorithm for a
many-to-one market (residents and capacity-constrained hospitals). It also
provides a separate blocking-pair audit so callers can check whether a
candidate assignment is stable under the supplied preferences.

## Contract

- Preferences are strict ordered sequences; earlier entries are preferred.
- A pair is acceptable only if both participants list one another.
- Omitted hospital capacities default to one. Explicit capacities are
  non-negative integers.
- Each resident proposes at most once to each listed hospital.
- Hospitals retain their most-preferred acceptable applicants up to capacity.
- The result maps every resident to a hospital or to None.

The algorithm returns the resident-optimal stable matching for this model.
It does not support ties, couples, complementarities, contracts with multiple
attributes, strategic preference elicitation or dynamic matching markets.
The implementation is intended for teaching and audit workloads, not a
replacement for specialist matching-market software.

## Run

    python -m pytest -q

Runtime code uses only the Python standard library; pytest is the test runner.
