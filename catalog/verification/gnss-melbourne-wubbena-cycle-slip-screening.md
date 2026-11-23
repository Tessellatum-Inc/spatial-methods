# Verification record: Melbourne–Wübbena observable and screening

## Identity
- Observable implementation: implementations/python/gnss-ambiguity/combinations.py
- Detector implementation: implementations/python/gnss-ambiguity/melbourne_wubbena.py
- Classification: formula-based combination plus a simplified sequential threshold screen.

## Bibliographic checks
- ESA Navipedia (Sanz Subirana, Juan Zornoza & Hernández-Pajares, 2011) describes MW as a noisy wide-lane ambiguity estimate formed from wide-lane carrier phase and a frequency-weighted code combination. It notes the trade-off from code noise and multipath.
- Bezmenov et al. (2019), DOI 10.1007/s11018-019-01639-5, studies jumps in the MW combination and explicitly treats noise and outliers.
- Liu (2011), DOI 10.1007/s00190-010-0426-y, is a broader single-receiver detection/repair method; this repository does not reproduce it.

## Technical checks
- Phase inputs are cycles; code inputs are metres; frequencies are hertz; output is wide-lane cycles.
- Formula: (L1-L2) - ((f1-f2)/c) * (f1*P1+f2*P2)/(f1+f2).
- Detector compares against the current arc mean using a configurable sigma threshold and resets its state after a detected jump or configured data gap.
- The detector's initial noise floor is a user parameter, not a universal physical constant.
- MW is insensitive to some paired slip patterns and remains exposed to code noise/multipath.

## Reproduction and rights
- Original implementation and tests; no source text, figures or data copied.
- Tests cover formula units/weights, one-cycle discontinuity, arc reset, data gaps and invalid inputs.
- Full repository pytest and CI have not been run in this authoring session.
