# Implementation walkthrough: deferred acceptance

This walkthrough follows stable_matching.py. Read it beside the algorithm
dossier.

## 1. Turn preferences into rank maps

An ordered preference list is easy to read but expensive to search repeatedly.
The implementation validates the participants and converts each list into a
rank dictionary. Rank zero means first choice; a smaller rank is better.

The validation also rejects duplicate choices and unknown participants.
Incomplete lists are intentional: a missing pair is unacceptable.

## 2. Track proposals, not repeated comparisons

Each resident has a next-choice index. A resident never proposes to the same
hospital twice. A FIFO queue stores residents who are currently unmatched and
still have a choice to try.

This gives a finite termination argument: the total number of proposals
cannot exceed the total number of resident-listed pairs.

## 3. Maintain tentative hospital rosters

Each hospital stores its current tentative roster. If it has spare capacity,
it holds an acceptable proposer. Otherwise, it compares the proposer with its
least-preferred incumbent and retains the better of the two.

The displaced incumbent becomes unmatched and returns to the queue if another
acceptable option remains.

## 4. Preserve the two-sided acceptability rule

A resident listing a hospital does not force the hospital to accept them.
The hospital must also list that resident. If it does not, the proposal is
rejected and the resident continues down their own list.

## 5. Audit stability independently

The blocking_pairs function reconstructs hospital rosters from a proposed
matching. For every resident, it checks hospitals ranked above their current
assignment. A pair blocks if the hospital has a vacancy or would prefer that
resident to one of its incumbents.

The audit is useful for checking outputs from other algorithms, not only the
matching returned by this package.

## 6. Tests

Tests cover a hand-worked market, many-to-one capacity, incomplete
preferences, zero-capacity institutions, exhausted proposal lists, malformed
input and an intentionally unstable matching. The blocking-pair tests are
separate from the proposal loop, reducing the risk that the algorithm and its
audit share the same mistake.
