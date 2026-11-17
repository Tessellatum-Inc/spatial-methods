# Principal-axis factor analysis

A NumPy teaching implementation of exploratory principal-axis factoring on the sample correlation matrix, with optional Kaiser varimax orthogonal rotation.

## Run

```bash
python -m pip install -r requirements.txt
python -m pytest -q
```

## Contract

Rows are observations and columns are measured variables. At least three observations and two non-constant variables are required; values must be finite and the factor count must be smaller than the number of variables. Variables are standardized using sample means and sample standard deviations.

Initial communalities are squared multiple correlations computed from the Moore–Penrose inverse of the correlation matrix. Principal-axis iterations replace the correlation matrix diagonal with communalities, extract leading eigenpairs and update communalities from squared loadings. Communalities are clipped to [0, 1]; the result exposes clipping and convergence diagnostics.

Varimax rotates loadings orthogonally. It preserves each variable's communality but changes factor orientation. Factor signs and order are not uniquely identified.

## Scope and limitations

This is a bounded exploratory baseline, not maximum-likelihood or confirmatory factor analysis, oblique rotation, factor-score estimation, measurement-invariance testing or a full latent-variable model. It does not estimate inferential standard errors or support missing-data likelihoods. Review loading patterns, communalities, uniquenesses and residual correlations before use.
