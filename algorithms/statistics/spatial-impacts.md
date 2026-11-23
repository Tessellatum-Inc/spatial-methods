# Spatial impacts: direct, indirect and total effects

Stable ID: `SA-STAT-SPATIAL-IMPACTS` · Supplementary spatial econometrics method

## Why regression coefficients are not the whole story

In an ordinary linear model, a coefficient describes the marginal effect of a predictor on the expected response, holding the other predictors fixed. In a spatial lag model, a change at one location can propagate through the spatial system and feed back to its origin.

For the spatial Durbin model (SDM),

[
y=ho Wy+Xeta+WXgamma+arepsilon
]

the reduced form is:

[
y=(I-ho W)^{-1}(Xeta+WXgamma)
 +(I-ho W)^{-1}arepsilon
]

The spatial multiplier means that the coefficient (eta_r) alone is not the marginal effect of covariate (r).

## The impact matrix

For covariate (r), define:

[
S_r=(I-ho W)^{-1}(eta_r I+gamma_r W)
]

The element ((S_r)_{ij}) is the change in expected outcome at location (i) associated with a one-unit change in covariate (r) at location (j), holding the model parameters fixed.

Summarise the matrix as:

[
	ext{Direct}_r=rac{operatorname{tr}(S_r)}{n}
]

[
	ext{Total}_r=rac{1}{n}sum_isum_j(S_r)_{ij}
]

[
	ext{Indirect}_r=	ext{Total}_r-	ext{Direct}_r
]

- **Direct impact:** average own-location response, including feedback that travels away and returns.
- **Indirect impact:** average spillover from changes in other locations.
- **Total impact:** direct plus indirect impact, equivalently the average row sum of the impact matrix.

For the spatial lag/SAR special case, set (gamma_r=0). For an SLX model with no lagged response, set (ho=0), so (S_r=eta_rI+gamma_rW).

## A tested dense-matrix calculation

~~~python
from impacts import spatial_impacts

weights = [
    [0, 1, 0, 0],
    [1, 0, 1, 0],
    [0, 1, 0, 1],
    [0, 0, 1, 0],
]
# One covariate: beta=1.5, spatially lagged coefficient gamma=0.75.
result, = spatial_impacts(weights, rho=0.15, beta=[1.5], gamma=[0.75])
print("Direct:", result.direct)
print("Indirect:", result.indirect)
print("Total:", result.total)
~~~

The implementation solves a linear system rather than explicitly forming ((I-ho W)^{-1}), which is numerically preferable. It returns the full impact matrix for inspection and the three average summaries.

## Inference and interpretation

These calculations condition on supplied parameter estimates. They do not estimate (ho,eta,gamma), calculate standard errors, or propagate parameter uncertainty. In applied work, direct, indirect and total impacts should be accompanied by uncertainty estimates derived from the fitted model's variance-covariance matrix or an appropriate simulation procedure.

The weights matrix, its transformation, the included spatially lagged covariates and the parameter space for (ho) are part of the model specification. A singular (I-ho W) makes the reduced form undefined. A numerically solvable matrix is not, by itself, proof that the chosen spatial process is substantively defensible.

## References

- LeSage, J. and Pace, R. K. (2009). *Introduction to Spatial Econometrics*. CRC Press.
- Elhorst, J. P. (2010). “Applied Spatial Econometrics: Raising the Bar.” *Spatial Economic Analysis*, 5(1), 9–28.
- [Spatial Data Science: Spatial Econometrics Models](https://r-spatial.org/book/17-Econometrics.html), especially the reduced form, impact matrix and direct/indirect impact discussion.
- [spatialreg maximum-likelihood model reference](https://r-spatial.github.io/spatialreg/reference/ML_models.html), which cautions that lag and Durbin coefficients should be interpreted through impact measures.

## Repository implementation

- [Implementation package](../../implementations/python/spatial-econometrics/README.md)
- [Impact source](../../implementations/python/spatial-econometrics/impacts.py)
- [Tests](../../implementations/python/spatial-econometrics/test_spatial_econometrics.py)

The package is a dense teaching calculation, not a spatial model estimator.
