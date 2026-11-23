# Implementation verification — principal-axis factor analysis

## Implemented scope

The `implementations/python/factor-analysis` package fits principal-axis exploratory factor models to the sample correlation matrix. It initializes communalities from squared multiple correlations using a Moore–Penrose inverse, iteratively extracts leading eigenpairs from the reduced correlation matrix, and optionally applies Kaiser varimax orthogonal rotation.

## Verification evidence

Tests use deterministic synthetic two-factor data with a known simple loading structure, check primary and cross-loadings without relying on factor sign/order, verify orthogonal rotation and communality preservation, test invariance to offsets and positive changes of measurement units, and exercise deterministic output and invalid-input rejection.

The package is registered in the Python CI manifest. Authored tests and registration do not establish that the latest workflow executed successfully; confirm the exact-head Actions run before claiming CI verification.

## Limitations

This is a teaching baseline for small dense matrices. It is not maximum-likelihood or confirmatory factor analysis, does not estimate factor scores or inferential standard errors, and does not support missing-data likelihoods or oblique rotations. Communality clipping is a numerical policy, not a general resolution of Heywood cases.

## Reproduction

```bash
python -m pip install -r requirements.txt
python -m pytest -q
```
