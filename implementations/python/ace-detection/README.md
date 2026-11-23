# Adaptive Coherence Estimator (ACE)

Run `pytest -q`. ACE compares each background-mean-centred pixel with a target contrast vector using the background covariance metric. It is the squared cosine similarity in the whitened spectral space and is bounded between zero and one (up to numerical error).

This global covariance implementation assumes a representative background population and a known target spectrum in the same calibrated band space. It is not a probability or false-alarm estimate; threshold calibration requires representative background data. It is distinct from RX anomaly scoring, matched filtering and CEM.
