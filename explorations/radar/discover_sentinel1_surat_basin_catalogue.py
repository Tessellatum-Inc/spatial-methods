#!/usr/bin/env python3
"""Discover repeated Sentinel-1A IW acquisitions covering the CEOS Surat Basin reflector array."""
from __future__ import annotations
import argparse, importlib.util, json, os, sys
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path
from shapely.geometry import Point, shape

RADAR=Path(__file__).resolve().parent
def load_helper(name,path):
    spec=importlib.util.spec_from_file_location(name,RADAR/path)
    if spec is None or spec.loader is None: raise RuntimeError(f"Cannot load {path}")
    module=importlib.util.module_from_spec(spec); spec.loader.exec_module(module); return module
CAT=load_helper("query_sentinelhub_sentinel1","query_sentinelhub_sentinel1.py")
CEOS=load_helper("inventory_ceos_surat_corner_reflectors","inventory_ceos_surat_corner_reflectors.py")

def collect(token,bbox,start,end,limit=100,max_pages=50):
    payload=CAT.build_search_payload(start,end,limit); payload["bbox"]=bbox
    found={}
    for _ in range(max_pages):
        page=CAT.search_catalog(token,payload,timeout=60)
        for feature in page["features"]: found[feature["id"]]=feature
        nxt=page.get("context",{}).get("next")
        if nxt is None: return list(found.values()),payload
        payload={**payload,"next":nxt}
    raise RuntimeError("Catalogue pagination exceeded safety limit")

def count_covered_targets(feature,targets):
    geometry=feature.get("geometry")
    if not isinstance(geometry,dict): return 0
    try: footprint=shape(geometry)
    except Exception: return 0
    if footprint.is_empty or not footprint.is_valid: return 0
    return sum(1 for target in targets if footprint.covers(Point(target["longitude"],target["latitude"])))

def summarize(features,targets,min_scenes=4,min_target_fraction=0.90):
    groups=defaultdict(list)
    for feature in features:
        props=feature.get("properties",{})
        platform=str(props.get("platform","")).lower()
        direction=str(props.get("sat:orbit_state","")).upper()
        orbit=props.get("sat:relative_orbit")
        if platform!="sentinel-1a" or direction not in ("ASCENDING","DESCENDING") or not isinstance(orbit,int): continue
        stamp=props.get("datetime")
        if not isinstance(stamp,str): continue
        try:
            dt=datetime.fromisoformat(stamp.replace("Z","+00:00"))
            if dt.tzinfo is None: continue
            stamp=dt.astimezone(timezone.utc).isoformat().replace("+00:00","Z")
        except ValueError: continue
        covered=count_covered_targets(feature,targets)
        fraction=covered/len(targets)
        pols=props.get("sar:polarizations")
        groups[(platform,direction,orbit)].append({"item_id":feature.get("id"),
            "datetime_utc":stamp,"covered_target_count":covered,
            "target_coverage_fraction":round(fraction,6),
            "polarizations":pols if isinstance(pols,list) else []})
    tracks=[]
    for (platform,direction,orbit),scenes in sorted(groups.items(),key=lambda x:(x[0][1],x[0][2])):
        scenes.sort(key=lambda x:x["datetime_utc"])
        fractions=[x["target_coverage_fraction"] for x in scenes]
        full=[x for x in scenes if x["target_coverage_fraction"]>=min_target_fraction
            and {"VV","VH"}.issubset(set(x["polarizations"]))]
        tracks.append({"platform":platform,"orbit_direction":direction,"relative_orbit":orbit,
            "scene_count":len(scenes),"scenes_with_target_coverage_threshold_and_dual_pol":len(full),
            "minimum_target_coverage_fraction":min(fractions),"median_target_coverage_fraction":sorted(fractions)[len(fractions)//2],
            "candidate_for_processing":direction=="ASCENDING" and len(full)>=min_scenes,
            "qualifying_scenes":full,"scenes":scenes})
    candidates=[t for t in tracks if t["candidate_for_processing"]]
    return {"schema":"tessellatum.sentinel1.surat-basin-corner-reflector-catalogue-screen.v1",
        "catalogue_feature_count":len(features),"target_count":len(targets),
        "track_count":len(tracks),"candidate_track_count":len(candidates),
        "minimum_scenes":min_scenes,"minimum_target_coverage_fraction":min_target_fraction,
        "tracks":tracks,"candidates":candidates,"analysis_ready":False,
        "limitations":["Catalogue footprints are used only to screen whether surveyed reflector coordinates fall inside a scene; they do not establish pixel-level data validity.",
            "Corner-reflector orientation and visibility must be checked for each acquisition.",
            "The catalogue screen does not prove the provider's RTC and ellipsoid outputs have matching coverage or processing lineage.",
            "No radiometric calibration or change detection is performed."]}

def main(argv=None):
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--start",default="2025-01-01T00:00:00Z")
    p.add_argument("--end",default="2026-11-23T00:00:00Z")
    p.add_argument("--min-scenes",type=int,default=4)
    p.add_argument("--min-target-fraction",type=float,default=0.90)
    p.add_argument("--output",type=Path,default=Path("data/sentinelhub/surat_basin/sentinel1a_catalogue_candidates.json"))
    a=p.parse_args(argv)
    if a.min_scenes<2 or not 0<a.min_target_fraction<=1: p.error("Invalid candidate thresholds")
    try:
        targets=CEOS.parse_surat_targets(CEOS.fetch_kml())
        lons=[x["longitude"] for x in targets]; lats=[x["latitude"] for x in targets]
        pad=0.05
        bbox=[min(lons)-pad,min(lats)-pad,max(lons)+pad,max(lats)+pad]
        token=CAT.request_access_token(os.environ.get("SENTINEL_HUB_CLIENT_ID",""),
            os.environ.get("SENTINEL_HUB_CLIENT_SECRET",""),timeout=30)
        features,payload=collect(token,bbox,a.start,a.end)
        report=summarize(features,targets,a.min_scenes,a.min_target_fraction)
    except Exception as exc:
        print(f"Surat Basin Sentinel-1 catalogue screen failed: {type(exc).__name__}: {exc}",file=sys.stderr); return 2
    report["query"]={"collection":"sentinel-1-grd","instrument_mode":"IW","bbox_crs84":bbox,
        "start":a.start,"end":a.end,"platform":"sentinel-1a",
        "target_extent_buffer_degrees":pad,"pagination_complete":True}
    report["retrieved_at_utc"]=datetime.now(timezone.utc).isoformat().replace("+00:00","Z")
    report["target_coordinates"]=targets
    a.output.parent.mkdir(parents=True,exist_ok=True); a.output.write_text(json.dumps(report,indent=2)+"\n",encoding="utf-8")
    print(f"CEOS targets: {len(targets)}; Sentinel-1A IW features: {len(features)}; qualifying tracks: {len(report['tracks'])}; ascending candidates: {len(report['candidates'])}")
    for track in report["tracks"]:
        print(f"{track['orbit_direction']} R{track['relative_orbit']:03d}: scenes={track['scene_count']}; qualifying dual-pol scenes={track['scenes_with_target_coverage_threshold_and_dual_pol']}; median target coverage={track['median_target_coverage_fraction']:.3f}; candidate={track['candidate_for_processing']}")
    print(f"Report: {a.output}; analysis_ready=false")
    return 0
if __name__=="__main__": raise SystemExit(main())
