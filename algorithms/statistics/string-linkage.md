# String similarity and probabilistic record linkage

Edit distance, Jaro-Winkler and character n-gram similarity quantify field-level
resemblance; phonetic encodings create coarse keys; blocking and canopy methods
reduce the number of pairs compared. These are distinct stages of record
linkage, not identity guarantees.

Levenshtein distance is the minimum number of insertions, deletions and
substitutions. A normalized score is
\[
s_L(x,y)=1-\frac{d_L(x,y)}{\max(|x|,|y|)}
\]
with two empty strings assigned one. Jaro-Winkler adds a bounded common-prefix
bonus to Jaro similarity. Character n-gram cosine compares count vectors of
overlapping substrings.

For comparison outcome gamma_k, let m_k=P(agreement|match) and
u_k=P(agreement|non-match). The Fellegi-Sunter log weight is
\[
W=\sum_k \begin{cases}
\log(m_k/u_k), & \text{agreement}\\
\log((1-m_k)/(1-u_k)), & \text{disagreement}
\end{cases}
\]
Positive values support match relative to non-match. The implementation accepts
m/u values rather than estimating them. Missingness, partial agreements,
dependent fields and prior match odds need explicit treatment.

Prefix blocking and canopy generation are illustrative small-data candidate
generators. Measure candidate recall separately from pairwise accuracy. For
place records, combine names and addresses with spatial proximity and source
provenance; text similarity alone is insufficient.

The tested [Python package](../../implementations/python/string-linkage/README.md)
covers these reference baselines. It does not implement Metaphone, production
scale indexing, automatic parameter estimation or full POI deduplication.
