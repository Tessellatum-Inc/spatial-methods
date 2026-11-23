# Verification record: Pope's tau test

## Identity and implementation
- Method: internally studentized residual test for geodetic least-squares adjustment with an a-posteriori variance factor.
- Implementation: implementations/python/helmert-7-parameter/data_snooping.py, function pope_tau_test.
- Test suite: implementations/python/helmert-7-parameter/test_data_snooping.py.

## Technical checks
- Variance factor: \(\hat\sigma_0^2=\mathbf v^T\mathbf Q_{ll}^{-1}\mathbf v/r\), with \(r=m-\operatorname{rank}(A)\).
- Individual statistic: \(|v_i|/(\hat\sigma_0\sqrt{q_{vv,ii}})\).
- Tau critical value is the Student-t transform \(\sqrt r t/\sqrt{r-1+t^2}\), with t degrees of freedom r-1.
- A two-sided Bonferroni allocation alpha/(2m) is used to control family-wise error conservatively; this policy is stated explicitly rather than silently treating each residual as an independent test.
- Requires r >= 2; zero estimated residual variance is a distinct status; zero-redundancy residuals remain undefined.

## Reproduction and rights
- Original NumPy/SciPy implementation with synthetic fixtures.
- Tests cover a gross-error fixture, the exact Student-t transformation, perfect-fit handling, insufficient redundancy and invalid significance levels.
- The method is a single-adjustment diagnostic, not iterative robust estimation or automatic deletion.
