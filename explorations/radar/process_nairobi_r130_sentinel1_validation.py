#!/usr/bin/env python3
"""Process five source-verified Sentinel-1D R130 acquisitions as paired gamma0 rasters."""
from __future__ import annotations
import argparse,hashlib,importlib.util,json,os,sys
from datetime import datetime,timedelta,timezone
from pathlib import Path
import numpy as np
import rasterio
from shapely.geometry import box,shape

RADAR=Path(__file__).resolve().parent
def load_module(name,filename):
    spec=importlib.util.spec_from_file_location(name,RADAR/filename)
    if spec is None or spec.loader is None: raise RuntimeError(f"Cannot load {filename}")
    module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module);return module
PROCESS=load_module("process_sentinelhub_sentinel1","process_sentinelhub_sentinel1.py")
RTC=load_module("process_sentinel1_gamma0_terrain","process_sentinel1_gamma0_terrain.py")
CAT=PROCESS._CATALOG
BBOX=[36.65,-1.45,37.05,-1.15]
WIDTH=2500;HEIGHT=2200
DEM="COPERNICUS_30";OVERSAMPLING=2
PRODUCTS=[
 {"date":"2026-10-06","item_id":"S1D_IW_GRDH_1SDV_20261006T155531_20261006T155556_004896_009371_B797_COG.SAFE","absolute_orbit":4896,"datatake_id":"009371","source_start":"2026-10-06T15:55:31Z"},
 {"date":"2026-10-18","item_id":"S1D_IW_GRDH_1SDV_20261018T155531_20261018T155556_005071_009986_8434_COG.SAFE","absolute_orbit":5071,"datatake_id":"009986","source_start":"2026-10-18T15:55:31Z"},
 {"date":"2026-10-30","item_id":"S1D_IW_GRDH_1SDV_20261030T155531_20261030T155556_005246_009F7F_498E_COG.SAFE","absolute_orbit":5246,"datatake_id":"009F7F","source_start":"2026-10-30T15:55:31Z"},
 {"date":"2026-11-11","item_id":"S1D_IW_GRDH_1SDV_20261111T155531_20261111T155556_005421_00A58B_0CEC_COG.SAFE","absolute_orbit":5421,"datatake_id":"00A58B","source_start":"2026-11-11T15:55:31Z"},
 {"date":"2026-11-23","item_id":"S1D_IW_GRDH_1SDV_20261123T155530_20261123T155555_005596_00AB9A_AA88_COG.SAFE","absolute_orbit":5596,"datatake_id":"00AB9A","source_start":"2026-11-23T15:55:30Z"},
]

def resolve_feature(token,product,timeout):
    target=datetime.fromisoformat(product["source_start"].replace("Z","+00:00"))
    start=(target-timedelta(minutes=2)).isoformat(timespec="seconds").replace("+00:00","Z")
    end=(target+timedelta(minutes=2)).isoformat(timespec="seconds").replace("+00:00","Z")
    payload=CAT.build_search_payload(start,end,100)
    payload["bbox"]=BBOX
    result=CAT.search_catalog(token,payload,timeout=min(timeout,60))
    matches=[x for x in result["features"] if x.get("id")==product["item_id"]]
    if len(matches)!=1: raise ValueError(f"Expected exactly one exact Sentinel Hub item {product['item_id']}; found {len(matches)}")
    feature=matches[0];props=feature.get("properties") or {}
    if int(props.get("sat:relative_orbit",-1))!=130: raise ValueError("Relative orbit mismatch")
    if int(props.get("sat:absolute_orbit",-1))!=product["absolute_orbit"]: raise ValueError("Absolute orbit mismatch")
    if str(props.get("sat:orbit_state","")).upper()!="ASCENDING": raise ValueError("Orbit direction mismatch")
    if not {"VV","VH"}.issubset(set(props.get("sar:polarizations") or [])): raise ValueError("Dual polarization is missing")
    platform=str(props.get("platform","")).lower().replace("-","")
    if platform!="sentinel1d": raise ValueError(f"Platform mismatch: {props.get('platform')}")
    geometry=feature.get("geometry")
    if not isinstance(geometry,dict): raise ValueError("Catalogue feature has no footprint geometry")
    footprint=shape(geometry);aoi=box(*BBOX)
    fraction=float(footprint.intersection(aoi).area/aoi.area)
    if fraction<=0: raise ValueError("Scene does not intersect study AOI")
    return feature,fraction

def inspect_pair(ell_path,rtc_path):
    with rasterio.open(ell_path) as ell,rasterio.open(rtc_path) as rtc:
        if ell.count!=3 or rtc.count!=6: raise ValueError("Unexpected band schema; expected 3 and 6 bands")
        if ell.crs is None or rtc.crs!=ell.crs or rtc.transform!=ell.transform or (rtc.width,rtc.height)!=(ell.width,ell.height):
            raise ValueError("Sentinel Hub ellipsoid and terrain rasters do not share one grid")
        e=ell.read();r=rtc.read()
        emask=e[2]>0.5; rmask=(r[5]>0.5)&(r[4]<0.5)
        common=emask&rmask&np.isfinite(e[:2]).all(axis=0)&np.isfinite(r[:2]).all(axis=0)
        if not common.any(): raise ValueError("No common valid pixels across ellipsoid and RTC branches")
        def stats(x):
            v=x[common]
            q=np.percentile(v,[1,5,25,50,75,95,99])
            return {"count":int(v.size),"min":float(v.min()),"p01":float(q[0]),"p05":float(q[1]),
              "median":float(q[3]),"p95":float(q[5]),"p99":float(q[6]),"max":float(v.max())}
        return {"crs":ell.crs.to_string(),"width":ell.width,"height":ell.height,
          "transform":list(ell.transform)[:6],"ellipsoid_valid_pixels":int(emask.sum()),
          "rtc_valid_unshadowed_pixels":int(rmask.sum()),"common_valid_pixels":int(common.sum()),
          "common_valid_fraction":float(common.mean()),
          "vv_ellipsoid_linear_power":stats(e[0]),"vh_ellipsoid_linear_power":stats(e[1]),
          "vv_rtc_linear_power":stats(r[0]),"vh_rtc_linear_power":stats(r[1]),
          "shadow_flag_fraction_of_rtc_valid":float(np.mean(r[4][rmask]>0.5)) if rmask.any() else None}

def process_all(output_dir,timeout):
    cid=os.environ.get("SENTINEL_HUB_CLIENT_ID","");secret=os.environ.get("SENTINEL_HUB_CLIENT_SECRET","")
    token=CAT.request_access_token(cid,secret,timeout=30)
    output_dir.mkdir(parents=True,exist_ok=True)
    records=[]
    for p in PRODUCTS:
        feature,coverage=resolve_feature(token,p,timeout)
        ep=PROCESS.build_process_payload(feature,width=WIDTH,height=HEIGHT,bbox=BBOX)
        rp=RTC.build_rtc_payload(feature,width=WIDTH,height=HEIGHT,dem_instance=DEM,oversampling=OVERSAMPLING,bbox=BBOX)
        eb=PROCESS.request_geotiff(token,ep,timeout=timeout)
        rb=PROCESS.request_geotiff(token,rp,timeout=timeout)
        date=p["date"]
        epath=output_dir/f"nairobi_r130_{date}_gamma0-ellipsoid.tif"
        rpath=output_dir/f"nairobi_r130_{date}_gamma0-terrain-rtc.tif"
        epath.write_bytes(eb);rpath.write_bytes(rb)
        qa=inspect_pair(epath,rpath)
        rec={**p,"catalog_item_id":feature["id"],"catalogue_aoi_intersection_fraction":coverage,
             "ellipsoid_file":epath.name,"rtc_file":rpath.name,
             "ellipsoid_sha256":hashlib.sha256(eb).hexdigest(),"rtc_sha256":hashlib.sha256(rb).hexdigest(),
             "qa":qa}
        records.append(rec)
        print(f"Processed {date}: common={qa['common_valid_pixels']:,} ({qa['common_valid_fraction']:.3%}); catalogue AOI intersection={coverage:.3%}; CRS={qa['crs']}")
    report={"schema":"tessellatum.sentinel1.nairobi-r130-paired-processing.v1",
      "study_area":"Nairobi County and environs, Kenya","platform":"Sentinel-1D",
      "relative_orbit":130,"orbit_direction":"ASCENDING","polarizations":["VV","VH"],
      "bbox_crs84":BBOX,"output_grid":{"width":WIDTH,"height":HEIGHT,"crs":"EPSG:4326"},
      "processing":{"ellipsoid_backscatter":"GAMMA0_ELLIPSOID","terrain_backscatter":"GAMMA0_TERRAIN",
        "orthorectify":True,"dem_instance":DEM,"radiometric_terrain_oversampling":OVERSAMPLING,
        "ellipsoid_units":"linear power","rtc_units":"linear power"},
      "source_identity":"Each GRD product was reconciled to the corresponding OPERA SLC datatake by platform, absolute orbit, datatake ID, IW mode, and acquisition start time (two-second tolerance).",
      "scene_count":len(records),"scenes":records,
      "analysis_ready":False,
      "limitations":["Catalogue intersection is not raster-valid overlap; this report separately records Process API masks.",
        "This is a cross-processor comparison between Sentinel Hub GRD and OPERA SLC-derived RTC; products are not pixel-identical.",
        "The broad rectangular AOI includes urban and peri-urban land cover; no reflectors or absolute RCS targets are asserted.",
        "The 2500x2200 EPSG:4326 output grid is a sampling grid, not native Sentinel-1 resolution.",
        "Pixel-level common support with each OPERA burst and static/dynamic masks is still to be audited before radiometric statistics."]}
    path=output_dir/"nairobi_r130_paired_processing_qa.json"
    path.write_text(json.dumps(report,indent=2)+"\n")
    print(f"Report: {path}; analysis_ready=false")
    return report

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--output-dir",type=Path,default=Path("data/sentinelhub/nairobi/r130"))
    p.add_argument("--timeout",type=int,default=300)
    a=p.parse_args()
    if a.timeout<1: p.error("--timeout must be positive")
    try: process_all(a.output_dir,a.timeout)
    except Exception as e: print(f"Nairobi R130 paired processing failed: {type(e).__name__}: {e}",file=sys.stderr);return 2
    return 0

if __name__=="__main__": raise SystemExit(main())
