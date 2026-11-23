#!/usr/bin/env python3
"""Validate RTC/ellipsoid backscatter relation over the independent Surat R009 site."""
from __future__ import annotations
import argparse, json, sys
from pathlib import Path
import numpy as np
import rasterio

TARGETS=[
 {"name":"Surat Basin 26","longitude":150.485114,"latitude":-27.258849},
 {"name":"Surat Basin 31","longitude":150.331548,"latitude":-27.207314},
 {"name":"Surat Basin 35","longitude":150.259625,"latitude":-27.085649},
]
SAMPLE_STEP=4
TARGET_EXCLUSION_RADIUS=15

def residual_stats(values):
    v=np.asarray(values,dtype=np.float64); v=v[np.isfinite(v)]
    if not len(v): raise ValueError("No finite residual samples")
    return {"count":int(len(v)),"median_db":float(np.median(v)),
        "mae_db":float(np.mean(np.abs(v))),"rmse_db":float(np.sqrt(np.mean(v*v))),
        "p95_absolute_db":float(np.percentile(np.abs(v),95)),
        "max_absolute_db":float(np.max(np.abs(v)))}

def relation_summary(delta_db,scattering_area,ellipsoid_angle_degrees):
    delta=np.asarray(delta_db,dtype=np.float64)
    area=np.asarray(scattering_area,dtype=np.float64)
    angle=np.asarray(ellipsoid_angle_degrees,dtype=np.float64)
    valid=np.isfinite(delta)&np.isfinite(area)&np.isfinite(angle)&(area>0)&(angle>0)&(angle<90)
    delta=delta[valid]; area=area[valid]; angle=angle[valid]
    if len(delta)<10: raise ValueError("Too few valid samples for relation summary")
    area_term=-10*np.log10(area)
    angle_term=-10*np.log10(np.tan(np.deg2rad(angle)))
    design=np.column_stack([np.ones(len(delta)),area_term])
    coefficients=np.linalg.lstsq(design,delta,rcond=None)[0]
    predicted=design@coefficients
    ss_res=float(np.sum((delta-predicted)**2)); ss_tot=float(np.sum((delta-np.mean(delta))**2))
    r2=1.0-ss_res/ss_tot if ss_tot>0 else None
    return {"sample_count":int(len(delta)),
        "area_only_ols":{"intercept_db":float(coefficients[0]),"slope":float(coefficients[1]),"r_squared":r2},
        "area_only_residual":residual_stats(delta-area_term),
        "area_plus_ellipsoid_angle_residual":residual_stats(delta-area_term-angle_term),
        "equation":"RTC_gamma0_dB - ellipsoid_gamma0_dB = -10log10(scatteringArea) - 10log10(tan(ellipsoid_incidence_angle))"}

def target_exclusion_mask(shape,transform,targets,radius):
    excluded=np.zeros(shape,dtype=bool)
    for target in targets:
        row,col=rasterio.transform.rowcol(transform,target["longitude"],target["latitude"])
        r0=max(0,row-radius); r1=min(shape[0],row+radius+1)
        c0=max(0,col-radius); c1=min(shape[1],col+radius+1)
        excluded[r0:r1,c0:c1]=True
    return excluded

def analyze(process_report,incidence_report,process_dir,angle_dir):
    scenes=process_report.get("scenes",[])
    angle_scenes=incidence_report.get("products",[])
    if len(scenes)!=4 or len(angle_scenes)!=4: raise ValueError("Expected four paired scenes and four incidence rasters")
    angles={x["datetime_utc"][:10]:x for x in angle_scenes}
    handles=[]; common=None; signature=None; records=[]
    try:
        for scene in scenes:
            date=scene["acquisition_datetime_utc"][:10]
            angle_record=angles.get(date)
            if angle_record is None: raise ValueError(f"Missing source incidence raster for {date}")
            ell_path=process_dir/scene["ellipsoid_file"]
            rtc_path=process_dir/scene["rtc_file"]
            angle_path=angle_dir/angle_record["output_file"]
            ell=rasterio.open(ell_path); rtc=rasterio.open(rtc_path); ang=rasterio.open(angle_path)
            handles.extend([ell,rtc,ang])
            sig=(ell.crs,ell.transform,ell.width,ell.height)
            if signature is None: signature=sig
            if sig!=signature or (rtc.crs,rtc.transform,rtc.width,rtc.height)!=signature or (ang.crs,ang.transform,ang.width,ang.height)!=signature:
                raise ValueError(f"Grid mismatch across scenes or source incidence raster for {date}")
            if ell.count!=3 or rtc.count!=6 or ang.count!=1: raise ValueError(f"Unexpected band count for {date}")
            em=ell.read(3)>0.5; rm=rtc.read(6)>0.5
            av=ang.read(1)
            valid=em&rm&np.isfinite(av)&(av>0)&(av<90)
            common=valid if common is None else common&valid
            records.append((date,ell,rtc,ang))
        excluded=target_exclusion_mask(common.shape,signature[1],TARGETS,TARGET_EXCLUSION_RADIUS)
        common&=~excluded
        common_pixels=int(common.sum()); common_fraction=float(common.mean())
        all_samples={"VV":{"delta":[],"area":[],"angle":[]},"VH":{"delta":[],"area":[],"angle":[]}}
        per_scene={}
        for date,ell,rtc,ang in records:
            angle=ang.read(1)
            area=rtc.read(3)
            scene_result={}
            for pol,band in (("VV",1),("VH",2)):
                e=ell.read(band); r=rtc.read(band)
                valid=common&(e>0)&(r>0)&(area>0)&np.isfinite(e)&np.isfinite(r)&np.isfinite(area)
                sl=(slice(None,None,SAMPLE_STEP),slice(None,None,SAMPLE_STEP))
                m=valid[sl]
                delta=(10*np.log10(r[sl][m])-10*np.log10(e[sl][m]))
                aa=area[sl][m]; theta=angle[sl][m]
                if len(delta)<10: raise ValueError(f"Too few common valid {pol} samples for {date}")
                all_samples[pol]["delta"].append(delta)
                all_samples[pol]["area"].append(aa)
                all_samples[pol]["angle"].append(theta)
                scene_result[pol]=relation_summary(delta,aa,theta)
            per_scene[date]=scene_result
        aggregate={}
        for pol,samples in all_samples.items():
            aggregate[pol]=relation_summary(np.concatenate(samples["delta"]),
                np.concatenate(samples["area"]),np.concatenate(samples["angle"]))
        return {"schema":"tessellatum.sentinel1.surat-r009-independent-angle-equation-qa.v1",
            "site":"CEOS Surat Basin, Queensland, Australia","relative_orbit":9,"orbit_direction":"ASCENDING",
            "scene_count":len(records),"grid":{"crs":str(signature[0]),"width":signature[2],"height":signature[3],
                "common_valid_pixels_after_target_exclusion":common_pixels,"common_valid_fraction_after_target_exclusion":common_fraction,
                "sample_step_pixels":SAMPLE_STEP},
            "target_exclusion":{"targets":[x["name"] for x in TARGETS],"radius_pixels":TARGET_EXCLUSION_RADIUS},
            "aggregate_metrics":aggregate,"per_scene_metrics":per_scene,
            "corner_reflector_diagnostics":{s["acquisition_datetime_utc"][:10]:s["corner_reflector_vv_diagnostics"] for s in scenes},
            "analysis_ready":False,
            "interpretation_limits":["This is an independent-site test of the geometric RTC/ellipsoid relation, not a production correction validation.",
                "The 13-reflector repeatable subset spans the regional array; three nearby 1.5 m reflectors are used for point-target diagnostics.",
                "Corner-reflector windows are excluded from the distributed-target pixel regression.",
                "The source incidence angle is interpolated from sparse GRD annotation geolocation tie points and internally cross-validated.",
                "Sentinel Hub RTC and ellipsoid outputs share a provider; independent processor comparison remains outstanding.",
                "No radiometric normalization or change detection is performed."]}
    finally:
        for handle in handles: handle.close()

def main(argv=None):
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--process-dir",type=Path,default=Path("data/sentinelhub/surat_basin/processed"))
    p.add_argument("--angle-dir",type=Path,default=Path("data/sentinelhub/surat_basin/processed/ellipsoid_incidence"))
    p.add_argument("--process-report",type=Path,default=Path("data/sentinelhub/surat_basin/processed/surat_r009_paired_processing_qa.json"))
    p.add_argument("--angle-report",type=Path,default=Path("data/sentinelhub/surat_basin/processed/surat_r009_incidence_interpolation_qa.json"))
    p.add_argument("--output",type=Path,default=Path("data/sentinelhub/surat_basin/processed/surat_r009_independent_angle_equation_qa.json"))
    a=p.parse_args(argv)
    try:
        process_report=json.loads(a.process_report.read_text(encoding="utf-8"))
        incidence_report=json.loads(a.angle_report.read_text(encoding="utf-8"))
        report=analyze(process_report,incidence_report,a.process_dir,a.angle_dir)
        a.output.parent.mkdir(parents=True,exist_ok=True); a.output.write_text(json.dumps(report,indent=2)+"\n",encoding="utf-8")
    except Exception as exc:
        print(f"Surat equation QA failed: {type(exc).__name__}: {exc}",file=sys.stderr); return 2
    for pol,metrics in report["aggregate_metrics"].items():
        a=metrics["area_only_residual"]; b=metrics["area_plus_ellipsoid_angle_residual"]
        print(f"{pol}: area-only residual MAE={a['mae_db']:.5f} dB; after ellipsoid-angle term MAE={b['mae_db']:.5f} dB; P95={b['p95_absolute_db']:.5f} dB")
    print(f"Common valid pixels: {report['grid']['common_valid_pixels_after_target_exclusion']} ({report['grid']['common_valid_fraction_after_target_exclusion']:.4f}); report={a.output}; analysis_ready=false")
    return 0
if __name__=="__main__": raise SystemExit(main())
