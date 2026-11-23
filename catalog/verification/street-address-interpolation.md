# Verification dossier: street address interpolation

## Implemented scope

Address-range interpolation along projected polylines using cumulative line distance, same-parity step-two numbering, mixed-parity consecutive numbering, explicit requested numbers and optional left/right side offsets.

## Independent tests

Tests cover even and mixed-parity ranges, descending numbering, cumulative distance across a bent polyline, explicit number selection, left/right offsets, and malformed ranges, duplicates, zero-length segments and non-finite coordinates.

## Exclusions

Building-footprint matching, local address-standard inference, address quality scoring, intersection resolution and verification against authoritative address registers remain open. The source row is Partial.