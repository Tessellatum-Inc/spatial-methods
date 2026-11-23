#!/usr/bin/env python3
"""Discover repeated Sentinel-1A IW acquisitions covering the CEOS Surat Basin reflector array."""
from __future__ import annotations
import argparse, importlib.util, json, os, sys
from collections import defaultdict
from datetime import datetime, timezone
from itertools import combinations
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

def covered_target_names(feature,targets):
    geometry=feature.get("geometry")
    if not isinstance(geometry,dict): return []
    try: footprint=shape(geometry)
    except Exception: return []
    if footprint.is_empty or not footprint.is_valid: return []
    return [target["name"] for target in targets
        if footprint.covers(Point(target["longitude"],target["latitude"]))]

def select_common_scene_set(scenes,count=4,max_span_days=90):
    best_scenes=[]; best_targets=[]; best_key=None
    for group in combinations(scenes,count):
        dates=[datetime.fromisoformat(x["datetime_utc"].replace("Z","+00:00")) for x in group]
        span=(max(dates)-min(dates)).total_seconds()/86400.0
        if span>max_span_days: continue
        common=set(group[0]["covered_target_names"])
        for scene in group[1:]: common.intersection_update(scene["covered_target_names"])
        key=(len(common),-span,tuple(x["datetime_utc"] for x in group))
        if best_key is None or key[:2]>best_key[:2]:
            best_key=key; best_scenes=list(group); best_targets=sorted(common)
    return best_scenes,best_targets

def summarize(features,targets,min_scenes=4,min_target_fraction=0.90,min_repeated_targets=10,min_scene_targets=10):
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
        covered_names=covered_target_names(feature,targets)
        fraction=len(covered_names)/len(targets)
        pols=props.get("sar:polarizations")
        groups[(platform,direction,orbit)].append({"item_id":feature.get("id"),
            "datetime_utc":stamp,"covered_target_count":len(covered_names),
            "covered_target_names":covered_names,"target_coverage_fraction":round(fraction,6),
            "polarizations":pols if isinstance(pols,list) else []})
    tracks=[]
    for (platform,direction,orbit),scenes in sorted(groups.items(),key=lambda x:(x[0][1],x[0][2])):
        scenes.sort(key=lambda x:x["datetime_utc"])
        fractions=[x["target_coverage_fraction"] for x in scenes]
        dual=[x for x in scenes if {"VV","VH"}.issubset(set(x["polarizations"]))]
        full=[x for x in dual if x["target_coverage_fraction"]>=min_target_fraction]
        partial=[x for x in dual if x["covered_target_count"]>=min_scene_targets]
        target_counts={target["name"]:sum(target["name"] in scene["covered_target_names"] for scene in dual) for target in targets}
        repeated=[name for name,count in target_counts.items() if count>=min_scenes]
        selected,common_targets=select_common_scene_set(partial,min_scenes)
        partial_candidate=direction=="ASCENDING" and len(selected)==min_scenes and len(common_targets)>=min_repeated_targets
        full_candidate=direction=="ASCENDING" and len(full)>=min_scenes
        chosen=selected if partial_candidate else full
        tracks.append({"platform":platform,"orbit_direction":direction,"relative_orbit":orbit,
            "scene_count":len(scenes),"dual_pol_scene_count":len(dual),
            "scenes_with_full_array_coverage":len(full),"scenes_with_minimum_partial_target_count":len(partial),
            "minimum_target_coverage_fraction":min(fractions),"median_target_coverage_fraction":sorted(fractions)[len(fractions)//2],
            "repeated_target_count":len(repeated),"repeated_target_names":repeated,
            "best_common_subset_target_count":len(common_targets),"best_common_subset_target_names":common_targets,
            "partial_array_candidate":partial_candidate,"full_array_candidate":full_candidate,
            "candidate_for_processing":partial_candidate or full_candidate,
            "qualifying_scene_count":len(chosen),"qualifying_scenes":chosen,"scenes":scenes})
    candidates=[t for t in tracks if t["candidate_for_processing"]]
    return {"schema":"tessellatum.sentinel1.surat-basin-corner-reflector-catalogue-screen.v1",
        "catalogue_feature_count":len(features),"target_count":len(targets),
        "track_count":len(tracks),"candidate_track_count":len(candidates),
        "minimum_scenes":min_scenes,"minimum_target_coverage_fraction":min_target_fraction,
        "minimum_repeated_targets":min_repeated_targets,"minimum_targets_per_scene":min_scene_targets,
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
        print(f"{track['orbit_direction']} R{track['relative_orbit']:03d}: scenes={track['scene_count']}; full-array scenes={track['scenes_with_full_array_coverage']}; repeated targets={track['repeated_target_count']}; partial candidate={track['partial_array_candidate']}; candidate={track['candidate_for_processing']}")
        if track["candidate_for_processing"]:
            print("  Common reflectors across selected acquisitions: " + ", ".join(track["best_common_subset_target_names"]))
            for scene in track["qualifying_scenes"]:
                print(f"  SELECT {scene['datetime_utc']}: {scene['covered_target_count']} targets; {scene['item_id']}")
    print(f"Report: {a.output}; analysis_ready=false")
    return 0
if __name__=="__main__": raise SystemExit(main())
