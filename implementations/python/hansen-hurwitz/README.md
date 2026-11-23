# Hansen–Hurwitz estimator

A NumPy teaching implementation for the unbiased total estimator under independent sampling with replacement and known per-draw selection probabilities.

For ordered draws (i=1,\ldots,n), the draw-level estimate is (z_i=y_i/p_i) and the estimator is

\[
\widehat{T}_{HH}=\frac{1}{n}\sum_{i=1}^{n}\frac{y_i}{p_i}.
\]

The estimated variance of the total is the sample variance of the draw-level estimates divided by (n). If a population size (N) is provided, the mean estimate is (widehat{T}_{HH}/N) and its estimated variance is divided by (N^2). The variance estimate is unavailable for one draw.

## Use

```python
from hansen_hurwitz import hansen_hurwitz

result = hansen_hurwitz(
    values=[2, 4, 6],
    draw_probabilities=[0.2, 0.2, 0.2],
    population_size=10,
)
print(result.total_estimate)
print(result.total_variance_estimate)
print(result.mean_estimate)
```

## Contract and limitations

- `values` and `draw_probabilities` are aligned ordered vectors from the **draw sequence**, not a deduplicated set of selected units.
- Draws must be independent and with replacement; probabilities are draw-by-draw probabilities and each sampled unit's probability must be known and positive.
- Duplicate units are represented by repeated observations and are not collapsed.
- This is not a Horvitz–Thompson inclusion-probability estimator for a without-replacement sample.
- The estimator is unbiased for a population total under its sampling design; no design can be inferred from the arrays alone.
- Overflow in weighted estimates or variance calculations is rejected explicitly instead of returning non-finite results.
- No spatial autocorrelation adjustment, cluster variance, nonresponse correction, PPS design generator or confidence-interval routine is included.

## Run tests

```bash
python -m pip install -r requirements.txt
python -m pytest -q
```
