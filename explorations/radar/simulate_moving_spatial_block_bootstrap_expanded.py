"""Expanded window-width diagnostic for the moving spatial-block bootstrap.

Extends the first dense-grid experiment to wider windows. This is a diagnostic
for finite-domain effects, not a width-selection or calibration procedure.
"""
from __future__ import annotations

import json
from explorations.radar.simulate_moving_spatial_block_bootstrap import run_simulation

if __name__ == "__main__":
    result = run_simulation(
        simulations=150,
        bootstrap_replicates=400,
        grid_size=30,
        correlations=(0.3, 0.6, 0.8),
        widths=(1, 2, 3, 4, 5, 6, 8, 10, 12),
        seed=20261127,
    )
    result["schema"] = "tessellatum.moving-spatial-block-bootstrap-expanded-widths.v1"
    result["purpose"] = (
        "Assess whether wider moving windows approach nominal coverage "
        "on a finite 30x30 grid; not a calibration claim."
    )
    result["limitations"].append(
        "Wider windows leave fewer effectively independent sampled windows; "
        "the experiment does not establish a generally valid width."
    )
    print(json.dumps(result, indent=2))
