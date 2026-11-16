## Kalman filter and RTS smoother source check

- **Kalman filter:** Kalman, R. E. (1960), “A New Approach to Linear Filtering and Prediction Problems,” *Journal of Basic Engineering* 82(1), 35–45, DOI 10.1115/1.3662552. Publisher metadata checked.
- **RTS smoother:** Rauch, H. E., Tung, F., & Striebel, C. T. (1965), “Maximum Likelihood Estimates of Linear Dynamic Systems,” *AIAA Journal* 3(8), 1445–1450, DOI 10.2514/3.3166. Bibliographic record checked.
- **Implementation boundary:** scalar local-level random walk only; missing observations are prediction-only updates. RTS is retrospective smoothing and must not be represented as causal online filtering.
- **Rights:** bibliographic metadata and DOI links only; no article text or figures copied.
- **Status:** source identities checked; scalar filter/smoother implementation and regression tests authored; deterministic local regression checks passed, including prediction-only missing-data handling and backward smoothing; repository CI and independent review pending.
