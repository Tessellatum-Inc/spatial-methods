# Source verification — GNSS geometry-free cycle-slip screening

## Identity and bibliography
- Blewitt (1990), “An automatic editing algorithm for GPS data,” *Geophysical Research Letters* 17(3), 199–202, DOI 10.1029/GL017i003p00199.
- Zhao et al. (2023), “Dual-Frequency GNSS Observations Cycle Slip Detection and Repair Method Using the Ensemble Hatch–Melbourne–Wübbena (HMW) Combination—Prophet Model,” *Journal of the Indian Society of Remote Sensing* 51, 1937–1953, DOI 10.1007/s12524-023-01722-z.

## Scope and evidence
Implemented: sequential quadratic prediction of the geometry-free phase-combination series, threshold residual screening, exclusion of flagged observations from the fitting history and optional gap reset. The source literature supports GF and HMW combinations as complementary cycle-slip detection signals; the code here is only a simplified GF screening baseline.

Not implemented: Melbourne–Wübbena detector, TurboEdit, integer slip identification/repair, ionosphere estimation, elevation-dependent stochastic model, PPP-AR or integrity monitoring.

## Reproduction
Regression tests are authored for synthetic trend-plus-jump data, irregular epochs, gap resets and invalid inputs. These tests have not been executed by repository CI in this work session.

## Rights
Bibliographic metadata and original explanatory text only. No source figures, code or datasets are reproduced.
