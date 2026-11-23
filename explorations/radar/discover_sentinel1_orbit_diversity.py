#!/usr/bin/env python3
"""Catalogue-only discovery of Sentinel-1 IW tracks independent of Nairobi R079."""
from __future__ import annotations
import argparse, importlib.util, json, os, sys
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path

RADAR=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location("query_sentinelhub_sentinel1",RADAR/"query_sentinelhub_sentinel1.py")
if spec is None or spec.loader is None: raise RuntimeError("Cannot load catalogue client")
CAT=importlib.util.module_from_spec(spec); spec.loader.exec_module(CAT)
BASELINE=("DESCENDING",79)

def utc(value):
    dt=datetime.fromisoformat(value.replace("Z","+00:00"))
    if dt.tzinfo is None: raise ValueError("Timestamp must include timezone")
    return dt.astimezone(timezone.utc).isoformat().replace("+00:00","Z")

def coverage(feature):
    from shapely.geometry import box,shape
    try:
        geom=feature.get("geometry")
        if not isinstance(geom,dict): return False,0.0
        footprint=shape(geom); aoi=box(*CAT.NAIROBI_BBOX)
        if footprint.is_empty or not footprint.is_valid: return False,0.0
        fraction=float(footprint.intersection(aoi).area/aoi.area)
        return bool(footprint.covers(aoi)),max(0.0,min(1.0,fraction))
    except (TypeError,ValueError): return False,0.0

def collect(token,start,end,limit=100,max_pages=50):
    payload=CAT.build_search_payload(start,end,limit); found={}
    for _ in range(max_pages):
        page=CAT.search_catalog(token,payload,timeout=60)
        for f in page["features"]: found[f["id"]]=f
        nxt=page.get("context",{}).get("next")
        if nxt is None: return list(found.values())
        payload={**payload,"next":nxt}
    raise RuntimeError("Catalogue pagination exceeded safety limit")

def summarize(features,min_acquisitions=2):
    groups=defaultdict(list); missing=0; partial=0
    for f in features:
        p=f.get("properties",{}); direction=p.get("sat:orbit_state"); orbit=p.get("sat:relative_orbit")
        direction=direction.upper() if isinstance(direction,str) else None
        if direction not in ("ASCENDING","DESCENDING") or not isinstance(orbit,int):
            missing+=1; continue
        full,fraction=coverage(f); partial+=not full
        try: stamp=utc(p["datetime"])
        except (KeyError,TypeError,ValueError): stamp=None
        groups[(direction,orbit)].append({"item_id":f.get("id"),"datetime_utc":stamp,
            "platform":p.get("platform"),"polarizations":p.get("sar:polarizations"),
            "full_aoi_coverage":full,"aoi_intersection_fraction":round(fraction,6)})
    tracks=[]
    for (direction,orbit),scenes in sorted(groups.items()):
        scenes.sort(key=lambda x:x["datetime_utc"] or "")
        full=[s for s in scenes if s["full_aoi_coverage"]]
        independent=(direction,orbit)!=BASELINE
        tracks.append({"orbit_direction":direction,"relative_orbit":orbit,
            "independent_of_baseline":independent,"catalogue_item_count":len(scenes),
            "full_aoi_item_count":len(full),
            "candidate_for_followup":independent and len(full)>=min_acquisitions,"scenes":scenes})
    candidates=[t for t in tracks if t["candidate_for_followup"]]
    return {"baseline":{"orbit_direction":BASELINE[0],"relative_orbit":BASELINE[1]},
        "catalogue_feature_count":len(features),"tracks_with_orbit_metadata":len(tracks),
        "features_missing_orbit_metadata":missing,"partial_or_noncovering_feature_count":partial,
        "minimum_full_coverage_acquisitions":min_acquisitions,"tracks":tracks,
        "independent_full_coverage_candidates":candidates,
        "status":"candidate_tracks_found" if candidates else "no_independent_full_coverage_track_found",
        "analysis_ready":False,
        "limitations":["Catalogue footprints are a discovery screen, not proof of valid raster coverage.",
        "A candidate requires repeated full-AOI items but still needs same-track processing and geometric QA.",
        "No raster processing, normalization, calibration or change detection is performed."]}

def main(argv=None):
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--start",default="2026-10-01T00:00:00Z")
    p.add_argument("--end",default="2026-11-23T00:00:00Z")
    p.add_argument("--min-acquisitions",type=int,default=2)
    p.add_argument("--output",type=Path,default=Path("data/sentinelhub/nairobi/sentinel1_orbit_diversity_screen.json"))
    a=p.parse_args(argv)
    if a.min_acquisitions<2: p.error("--min-acquisitions must be >=2")
    try:
        utc(a.start); utc(a.end)
        token=CAT.request_access_token(os.environ.get("SENTINEL_HUB_CLIENT_ID",""),os.environ.get("SENTINEL_HUB_CLIENT_SECRET",""),timeout=30)
        features=collect(token,a.start,a.end)
        report=summarize(features,a.min_acquisitions)
    except (OSError,ValueError,RuntimeError) as e:
        print(f"Orbit-diversity screen failed: {e}",file=sys.stderr); return 2
    report["query"]={"collection":"sentinel-1-grd","instrument_mode":"IW","bbox_crs84":CAT.NAIROBI_BBOX,"start":a.start,"end":a.end}
    report["retrieved_at_utc"]=datetime.now(timezone.utc).isoformat().replace("+00:00","Z")
    a.output.parent.mkdir(parents=True,exist_ok=True); a.output.write_text(json.dumps(report,indent=2)+"\n",encoding="utf-8")
    print(f"Catalogue features: {len(features)}; independent repeated full-AOI tracks: {len(report['independent_full_coverage_candidates'])}")
    for t in report["independent_full_coverage_candidates"]: print(f"{t['orbit_direction']} R{t['relative_orbit']}: {t['full_aoi_item_count']} full-AOI items")
    print(f"Report: {a.output}; analysis_ready=false")
    return 0
if __name__=="__main__": raise SystemExit(main())
