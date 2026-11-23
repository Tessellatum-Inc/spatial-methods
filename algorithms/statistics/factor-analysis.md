# Principal-axis factor analysis

Factor analysis models shared covariance through latent factors. For standardized variables, write R = LLᵀ + Ψ, where L contains factor loadings and Ψ is diagonal uniqueness. Communality is the row-wise sum of squared loadings.

## Principal-axis extraction

Initialize communalities from squared multiple correlations. Replace the correlation-matrix diagonal with those communalities, eigendecompose the reduced matrix, retain the leading factors, and update communalities from squared loadings until convergence.

## Varimax rotation

Orthogonal varimax seeks a simpler loading pattern. It preserves each variable's communality; factor signs and order remain arbitrary.

## Implementation and limits

The [tested implementation](../../implementations/python/factor-analysis/README.md) is a small-matrix exploratory principal-axis baseline with optional varimax. It is not maximum-likelihood or confirmatory factor analysis and does not estimate factor scores. OAC-style geodemographic classification is a separate workflow requiring indicator selection, geographic units, scaling, clustering, stability and external validation.

## References

- Harman, H. H. (1976). *Modern Factor Analysis* (3rd ed.). University of Chicago Press.
- Kaiser, H. F. (1958). The varimax criterion for analytic rotation in factor analysis. *Psychometrika*, 23, 187–200. https://doi.org/10.1007/BF02289233
