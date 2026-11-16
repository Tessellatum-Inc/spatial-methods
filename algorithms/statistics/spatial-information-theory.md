# Spatial information-theoretic measures

For normalized probabilities p_i, Shannon entropy is H=-sum(p_i log p_i). Renyi entropy of order alpha is H_alpha=log(sum(p_i^alpha))/(1-alpha), with Shannon as the alpha-to-one limit. Tsallis entropy is S_q=(1-sum(p_i^q))/(q-1), also with Shannon as q-to-one limit. The implementation accepts nonnegative counts/weights and normalizes them.

Categorical raster entropy uses class proportions after an optional boolean mask. Permutation entropy embeds a time series into delayed ordinal patterns and computes the Shannon entropy of their frequencies, optionally divided by log(order!) to yield [0,1]. Stable sorting breaks ties by original position; heavily quantized data therefore needs a stated tie policy.

Sample entropy estimates the negative log ratio of non-self template-pair matches at lengths m+1 and m, using the Chebyshev metric. The default tolerance is r times the population standard deviation. It returns infinity when length-m matches exist but no length-(m+1) matches do, and raises when the denominator count is zero.

Spatial conditional entropy and mutual information treat positive off-diagonal adjacency entries as weights on directed edges. They estimate H(Y|X) and I(X;Y) from the weighted joint distribution of origin and neighbour categories. They are descriptive edge-distribution summaries, not causal measures; row-standardisation, directionality, edge weighting and islands alter the estimand. Self-edges are ignored.

Transfer entropy, spatially conditioned information flow, recurrence analysis and Granger/PCMCI methods remain separate.
