# Reed-Xiaoli (RX) anomaly detector

Install requirements and run `pytest -q`. The global RX detector calculates squared Mahalanobis distance from a background mean and covariance for every pixel. A mask selects background-estimation pixels and masked-out output scores are NaN. A supplied covariance can replace the empirical covariance; eigenvalue flooring regularises singular matrices.

This is the global Gaussian-background RX baseline. It does not implement local RX, kernel RX, subspace RX, matched filtering or constrained energy minimisation. A global covariance can hide anomalies that contaminate the background sample and can be inappropriate for heterogeneous scenes. Scores are uncalibrated anomaly statistics, not probabilities; threshold selection and false-alarm control are separate tasks.
