#!/usr/bin/env python3
"""Audit common raster support for Nairobi R130 OPERA and Sentinel Hub gamma0 pairs."""
from __future__ import annotations
import argparse,json,re,sys
from pathlib import Path
import numpy as np
import rasterio
from rasterio.enums import Resampling
from rasterio.warp import reproject

BURST_RE=re.compile(r"(T130[-_]\d{6}[-_]IW3)",re.I)
DATE_RE=re.compile(r"(20\d{6})T\d{6}Z")
POLARIZATIONS=("VV","VH")
MIN_COMMON_PIXELS=1000
SUPPORT_THRESHOLD=0.95

def db_stats(values):
    v=np.asarray(values,dtype=np.float64);v=v[np.isfinite(v)&(v>0)]
    if not v.size:return None
    q=np.percentile(v,[1,5,25,50,75,95,99])
    return {"count":int(v.size),"min_db":float(10*np.log10(v.min())),
      "p01_db":float(10*np.log10(q[0])),"p05_db":float(10*np.log10(q[1])),
      "median_db":float(10*np.log10(q[3])),"p95_db":float(10*np.log10(q[5])),
      "p99_db":float(10*np.log10(q[6])),"max_db":float(10*np.log10(v.max()))}

def reproject_average(source,src,dst):
    out=np.full((dst.height,dst.width),np.nan,dtype=np.float32)
    reproject(source=np.asarray(source,dtype=np.float32),destination=out,
      src_transform=src.transform,src_crs=src.crs,src_nodata=np.nan,
      dst_transform=dst.transform,dst_crs=dst.crs,dst_nodata=np.nan,
      resampling=Resampling.average,init_dest_nodata=True)
    return out

def locate(folder,pattern,description):
    matches=sorted(folder.rglob(pattern))
    if len(matches)!=1:raise ValueError(f"Expected one {description}; found {len(matches)}: {[x.name for x in matches]}")
    return matches[0]

def inspect_scene(opera_dir,sh_dir,date,burst):
    iso=f"{date[:4]}-{date[4:6]}-{date[6:8]}"
    stem_prefix=f"OPERA_L2_RTC-S1_{burst}_{date}"
    rtc_dir=opera_dir/"rtc";static_dir=opera_dir/"static"
    def rtc(suffix):return locate(rtc_dir,f"{stem_prefix}*{suffix}",f"{date} {burst} {suffix}")
    def static(suffix):
        found=[x for x in static_dir.glob("*.tif") if burst in x.name and x.name.endswith(suffix)
          and not(suffix=="_incidence_angle.tif" and x.name.endswith("_local_incidence_angle.tif"))]
        if len(found)!=1:raise ValueError(f"Expected one static {suffix} for {burst}; found {[x.name for x in found]}")
        return found[0]
    ell_path=sh_dir/f"nairobi_r130_{iso}_gamma0-ellipsoid.tif"
    terrain_path=sh_dir/f"nairobi_r130_{iso}_gamma0-terrain-rtc.tif"
    if not ell_path.is_file() or not terrain_path.is_file():raise FileNotFoundError(f"Missing Sentinel Hub pair for {iso}")
    with rasterio.open(rtc("_VV.tif")) as vv,rasterio.open(rtc("_VH.tif")) as vh,\
         rasterio.open(rtc("_mask.tif")) as dm,rasterio.open(static("_mask.tif")) as sm,\
         rasterio.open(static("_rtc_anf_gamma0_to_beta0.tif")) as anf,rasterio.open(static("_incidence_angle.tif")) as inc,\
         rasterio.open(ell_path) as ell,rasterio.open(terrain_path) as terrain:
        for label,ds in [("VH",vh),("dynamic mask",dm),("static mask",sm),("ANF",anf),("incidence angle",inc)]:
            if (ds.crs,ds.transform,ds.width,ds.height)!=(vv.crs,vv.transform,vv.width,vv.height):
                raise ValueError(f"OPERA {label} grid mismatch for {burst}")
        if ell.count!=3 or terrain.count!=6:raise ValueError("Sentinel Hub band schema mismatch")
        if (ell.crs,ell.transform,ell.width,ell.height)!=(terrain.crs,terrain.transform,terrain.width,terrain.height):
            raise ValueError("Sentinel Hub ellipsoid and terrain grids differ")
        # OPERA RTC-S1 dynamic mask: class 0 valid/unaffected. Static mask class 0 valid.
        dyn=dm.read(1);stat=sm.read(1)
        opera_geometry=(dyn==0)&(stat==0)
        anf_values=anf.read(1).astype(np.float32);theta=inc.read(1).astype(np.float32)
        static_valid=np.isfinite(anf_values)&(anf_values>0)&np.isfinite(theta)&(theta>0)&(theta<90)
        opera_base=opera_geometry&static_valid
        # Sentinel Hub common validity: both branches dataMask=1 and RTC shadowMask=0.
        ell_data=ell.read(3)>0.5;rtc_data=terrain.read(6)>0.5
        shadow=terrain.read(5)>0.5
        sh_base=ell_data&rtc_data&~shadow
        sh_base &= np.isfinite(ell.read(1))&np.isfinite(ell.read(2))
        sh_base &= np.isfinite(terrain.read(1))&np.isfinite(terrain.read(2))
        sh_support=reproject_average(sh_base.astype(np.float32),ell,vv)
        sh_on_opera=np.isfinite(sh_support)&(sh_support>=SUPPORT_THRESHOLD)
        pol_results={}
        for idx,pol in enumerate(POLARIZATIONS,1):
            op=vv.read(1) if pol=="VV" else vh.read(1)
            sh_ell=reproject_average(np.where(sh_base,ell.read(idx),np.nan),ell,vv)
            sh_rtc=reproject_average(np.where(sh_base,terrain.read(idx),np.nan),terrain,vv)
            valid_op=opera_base&np.isfinite(op)&(op>0)
            valid_sh=sh_on_opera&np.isfinite(sh_ell)&np.isfinite(sh_rtc)&(sh_ell>0)&(sh_rtc>0)
            common=valid_op&valid_sh
            count=int(common.sum())
            pol_results[pol]={"opera_valid_pixels":int(valid_op.sum()),
              "sentinelhub_valid_support_pixels":int(valid_sh.sum()),
              "common_valid_pixels":count,
              "common_fraction_of_opera_valid":float(count/max(1,int(valid_op.sum()))),
              "common_fraction_of_burst_grid":float(count/(vv.width*vv.height)),
              "minimum_common_pixel_gate":"passed" if count>=MIN_COMMON_PIXELS else "failed",
              "opera_terrain_gamma0_db":db_stats(op[common]),
              "sentinelhub_terrain_gamma0_db":db_stats(sh_rtc[common]),
              "sentinelhub_ellipsoid_gamma0_db":db_stats(sh_ell[common])}
        classes,counts=np.unique(dyn,return_counts=True)
        static_classes,static_counts=np.unique(stat,return_counts=True)
        return {"date":iso,"burst_id":burst,"crs":vv.crs.to_string(),
          "width":vv.width,"height":vv.height,"resolution_m":list(vv.res),
          "opera_dynamic_mask_classes":{str(int(k)):int(v) for k,v in zip(classes,counts)},
          "opera_static_mask_classes":{str(int(k)):int(v) for k,v in zip(static_classes,static_counts)},
          "opera_valid_geometry_fraction":float(opera_geometry.mean()),
          "sentinelhub_common_valid_fraction_on_source_grid":float(sh_base.mean()),
          "sentinelhub_support_threshold":SUPPORT_THRESHOLD,
          "polarizations":pol_results}

def run(opera_dir,sh_dir,output):
    vv_files=sorted((opera_dir/"rtc").glob("*_VV.tif"))
    keys=set()
    for p in vv_files:
        b=BURST_RE.search(p.name);d=DATE_RE.search(p.name)
        if b and d:keys.add((d.group(1),b.group(1).replace("_","-")))
    if len(keys)!=15:raise ValueError(f"Expected 15 date/burst combinations, found {len(keys)}")
    records=[inspect_scene(opera_dir,sh_dir,d,b) for d,b in sorted(keys)]
    failed=[{"date":x["date"],"burst_id":x["burst_id"],"polarization":pol,"count":v["common_valid_pixels"]}
      for x in records for pol,v in x["polarizations"].items() if v["minimum_common_pixel_gate"]!="passed"]
    report={"schema":"tessellatum.opera-nairobi-r130-common-support-qa.v1",
      "study_area":"Nairobi County and environs, Kenya","date_count":5,"burst_count":3,
      "date_burst_count":len(records),"polarizations":list(POLARIZATIONS),
      "minimum_common_pixels_per_burst_date_polarization":MIN_COMMON_PIXELS,
      "sentinelhub_support_threshold":SUPPORT_THRESHOLD,
      "records":records,"failed_sample_gates":failed,
      "checks":{"all_15_burst_date_combinations_processed":len(records)==15,
        "all_30_burst_date_polarization_sample_gates_pass":len(failed)==0},
      "limitations":["This is spatial-support and mask QA, not a radiometric comparison or validation result.",
        "Sentinel Hub values are area-averaged in linear power onto each native OPERA burst grid.",
        "OPERA dynamic mask class 0 and static mask class 0 are treated as valid; mask histograms are retained for review.",
        "Sentinel Hub valid support requires both dataMask bands valid and RTC shadowMask unflagged.",
        "No corner-reflector inventory or absolute RCS calibration is claimed."]}
    output.parent.mkdir(parents=True,exist_ok=True);output.write_text(json.dumps(report,indent=2)+"\n")
    for x in records:
        print(f"{x['date']} {x['burst_id']} | VV={x['polarizations']['VV']['common_valid_pixels']:,} | VH={x['polarizations']['VH']['common_valid_pixels']:,}")
    print("Checks:",json.dumps(report["checks"],sort_keys=True))
    return report

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--opera-dir",type=Path,default=Path("opera-assets"))
    p.add_argument("--sentinelhub-dir",type=Path,default=Path("data/sentinelhub/nairobi/r130"))
    p.add_argument("--output",type=Path,default=Path("data/sentinelhub/nairobi/r130/common-support-qa.json"))
    a=p.parse_args()
    try:r=run(a.opera_dir,a.sentinelhub_dir,a.output)
    except Exception as e:print(f"Common-support QA failed: {type(e).__name__}: {e}",file=sys.stderr);return 2
    return 0 if all(r["checks"].values()) else 1
if __name__=="__main__":raise SystemExit(main())
