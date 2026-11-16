# Run-theory drought and threshold events

Run theory identifies contiguous periods during which a time series lies below or above a threshold. For drought, a common example is SPI below a selected negative threshold. Each event records inclusive start/end indices, calendar duration, number of exceedance samples, cumulative severity, peak severity and mean severity on exceedance days. Optional short gaps may be bridged; missing values always terminate events.

Severity is the sum of threshold deficit (below-threshold mode) or excess (above-threshold mode) over exceedance samples only. The implementation is a one-dimensional event extractor; it does not perform spatial event tracking, probabilistic return-period analysis or threshold calibration.
