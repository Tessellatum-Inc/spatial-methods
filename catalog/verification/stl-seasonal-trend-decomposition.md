# Source verification — STL

## Identity and bibliography
Canonical method: Seasonal-Trend decomposition based on Loess (STL). Primary source: Cleveland, R. B., Cleveland, W. S., McRae, J. E., & Terpenning, I. (1990), Journal of Official Statistics, 6(1), 3–73. The publisher-hosted Statistics Sweden paper and R stats::stl documentation corroborate the bibliographic record.

## Technical claims checked
The original method describes additive decomposition into trend, seasonal and remainder; a sequence of LOESS smoothers; seasonal subseries smoothing; low-pass filtering; and robust estimation. R documentation corroborates iterative seasonal-subseries extraction, low-pass filtering and robust fitting.

## Implementation and reproduction
The repository implementation is explicitly an STL-style educational baseline, not an exact port of the original Fortran/R algorithm. It uses local-linear LOESS, cycle-subseries filtering, a moving-average low-pass sequence, iterative backfitting and optional bisquare robust weights. Tests cover additive reconstruction, seasonal phase centering, outlier downweighting and invalid inputs. It does not support missing values, irregular timestamps, all original smoother degrees/jump parameters or production parameter defaults. Repository tests and CI must be run independently before this note is upgraded.

## Rights
Only bibliographic metadata and paraphrased method descriptions are used; no paper text or figures are copied.
