# Verification dossier: local InSAR coherence

## Implemented scope

Local magnitude coherence from two complex SLC arrays using valid square moving windows, plus signed coherence-map differencing.

## Independent tests

Tests verify unit coherence for identical complex imagery and a constant phase offset, low mean coherence for independent complex noise fields, reduced output dimensions, low/zero-power NaN handling, signed difference direction, and rejection of mismatched shapes, non-finite arrays, invalid window sizes and invalid thresholds.

## Exclusions

The implementation does not reproduce a full InSAR chain, phase unwrapping, PS/SBAS, orbit correction, co-registration, offset tracking or atmospheric correction. The broad source entry remains Partial.