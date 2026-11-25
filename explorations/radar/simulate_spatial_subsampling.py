"""Coverage diagnostic for fixed-size spatial subsampling intervals."""
from __future__ import annotations
import json
import numpy as np
from explorations.radar.simulate_moving_spatial_block_bootstrap import separable_ar1_field
from explorations.radar.spatial_subsampling import spatial_subsampling_mean_interval


def wilson(successes, trials, z=1.959963984540054):
    p=successes/trials; den=1+z*z/trials
    centre=(p+z*z/(2*trials))/den
    half=z*np.sqrt(p*(1-p)/trials+z*z/(4*trials*trials))/den
    return [float(centre-half),float(centre+half)]


def run(simulations=150, grid_size=30, correlations=(0.3,0.6,0.8),
        widths=(4,6,8,10,12,15,20), seed=20261129):
    rng=np.random.default_rng(seed); ids=np.arange(grid_size*grid_size,dtype=np.int64)
    rows=[]
    for rho in correlations:
        fields=[separable_ar1_field(grid_size,rho,rng).ravel() for _ in range(simulations)]
        for b in widths:
            covered=0; interval_widths=[]
            for y in fields:
                result=spatial_subsampling_mean_interval(
                    ids,y,grid_rows=grid_size,grid_columns=grid_size,
                    subsample_width_blocks=b,confidence_level=0.95,min_subwindows=20)
                covered+=int(result["lower"]<=0.0<=result["upper"])
                interval_widths.append(result["upper"]-result["lower"])
            rows.append({"rho":float(rho),"subsample_width_blocks":int(b),
                "simulations":int(simulations),"coverage":covered/simulations,
                "covered_simulations":covered,"coverage_wilson_95":wilson(covered,simulations),
                "mean_interval_width":float(np.mean(interval_widths)),
                "median_interval_width":float(np.median(interval_widths))})
    return {"schema":"tessellatum.spatial-subsampling-coverage.v1",
        "estimator":"fixed-size overlapping rectangular spatial subsampling",
        "data_generating_process":"mean-zero separable Gaussian AR(1) field",
        "grid_size":[grid_size,grid_size],"seed":seed,"results":rows,
        "limitations":["Stationary isotropic Gaussian fields only.",
        "Complete regular grids only; irregular masks are explicitly unsupported.",
        "Subsample widths and overlapping windows are finite-sample sensitivity choices.",
        "No claim of nominal coverage or universal subsample width selection."]}


if __name__=="__main__":
    print(json.dumps(run(),indent=2))
