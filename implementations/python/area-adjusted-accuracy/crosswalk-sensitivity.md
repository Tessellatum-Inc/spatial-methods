# Fiji–WorldCover class-crosswalk sensitivity analysis

**Status:** Executed against the same 834-point sample used in the primary Fiji–WorldCover comparison. Three explicit legend scenarios were evaluated with the original Fiji sampling strata and area weights held fixed.

## Why test the crosswalk?

Overall accuracy depends on the definition of a correct class match. WorldCover and the Fiji reference dataset do not use identical legends. The primary result uses direct working-label matches; WorldCover herbaceous wetland has no matching class in the Fiji reference legend and is counted as disagreement.

That is transparent, but it is not the only possible analytical choice. This sensitivity analysis changes only the declared class harmonisation, not the sample, sample locations, reference observations, sampling strata, area weights, population sizes or point extraction protocol.

## Results

| Scenario | Original Fiji map OA | WorldCover OA | WorldCover − Fiji | Paired SE | Approx. 95% interval for difference |
|---|---:|---:|---:|---:|---:|
| Strict eight-class working labels | 82.51% | 74.12% | −8.39 pp | 1.50 pp | −11.32 to −5.45 pp |
| Herbaceous wetland recoded as grassland | 82.51% | 74.76% | −7.74 pp | 1.61 pp | −10.90 to −4.59 pp |
| Broad six-class vegetation grouping | 85.26% | 76.64% | −8.62 pp | 1.64 pp | −11.83 to −5.40 pp |

WorldCover overall-accuracy uncertainty estimates:

| Scenario | Standard error | Approx. 95% Wald interval |
|---|---:|---:|
| Strict eight-class working labels | 2.37 pp | 69.47%–78.76% |
| Herbaceous wetland recoded as grassland | 2.33 pp | 70.20%–79.32% |
| Broad six-class vegetation grouping | 2.28 pp | 72.18%–81.11% |

The strict scenario reproduces the primary assessment. Reclassifying the 12 herbaceous-wetland sample observations as grassland increases WorldCover OA by about 0.64 percentage points. The broad grouping increases it by about 2.53 points. In all three scenarios the paired difference remains negative and its approximate 95% interval remains below zero.

## Exact scenario definitions

1. **Strict eight-class working labels:** retain each class label. WorldCover herbaceous_wetland remains distinct because the Fiji reference legend has no corresponding class. It therefore counts as disagreement in the detailed comparison.
2. **Wetland as grassland:** recode WorldCover herbaceous_wetland to grassland; leave all reference labels and original Fiji map labels unchanged. This is a sensitivity assumption, not a claim that all herbaceous wetlands are grassland.
3. **Broad six-class grouping:** apply the same aggregation to WorldCover, original Fiji map and reference labels: tree + mangrove → woody_cover; grassland + shrubland + herbaceous_wetland → open_vegetation; retain agriculture, bare_soil_rock, urban and water as separate classes. This assesses broad thematic agreement, not detailed eight-class accuracy.

The broad grouping changes the legend and therefore changes the question being answered. Its OA must not be presented as a like-for-like replacement for detailed class accuracy.

## Estimator

For each scenario, the script transforms the point-level WorldCover, reference and baseline Fiji labels, then recomputes the stratified area-adjusted overall accuracy. The paired map difference is calculated from the within-stratum sample variance of the difference between the two correctness indicators. This retains covariance from assessing both maps on the same sampled points.

For sampling stratum \(h\), the variance contribution for the paired difference is

\[
W_h^2\left(1-\frac{n_h}{N_h}\right)\frac{s^2_{d,h}}{n_h},
\]

where \(W_h\) is the supplied eligible-domain area proportion, \(n_h\) the sample size, \(N_h\) the supplied stratum population size and \(s^2_{d,h}\) the sample variance of paired correctness differences. The finite-population correction is effectively very close to one for this sample.

## Reproduce

Run from this directory with the sampled CSV produced by sample_worldcover.py:

    python crosswalk_sensitivity.py worldcover-fiji-sample.csv \
      --stratum-area-weights '{"water":0.011331967836,"mangrove":0.022598921173,"bare_soil_rock":0.003445902118,"urban":0.004378396325,"agriculture":0.090917519797,"grassland":0.096242589869,"shrubland":0.031660519822,"tree":0.739424183060}' \
      --stratum-population-sizes '{"water":1779768,"mangrove":3549325,"bare_soil_rock":541204,"urban":687659,"agriculture":14279258,"grassland":15115599,"shrubland":4972515,"tree":116131948}' \
      --json-out worldcover-fiji-crosswalk-sensitivity.json

The JSON report records the input CSV SHA-256, all scenario definitions, estimates, paired standard errors, intervals and stratum diagnostics. The GitHub Actions rehearsal runs this command and uploads the JSON alongside the extracted sample and primary accuracy reports.

## Interpretation and limits

- The sensitivity result is robust in direction across these three declared scenarios: the original Fiji map has higher estimated OA than WorldCover on this sample.
- This does not prove that one product is universally more accurate, more useful or better for every application. The estimate applies to the eligible Fiji sampling frame represented by the supplied weights, excluding training Tikinas.
- The Fiji reference labels are supplied visual interpretations, not independently field-verified labels.
- The class groupings are analyst-defined. A domain specialist should review them against the actual class definitions and intended use before adopting one as the primary legend.
- The broad scenario deliberately sacrifices thematic detail. It is useful as a sensitivity view, not necessarily the right reporting legend.
- The analysis assumes independent simple random sampling without replacement within each original sampling stratum. It does not account for reference-label uncertainty, uncertainty in supplied area weights, positional mismatch, mixed pixels or temporal differences.
- The reported intervals are approximate Wald intervals. They do not include uncertainty arising from choosing the crosswalk itself.

The conclusion is therefore narrower than “WorldCover is 8.4 points worse”: **under the documented sample, reference labels and three tested legend choices, the estimated paired accuracy difference remains in favour of the original Fiji map.**
