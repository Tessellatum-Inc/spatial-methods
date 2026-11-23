# Topographic position index (TPI)

## Definition

For elevation raster \(z\), the focal topographic position index is

\[
\operatorname{TPI}_i = z_i - \frac{1}{|N_i|}\sum_{j\in N_i} z_j,
\]

where \(N_i\) is the valid-cell neighbourhood around cell \(i\). This implementation uses a square odd-sized window and includes the centre cell in its mean.

- Positive TPI: the cell is higher than its local surroundings (ridge-like).
- Negative TPI: the cell is lower than its local surroundings (valley-like).
- Near-zero TPI: the cell is close to its local neighbourhood mean.

## Implementation contract

The topographic_position_index function uses a summed-area/integral image for both elevation sums and valid-cell counts. It runs in O(rows × columns) time and O(rows × columns) additional memory, rather than scanning every window independently.

The window must be an odd integer of at least 3. Only complete windows are evaluated, so the outer half-window border is NaN. Non-finite cells are excluded from sums; a result is returned only if the valid-cell fraction meets the configured threshold and the centre cell is valid. The default threshold of 1.0 requires a fully valid window.

## Interpretation and limitations

TPI is scale-dependent. A small window describes microtopography; a larger window describes broader landform position. Choose window dimensions in map units relative to the landforms of interest, and consider multi-scale analysis where appropriate. The square window is not circular or terrain-adaptive. TPI alone does not classify landforms, infer process, or account for slope, geology, drainage or spatially varying terrain structure. Use a projected, appropriately sampled elevation model and document the window size and NoData policy.

## Verification

Tests cover constant surfaces, positive and negative local anomalies, larger windows, NoData threshold behaviour, invalid parameters and non-2D inputs.
