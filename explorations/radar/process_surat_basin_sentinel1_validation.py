#!/usr/bin/env python3
"""Process four Sentinel-1A R009 scenes over a compact CEOS Surat reflector subset."""
from __future__ import annotations
import argparse, importlib.util, json, os, sys
from datetime import datetime, timedelta, timezone
from pathlib import Path
import numpy as np
import rasterio
from rasterio.windows import Window
from shapely.geometry import Point, shape

RADAR=Path(__file__).resolve().parent
def load_module(name,filename):
    spec=importlib.util.spec_from_file_location(name,RADAR/filename)
    if spec is None or spec.loader is None: raise RuntimeError(f"Cannot load {filename}")
    module=importlib.util.module_from_spec(spec); spec.loader.exec_module(module); return module
PROCESS=load_module("process_sentinelhub_sentinel1","process_sentinelhub_sentinel1.py")
RTC=load_module("process_sentinel1_gamma0_terrain","process_sentinel1_gamma0_terrain.py")
CAT=PROCESS._CATALOG
BBOX=[150.244625,-27.273849,150.500114,-27.070649]
WIDTH=2500; HEIGHT=2200
DEM="COPERNICUS_30"; OVERSAMPLING=2
TARGETS=[
 {"name":"Surat Basin 26","longitude":150.485114,"latitude":-27.258849,"side_length_m":1.5},
 {"name":"Surat Basin 31","longitude":150.331548,"latitude":-27.207314,"side_length_m":1.5},
 {"name":"Surat Basin 35","longitude":150.259625,"latitude":-27.085649,"side_length_m":1.5},
]
PRODUCTS=[
 ("2025-12-19T08:41:12Z","S1A_IW_GRDH_1SDV_20251219T084112_20251219T084137_062381_07D052_4725_COG.SAFE"),
 ("2025-12-31T08:41:11Z","S1A_IW_GRDH_1SDV_20251231T084111_20251231T084136_062556_07D710_2940_COG.SAFE"),
 ("2026-01-12T08:41:10Z","S1A_IW_GRDH_1SDV_20260112T084110_20260112T084135_062731_07DDCA_F1E5_COG.SAFE"),
 ("2026-01-24T08:41:08Z","S1A_IW_GRDH_1SDV_20260124T084108_20260124T084133_062906_07E425_80AF_COG.SAFE"),
]

def resolve_feature(token,stamp,product_id,timeout):
    target=datetime.fromisoformat(stamp.replace("Z","+00:00")).astimezone(timezone.utc)
    start=(target-timedelta(minutes=2)).isoformat(timespec="seconds").replace("+00:00","Z")
    end=(target+timedelta(minutes=2)).isoformat(timespec="seconds").replace("+00:00","Z")
    payload=CAT.build_search_payload(start,end,100); payload["bbox"]=BBOX
    result=CAT.search_catalog(token,payload,timeout=min(timeout,60))
    matches=[]
    for feature in result["features"]:
        if feature.get("id")!=product_id: continue
        props=feature.get("properties",{})
        stamp_value=props.get("datetime")
        if not isinstance(stamp_value,str): continue
        acquired=datetime.fromisoformat(stamp_value.replace("Z","+00:00"))
        if acquired.tzinfo is None: continue
        geom=feature.get("geometry")
        if not isinstance(geom,dict): continue
        footprint=shape(geom)
        if not all(footprint.covers(Point(t["longitude"],t["latitude"])) for t in TARGETS): continue
        matches.append(feature)
    if not matches: raise ValueError(f"Exact catalogue product missing or does not cover all three reflectors: {product_id}")
    return matches[0]

def target_window_stats(ds,band,mask_band,target):
    row,col=rasterio.transform.rowcol(ds.transform,target["longitude"],target["latitude"])
    radius=10; r0=max(0,row-radius); c0=max(0,col-radius)
    height=min(ds.height-r0,2*radius+1); width=min(ds.width-c0,2*radius+1)
    if height<=0 or width<=0: raise ValueError(f"{target['name']} falls outside output raster")
    window=Window(c0,r0,width,height)
    values=ds.read(band,window=window).astype(np.float64)
    mask=ds.read(mask_band,window=window)>0.5
    valid=mask&np.isfinite(values)&(values>0)
    if not valid.any(): return {"valid":False,"row":int(row),"column":int(col)}
    work=np.where(valid,values,np.nan)
    peak_index=np.nanargmax(work); pr,pc=np.unravel_index(peak_index,work.shape)
    peak=float(work[pr,pc])
    rr,cc=np.indices(work.shape); distance=np.maximum(np.abs(rr-(row-r0)),np.abs(cc-(col-c0)))
    background=valid&(distance>=5)
    bg=float(np.median(values[background])) if background.any() else float("nan")
    return {"valid":True,"row":int(row),"column":int(col),
        "peak_offset_pixels":[int(pc-(col-c0)),int(pr-(row-r0))],
        "peak_vv_linear_power":peak,"peak_vv_db":float(10*np.log10(peak)),
        "background_median_vv_linear_power":bg if np.isfinite(bg) else None,
        "background_median_vv_db":float(10*np.log10(bg)) if np.isfinite(bg) and bg>0 else None,
        "peak_to_background_db":float(10*np.log10(peak/bg)) if np.isfinite(bg) and bg>0 else None,
        "window_valid_fraction":float(valid.mean())}

def process_all(output_dir,timeout):
    client_id=os.environ.get("SENTINEL_HUB_CLIENT_ID","")
    client_secret=os.environ.get("SENTINEL_HUB_CLIENT_SECRET","")
    token=CAT.request_access_token(client_id,client_secret,timeout=30)
    output_dir.mkdir(parents=True,exist_ok=True)
    records=[]
    for stamp,product_id in PRODUCTS:
        feature=resolve_feature(token,stamp,product_id,timeout)
        ell_payload=PROCESS.build_process_payload(feature,width=WIDTH,height=HEIGHT,bbox=BBOX)
        rtc_payload=RTC.build_rtc_payload(feature,width=WIDTH,height=HEIGHT,
            dem_instance=DEM,oversampling=OVERSAMPLING,bbox=BBOX)
        ell_body=PROCESS.request_geotiff(token,ell_payload,timeout=timeout)
        rtc_body=PROCESS.request_geotiff(token,rtc_payload,timeout=timeout)
        date=stamp[:10]
        ell_path=output_dir/f"surat_r009_{date}_gamma0-ellipsoid.tif"
        rtc_path=output_dir/f"surat_r009_{date}_gamma0-terrain-rtc.tif"
        ell_path.write_bytes(ell_body); rtc_path.write_bytes(rtc_body)
        with rasterio.open(ell_path) as ell, rasterio.open(rtc_path) as rtc:
            signature=(ell.crs,ell.transform,ell.width,ell.height)
            if signature!=(rtc.crs,rtc.transform,rtc.width,rtc.height):
                raise ValueError(f"RTC/ellipsoid grids differ for {date}")
            if (ell.width,ell.height)!=(WIDTH,HEIGHT) or ell.count!=3 or rtc.count!=6:
                raise ValueError(f"Unexpected raster dimensions or bands for {date}")
            ell_mask=ell.read(3)>0.5; rtc_mask=rtc.read(6)>0.5
            valid=ell_mask&rtc_mask
            target_stats={}
            for target in TARGETS:
                target_stats[target["name"]]={
                    "ellipsoid":target_window_stats(ell,1,3,target),
                    "rtc":target_window_stats(rtc,1,6,target)}
            records.append({"acquisition_datetime_utc":stamp,"product_id":product_id,
                "catalog_item_id":feature.get("id"),"ellipsoid_file":ell_path.name,
                "rtc_file":rtc_path.name,"grid_matches":True,
                "valid_pixels_ellipsoid":int(ell_mask.sum()),"valid_pixels_rtc":int(rtc_mask.sum()),
                "valid_pixels_both":int(valid.sum()),"common_valid_fraction":float(valid.mean()),
                "corner_reflector_vv_diagnostics":target_stats})
        print(f"Processed {date}: {int(valid.sum())} common pixels; grid={WIDTH}x{HEIGHT}; targets={len(TARGETS)}")
    report={"schema":"tessellatum.sentinel1.surat-basin-r009-paired-rtc-ellipsoid.v1",
        "site":"CEOS Surat Basin, Queensland, Australia","platform":"Sentinel-1A",
        "relative_orbit":9,"orbit_direction":"ASCENDING","bbox_crs84":BBOX,
        "grid":{"width":WIDTH,"height":HEIGHT,"crs":"EPSG:4326",
            "pixel_size_degrees":[(BBOX[2]-BBOX[0])/WIDTH,(BBOX[3]-BBOX[1])/HEIGHT]},
        "processing":{"ellipsoid_backscatter":"GAMMA0_ELLIPSOID","rtc_backscatter":"GAMMA0_TERRAIN",
            "orthorectify":True,"dem_instance":DEM,"radiometric_terrain_oversampling":OVERSAMPLING},
        "targets":TARGETS,"scene_count":len(records),"scenes":records,
        "analysis_ready":False,
        "limitations":["Catalogue coverage was screened against all three reflector coordinates, but raster validity is evaluated separately.",
            "The 1.5 m corner reflectors are point targets; VV peak/background diagnostics are exploratory and not yet an absolute RCS calibration.",
            "The 10 m output spacing is not native Sentinel-1 resolution and does not improve the underlying impulse response.",
            "The ellipsoid and RTC branches share a provider and processing platform; independent provider validation remains outstanding.",
            "No normalization or change detection is performed."]}
    report_path=output_dir/"surat_r009_paired_processing_qa.json"
    report_path.write_text(json.dumps(report,indent=2)+"\n",encoding="utf-8")
    print(f"Report: {report_path}; analysis_ready=false")
    return report

def main(argv=None):
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--output-dir",type=Path,default=Path("data/sentinelhub/surat_basin/processed"))
    p.add_argument("--timeout",type=int,default=300)
    a=p.parse_args(argv)
    if a.timeout<30: p.error("--timeout must be at least 30 seconds")
    try:
        report=process_all(a.output_dir,a.timeout)
    except Exception as exc:
        print(f"Surat paired processing failed: {type(exc).__name__}: {exc}",file=sys.stderr); return 2
    return 0 if report["scene_count"]==4 else 2
if __name__=="__main__": raise SystemExit(main())
