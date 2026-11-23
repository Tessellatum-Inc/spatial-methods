#!/usr/bin/env python3
"""Find repeated Sentinel-1A tracks with useful Nairobi overlap across both orbit directions."""
from __future__ import annotations
import argparse, importlib.util, json, os, sys
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path

RADAR=Path(__file__).resolve().parent
SPEC=importlib.util.spec_from_file_location("query_sentinelhub_sentinel1",RADAR/"query_sentinelhub_sentinel1.py")
if SPEC is None or SPEC.loader is None: raise RuntimeError("Cannot load Sentinel Hub catalogue client")
CAT=importlib.util.module_from_spec(SPEC); SPEC.loader.exec_module(CAT)

def utc(value):
    dt=datetime.fromisoformat(value.replace("Z","+00:00"))
    if dt.tzinfo is None: raise ValueError("Timestamp must include timezone")
    return dt.astimezone(timezone.utc).isoformat().replace("+00:00","Z")

def collect(token,start,end,limit=100,max_pages=50):
    payload=CAT.build_search_payload(start,end,limit); found={}
    for _ in range(max_pages):
        page=CAT.search_catalog(token,payload,timeout=60)
        for feature in page["features"]: found[feature["id"]]=feature
        nxt=page.get("context",{}).get("next")
        if nxt is None: return list(found.values())
        payload={**payload,"next":nxt}
    raise RuntimeError("Catalogue pagination exceeded safety limit")

def feature_coverage(feature):
    from shapely.geometry import box,shape
    try:
        geom=feature.get("geometry")
        if not isinstance(geom,dict): return 0.0
        footprint=shape(geom); aoi=box(*CAT.NAIROBI_BBOX)
        if footprint.is_empty or not footprint.is_valid: return 0.0
        return max(0.0,min(1.0,float(footprint.intersection(aoi).area/aoi.area)))
    except (TypeError,ValueError): return 0.0

def summarize(features,min_scenes=4,min_fraction=0.70):
    groups=defaultdict(list); skipped=0
    for feature in features:
        p=feature.get("properties",{})
        platform=str(p.get("platform","")).lower()
        direction=str(p.get("sat:orbit_state","")).upper()
        orbit=p.get("sat:relative_orbit")
        pols=p.get("sar:polarizations")
        if platform!="sentinel-1a" or direction not in ("ASCENDING","DESCENDING") or not isinstance(orbit,int):
            skipped+=1; continue
        if isinstance(pols,list) and not {"VV","VH"}.issubset(set(pols)): continue
        stamp=p.get("datetime")
        if not isinstance(stamp,str): continue
        try: stamp=utc(stamp)
        except ValueError: continue
        fraction=feature_coverage(feature)
        if fraction<min_fraction: continue
        groups[(platform,direction,orbit)].append({
            "item_id":feature.get("id"),"datetime_utc":stamp,
            "aoi_intersection_fraction":round(fraction,6),"polarizations":pols})
    tracks=[]
    for (platform,direction,orbit),scenes in sorted(groups.items(),key=lambda item:item[0][2]):
        scenes.sort(key=lambda scene:scene["datetime_utc"])
        tracks.append({"platform":platform,"orbit_direction":direction,"relative_orbit":orbit,
            "scene_count":len(scenes),"minimum_aoi_intersection_fraction":min(s["aoi_intersection_fraction"] for s in scenes),
            "median_aoi_intersection_fraction":sorted(s["aoi_intersection_fraction"] for s in scenes)[len(scenes)//2],
            "candidate_for_processing":len(scenes)>=min_scenes and (direction,orbit) not in {("ASCENDING",57),("ASCENDING",130)},
            "scenes":scenes})
    candidates=[t for t in tracks if t["candidate_for_processing"]]
    return {"schema":"tessellatum.sentinel1.same-platform-intermediate-orbit-catalogue-screen.v1",
        "catalogue_feature_count":len(features),"candidate_track_count":len(candidates),
        "minimum_scenes_per_track":min_scenes,"minimum_aoi_intersection_fraction":min_fraction,
        "tracks":tracks,"candidates":candidates,"analysis_ready":False,
        "limitations":["Catalogue footprint overlap does not prove valid raster coverage.",
        "The catalogue does not provide the processed local-incidence-angle distribution used in this comparison.",
        "A candidate must be processed and its RTC angle band measured before it can be judged intermediate.",
        "No normalization, calibration or change detection is performed."]}

def main(argv=None):
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--start",default="2025-01-01T00:00:00Z")
    p.add_argument("--end",default="2025-02-20T00:00:00Z")
    p.add_argument("--min-scenes",type=int,default=4)
    p.add_argument("--min-fraction",type=float,default=0.70)
    p.add_argument("--output",type=Path,default=Path("data/sentinelhub/nairobi/same_platform_intermediate_orbit_candidates.json"))
    a=p.parse_args(argv)
    if a.min_scenes<2 or not 0<a.min_fraction<=1: p.error("Invalid scene-count or coverage threshold")
    try:
        utc(a.start); utc(a.end)
        token=CAT.request_access_token(os.environ.get("SENTINEL_HUB_CLIENT_ID",""),os.environ.get("SENTINEL_HUB_CLIENT_SECRET",""),timeout=30)
        features=collect(token,a.start,a.end)
        report=summarize(features,a.min_scenes,a.min_fraction)
    except (OSError,ValueError,RuntimeError) as exc:
        print(f"Intermediate-orbit catalogue screen failed: {exc}",file=sys.stderr); return 2
    report["query"]={"collection":"sentinel-1-grd","instrument_mode":"IW","bbox_crs84":CAT.NAIROBI_BBOX,
        "start":utc(a.start),"end":utc(a.end),"platform":"sentinel-1a","orbit_direction":"ASCENDING_AND_DESCENDING"}
    report["retrieved_at_utc"]=datetime.now(timezone.utc).isoformat().replace("+00:00","Z")
    a.output.parent.mkdir(parents=True,exist_ok=True); a.output.write_text(json.dumps(report,indent=2)+"\n",encoding="utf-8")
    print(f"Catalogue features: {len(features)}; qualifying tracks: {len(report['tracks'])}; intermediate candidates: {len(report['candidates'])}")
    for track in report["candidates"]:
        print(f"{track['orbit_direction']} R{track['relative_orbit']:03d}: {track['scene_count']} scenes; median AOI overlap={track['median_aoi_intersection_fraction']:.3f}")
    print(f"Report: {a.output}; analysis_ready=false")
    return 0
if __name__=="__main__": raise SystemExit(main())
