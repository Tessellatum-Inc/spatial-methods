# Verification record: Baarda-style data snooping

## Identity
- Canonical record: Baarda-style data snooping for linear geodetic least-squares adjustment.
- Implementation: implementations/python/helmert-7-parameter/data_snooping.py.
- Scope: full-rank linear Gauss–Markov model, known a-priori variance factor, full positive-definite observation covariance/cofactor matrix.

## Bibliographic verification
- Baarda (1968), A Testing Procedure for Use in Geodetic Networks, Netherlands Geodetic Commission, Publications on Geodesy, New Series 2(5), primary method source.
- Kok (1982), NOAA Technical Report NOS NGS 30, documents data snooping, multiple-outlier testing and network reliability.
- Schwarz & Kok (1993), DOI 10.1061/(ASCE)0733-9453(1993)119:4(127), describes standardized-residual testing and iterative single-observation identification.

## Technical checks
- Weighted normal equations use the supplied observation covariance/cofactor matrix.
- Residual cofactor is Qvv=Qll-A(A^T Qll^-1 A)^-1 A^T.
- Local statistic is wi=vi/(sigma0 sqrt(qvvi)).
- Global statistic is v^T Qll^-1 v/sigma0^2, with m-rank(A) degrees of freedom.
- Critical values are caller-supplied; no unverified significance or multiple-testing default is embedded.
- The package reports suspect indices but does not delete observations or claim proof of blunders.

## Reproduction and rights
- Original NumPy implementation and tests.
- Tests cover exact linear recovery, injected single gross error, correlated covariance, redundancy sum, invalid dimensions, rank deficiency and invalid covariance.
- No third-party source code, figures, tables or data are reproduced.
- Repository CI is pending; tests have not yet been confirmed by GitHub Actions.
