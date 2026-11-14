# Robust trend, rank change detection and hidden-state decoding

This package adds three complementary tools for ordered observations. They solve different problems: robust trend estimation, a single rank-based distributional change test, and decoding a latent-state sequence.

## Theil–Sen trend

For paired observations \((x_i,y_i)\), the slope estimate is the median of all pairwise slopes:

\[
\hat\beta=\operatorname{median}_{i<j,\,x_i\ne x_j}
\frac{y_j-y_i}{x_j-x_i},\qquad
\hat\alpha=\operatorname{median}_i(y_i-\hat\beta x_i).
\]

It is resistant to some vertical outliers, but the direct all-pairs implementation is \(O(n^2)\). It estimates a single linear trend; it does not model seasonality, autocorrelation, multiple regimes or spatially varying trends.

## Pettitt single-change test

Pettitt's nonparametric test uses ranks to search for one dominant change in distribution. With average ranks \(r_i\) for ties, the cumulative statistic at split \(t\) is

\[
U_t=2\sum_{i=1}^{t}r_i-t(n+1),\qquad
K=\max_{1\le t<n}|U_t|.
\]

The implementation returns the split position, \(K\), and the common exponential approximation to the p-value. This is an approximate single-change test, not a multiple-boundary segmentation method. Its usual calibration assumes independent observations under the null; serial dependence, ties and repeated testing across many pixels require additional care.

## Hidden Markov model: Viterbi decoding

Given start probabilities \(\pi_i\), transition probabilities \(a_{ij}\), and discrete emission probabilities \(b_j(o_t)\), Viterbi finds the most probable hidden-state path:

\[
\hat z_{1:T}=\arg\max_{z_{1:T}}
\pi_{z_1}b_{z_1}(o_1)
\prod_{t=2}^{T}a_{z_{t-1},z_t}b_{z_t}(o_t).
\]

The implementation uses log probabilities and dynamic programming. It decodes a path for supplied parameters; it does not estimate transition/emission parameters, choose the number of states, or establish that the hidden states correspond to meaningful land-cover classes.

## Code and tests

See [the Python package](../implementations/python/temporal-models/README.md). It includes Theil–Sen, Pettitt and discrete-emission Viterbi, with validation tests. STL-style decomposition is now covered by a separate [STL lesson](stl-seasonal-trend-decomposition.md) and educational implementation; ARIMA, Prophet, BEAST, full unknown-variance BOCPD and continuous-emission HMMs remain open.

## Spatial-data cautions

For Earth-observation and spatial time series, inspect seasonal cycles, irregular acquisition intervals, missing observations, cloud contamination, sensor harmonization, spatial dependence and multiple testing. A Pettitt boundary or HMM state transition is a statistical description of the input sequence, not automatically a physical event. Validate with independent observations and domain knowledge.

## Sources

- Sen, P. K. (1968). “Estimates of the Regression Coefficient Based on Kendall's Tau.” *Journal of the American Statistical Association*, 63(324), 1379–1389. DOI: [10.1080/01621459.1968.10480934](https://doi.org/10.1080/01621459.1968.10480934). Theil–Sen slope estimation.
- Pettitt, A. N. (1979). “A Non-Parametric Approach to the Change-Point Problem.” *Applied Statistics*, 28(2), 126–135. DOI: [10.2307/2346729](https://doi.org/10.2307/2346729). Rank-based single-change test.
- Rabiner, L. R. (1989). “A Tutorial on Hidden Markov Models and Selected Applications in Speech Recognition.” *Proceedings of the IEEE*, 77(2), 257–286. DOI: [10.1109/5.18626](https://doi.org/10.1109/5.18626). HMM formulation and dynamic-programming decoding.

No source text or figures are reproduced.
