#!/usr/bin/env python3
"""Catalogue-only inspection of Sentinel-1 product assets for ellipsoid incidence-angle QA."""
from __future__ import annotations
import argparse, importlib.util, json, os, sys
from datetime import datetime, timezone
from pathlib import Path

RADAR=Path(__file__).resolve().parent
SPEC=importlib.util.spec_from_file_location("query_sentinelhub_sentinel1",RADAR/"query_sentinelhub_sentinel1.py")
if SPEC is None or SPEC.loader is None: raise RuntimeError("Cannot load Sentinel Hub catalogue client")
CAT=importlib.util.module_from_spec(SPEC); SPEC.loader.exec_module(CAT)

def collect(token,start,end):
    payload=CAT.build_search_payload(start,end,100); found={}
    for _ in range(50):
        page=CAT.search_catalog(token,payload,timeout=60)
        for feature in page["features"]: found[feature["id"]]=feature
        nxt=page.get("context",{}).get("next")
        if nxt is None: return list(found.values())
        payload={**payload,"next":nxt}
    raise RuntimeError("Catalogue pagination exceeded 50 pages")

def run(features,orbits):
    rows=[]
    for f in features:
        p=f.get("properties",{})
        if str(p.get("platform","")).lower()!="sentinel-1a": continue
        if str(p.get("sat:orbit_state","")).upper()!="ASCENDING": continue
        if p.get("sat:relative_orbit") not in orbits: continue
        if p.get("sar:instrument_mode") not in (None,"IW"): continue
        pols=p.get("sar:polarizations")
        if isinstance(pols,list) and not {"VV","VH"}.issubset(set(pols)): continue
        assets={}
        for key,value in (f.get("assets") or {}).items():
            if not isinstance(value,dict): continue
            assets[key]={k:value.get(k) for k in ("href","type","title","roles","description") if value.get(k) is not None}
        rows.append({"item_id":f.get("id"),"datetime_utc":p.get("datetime"),
            "relative_orbit":p.get("sat:relative_orbit"),"platform":p.get("platform"),
            "orbit_direction":p.get("sat:orbit_state"),"polarizations":pols,
            "product_identifier":p.get("s1:product_identifier") or p.get("sentinel1:product_identifier"),
            "assets":assets,"links":[{"rel":x.get("rel"),"href":x.get("href"),"type":x.get("type")}
                for x in f.get("links",[]) if isinstance(x,dict) and x.get("rel") in ("self","via","derived_from","parent")]})
    rows.sort(key=lambda x:(x["relative_orbit"],x["datetime_utc"] or ""))
    return {"schema":"tessellatum.sentinel1.ellipsoid-incidence-asset-inventory.v1",
        "tracks":[57,130],"platform":"Sentinel-1A","orbit_direction":"ASCENDING",
        "feature_count":len(rows),"items":rows,"analysis_ready":False,
        "purpose":"Locate original GRD annotation/geolocation-grid assets containing the ellipsoid incidenceAngle field. This is metadata discovery only."}

def main(argv=None):
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--start",default="2025-01-01T00:00:00Z")
    p.add_argument("--end",default="2025-02-20T00:00:00Z")
    p.add_argument("--output",type=Path,default=Path("data/sentinelhub/nairobi/sentinel1_ellipsoid_incidence_asset_inventory.json"))
    a=p.parse_args(argv)
    try:
        token=CAT.request_access_token(os.environ.get("SENTINEL_HUB_CLIENT_ID",""),os.environ.get("SENTINEL_HUB_CLIENT_SECRET",""),timeout=30)
        report=run(collect(token,a.start,a.end),{57,130})
    except (OSError,ValueError,RuntimeError) as exc:
        print(f"Asset inventory failed: {exc}",file=sys.stderr); return 2
    report["query"]={"start":a.start,"end":a.end,"collection":"sentinel-1-grd","bbox_crs84":CAT.NAIROBI_BBOX}
    report["retrieved_at_utc"]=datetime.now(timezone.utc).isoformat().replace("+00:00","Z")
    a.output.parent.mkdir(parents=True,exist_ok=True); a.output.write_text(json.dumps(report,indent=2)+"\n",encoding="utf-8")
    print(f"Matching product items: {len(report['items'])}")
    for row in report["items"]:
        print(f"R{row['relative_orbit']:03d} {row['datetime_utc']} {row['item_id']} asset_keys={','.join(row['assets'])}")
        for key,value in row["assets"].items():
            href=value.get("href","")
            if "annotation" in href.lower() or "manifest" in href.lower() or "product" in key.lower():
                print(f"  {key}: {href}")
    print(f"Report: {a.output}; analysis_ready=false")
    return 0
if __name__=="__main__": raise SystemExit(main())
