# GNSS cycle-slip screening with a geometry-free phase combination

A carrier-phase cycle slip is a discontinuity in the accumulated phase observable. Dual-frequency receivers provide complementary combinations that help expose such discontinuities. The geometry-free (GF) phase combination removes the common geometric range term while retaining ionospheric content; therefore, its temporal evolution is not perfectly constant.

## Implemented baseline

The [Python implementation](../implementations/python/gnss-ambiguity/cycle_slips.py) performs sequential screening on a supplied GF phase series:

1. Fit a quadratic least-squares predictor to a configurable window of previously accepted observations.
2. Predict the current epoch and calculate its residual.
3. Flag a discontinuity when the absolute residual exceeds a user-specified metre threshold.
4. Exclude flagged observations from subsequent fitting so a detected jump does not contaminate the local trend.
5. Optionally reset the history after a sufficiently large epoch gap.

The implementation supports irregular epoch spacing. It is an anomaly-screening baseline, not an integer repair algorithm.

## Limitations

The threshold is user supplied and must be calibrated to sampling interval, signal, receiver noise, satellite elevation and ionospheric conditions. Rapid ionospheric variation, multipath, bad observations or receiver events can produce false alarms; small or specially paired slips can be missed. The algorithm does not use the Melbourne–Wübbena combination, estimate wide-lane ambiguities, identify the integer slip pair, or repair carrier-phase observations. It is not a full TurboEdit implementation and should not be used as a production integrity monitor.

A practical dual-frequency detector commonly combines GF and Melbourne–Wübbena information because their sensitivities and noise characteristics complement one another. Published work also documents the limitations of conventional combinations under strong ionospheric variation and code multipath.

## Sources

- Blewitt, G. (1990). “An automatic editing algorithm for GPS data.” *Geophysical Research Letters*, 17(3), 199–202. [DOI](https://doi.org/10.1029/GL017i003p00199).
- Zhao, J. et al. (2023). “Dual-Frequency GNSS Observations Cycle Slip Detection and Repair Method Using the Ensemble Hatch–Melbourne–Wübbena (HMW) Combination—Prophet Model.” *Journal of the Indian Society of Remote Sensing*, 51, 1937–1953. [DOI](https://doi.org/10.1007/s12524-023-01722-z).

No source text, figures or observation data are reproduced.
