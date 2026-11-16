# Exercise: build and audit a stable matching

## Scenario

Three applicants are applying to two training hospitals. Each hospital has
one place.

| Applicant | Preference order |
|---|---|
| A | North, South |
| B | South, North |
| C | North, South |

| Hospital | Preference order |
|---|---|
| North | B, A, C |
| South | A, C, B |

## Tasks

1. Run resident-proposing deferred acceptance by hand. Record every proposal,
   tentative hold and rejection.
2. Write the final matching and check whether every applicant is assigned.
3. List all mutually acceptable pairs. For each applicant, inspect only
   hospitals they prefer to their assigned outcome. Does any such hospital
   have a vacancy or prefer them to an incumbent?
4. Change North's capacity to two. Re-run the algorithm and explain which
   applicant is displaced from the original outcome.
5. Remove C from South's preference list. Explain why C's proposal to South
   cannot result in an assignment even if South has a vacancy.

## Reflection

- Why does the resident-proposing side matter?
- What changes if preferences contain ties?
- Which real-world matching settings would violate the model's assumptions?
- Why is stability not the same as maximizing a sum of preference scores?
