# Classification accuracy and disagreement measures

A confusion matrix compares mapped predictions against a reference sample.
This implementation uses reference classes as rows and mapped classes as
columns; reversing that convention swaps producer and user accuracy.

Overall accuracy is the diagonal total divided by sample size. Producer
accuracy is the diagonal count divided by its reference-row total (omission
complement); user accuracy is divided by its mapped-column total (commission
complement). Cohen's kappa adjusts overall agreement for the agreement
expected from the observed marginals:

\[
\kappa=\frac{p_o-p_e}{1-p_e},\qquad
p_e=\sum_i r_i c_i/n^2.
\]

Quantity disagreement is the total absolute difference between reference and
mapped class proportions divided by two. Allocation disagreement is the
remaining disagreement after subtracting quantity disagreement from total
error. For binary change maps, Figure of Merit is hits divided by hits, misses
and false alarms; correct rejections are excluded.

These sample-based measures are not automatically area-adjusted estimates.
Probability sampling, inclusion weights, reference-label uncertainty and
confidence intervals must be handled separately. The companion package does
not implement Olofsson-style area adjustment or fuzzy kappa.

See the tested [Python implementation](../../implementations/python/accuracy-assessment/README.md).
