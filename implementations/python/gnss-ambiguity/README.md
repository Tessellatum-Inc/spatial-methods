# GNSS integer ambiguity least squares

Implements the integer least-squares objective
\[
\check{a}=\arg\min_{z\in\mathbb Z^n}(\hat a-z)^TQ_{\hat a}^{-1}(\hat a-z)
\]
using Cholesky-based sphere enumeration, returning the best and second-best integer candidates and their objective values.

This is **not the LAMBDA method**: it does not decorrelate ambiguities with an integer unimodular transformation or implement the production LAMBDA/MLAMBDA reduction and search. It is an exact low-dimensional reference search for a supplied positive-definite float covariance. Highly correlated or high-dimensional cases can be computationally expensive. A ratio is returned as a diagnostic only; operational acceptance thresholds and validation depend on the full GNSS model, observation quality and integrity requirements.

Run with `python -m pytest -q` from this directory. The code does not ingest raw carrier-phase observations, estimate float ambiguities, detect cycle slips or produce a position solution.
