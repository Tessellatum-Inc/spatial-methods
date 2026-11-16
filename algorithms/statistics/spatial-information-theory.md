# Spatial information-theoretic measures

For normalized probabilities p_i, Shannon entropy is H=-sum(p_i log p_i). Renyi entropy of order alpha is H_alpha=log(sum(p_i^alpha))/(1-alpha), with Shannon as the alpha-to-one limit. Tsallis entropy is S_q=(1-sum(p_i^q))/(q-1), also with Shannon as q-to-one limit. The implementation accepts nonnegative counts/weights and normalizes them.

Categorical raster entropy uses class proportions after an optional boolean mask. Permutation entropy embeds a time series into delayed ordinal patterns and computes the Shannon entropy of their frequencies, optionally divided by log(order!) to yield [0,1]. Stable sorting breaks ties by original position; heavily quantized data therefore needs a stated tie policy.

These statistics do not by themselves model spatial dependence or causal information flow. Transfer entropy, spatially conditioned entropy, recurrence analysis and Granger/PCMCI methods remain separate.
