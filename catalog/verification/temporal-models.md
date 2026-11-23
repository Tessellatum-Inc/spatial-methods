## Robust trend, Pettitt and HMM source check

- **Theil–Sen:** Sen, P. K. (1968), “Estimates of the Regression Coefficient Based on Kendall's Tau,” *JASA* 63(324), 1379–1389, DOI 10.1080/01621459.1968.10480934. The package computes the median of all pairwise slopes and a median intercept; it is a direct O(n²) implementation.
- **Pettitt:** Pettitt, A. N. (1979), “A Non-Parametric Approach to the Change-Point Problem,” *Applied Statistics* 28(2), 126–135, DOI 10.2307/2346729. The package implements the rank statistic with average ranks for ties and an approximate p-value. Independence and multiple-testing limitations are stated.
- **HMM/Viterbi:** Rabiner, L. R. (1989), “A Tutorial on Hidden Markov Models and Selected Applications in Speech Recognition,” *Proceedings of the IEEE* 77(2), 257–286, DOI 10.1109/5.18626. The package decodes a discrete-emission HMM path in log space; it does not estimate parameters.
- **Rights:** bibliographic metadata and DOI links only; no article text or figures copied.
- **Status:** identity and core bibliography checked; algorithm scope documented; local deterministic smoke checks passed; repository CI execution and independent review remain pending.
