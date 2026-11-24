#!/usr/bin/env python3
"""Map and stratify Nairobi R130 OPERA/Sentinel Hub terrain-delta residuals."""
from __future__ import annotations
import argparse, json, re, sys
from pathlib import Path
import numpy as np
import rasterio
from rasterio.enums import Resampling
from rasterio.warp import reproject

BURST_RE = re.compile(r"(T130[-_]\d{6}[-_]IW3)", re.I)
DATE_RE = re.compile(r"(20\d{6})T\d{6}Z")
POLS = ("VV", "VH")
SUPPORT_THRESHOLD = 0.95
DB_FLOOR = 1e-12
ANGLE_EDGES = np.array([35, 40, 42, 44, 46, 48, 50, 55, 60], dtype=float)

def db(x):
    return 10.0 * np.log10(np.maximum(np.asarray(x, dtype=np.float64), DB_FLOOR))

def summarize(values):
    v = np.asarray(values, dtype=np.float64)
    v = v[np.isfinite(v)]
    if not v.size:
        return {"count": 0}
    a = np.abs(v)
    return {
        "count": int(v.size), "bias_mean_db": float(v.mean()),
        "mae_db": float(a.mean()), "rmse_db": float(np.sqrt(np.mean(v*v))),
        "p50_absolute_db": float(np.percentile(a, 50)),
        "p95_absolute_db": float(np.percentile(a, 95)),
        "max_absolute_db": float(a.max()),
        "fraction_abs_gt_0_5_db": float(np.mean(a > 0.5)),
        "fraction_abs_gt_1_db": float(np.mean(a > 1.0)),
        "fraction_abs_gt_2_db": float(np.mean(a > 2.0)),
    }

def reproject_average(values, src, dst):
    out = np.full((dst.height, dst.width), np.nan, dtype=np.float32)
    reproject(source=np.asarray(values, dtype=np.float32), destination=out,
        src_transform=src.transform, src_crs=src.crs, src_nodata=np.nan,
        dst_transform=dst.transform, dst_crs=dst.crs, dst_nodata=np.nan,
        resampling=Resampling.average, init_dest_nodata=True)
    return out

def one(folder, pattern, label):
    hits = sorted(folder.glob(pattern))
    if len(hits) != 1:
        raise ValueError(f"Expected one {label}; found {[p.name for p in hits]}")
    return hits[0]

def static_file(folder, burst, suffix):
    hits = [p for p in folder.glob("*.tif") if burst in p.name and p.name.endswith(suffix)
            and not (suffix == "_incidence_angle.tif" and p.name.endswith("_local_incidence_angle.tif"))]
    if len(hits) != 1:
        raise ValueError(f"Expected one {suffix} for {burst}; found {[p.name for p in hits]}")
    return hits[0]

def stratify(values, covariate, edges, labels):
    records = []
    v = np.asarray(values); c = np.asarray(covariate)
    finite = np.isfinite(v) & np.isfinite(c)
    for i, label in enumerate(labels):
        selected = finite & (c >= edges[i]) & (c < edges[i+1])
        records.append({"bin": label, "lower": float(edges[i]), "upper_exclusive": float(edges[i+1]),
                        **summarize(v[selected])})
    under = finite & (c < edges[0]); over = finite & (c >= edges[-1])
    return {"bins": records, "underflow": summarize(v[under]), "overflow": summarize(v[over])}

def quantile_strata(values, covariate, names=("Q1", "Q2", "Q3", "Q4")):
    v=np.asarray(values); c=np.asarray(covariate)
    valid=np.isfinite(v)&np.isfinite(c)
    if valid.sum() < 4:
        return {"bins": [], "note": "Insufficient finite samples for quartiles"}
    q=np.quantile(c[valid], [0,.25,.5,.75,1])
    q=np.unique(q)
    if len(q)<2:
        return {"bins": [], "note": "ANF has no usable spread"}
    labels=list(names[:len(q)-1])
    return stratify(v,c,q,labels) | {"quantile_edges": [float(x) for x in q]}

def write_residual(path, residual, template):
    arr=np.where(np.isfinite(residual), residual, -9999).astype(np.float32)
    profile=template.profile.copy()
    profile.update(driver="GTiff", count=1, dtype="float32", nodata=-9999.0,
                   compress="deflate", predictor=3, tiled=True, BIGTIFF="IF_SAFER")
    path.parent.mkdir(parents=True, exist_ok=True)
    with rasterio.open(path, "w", **profile) as dst:
        dst.write(arr, 1)
        dst.set_band_description(1, "Sentinel Hub delta minus OPERA delta residual (dB)")

def diagnose_scene(opera_dir, sh_dir, date, burst, map_dir):
    iso=f"{date[:4]}-{date[4:6]}-{date[6:8]}"
    rtc=opera_dir/"rtc"; static=opera_dir/"static"
    def dyn(pol):
        return one(rtc, f"OPERA_L2_RTC-S1_{burst}_{date}T*_S1D_30_v1.0_{pol}.tif", f"{burst} {date} {pol}")
    with rasterio.open(dyn("VV")) as vv, rasterio.open(dyn("VH")) as vh, \
         rasterio.open(one(rtc, f"OPERA_L2_RTC-S1_{burst}_{date}T*_S1D_30_v1.0_mask.tif", "dynamic mask")) as dm, \
         rasterio.open(static_file(static, burst, "_rtc_anf_gamma0_to_beta0.tif")) as anf_ds, \
         rasterio.open(static_file(static, burst, "_incidence_angle.tif")) as inc_ds, \
         rasterio.open(static_file(static, burst, "_mask.tif")) as sm, \
         rasterio.open(sh_dir/f"nairobi_r130_{iso}_gamma0-ellipsoid.tif") as ell, \
         rasterio.open(sh_dir/f"nairobi_r130_{iso}_gamma0-terrain-rtc.tif") as shrtc:
        for label, ds in [("VH",vh),("dynamic mask",dm),("ANF",anf_ds),("incidence",inc_ds),("static mask",sm)]:
            if (ds.crs,ds.transform,ds.width,ds.height)!=(vv.crs,vv.transform,vv.width,vv.height):
                raise ValueError(f"OPERA {label} grid mismatch for {burst}")
        if ell.count!=3 or shrtc.count!=6:
            raise ValueError("Unexpected Sentinel Hub band schema")
        if (ell.crs,ell.transform,ell.width,ell.height)!=(shrtc.crs,shrtc.transform,shrtc.width,shrtc.height):
            raise ValueError("Sentinel Hub pair grids differ")
        theta_deg=inc_ds.read(1).astype(np.float32)
        theta=np.deg2rad(theta_deg)
        anf=anf_ds.read(1).astype(np.float32)
        op_mask=(dm.read(1)==0)&(sm.read(1)==0)&np.isfinite(anf)&(anf>0)&np.isfinite(theta)&(theta>0)&(theta<np.pi/2)
        sh_mask=(ell.read(3)>0.5)&(shrtc.read(6)>0.5)&(shrtc.read(5)<0.5)
        for ds, bands in ((ell,(1,2)),(shrtc,(1,2))):
            for band in bands: sh_mask &= np.isfinite(ds.read(band))
        support=reproject_average(sh_mask.astype(np.float32),ell,vv)
        sh_support=np.isfinite(support)&(support>=SUPPORT_THRESHOLD)
        results={}
        for idx, pol in enumerate(POLS,1):
            op_terrain=(vv if pol=="VV" else vh).read(1)
            op_ell=op_terrain*anf*np.tan(theta)
            sh_ell=reproject_average(np.where(sh_mask,ell.read(idx),np.nan),ell,vv)
            sh_terrain=reproject_average(np.where(sh_mask,shrtc.read(idx),np.nan),ell,vv)
            valid=op_mask&sh_support&np.isfinite(op_terrain)&(op_terrain>0)&np.isfinite(op_ell)&(op_ell>0)
            valid &= np.isfinite(sh_ell)&(sh_ell>0)&np.isfinite(sh_terrain)&(sh_terrain>0)
            if int(valid.sum())<1000:
                raise ValueError(f"{iso} {burst} {pol}: fewer than 1000 common pixels")
            residual_grid=np.full((vv.height,vv.width),np.nan,dtype=np.float32)
            residual_grid[valid]=((db(sh_terrain[valid])-db(sh_ell[valid]))-
                                  (db(op_terrain[valid])-db(op_ell[valid]))).astype(np.float32)
            map_name=f"{iso}_{burst}_{pol}_delta-residual-db.tif"
            write_residual(map_dir/map_name,residual_grid,vv)
            vals=residual_grid[valid]
            angle_stats=stratify(vals,theta_deg[valid],ANGLE_EDGES,
                [f"{ANGLE_EDGES[i]:g}-{ANGLE_EDGES[i+1]:g}°" for i in range(len(ANGLE_EDGES)-1)])
            anf_stats=quantile_strata(vals,anf[valid])
            # Highest residual locations are pixel-centre coordinates in the native OPERA CRS.
            flat=np.flatnonzero(valid)
            order=np.argsort(np.abs(vals))[-10:][::-1]
            top=[]
            for j in order:
                r,c=np.unravel_index(flat[j],valid.shape)
                x,y=vv.xy(int(r),int(c))
                top.append({"x":float(x),"y":float(y),"residual_db":float(vals[j]),
                            "incidence_angle_deg":float(theta_deg[r,c]),"anf":float(anf[r,c])})
            results[pol]={"residual_map":map_name,"common_pixels":int(valid.sum()),
                "overall":summarize(vals),"incidence_angle_strata":angle_stats,
                "anf_quartile_strata":anf_stats,"largest_absolute_residuals":top,
                "map_nodata_value":-9999.0,"map_crs":vv.crs.to_string(),
                "map_resolution":list(vv.res),"map_grid":"native OPERA burst grid"}
        return {"date":iso,"burst_id":burst,"width":vv.width,"height":vv.height,
                "crs":vv.crs.to_string(),"polarizations":results}

def run(opera_dir, sh_dir, output_dir, report_path):
    keys=set()
    for p in (opera_dir/"rtc").glob("*_VV.tif"):
        b=BURST_RE.search(p.name); d=DATE_RE.search(p.name)
        if b and d: keys.add((d.group(1),b.group(1).replace("_","-")))
    if len(keys)!=15: raise ValueError(f"Expected 15 date/burst combinations; found {len(keys)}")
    records=[diagnose_scene(opera_dir,sh_dir,d,b,output_dir) for d,b in sorted(keys)]
    report={"schema":"tessellatum.opera-nairobi-r130-residual-diagnostics.v1",
      "study_area":"Nairobi County and environs, Kenya","relative_orbit":130,
      "method":"Same common-support masks, 0.95 Sentinel Hub valid-support threshold, masked linear-power area averaging, and OPERA reconstruction as the first-pass comparison.",
      "residual_definition":"(Sentinel Hub terrain gamma0 - Sentinel Hub ellipsoid gamma0) - (OPERA terrain gamma0 - reconstructed OPERA ellipsoid gamma0), dB.",
      "stratification":{"incidence_angle_edges_degrees":ANGLE_EDGES.tolist(),
        "anf":"Within-scene quartiles; edges are scene-specific and must not be compared as common absolute thresholds."},
      "reflector_exclusion_applied":False,"records":records,
      "checks":{"all_15_date_burst_combinations_processed":len(records)==15,
        "all_30_residual_maps_written":sum(len(x["polarizations"]) for x in records)==30},
      "limitations":["Residual maps describe cross-processor terrain-to-ellipsoid delta differences, not absolute backscatter error or absolute calibration.",
        "Incidence and ANF strata are descriptive; association does not establish causation.",
        "No land-cover attribution is made because a separately validated, date-appropriate land-cover layer has not yet been admitted.",
        "No outliers are removed. Largest residual coordinates are reported for inspection.",
        "Adjacent OPERA bursts remain on separate native grids; no mosaicking is performed."]}
    report_path.parent.mkdir(parents=True,exist_ok=True)
    report_path.write_text(json.dumps(report,indent=2)+"\n")
    print("Diagnostic checks:",json.dumps(report["checks"],sort_keys=True),flush=True)
    for rec in records:
        for pol,item in rec["polarizations"].items():
            m=item["overall"]
            print(f"{rec['date']} {rec['burst_id']} {pol} | n={m['count']:,} | MAE={m['mae_db']:.4f} dB | RMSE={m['rmse_db']:.4f} dB | >1dB={m['fraction_abs_gt_1_db']:.3%}",flush=True)
    return report

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--opera-dir",type=Path,default=Path("opera-assets"))
    p.add_argument("--sentinelhub-dir",type=Path,default=Path("sentinelhub-assets"))
    p.add_argument("--output-dir",type=Path,default=Path("residual-maps"))
    p.add_argument("--report",type=Path,default=Path("residual-diagnostics.json"))
    a=p.parse_args()
    try: result=run(a.opera_dir,a.sentinelhub_dir,a.output_dir,a.report)
    except Exception as exc:
        print(f"Residual diagnostics failed: {type(exc).__name__}: {exc}",file=sys.stderr); return 2
    return 0 if all(result["checks"].values()) else 1

if __name__=="__main__": raise SystemExit(main())
