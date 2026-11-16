# Two-market food price transmission

A long-run price relation between source and target markets is estimated as

\[
p^T_t=c+\beta p^S_t+e_t.
\]

The short-run error-correction model is

\[
\Delta p^T_t=a+\lambda e_{t-1}
+\gamma\Delta p^S_t+\varepsilon_t.
\]

A negative adjustment coefficient \(\lambda\) indicates that the target-market price change tends to correct the previous period's disequilibrium. The source-price effect \(\gamma\) describes contemporaneous short-run transmission in this specification.

## Scope and cautions

The implementation is a two-stage OLS teaching baseline. It does not run a formal Engle–Granger residual unit-root test, select lag order, model asymmetric adjustment, structural breaks, transport costs or multi-market equilibrium. Price series should be made comparable in currency, units and frequency, and deflated where necessary. A fitted long-run relation alone is not proof of market integration.

## Verification

Seeded synthetic cointegrated price pairs test recovery of long-run elasticity, short-run transmission and negative adjustment speed. Validation tests cover insufficient, constant and non-finite series.

See the [implementation package](../../implementations/python/food-price-transmission/README.md).
