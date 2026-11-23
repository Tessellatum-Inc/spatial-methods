# C-logit route choice

This dependency-free implementation calculates the length-based commonality
factor for each route and applies it as a penalty to deterministic utility:

```
CF_k = log(sum_j (L_kj / sqrt(L_k * L_j)) ** gamma)
U_k  = V_k - beta_cf * CF_k
P_k  = exp(U_k) / sum_j exp(U_j)
```

The sum includes the route itself, so a choice set containing one route has
a zero commonality factor. Shared length is calculated from common segment
identifiers and caller-supplied positive segment lengths.

## Use

```python
from c_logit_route_choice import c_logit_route_choice

routes = [["A", "B", "C"], ["A", "D"], ["E", "F"]]
lengths = {"A": 1, "B": 1, "C": 1, "D": 2, "E": 1, "F": 1}
result = c_logit_route_choice(routes, lengths, utilities=[-4.2, -3.8, -5.0])
```

## Limits

This implements the first length-based commonality-factor specification
only. It assumes unique segment IDs per route and positive, additive segment
lengths. It does not estimate parameters, generate choice sets, implement
the other published commonality-factor definitions, account for time or
cost-specific overlap, or solve stochastic user equilibrium. The route
choice set is assumed to contain feasible alternatives supplied by the
caller.
