# Class-specific error investigation: Fiji 2021 and ESA WorldCover 2021 v200

**Status:** Executed on the same 834-point probability sample used for the Fiji–WorldCover comparison. The analysis decomposes design-weighted confusion by reference class and mapped class. It identifies where estimated error mass sits; it does not establish why any classification error occurred.

## Design and estimator

The sample was stratified by the original Fiji 2021 mapped class. Each error-matrix cell is estimated as

\[
\hat p_{ij}=\sum_h W_h\frac{n_{hij}}{n_h},
\]

where \(h\) indexes the original Fiji sampling strata, \(W_h\) is the supplied eligible-domain area proportion, and \(n_{hij}/n_h\) is the observed within-stratum proportion assigned to mapped class \(i\) and reference class \(j\).

The original Fiji map class is represented by \`sampling_stratum\`, because that map defined the sampling strata. WorldCover's mapped class is the raster class sampled at the same point. Producer's accuracy is the diagonal cell divided by the estimated reference-class area; user's accuracy is the diagonal cell divided by the estimated mapped-class area. Class accuracy ratios are point estimates here; the script does not report confidence intervals for those ratios.

## Overall and reference-class results

The reproduced overall accuracies are 82.51% for the Fiji map and 74.12% for WorldCover. The class-specific producer's accuracy comparison is:

| Reference class | Sample points | Estimated reference area | Fiji producer's accuracy | WorldCover producer's accuracy | Difference (WorldCover − Fiji) |
|---|---:|---:|---:|---:|---:|
| Shrubland | 109 | 11.44% | 15.22% | 0.00% | −15.22 pp |
| Agriculture | 69 | 5.64% | 88.70% | 3.23% | −85.48 pp |
| Grassland | 135 | 10.20% | 66.02% | 62.01% | −4.02 pp |
| Tree | 187 | 67.92% | 96.69% | 95.45% | −1.23 pp |
| Mangrove | 101 | 2.67% | 76.25% | 70.16% | −6.09 pp |
| Bare soil / rock | 86 | 0.65% | 28.06% | 3.75% | −24.31 pp |
| Urban | 48 | 0.48% | 40.18% | 14.61% | −25.57 pp |
| Water | 99 | 1.01% | 94.50% | 80.98% | −13.52 pp |

The largest WorldCover omission-error contributions to the eligible-domain estimate are shrubland (11.44 percentage points), agriculture (5.46 pp), grassland (3.88 pp) and tree (3.09 pp). These design-weighted contributions are not rankings by raw error count.

## Largest WorldCover map-to-reference transitions

| WorldCover class | Reference class | Sample points | Weighted error contribution |
|---|---|---:|---:|
| Tree | Shrubland | 89 | 10.13 pp |
| Tree | Grassland | 52 | 3.22 pp |
| Grassland | Agriculture | 38 | 3.13 pp |
| Tree | Agriculture | 25 | 2.13 pp |
| Herbaceous wetland | Tree | 7 | 1.75 pp |
| Grassland | Shrubland | 16 | 1.17 pp |
| Water | Tree | 6 | 1.13 pp |
| Tree | Mangrove | 8 | 0.71 pp |

The largest transition is WorldCover tree at reference shrubland points. The strict working crosswalk has no WorldCover shrubland predictions in this sample, while the reference interpretation includes an estimated 11.44% shrubland area. This is a strong signal for targeted legend and image review, but not proof that WorldCover's shrubland concept is absent or that every affected point is a classifier error.

Agriculture is another major discrepancy: 69 sampled points carry the reference agriculture label, but WorldCover predicts agriculture at only two points. Most of the weighted omission contribution appears as WorldCover grassland (3.13 pp) or tree (2.13 pp). Bare soil/rock and urban also have low producer's accuracy, but their estimated reference-area shares are small in this eligible domain.

## Mapped-class diagnostics

WorldCover's estimated mapped-area shares and user's accuracy reveal additional imbalance:

| WorldCover class | Sample predictions | Estimated mapped area | User's accuracy |
|---|---:|---:|---:|
| Tree | 383 | 81.46% | 79.58% |
| Grassland | 190 | 11.33% | 55.85% |
| Water | 110 | 2.31% | 35.33% |
| Mangrove | 102 | 1.98% | 94.43% |
| Herbaceous wetland | 12 | 2.49% | 0.00% under the strict working crosswalk |
| Urban | 28 | 0.21% | 32.95% |
| Agriculture | 2 | 0.18% | 100.00% from only two predictions |
| Bare soil / rock | 7 | 0.03% | 84.79% from seven predictions |
| Shrubland | 0 | 0.00% | Undefined; no WorldCover shrubland predictions in this sample |

The 100% user's accuracy for agriculture is not evidence of strong class performance: it is based on only two WorldCover agriculture predictions, while most reference agriculture points are omitted. Similarly, the seven bare-soil/rock predictions are too few for a confident operational conclusion. Herbaceous wetland has no counterpart in the eight-class reference legend; its strict-crosswalk user's accuracy of zero is a legend-harmonisation result as well as a disagreement count. Crosswalk sensitivity is reported separately.

## What the analysis suggests—and what it cannot establish

Three review priorities emerge:

1. **Woody/open-vegetation boundary:** inspect the tree–shrubland and tree–grassland transitions first. Confirm whether the two products' class definitions and the visual reference protocol distinguish shrubland, woody savanna, open woodland and grass-dominated cover consistently.
2. **Agriculture mapping:** inspect reference agriculture points mapped as grassland or tree. Potential explanations include seasonal/temporal mismatch, fallow or mixed land cover, spatial support, reference interpretation, and product classification. The sample alone cannot choose among them.
3. **Rare and semantically difficult classes:** investigate bare soil/rock, urban and herbaceous wetland with the legend definitions and imagery in view. The mapped-class sample counts are small, so class-specific ratios are fragile.

These are hypotheses for review, not causal findings. The sample uses supplied visual reference labels, not independent field verification. WorldCover was sampled from the single 10 m cell containing each point. Positional tolerance, mixed-pixel effects, temporal mismatch and reference-label uncertainty are not modelled. The target frame excludes Tikinas used for training samples. The strict class crosswalk is provisional. The estimates are conditional on the supplied eligible-domain area weights.

## Reproduction

From this directory, using \`worldcover-fiji-sample.csv\` generated by the successful WorldCover rehearsal:

\`\`\`bash
python -m unittest -v test_class_error_analysis.py
python class_error_analysis.py worldcover-fiji-sample.csv \\
  --stratum-area-weights '{"water":0.011331967836,"mangrove":0.022598921173,"bare_soil_rock":0.003445902118,"urban":0.004378396325,"agriculture":0.090917519797,"grassland":0.096242589869,"shrubland":0.031660519822,"tree":0.739424183060}' \\
  --json-out fiji-worldcover-class-error-analysis.json
\`\`\`

The JSON contains both area-adjusted error matrices, class-level producer's and user's accuracy, weighted omission and commission contributions, and the dominant map-to-reference transitions. It records the input CSV SHA-256. The workflow uploads this JSON with the other rehearsal outputs.
