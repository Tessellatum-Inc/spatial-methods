# Spatial impact uncertainty: analytic delta method

Stable ID: `SA-STAT-SPATIAL-IMPACT-DELTA` · Spatial econometrics inference

## Purpose

SAR/SDM impact summaries are nonlinear functions of the spatial parameter and regression coefficients. This method propagates a fitted model's joint parameter covariance through those functions using a first-order Taylor approximation. It complements, rather than replaces, parametric Monte Carlo intervals.

For covariate (r), let

[
S_r(	heta)=(I-ho W)^{-1}(eta_r I+gamma_r W),qquad A=I-ho W.
]

The reported effects are (d_r=operatorname{tr}(S_r)/n), (t_r=mathbf{1}'S_rmathbf{1}/n), and (q_r=t_r-d_r).

## Analytic Jacobian

The matrix differential identity (d(A^{-1})=-A^{-1}(dA)A^{-1}), with (dA/dho=-W), gives

[
rac{partial S_r}{partial ho}=A^{-1}WS_r,quad
rac{partial S_r}{partial eta_r}=A^{-1},quad
rac{partial S_r}{partial gamma_r}=A^{-1}W.
]

For any matrix derivative (D), the direct-effect derivative is (operatorname{tr}(D)/n) and the total-effect derivative is (sum_{ij}D_{ij}/n). The indirect derivative is their difference. All other coefficient columns in a given covariate's gradient are zero.

With joint covariance (widehat V_	heta), each impact variance is

[
widehat{operatorname{Var}}(g(hat	heta))=

abla g(hat	heta)'widehat V_	heta
abla g(hat	heta).
]

The implementation reports a two-sided Wald interval using the standard-normal quantile.

## Parameter ordering and use

- SAR: ([ho,eta_1,ldots,eta_k]).
- SDM: ([ho,eta_1,ldots,eta_k,gamma_1,ldots,gamma_k]).

```python
from impacts import spatial_impact_delta_uncertainty

# covariance must follow [rho, beta..., gamma...] exactly.
intervals = spatial_impact_delta_uncertainty(
    weights, rho, beta, joint_covariance, gamma,
    confidence=0.95,
)
for item in intervals:
    print(item.direct, item.indirect, item.total)
```

## Numerical and inferential limits

This is a local linear approximation. It can be inaccurate when the spatial multiplier is near singularity, the parameter distribution is strongly skewed, or impact distributions are highly nonlinear. Wald intervals are symmetric and may be misleading for bounded or asymmetric effects. Compare with the existing seeded parametric Monte Carlo procedure when nonlinear uncertainty matters. Both methods condition on the supplied weights matrix and fitted parameter covariance; neither repairs a misspecified covariance estimator.

The implementation checks covariance symmetry and positive semidefiniteness, parameter dimensions, finiteness and invertibility of (I-ho W). The analytic Jacobian is independently tested against central finite differences.

## References

- LeSage, J. and Pace, R. K. (2009). *Introduction to Spatial Econometrics*. CRC Press.
- Greene, W. H. (2018). *Econometric Analysis*, 8th ed. Pearson. Delta-method inference for nonlinear functions.
- [Spatial impacts implementation](../../implementations/python/spatial-econometrics/impacts.py).
- [Monte Carlo impact uncertainty record](spatial-impact-uncertainty.md).
