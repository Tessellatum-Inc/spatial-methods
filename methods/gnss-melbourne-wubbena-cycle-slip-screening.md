# Melbourne–Wübbena combination and cycle-slip screening

## Observable

For dual-frequency carrier phases L1 and L2 expressed in cycles, code pseudoranges P1 and P2 in metres, and frequencies f1 and f2 in hertz, the Melbourne–Wübbena (MW) wide-lane observable in wide-lane cycles is

MW = (L1 - L2) - ((f1 - f2) / c) * ((f1 P1 + f2 P2) / (f1 + f2)).

The code term is a frequency-weighted narrow-lane pseudorange scaled by the wide-lane wavelength. The observable is centred on a wide-lane ambiguity plus receiver/satellite hardware-bias terms and measurement noise. Code multipath/noise can be substantial. The MW observable suppresses the first-order ionospheric term and geometry in the standard dual-frequency model, but it is not noiseless and it does not by itself fix ambiguities.

## Implemented baseline

- melbourne_wubbena in implementations/python/gnss-ambiguity/combinations.py computes the observable in wide-lane cycles.
- detect_melbourne_wubbena_slips in implementations/python/gnss-ambiguity/melbourne_wubbena.py screens a time series using a running arc mean and standard-deviation threshold.
- A detected jump starts a new arc so subsequent observations are not repeatedly compared against a pre-slip mean. A configured epoch gap also resets the arc, but is separately reported and is not automatically classified as a slip.

## Use and limitations

The threshold and initial noise floor must be calibrated to the receiver, signal, sampling rate, satellite elevation and multipath environment. A threshold that is too high misses small slips; one that is too low creates false alarms. MW detects the wide-lane combination of slips: some paired slips, including equal slips on both frequencies, can be invisible to this combination. Combine it with geometry-free phase screening and other quality controls.

This is a transparent screening baseline, not a full Springer detector, TurboEdit, integer slip-pair identification, ambiguity resolution, slip repair, PPP-AR or an integrity monitor. No real receiver observations are included.

## References

- Sanz Subirana, J., Juan Zornoza, J. M., & Hernández-Pajares, M. (2011). Detector based in code and carrier phase data: The Melbourne–Wübbena combination. ESA Navipedia, GNSS Data Processing.
- Bezmenov, I. V., Blinov, I. Yu., Naumov, A. V., & Pasynok, S. L. (2019). An algorithm for cycle-slip detection in a Melbourne–Wübbena combination formed of code and carrier phase GNSS measurements. Measurement Techniques, 62, 415–421. DOI: 10.1007/s11018-019-01639-5.
- Liu, Z. (2011). A new automated cycle slip detection and repair method for a single dual-frequency GPS receiver. Journal of Geodesy, 85, 171–183. DOI: 10.1007/s00190-010-0426-y.

No source code, text, figures or observation data are reproduced.
