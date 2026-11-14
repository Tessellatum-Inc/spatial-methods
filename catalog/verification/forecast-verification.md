# Source verification — forecast verification

## Identity and scope
The Section 10 grouped forecast-verification entry contains several distinct families: neighborhood FSS, object-based SAL/MODE, categorical contingency scores, probabilistic scores/diagnostics and optical-flow motion estimation. This record verifies only a subset.

## Bibliography
- Roberts & Lean (2008), *Monthly Weather Review* 136, 78–97: primary FSS source; full paper checked.
- Brier (1950), *Monthly Weather Review* 78, 1–3: foundational probability forecast verification score.
- Wilks (2011), *Statistical Methods in the Atmospheric Sciences*, 3rd edition: standard reference for contingency and probabilistic verification definitions.

## Technical and implementation checks
The package defines POD, FAR, CSI and ETS from a 2x2 event contingency table; Brier score for binary outcomes; tie-corrected rank ROC AUC; FSS from thresholded square-neighborhood fractions, empirical-ensemble CRPS, and a tie-aware expected rank histogram. The FSS implementation clips neighborhoods at domain edges and requires pre-aligned finite rectangular grids. It does not calculate SAL, MODE, CRPS decomposition, rank histograms, optical flow, uncertainty intervals or scale-dependent usefulness thresholds.

## Reproduction status
Tests cover hand-calculated contingency counts, score edge cases, tied AUC ranks, perfect/displaced neighborhood fields and input validation. Run repository tests/CI before treating the implementation as independently reproduced. These are educational functions, not an operational forecast-verification workflow.

## Rights
Only metadata and paraphrased mathematical definitions are used; no paper text, figures or data are copied.
