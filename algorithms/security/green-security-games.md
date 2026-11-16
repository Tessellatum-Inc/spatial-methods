# Green security-game patrol allocation

For site (i), let (v_i>0) be attacker value, (e_i\in(0,1]) detection effectiveness, and (x_i\in[0,1]) fractional patrol coverage. Under a resource budget (R), the defender solves

\[
\min_{x}\;\max_i v_i(1-e_ix_i)
\quad\text{subject to}\quad
\sum_i x_i\le R.
\]

At the minimax solution, partially covered sites have equal attacker payoff. The resulting water-filling relation is

\[
x_i(z)=\operatorname{clip}\left(\frac{1-z/v_i}{e_i},0,1\right),
\]

where bisection finds the payoff threshold (z) that uses the resource budget.

## Scope

This is a static fractional coverage game. It assumes independent site coverage and does not plan patrol routes, model travel constraints, infer attacker behaviour or learn from patrol histories. It is a mathematical baseline for understanding green security games, not a full anti-poaching operational system.

## Verification

Tests cover equal-value sites, heterogeneous values and equalized payoffs, imperfect detection under full coverage, zero resources and input validation.

See the [implementation package](../../implementations/python/green-security-games/README.md).
