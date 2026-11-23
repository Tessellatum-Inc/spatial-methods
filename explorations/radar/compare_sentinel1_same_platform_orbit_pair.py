#!/usr/bin/env python3
"""Compare same-platform ascending Sentinel-1 orbit tracks on shared valid pixels."""
from __future__ import annotations
import argparse, json
from pathlib import Path
import numpy as np
import rasterio

def summarize_relation(ellipsoid, rtc, area, angle, mask):
    ell=np.asarray(ellipsoid,dtype=np.float64)[mask]
    rt=np.asarray(rtc,dtype=np.float64)[mask]
    ar=np.asarray(area,dtype=np.float64)[mask]
    ang=np.asarray(angle,dtype=np.float64)[mask]
    valid=(ell>0)&(rt>0)&(ar>0)&np.isfinite(ell)&np.isfinite(rt)&np.isfinite(ar)&np.isfinite(ang)&(ang>0)&(ang<90)
    ell,rt,ar,ang=ell[valid],rt[valid],ar[valid],ang[valid]
    if len(ar)<100: raise ValueError("Too few shared positive pixels for relation metrics")
    x=-10.0*np.log10(ar); y=10.0*np.log10(rt)-10.0*np.log10(ell)
    slope,intercept=np.polyfit(x,y,1)
    fitted=slope*x+intercept
    ss_res=float(np.sum((y-fitted)**2)); ss_tot=float(np.sum((y-y.mean())**2))
    residual=y-x; centered=residual-np.median(residual)
    local_angle_term=-10.0*np.log10(np.tan(np.deg2rad(ang)))
    geometry_adjusted=residual-local_angle_term
    return {"pixels":int(len(x)),"ols_slope":float(slope),"ols_intercept_db":float(intercept),
        "ols_r_squared":float(1-ss_res/ss_tot) if ss_tot>0 else None,
        "median_direct_rtc_minus_ellipsoid_db":float(np.median(y)),
        "mean_absolute_direct_rtc_minus_ellipsoid_db":float(np.mean(np.abs(y))),
        "p95_absolute_direct_rtc_minus_ellipsoid_db":float(np.percentile(np.abs(y),95)),
        "median_observed_minus_area_factor_db":float(np.median(residual)),
        "mean_absolute_area_factor_residual_db":float(np.mean(np.abs(residual))),
        "p95_absolute_centered_area_factor_residual_db":float(np.percentile(np.abs(centered),95)),
        "median_local_angle_term_db":float(np.median(local_angle_term)),
        "median_geometry_adjusted_residual_db":float(np.median(geometry_adjusted)),
        "mean_absolute_geometry_adjusted_residual_db":float(np.mean(np.abs(geometry_adjusted))),
        "p95_absolute_geometry_adjusted_residual_db":float(np.percentile(np.abs(geometry_adjusted),95)),
        "median_scattering_area":float(np.median(ar)),
        "median_local_incidence_angle_degrees":float(np.median(ang)),
        "p10_local_incidence_angle_degrees":float(np.percentile(ang,10)),
        "p90_local_incidence_angle_degrees":float(np.percentile(ang,90)),
        "area_factor_residual_vs_angle_correlation":float(np.corrcoef(residual,ang)[0,1]) if np.std(residual)>0 and np.std(ang)>0 else None}

def load_tracks(root):
    tracks={}
    for stack_path in sorted(root.rglob("sentinel1_nairobi_temporal_stack.metadata.json")):
        stack=json.loads(stack_path.read_text(encoding="utf-8"))
        orbit=stack.get("processing_config",{}).get("relative_orbit")
        if orbit not in (57,130): continue
        scenes=[]
        for scene in stack.get("scenes",[]):
            stamp=scene["catalog_item_datetime_utc"][:19].replace("-","").replace(":","")+"Z"
            ell=stack_path.parent/scene["output"]["file"]
            rtc=stack_path.parent/"terrain_aux"/f"sentinel1_nairobi_{stamp}_gamma0-terrain-rtc.tif"
            if not ell.exists() or not rtc.exists(): raise FileNotFoundError(f"Missing raster pair for {stamp}")
            scenes.append({"datetime_utc":scene["catalog_item_datetime_utc"],"ellipsoid":ell,"rtc":rtc})
        if len(scenes)<2: raise ValueError(f"Orbit {orbit} has fewer than two scenes")
        tracks[int(orbit)]=scenes
    if set(tracks)!={57,130}: raise ValueError(f"Expected R057 and R130 artifacts; found {sorted(tracks)}")
    return tracks

def run(input_dir:Path,output:Path):
    tracks=load_tracks(input_dir); masks=[]; grid=None
    for scenes in tracks.values():
        for scene in scenes:
            with rasterio.open(scene["ellipsoid"]) as e, rasterio.open(scene["rtc"]) as r:
                signature=(e.crs,e.transform,e.width,e.height)
                if grid is None: grid=signature
                if signature!=grid or signature!=(r.crs,r.transform,r.width,r.height):
                    raise ValueError("Orbit artifacts do not share an identical ellipsoid/RTC grid")
                masks.append((e.read(3)>0.5)&(r.read(6)>0.5))
    common=np.logical_and.reduce(masks)
    if not common.any(): raise ValueError("No pixels are common to all scenes and both processing branches")
    results={}
    for orbit,scenes in tracks.items():
        per_scene=[]
        for scene in scenes:
            with rasterio.open(scene["ellipsoid"]) as e, rasterio.open(scene["rtc"]) as r:
                eb=e.read([1,2]); rb=r.read([1,2,3,4])
            per_scene.append({"datetime_utc":scene["datetime_utc"],"polarizations":{
                pol:summarize_relation(eb[i],rb[i],rb[2],rb[3],common) for i,pol in enumerate(("VV","VH"))}})
        aggregate={}
        for pol in ("VV","VH"):
            rows=[s["polarizations"][pol] for s in per_scene]
            keys=("ols_slope","ols_intercept_db","ols_r_squared","median_direct_rtc_minus_ellipsoid_db",
                "mean_absolute_direct_rtc_minus_ellipsoid_db","p95_absolute_direct_rtc_minus_ellipsoid_db",
                "median_observed_minus_area_factor_db",
                "mean_absolute_area_factor_residual_db","p95_absolute_centered_area_factor_residual_db",
                "median_local_angle_term_db","median_geometry_adjusted_residual_db",
                "mean_absolute_geometry_adjusted_residual_db","p95_absolute_geometry_adjusted_residual_db","median_scattering_area",
                "median_local_incidence_angle_degrees","p10_local_incidence_angle_degrees","p90_local_incidence_angle_degrees",
                "area_factor_residual_vs_angle_correlation")
            aggregate[pol]={key:float(np.mean([row[key] for row in rows])) for key in keys}
            aggregate[pol]["pixels_per_scene"]=int(min(row["pixels"] for row in rows))
        results[str(orbit)]={"scene_count":len(scenes),"scenes":per_scene,"mean_metrics_on_shared_mask":aggregate}
    report={"schema":"tessellatum.sentinel1.same-platform-orbit-pair-common-mask.v1",
        "platform":"Sentinel-1A","orbit_direction":"ASCENDING","relative_orbits":[57,130],
        "all_scene_pair_common_valid_pixels":int(common.sum()),
        "all_scene_pair_common_valid_fraction_of_requested_grid":float(common.mean()),
        "tracks":results,"analysis_ready":False,
        "interpretation":"R057 and R130 are compared on the same pixels valid in every acquisition and both processing branches.",
        "limitations":["This is one Nairobi site and two relative orbits, not independent-site validation.",
        "Acquisitions are not simultaneous; land-surface changes between dates remain possible.",
        "No stable radiometric reference or geodetic control is supplied.",
        "The fitted relation remains diagnostic and is not approved for normalization or change detection."]}
    output.parent.mkdir(parents=True,exist_ok=True); output.write_text(json.dumps(report,indent=2)+"\n",encoding="utf-8")
    print(f"Shared valid footprint: {common.mean():.4f} ({int(common.sum())} pixels)")
    print("Per-track mean metrics on the identical all-scenes common mask:")
    print(json.dumps({orbit:{"mean_metrics":data["mean_metrics_on_shared_mask"],"per_scene":data["scenes"]} for orbit,data in results.items()},sort_keys=True))
    return report

def main(argv=None):
    p=argparse.ArgumentParser(description=__doc__); p.add_argument("--input-dir",type=Path,required=True); p.add_argument("--output",type=Path,required=True)
    a=p.parse_args(argv)
    try: run(a.input_dir,a.output)
    except (OSError,ValueError,KeyError) as e: p.exit(2,f"Shared-footprint orbit comparison failed: {e}\n")
    return 0
if __name__=="__main__": raise SystemExit(main())
