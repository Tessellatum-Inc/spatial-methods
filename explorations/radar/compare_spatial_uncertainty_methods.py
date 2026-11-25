"""Paired comparison of three spatial uncertainty candidates on identical fields."""
from __future__ import annotations
import json
import numpy as np

from explorations.radar.simulate_moving_spatial_block_bootstrap import separable_ar1_field
from explorations.radar.spatial_moving_block_bootstrap import moving_spatial_block_bootstrap_interval
from explorations.radar.spatial_hac import spatial_hac_mean_interval
from explorations.radar.spatial_subsampling import spatial_subsampling_mean_interval


def wilson(successes, trials, z=1.959963984540054):
    p=successes/trials; den=1+z*z/trials
    centre=(p+z*z/(2*trials))/den
    half=z*np.sqrt(p*(1-p)/trials+z*z/(4*trials*trials))/den
    return [float(centre-half),float(centre+half)]


def run(simulations=100, grid_size=30, correlations=(0.3,0.6,0.8),
        widths=(4,8,12), bootstrap_replicates=300, seed=20261130):
    rng=np.random.default_rng(seed)
    ids=np.arange(grid_size*grid_size,dtype=np.int64)
    output=[]
    for rho in correlations:
        counts={(method,w):0 for method in ("moving_window","spatial_hac","subsampling") for w in widths}
        interval_widths={(method,w):[] for method in ("moving_window","spatial_hac","subsampling") for w in widths}
        for trial in range(simulations):
            # The exact same generated field is passed to all methods and widths.
            y=separable_ar1_field(grid_size,rho,rng).ravel()
            for w in widths:
                results={
                    "moving_window": moving_spatial_block_bootstrap_interval(
                        ids,y,grid_columns=grid_size,window_width_blocks=w,
                        replicates=bootstrap_replicates,seed=seed+trial*100+w,
                        min_windows=20,min_blocks=20),
                    "spatial_hac": spatial_hac_mean_interval(
                        ids,y,grid_columns=grid_size,bandwidth_rows=w,
                        bandwidth_columns=w,confidence_level=0.95,min_blocks=20),
                    "subsampling": spatial_subsampling_mean_interval(
                        ids,y,grid_rows=grid_size,grid_columns=grid_size,
                        subsample_width_blocks=w,confidence_level=0.95,
                        min_subwindows=20),
                }
                for method,result in results.items():
                    counts[(method,w)]+=int(result["lower_95_db"] <= 0 <= result["upper_95_db"]) if method=="moving_window" else int(result["lower"] <= 0 <= result["upper"])
                    lo=result["lower_95_db"] if method=="moving_window" else result["lower"]
                    hi=result["upper_95_db"] if method=="moving_window" else result["upper"]
                    interval_widths[(method,w)].append(hi-lo)
        for (method,w),covered in counts.items():
            output.append({
                "rho":float(rho),"method":method,"tuning_width_blocks":int(w),
                "simulations":int(simulations),"covered_simulations":int(covered),
                "coverage":covered/simulations,"coverage_wilson_95":wilson(covered,simulations),
                "mean_interval_width":float(np.mean(interval_widths[(method,w)])),
                "median_interval_width":float(np.median(interval_widths[(method,w)])),
            })
    return {
        "schema":"tessellatum.paired-spatial-uncertainty-comparison.v1",
        "design":"Same simulated field realization evaluated by all three methods and all tuning widths.",
        "data_generating_process":"mean-zero separable Gaussian AR(1) field",
        "grid_size":[grid_size,grid_size],"seed":seed,
        "simulations_per_correlation":simulations,
        "bootstrap_replicates_moving_window":bootstrap_replicates,
        "results":output,
        "limitations":[
            "Stationary isotropic Gaussian fields and complete regular grids only.",
            "The three estimators use different tuning interpretations; width labels are not identical statistical objects.",
            "This comparison does not establish coverage for irregular masks, anisotropy, nonstationarity or matched block contrasts.",
            "Coverage is Monte Carlo estimated and the moving-window percentile method has bootstrap simulation error."
        ]
    }


if __name__=="__main__":
    print(json.dumps(run(),indent=2))
