# C-logit route choice

C-logit modifies multinomial logit utility to account for overlap among
routes. For route k and route j, let L_k and L_j be their total lengths and
L_kj the length shared by the two routes. One commonality-factor
specification is

```
CF_k = log(sum_j (L_kj / sqrt(L_k * L_j)) ** gamma)
U_k = V_k - beta_CF * CF_k
P_k = exp(U_k) / sum_j exp(U_j)
```

The sum includes j=k, ensuring each route contributes its own normalized
overlap term. The implementation calculates shared length from common
segment identifiers, applies the commonality penalty, and evaluates the
softmax stably.

## Scope

Only the length-based commonality-factor specification is implemented.
The model does not estimate beta_CF or gamma, generate route choice sets,
implement the other published commonality-factor definitions, or model
stochastic user equilibrium. Route feasibility and utility construction
are external responsibilities.

## Reference

Cascetta, E., Nuzzolo, A., Russo, F., & Vitetta, A. (1996). A modified logit
route choice model overcoming path overlapping problems: specification and
some calibration results for interurban networks. In *Transportation and
Traffic Theory: Proceedings of the 13th International Symposium on
Transportation and Traffic Theory*, 697–711.
