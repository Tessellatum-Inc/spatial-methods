# Source verification — GNSS dual-frequency combinations

## Identity and technical claims
The geometry-free combination is the difference of two same-unit frequency observables. The ionosphere-free combination weights each observable by the square of the other carrier's frequency and cancels the first-order ionospheric term under the standard dispersive model. It does not remove all ionospheric effects or other error sources.

## Implementation and reproduction
Tests verify geometry-free and wide-lane differences, first-order cancellation on synthetic observables, and invalid frequencies/inputs. The package does not claim cycle-slip detection or PPP-AR functionality. Run repository tests/CI independently.

## Rights
Only equations and technical explanations in original wording are used; no source text or figures are copied.
