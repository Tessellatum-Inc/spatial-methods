#!/usr/bin/env python3
"""Process a repeated partial-coverage Sentinel-1 track for independent RTC screening.

This is a separate experiment from the full-coverage descending R079 stack.
It retains the same Nairobi output grid and uses dataMask/common-valid pixels;
it does not fill or extrapolate the uncovered part of the AOI.
"""
from __future__ import annotations
import argparse, importlib.util, json, os, sys
from datetime import datetime, timezone
from pathlib import Path
import numpy as np
import rasterio

RADAR=Path(__file__).resolve().parent
def load(name):
    spec=importlib.util.spec_from_file_location(name,RADAR/f"{name}.py")
    if spec is None or spec.loader is None: raise RuntimeError(f"Cannot load {name}")
    module=importlib.util.module_from_spec(spec); spec.loader.exec_module(module); return module
CAT=load("query_sentinelhub_sentinel1")
ELL=load("process_sentinelhub_sentinel1")
RTC=load("process_sentinel1_gamma0_terrain")
COMPARE=load("compare_sentinel1_ellipsoid_vs_terrain")

def collect_track(token,start,end,direction,relative_orbit):
    payload=CAT.build_search_payload(start,end,100)
    # Query IW items broadly, then filter orbit metadata locally. This avoids
    # relying on provider-specific queryability of sat:relative_orbit.
    payload["filter"]="sar:instrument_mode='IW'"
    features={}
    for _ in range(50):
        page=CAT.search_catalog(token,payload,timeout=60)
        for f in page["features"]: features[f["id"]]=f
        nxt=page.get("context",{}).get("next")
        if nxt is None: break
        payload={**payload,"next":nxt}
    else: raise RuntimeError("Catalogue pagination exceeded 50 pages")
    return sorted(features.values(),key=lambda f:f.get("properties",{}).get("datetime",""))

def select_candidates(features,direction,relative_orbit,min_coverage=0.8):
    selected=[]; seen=set()
    for feature in features:
        p=feature.get("properties",{})
        if str(p.get("sat:orbit_state","")).upper()!=direction.upper(): continue
        if p.get("sat:relative_orbit")!=relative_orbit: continue
        stamp=p.get("datetime")
        if not isinstance(stamp,str): continue
        try: dt=datetime.fromisoformat(stamp.replace("Z","+00:00"))
        except ValueError: continue
        if dt.tzinfo is None: continue
        key=dt.astimezone(timezone.utc).replace(second=0,microsecond=0)
        if key in seen: continue
        covers,fraction=ELL.feature_coverage(feature)
        if fraction < min_coverage: continue
        polarizations=p.get("sar:polarizations")
        if isinstance(polarizations,list) and not {"VV","VH"}.issubset(set(polarizations)): continue
        selected.append((feature,covers,fraction))
        seen.add(key)
    return selected

def process(features,output_dir,token,direction,relative_orbit,min_coverage,timeout):
    output_dir.mkdir(parents=True,exist_ok=True)
    rtc_dir=output_dir/"terrain_aux"; rtc_dir.mkdir(parents=True,exist_ok=True)
    scenes=[]; failures=[]
    for feature,covers,fraction in features:
        stamp_dt=datetime.fromisoformat(feature["properties"]["datetime"].replace("Z","+00:00")).astimezone(timezone.utc)
        stamp=stamp_dt.strftime("%Y%m%dT%H%M%SZ")
        ell_name=f"sentinel1_nairobi_stack_{stamp}_vv-vh.tif"
        rtc_name=f"sentinel1_nairobi_{stamp}_gamma0-terrain-rtc.tif"
        try:
            ell_body=ELL.request_geotiff(token,ELL.build_process_payload(feature),timeout=timeout)
            rtc_body=ELL.request_geotiff(token,RTC.build_rtc_payload(feature),timeout=timeout)
            ell_path=output_dir/ell_name; rtc_path=rtc_dir/rtc_name
            ell_path.write_bytes(ell_body); rtc_path.write_bytes(rtc_body)
            with rasterio.open(ell_path) as e, rasterio.open(rtc_path) as r:
                if e.count!=3 or r.count!=6 or e.crs!=r.crs or e.transform!=r.transform or (e.width,e.height)!=(r.width,r.height):
                    raise ValueError("Ellipsoid and RTC outputs do not share the expected grid/bands")
                emask=e.read(3)>0.5; rmask=r.read(6)>0.5
                pair=emask & rmask
                stats=RTC.summarize_rtc(r.read())
                scenes.append({"catalog_item_id":feature.get("id"),
                    "catalog_item_datetime_utc":stamp_dt.isoformat().replace("+00:00","Z"),
                    "catalogue_orbit_direction":direction.upper(),"catalogue_relative_orbit":relative_orbit,
                    "catalogue_footprint_covers_full_aoi":bool(covers),
                    "catalogue_aoi_intersection_fraction":float(fraction),
                    "ellipsoid_valid_pixels":int(emask.sum()),"rtc_valid_pixels":int(rmask.sum()),
                    "pair_common_valid_pixels":int(pair.sum()),
                    "pair_common_valid_fraction":float(pair.mean()),
                    "rtc_statistics":stats,
                    "output":{"file":ell_name}})
            print(f"Processed {stamp}: catalogue coverage={fraction:.4f}; paired valid fraction={pair.mean():.4f}")
        except (OSError,ValueError,RuntimeError,KeyError) as exc:
            failures.append({"item_id":feature.get("id"),"datetime":feature.get("properties",{}).get("datetime"),"error":str(exc)})
            print(f"Failed {stamp}: {exc}",file=sys.stderr)
    stack={"schema":"tessellatum.sentinel1.processed-stack.v1",
        "processing_config":{"bbox_crs84":ELL.NAIROBI_BBOX,"width":ELL.WIDTH,"height":ELL.HEIGHT,
            "bands":["VV","VH","dataMask"],"backscatter_coefficient":"GAMMA0_ELLIPSOID",
            "orthorectify":True,"orbit_direction":direction.upper(),"relative_orbit":relative_orbit,
            "catalogue_minimum_aoi_intersection_fraction":min_coverage},
        "candidate_count":len(features),"processed_count":len(scenes),"failed_count":len(failures),
        "scenes":scenes,"failures":failures,"analysis_ready":False}
    stack_path=output_dir/"sentinel1_nairobi_temporal_stack.metadata.json"
    stack_path.write_text(json.dumps(stack,indent=2)+"\n",encoding="utf-8")
    if failures or len(scenes)!=len(features) or len(scenes)<2:
        raise RuntimeError(f"Alternate-orbit processing incomplete: {len(scenes)}/{len(features)} scenes")
    paired_path=rtc_dir/"sentinel1_nairobi_alternate_orbit_paired_screen.json"
    paired=COMPARE.run(stack_path,output_dir,rtc_dir,paired_path)
    # Compute intersection of data masks across all dates, not only per-date pairs.
    masks=[]
    for scene in scenes:
        with rasterio.open(output_dir/scene["output"]["file"]) as ds: masks.append(ds.read(3)>0.5)
    all_dates=np.logical_and.reduce(masks)
    report={"schema":"tessellatum.sentinel1.alternate-orbit-rtc-screen.v1",
        "orbit":{"direction":direction.upper(),"relative_orbit":relative_orbit},
        "candidate_count":len(features),"processed_count":len(scenes),"failed_count":len(failures),
        "scenes":scenes,"all_date_common_valid_pixels":int(all_dates.sum()),
        "all_date_common_valid_fraction_of_requested_grid":float(all_dates.mean()),
        "paired_comparison_report":paired_path.name,"paired_comparison_status":paired["status"],
        "analysis_ready":False,
        "interpretation":"Independent-orbit diagnostic on a partial-coverage AOI. Only actual common valid pixels are evaluated; no missing area is imputed.",
        "limitations":["The ascending track is not full-AOI coverage; the common data mask may be spatially selective.",
        "Different orbit geometry changes local incidence and viewing direction; do not pool tracks as one time series.",
        "Catalogue footprint fraction is not a substitute for raster dataMask QA.",
        "No independent radiometric reference or geodetic control is provided.",
        "No normalization or change detection is performed."]}
    report_path=output_dir/"sentinel1_nairobi_alternate_orbit_screen.json"
    report_path.write_text(json.dumps(report,indent=2)+"\n",encoding="utf-8")
    print(f"All-date common valid fraction: {all_dates.mean():.4f}; analysis_ready=false")
    return report

def main(argv=None):
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--start",default="2026-10-01T00:00:00Z"); p.add_argument("--end",default="2026-11-23T00:00:00Z")
    p.add_argument("--direction",choices=["ascending","descending"],default="ascending")
    p.add_argument("--relative-orbit",type=int,default=130); p.add_argument("--min-coverage",type=float,default=0.8)
    p.add_argument("--output-dir",type=Path,default=Path("data/sentinelhub/nairobi/alternate_orbit"))
    p.add_argument("--timeout",type=int,default=300); a=p.parse_args(argv)
    if not 0<float(a.min_coverage)<=1 or a.relative_orbit<1 or a.timeout<30: p.error("Invalid coverage, orbit or timeout")
    try:
        token=CAT.request_access_token(os.environ.get("SENTINEL_HUB_CLIENT_ID",""),os.environ.get("SENTINEL_HUB_CLIENT_SECRET",""),timeout=30)
        candidates=select_candidates(collect_track(token,a.start,a.end,a.direction,a.relative_orbit),a.direction,a.relative_orbit,a.min_coverage)
        if len(candidates)<2: raise ValueError(f"Only {len(candidates)} qualifying acquisitions; at least two are required")
        process(candidates,a.output_dir,token,a.direction,a.relative_orbit,a.min_coverage,a.timeout)
    except (OSError,ValueError,RuntimeError) as e:
        print(f"Alternate-orbit screen failed: {e}",file=sys.stderr); return 2
    return 0
if __name__=="__main__": raise SystemExit(main())
