"""Monte Carlo coverage experiment for moving spatial-block bootstrap.

Run from repository root:
    python explorations/radar/simulate_moving_spatial_block_bootstrap.py

The data-generating process is a mean-zero separable Gaussian AR(1) field on a
regular square lattice. This is a controlled diagnostic, not a model of the
Nairobi residual process. Coverage is assessed for the known population mean
of zero. Width 1 is the ordinary independent-block bootstrap comparator.
"""
from __future__ import annotations

import argparse
import json
import numpy as np

from explorations.radar.spatial_moving_block_bootstrap import (
    moving_spatial_block_bootstrap_interval,
)


def separable_ar1_field(size: int, rho: float, rng: np.random.Generator) -> np.ndarray:
    field = rng.normal(size=(size, size))
    innovation_scale = np.sqrt(1.0 - rho * rho)
    for row in range(1, size):
        field[row, :] = (
            rho * field[row - 1, :] + innovation_scale * field[row, :]
        )
    for col in range(1, size):
        field[:, col] = (
            rho * field[:, col - 1] + innovation_scale * field[:, col]
        )
    return field


def run_simulation(
    *, simulations: int = 150, bootstrap_replicates: int = 400,
    grid_size: int = 30, correlations=(0.3, 0.6, 0.8),
    widths=(1, 2, 3, 4, 5), seed: int = 20261126,
):
    rng = np.random.default_rng(seed)
    ids = np.arange(grid_size * grid_size, dtype=np.int64)
    rows = []
    for rho in correlations:
        for width in widths:
            covered = 0
            interval_widths = []
            for trial in range(simulations):
                field = separable_ar1_field(grid_size, rho, rng).ravel()
                result = moving_spatial_block_bootstrap_interval(
                    ids, field,
                    grid_columns=grid_size,
                    window_width_blocks=width,
                    replicates=bootstrap_replicates,
                    seed=200000 + trial,
                    min_windows=20,
                )
                lo, hi = result["lower_95_db"], result["upper_95_db"]
                covered += int(lo <= 0.0 <= hi)
                interval_widths.append(hi - lo)
            rows.append({
                "rho": float(rho),
                "window_width_blocks": int(width),
                "simulations": int(simulations),
                "bootstrap_replicates": int(bootstrap_replicates),
                "coverage": covered / simulations,
                "covered_simulations": int(covered),
                "mean_interval_width": float(np.mean(interval_widths)),
                "median_interval_width": float(np.median(interval_widths)),
            })
    return {
        "schema": "tessellatum.moving-spatial-block-bootstrap-simulation.v1",
        "data_generating_process": "mean-zero separable Gaussian AR(1) field",
        "grid_size": [int(grid_size), int(grid_size)],
        "seed": int(seed),
        "results": rows,
        "limitations": [
            "Synthetic stationary Gaussian fields are not a model of Nairobi residuals.",
            "Only the mean-zero population estimand is evaluated.",
            "Coverage estimates have Monte Carlo error and are not proof of nominal coverage.",
            "No irregular-mask or nonstationary scenarios are included in this initial experiment.",
        ],
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--simulations", type=int, default=150)
    parser.add_argument("--bootstrap-replicates", type=int, default=400)
    parser.add_argument("--grid-size", type=int, default=30)
    args = parser.parse_args()
    print(json.dumps(run_simulation(
        simulations=args.simulations,
        bootstrap_replicates=args.bootstrap_replicates,
        grid_size=args.grid_size,
    ), indent=2))
