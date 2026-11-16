# Stable matching: Gale–Shapley deferred acceptance

## The problem

Suppose applicants rank hospitals, schools or placements, while each
institution ranks applicants and has a fixed number of places. A matching is
stable when there is no mutually acceptable applicant–institution pair that
would rather be matched to one another than keep their current outcome.

Such a pair is called a **blocking pair**. Stability is stronger than merely
filling every available place: it rules out a participant pair with a justified
incentive to deviate.

## Model

Let R be residents and H hospitals. Each resident r has a strict preference
ordering over an acceptable subset of H; each hospital h has a strict ordering
over an acceptable subset of R and capacity q_h >= 0. A matching assigns each
resident to at most one hospital and no hospital more than q_h residents.

A pair (r, h) blocks a matching when the resident prefers h to their current
assignment and the hospital has a vacancy or prefers r to at least one current
resident. Only mutually acceptable pairs can block. An omitted pair is
unacceptable, not an implicit last-place choice.

## Deferred acceptance

1. Every resident begins unmatched.
2. An unmatched resident with an untried option proposes to their most
   preferred hospital not yet approached.
3. The hospital tentatively holds its best acceptable applicants up to
   capacity and rejects the rest.
4. A rejected resident becomes free and may propose to their next choice.
5. Stop when no free resident has an untried acceptable option.

Tentative acceptance is not final until the process ends. A hospital may
replace a less-preferred incumbent with a more-preferred applicant.

## Guarantees and complexity

With finite strict preferences and responsive hospital preferences, the
algorithm terminates after at most P = sum_r |P(r)| proposals, because no
resident proposes to the same hospital twice. The straightforward implementation
scans a hospital's held set when full, so its worst-case replacement work is
O(P * |R|). A priority-queue implementation can reduce that overhead.

The resident-proposing outcome is resident-optimal among stable matchings for
this model; it is not generally hospital-optimal. A stable matching exists
for the standard finite strict-preference model. Ties, couples, complementary
contracts and strategic preference elicitation require different models and
may change existence or guarantees.

## Worked example

Residents rank hospitals as follows:

| Resident | Preferences |
|---|---|
| A | X, Y, Z |
| B | Y, X, Z |
| C | Y, Z, X |

Hospitals rank residents as follows:

| Hospital | Preferences |
|---|---|
| X | B, A, C |
| Y | A, B, C |
| Z | A, B, C |

The resident-proposing process produces A–X, B–Y and C–Z. No resident and
hospital form a blocking pair.

## Implementation and verification

The [Python implementation](../../implementations/python/stable-matching/README.md)
includes strict-preference validation, incomplete lists, capacities and a
separate blocking-pair audit. Tests cover the hand-worked example, capacity
constraints, unacceptable pairs, zero-capacity institutions, exhausted lists,
malformed inputs and unstable-assignment detection.

## References

- Gale, D. & Shapley, L. S. (1962). College Admissions and the Stability of
  Marriage. The American Mathematical Monthly, 69(1), 9–15.
  https://doi.org/10.2307/2312726
- Roth, A. E. (1984). The Evolution of the Labor Market for Medical Interns and
  Residents: A Case Study in Game Theory. Journal of Political Economy,
  92(6), 991–1016. https://doi.org/10.1086/261272
