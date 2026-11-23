# Verification record: beta-convergence regression

## Identity
- Canonical record: cross-sectional absolute/conditional beta-convergence OLS.
- Implementation: implementations/python/regional-dynamics/regional_dynamics.py.
- Scope: one cross-section of positive start/end regional incomes, annualized log growth, optional observed controls, OLS and HC1 standard errors.

## Bibliographic verification
- Barro & Sala-i-Martin (1992), JPE 100(2), 223–251, DOI 10.1086/261816, is a foundational regional/cross-country beta-convergence source.
- Rey & Montouri (1999), Regional Studies 33(2), 143–156, DOI 10.1080/00343409950122945, studies US regional income convergence with spatial econometric diagnostics and models.
- Rey (2001), Geographical Analysis 33(3), 195–214, DOI 10.1111/j.1538-4632.2001.tb00444.x, connects spatial dependence and regional transition dynamics.

## Technical checks
- Dependent variable is log(y_end/y_start)/T.
- Regressor is log(y_start), plus optional controls.
- OLS requires full column rank and positive residual degrees of freedom.
- HC1 covariance uses n/(n-k) times the sandwich estimator.
- Convergence speed and half-life are reported only for -1 < beta < 0.
- HC1 does not account for spatial dependence; the method page states this explicitly.

## Reproduction and rights
- Original NumPy implementation and tests.
- Tests cover negative-slope recovery, controls, invalid inputs and undefined speed for a positive slope.
- No third-party code, figures or data are reproduced.
- Repository CI pending.
