# Spatial distribution-shift statistics

NumPy/SciPy teaching implementations of:
- unbiased squared maximum mean discrepancy (MMD) with a Gaussian RBF kernel;
- unbiased sample energy-distance statistic;
- a reproducible row-level permutation test for MMD (independent/exchangeable rows only);
- a whole-block MMD permutation test for equal-sized blocks under an explicit independent/exchangeable-block null;
- a nearest-neighbour predictor-space applicability envelope, calibrated by leave-one-out training distances, with optional feature weights.

Inputs are finite feature matrices with matching dimensions. MMD bandwidth is in feature-space units; standardise features deliberately and report the choice. Both unbiased finite-sample U-statistics can be negative and are not clipped; do not interpret an individual estimate as a guaranteed non-negative distance.

The permutation test assumes exchangeable independent rows. It is not valid for spatially autocorrelated samples without a defensible block/cluster permutation or other spatial null design. The applicability-envelope function is a transparent nearest-neighbour teaching baseline, not an exact Meyer–Pebesma AOA implementation or prediction-error guarantee. It does not use model-derived variable importance or a spatially calibrated threshold. Whole-block permutation is a spatially structured baseline only when the chosen blocks are genuinely independent/exchangeable and share comparable sampling designs; it does not guarantee valid spatial inference. Domain classifiers and kernel mean matching remain open.

Run python -m pip install -r requirements.txt and python -m pytest -q.


## Two complementary block-permutation designs

- `block_mmd_permutation_test` accepts equal-sized blocks and permutes whole blocks between source and target samples before evaluating the existing observation-level MMD statistic.
- `spatial_block_mmd_test` accepts variable-sized blocks, builds a block-to-block kernel by averaging RBF similarities across observation pairs, and permutes whole-block labels in an unbiased block-level MMD statistic.

Both methods require the blocks to be exchangeable under the null. Defining spatial blocks does not itself guarantee independence or exchangeability; choose block size and design from the dependence structure and sampling question.
