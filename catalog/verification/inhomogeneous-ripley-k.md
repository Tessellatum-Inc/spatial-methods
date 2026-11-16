# Verification record: inhomogeneous Ripley's K

## Implemented scope

The implementation accepts a positive finite intensity estimate at each observed event and calculates the ordered-pair inhomogeneous K estimator. It optionally applies rectangular-window translation correction. Constant event intensity n/A reduces to the ordinary uncorrected K estimator.

## Tests

Tests cover constant-intensity equivalence, event-specific intensity weights, translation correction and invalid intensities/zero-overlap displacements. CI status is tied to the commit containing the tests.

## Limits

The first-order intensity surface is supplied by the caller. Intensity estimation, bandwidth choice, irregular-window edge correction, parameter-estimation effects and global simulation inference are not implemented by this estimator.
