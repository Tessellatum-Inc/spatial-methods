"""Monte Carlo coverage diagnostic for product-Bartlett spatial HAC intervals."""
from __future__ import annotations

import json
import numpy as np

from explorations.radar.simulate_moving_spatial_block_bootstrap import separable_ar1_field
from explorations.radar.spatial_hac import spatial_hac_mean_interval


def wilson(successes: int, trials: int, z: float = 1.959963984540054):
    p = successes / trials
    den = 1 + z*z/trials
    centre = (p + z*z/(2*trials)) / den
    half = z * np.sqrt(p*(1-p)/trials + z*z/(4*trials*trials)) / den
    return [float(centre-half), float(centre+half)]


def run(simulations=150, grid_size=30, correlations=(0.3, 0.6, 0.8),
        bandwidths=(1, 2, 3, 4, 6, 8, 12), seed=20261128):
    rng = np.random.default_rng(seed)
    ids = np.arange(grid_size*grid_size, dtype=np.int64)
    rows = []
    for rho in correlations:
        fields = [separable_ar1_field(grid_size, rho, rng).ravel()
                  for _ in range(simulations)]
        for h in bandwidths:
            covered, widths, ses = 0, [], []
            for y in fields:
                result = spatial_hac_mean_interval(
                    ids, y, grid_columns=grid_size,
                    bandwidth_rows=h, bandwidth_columns=h,
                    confidence_level=0.95, min_blocks=20,
                )
                covered += int(result["lower"] <= 0.0 <= result["upper"])
                widths.append(result["upper"] - result["lower"])
                ses.append(result["standard_error"])
            rows.append({
                "rho": float(rho), "bandwidth_blocks": int(h),
                "simulations": int(simulations), "coverage": covered/simulations,
                "covered_simulations": covered,
                "coverage_wilson_95": wilson(covered, simulations),
                "mean_interval_width": float(np.mean(widths)),
                "median_interval_width": float(np.median(widths)),
                "mean_standard_error": float(np.mean(ses)),
            })
    return {
        "schema": "tessellatum.spatial-hac-coverage.v1",
        "estimator": "equal-block mean with product-Bartlett spatial HAC variance",
        "data_generating_process": "mean-zero separable Gaussian AR(1) field",
        "grid_size": [grid_size, grid_size], "seed": seed,
        "results": rows,
        "limitations": [
            "Stationary isotropic Gaussian fields only.",
            "Complete regular grids only; no missingness or anisotropy.",
            "Normal critical values and finite-sample bandwidths are exploratory.",
            "No claim of nominal coverage or universal bandwidth selection.",
        ],
    }


if __name__ == "__main__":
    print(json.dumps(run(), indent=2))
