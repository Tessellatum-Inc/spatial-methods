"""Coverage experiment for the matched-strata equal-block contrast estimand.

Each block contains shared strata. Within each stratum, target and reference
samples estimate a contrast; stratum contrasts are averaged equally within
block, then eligible blocks are averaged equally. A latent spatial field drives
block-level contrasts. Coverage is evaluated against the finite-population
mean of the latent equal-stratum block contrasts, not against a pixel-weighted
contrast. This remains a stylized synthetic design, not a Nairobi calibration.
"""
from __future__ import annotations
import json
import numpy as np

from explorations.radar.spatial_moving_block_bootstrap import moving_spatial_block_bootstrap_interval
from explorations.radar.spatial_hac import spatial_hac_mean_interval


def spatial_field(size, rho, rng):
    z=rng.normal(size=(size,size))
    scale=np.sqrt(1-rho*rho)
    for r in range(1,size):
        z[r,:]=rho*z[r-1,:]+scale*z[r,:]
    for c in range(1,size):
        z[:,c]=rho*z[:,c-1]+scale*z[:,c]
    return z


def wilson(successes,trials,z=1.959963984540054):
    p=successes/trials; d=1+z*z/trials
    centre=(p+z*z/(2*trials))/d
    half=z*np.sqrt(p*(1-p)/trials+z*z/(4*trials*trials))/d
    return [float(centre-half),float(centre+half)]


def equal_stratum_block_contrast(stratum_contrasts):
    """Average shared-stratum contrasts equally within one block."""
    values=np.asarray(stratum_contrasts,dtype=float)
    if values.ndim!=1 or values.size==0 or not np.isfinite(values).all():
        raise ValueError("stratum_contrasts must be a non-empty finite vector")
    return float(values.mean())


def equal_eligible_block_mean(block_contrasts):
    """Average eligible block contrasts equally, never pixel-weighting blocks."""
    values=np.asarray(block_contrasts,dtype=float)
    if values.ndim!=1 or values.size==0 or not np.isfinite(values).all():
        raise ValueError("block_contrasts must be a non-empty finite vector")
    return float(values.mean())


def one_realization(size,rho,rng,informative=False):
    latent=spatial_field(size,rho,rng)*0.7
    ids=np.arange(size*size,dtype=np.int64)
    # Baseline eligible population represents blocks with common matched support.
    baseline_eligible=rng.random(size*size)>=0.08
    population_truth=float(latent.ravel()[baseline_eligible].mean())
    eligible=baseline_eligible.copy()
    if informative:
        # Deliberately remove high-contrast blocks after defining the target population.
        cutoff=np.quantile(latent,0.80)
        eligible &= latent.ravel()<=cutoff
    block_observed=[]; kept_ids=[]
    for bid in ids[eligible]:
        r,c=divmod(int(bid),size)
        n_strata=int(rng.integers(2,6))
        # Heterogeneous stratum effects, centered within each block so their
        # equal-stratum mean is exactly the latent block contrast.
        heterogeneity=rng.normal(0,0.25,size=n_strata)
        heterogeneity-=heterogeneity.mean()
        true_strata=latent[r,c]+heterogeneity
        estimated=[]
        for delta in true_strata:
            # Unequal pixel counts across target/reference and strata.
            nt=int(rng.integers(8,80)); nr=int(rng.integers(8,80))
            target=delta+rng.normal(0,1.0,size=nt)
            reference=rng.normal(0,1.0,size=nr)
            estimated.append(float(target.mean()-reference.mean()))
        block_observed.append(equal_stratum_block_contrast(estimated))
        kept_ids.append(int(bid))
    return np.asarray(kept_ids),np.asarray(block_observed),population_truth


def run(simulations=100,size=24,correlations=(0.3,0.6,0.8),
        bootstrap_replicates=250,widths=(3,5,7),hac_bandwidths=(3,5,7),
        seed=20261204):
    rng=np.random.default_rng(seed); results=[]
    for informative in (False,True):
      for rho in correlations:
        configs=[("moving_window",w) for w in widths]+[("spatial_hac",w) for w in hac_bandwidths]
        stats={(m,w):{"covered":0,"widths":[],"biases":[],"valid":0,"unsupported":0}
               for m,w in configs}
        support=[]
        for trial in range(simulations):
            ids,observed,truth=one_realization(size,rho,rng,informative)
            support.append(len(ids))
            # Both interval procedures must preserve the pre-declared
            # equal-eligible-block point estimand. Fail loudly if a future
            # estimator edit silently changes its weighting.
            expected_estimate=equal_eligible_block_mean(observed)
            for method,w in configs:
                if method=="moving_window":
                    res=moving_spatial_block_bootstrap_interval(ids,observed,
                        grid_columns=size,window_width_blocks=w,
                        replicates=bootstrap_replicates,seed=seed+trial*97+w,
                        min_windows=20,min_blocks=20)
                    lo,hi,estimate=res["lower_95_db"],res["upper_95_db"],res["estimate_db"]
                else:
                    res=spatial_hac_mean_interval(ids,observed,grid_columns=size,
                        bandwidth_rows=w,bandwidth_columns=w,min_blocks=20)
                    lo,hi,estimate=res["lower"],res["upper"],res["estimate"]
                if estimate is not None and not np.isclose(
                    estimate,expected_estimate,rtol=1e-12,atol=1e-12
                ):
                    raise AssertionError(
                        f"{method} point estimate changed the equal-block estimand: "
                        f"{estimate} != {expected_estimate}"
                    )
                s=stats[(method,w)]
                if lo is None or hi is None:
                    s["unsupported"]+=1; continue
                s["valid"]+=1
                s["covered"]+=int(lo<=truth<=hi)
                s["widths"].append(float(hi-lo))
                s["biases"].append(float(estimate-truth))
        for (method,w),s in stats.items():
            n=s["valid"]
            results.append({"informative_eligibility":informative,"rho":rho,
                "method":method,"width_or_bandwidth":w,"simulations":simulations,
                "valid_intervals":n,"unsupported_intervals":s["unsupported"],
                "coverage":s["covered"]/n if n else None,
                "coverage_wilson_95":wilson(s["covered"],n) if n else None,
                "mean_interval_width":float(np.mean(s["widths"])) if n else None,
                "mean_estimate_bias":float(np.mean(s["biases"])) if n else None,
                "mean_eligible_blocks":float(np.mean(support))})
    return {"schema":"tessellatum.matched-strata-equal-block-contrast.v1",
      "design":"Matched stratum contrasts averaged equally within block; eligible block contrasts averaged equally across blocks.",
      "grid_size":[size,size],"seed":seed,"results":results,
      "target":"Finite-population mean of latent equal-stratum block contrasts among baseline-eligible blocks, before any informative selection.",
      "informative_eligibility":"When enabled, blocks above the 80th percentile of latent contrast are preferentially excluded after the baseline target population is defined; intervals are judged against that pre-selection target.",
      "limitations":["Synthetic block/stratum structure; not the Nairobi R130 data-generating process.",
        "Pixel-level noise is Gaussian and independent within strata.",
        "Only moving-window bootstrap and spatial HAC are compared; subsampling is omitted because its irregular-mask contract is restrictive.",
        "Informative eligibility is not corrected; under that condition coverage is assessed against the pre-selection population target.",
        "No nominal coverage claim or automatic tuning selection."]}


if __name__=="__main__":
    print(json.dumps(run(),indent=2))
