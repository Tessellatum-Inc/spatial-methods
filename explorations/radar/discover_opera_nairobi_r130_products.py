#!/usr/bin/env python3
"""Discover OPERA RTC-S1 products for the Nairobi ascending R130 candidate.

This is catalogue screening only. It does not download raster assets or claim
that any OPERA item matches a Sentinel Hub GRD acquisition.
"""
from __future__ import annotations
import argparse, hashlib, json, re, sys
from datetime import datetime, timezone
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from urllib.request import Request, urlopen

API_URL = "https://api.daac.asf.alaska.edu/services/search/param"
BBOX = (36.65, -1.45, 37.05, -1.15)
WKT = ("polygon((36.65 -1.45, 37.05 -1.45, 37.05 -1.15, "
       "36.65 -1.15, 36.65 -1.45))")
TARGET_RELATIVE_ORBIT = 130
BURST_RE = re.compile(r"T(\d{3})[-_](\d{6})[-_]IW(\d)", re.I)
STAMP_RE = re.compile(r"(20\d{6})T(\d{6})Z?")


def build_query(start: str, end: str, max_results: int = 2000) -> dict[str, str]:
    if max_results < 1:
        raise ValueError("max_results must be positive")
    for value in (start, end):
        dt = datetime.fromisoformat(value.replace("Z", "+00:00"))
        if dt.tzinfo is None or dt.utcoffset().total_seconds() != 0:
            raise ValueError("timestamps must be UTC")
    if datetime.fromisoformat(start.replace("Z", "+00:00")) >= datetime.fromisoformat(end.replace("Z", "+00:00")):
        raise ValueError("start must be before end")
    return {"dataset":"OPERA-S1","processingLevel":"RTC","intersectsWith":WKT,
            "start":start,"end":end,"output":"geojson","maxResults":str(max_results)}


def retrieve(params: dict[str,str], timeout: int) -> tuple[bytes,str]:
    url = API_URL + "?" + urlencode(params)
    req = Request(url, headers={"Accept":"application/geo+json, application/json",
                                "User-Agent":"Tessellatum-Spatial-Methods/1.0"})
    with urlopen(req, timeout=timeout) as response:
        return response.read(), url


def parse_collection(raw: bytes) -> dict:
    data=json.loads(raw)
    if data.get("type")!="FeatureCollection" or not isinstance(data.get("features"),list):
        raise ValueError("ASF response is not a GeoJSON FeatureCollection")
    return data


def prop(p:dict,*keys):
    for k in keys:
        if p.get(k) not in (None,""): return p[k]
    return None


def identify(p:dict) -> dict:
    text=" ".join(str(prop(p,k) or "") for k in
                  ("fileID","fileName","granuleName","sceneName","productName"))
    burst=prop(p,"operaBurstID","operaBurstId","burstID")
    match=BURST_RE.search(str(burst or text))
    stamp=prop(p,"startTime","starttime","acquisitionDate","sceneDate")
    if not stamp:
        m=STAMP_RE.search(text)
        if m: stamp=datetime.strptime("".join(m.groups()),"%Y%m%d%H%M%S").replace(tzinfo=timezone.utc).isoformat().replace("+00:00","Z")
    acquired=None
    if stamp:
        try:
            acquired=datetime.fromisoformat(str(stamp).replace("Z","+00:00"))
            if acquired.tzinfo is None: acquired=acquired.replace(tzinfo=timezone.utc)
            acquired=acquired.astimezone(timezone.utc).isoformat().replace("+00:00","Z")
        except ValueError: acquired=None
    return {"burst_id":str(burst or (match.group(0) if match else "")),
            "relative_orbit_from_burst":int(match.group(1)) if match else None,
            "acquisition_datetime_utc":acquired,
            "polarization":prop(p,"polarization","polarisation"),
            "platform":prop(p,"platform","platformName"),
            "file_id":prop(p,"fileID","fileId","granuleName","sceneName"),
            "product_name":prop(p,"fileName","productName","granuleName")}


def summarize(collection:dict) -> dict:
    rows=[]
    all_identified=[]
    for feature in collection["features"]:
        p=feature.get("properties") or {}
        item=identify(p)
        all_identified.append(item)
        if item["relative_orbit_from_burst"] != TARGET_RELATIVE_ORBIT: continue
        rows.append({**item,"properties":p,"geometry":feature.get("geometry")})
    rows.sort(key=lambda x:(x["acquisition_datetime_utc"] or "",x["burst_id"],str(x["polarization"])))
    groups={}
    for row in rows:
        # Burst start times differ by seconds within one Sentinel-1 pass.
        # Group by UTC acquisition date; retain each burst's exact timestamp.
        key=row["acquisition_datetime_utc"][:10] if row["acquisition_datetime_utc"] else "unknown"
        groups.setdefault(key,[]).append(row)
    return {"schema":"tessellatum.opera-nairobi-r130-catalogue-discovery.v1",
        "query":{"source":API_URL,"aoi_bbox_wgs84":list(BBOX),"wkt":WKT,
                 "target_relative_orbit":TARGET_RELATIVE_ORBIT},
        "catalogue_feature_count":len(collection["features"]),
        "catalogue_burst_id_samples":all_identified[:20],
        "observed_relative_orbit_counts":{str(k):sum(1 for x in all_identified if x["relative_orbit_from_burst"]==k)
            for k in sorted({x["relative_orbit_from_burst"] for x in all_identified if x["relative_orbit_from_burst"] is not None})},
        "target_orbit_feature_count":len(rows),
        "acquisition_groups":[{"acquisition_date_utc":k,"feature_count":len(v),
             "burst_ids":sorted({x["burst_id"] for x in v}),
             "burst_start_times_utc":sorted({x["acquisition_datetime_utc"] for x in v if x["acquisition_datetime_utc"]}),
             "polarizations":sorted({pol for x in v for pol in (x["polarization"] if isinstance(x["polarization"],list) else [x["polarization"]]) if pol}),
             "products":v} for k,v in groups.items()],
        "features":rows,
        "limitations":["Burst track number is used as a relative-orbit candidate and must be cross-checked against source Sentinel-1 metadata.",
          "Catalogue intersection is not raster-valid coverage.",
          "A date/time match to Sentinel Hub is only a candidate until original source scene identity is reconciled.",
          "This report does not establish availability of matching RTC-STATIC layers or radiometric comparability."]}


def main(argv=None):
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--start",default="2026-10-01T00:00:00Z")
    p.add_argument("--end",default="2026-11-24T00:00:00Z")
    p.add_argument("--max-results",type=int,default=2000)
    p.add_argument("--timeout",type=int,default=120)
    p.add_argument("--output",type=Path,default=Path("data/asf/nairobi_r130/opera_rtc_catalogue.json"))
    a=p.parse_args(argv)
    try:
        raw,url=retrieve(build_query(a.start,a.end,a.max_results),a.timeout)
        collection=parse_collection(raw); report=summarize(collection)
    except HTTPError as e:
        print(f"ASF HTTP error {e.code}: {e.reason}",file=sys.stderr); return 2
    except (URLError,TimeoutError,OSError,ValueError,json.JSONDecodeError) as e:
        print(f"ASF catalogue discovery failed: {e}",file=sys.stderr); return 3
    report["query"]["url"]=url
    report["query"]["response_sha256"]=hashlib.sha256(raw).hexdigest()
    report["query"]["start"]=a.start; report["query"]["end"]=a.end
    a.output.parent.mkdir(parents=True,exist_ok=True)
    a.output.write_text(json.dumps(report,indent=2)+"\n",encoding="utf-8")
    print(f"ASF features: {report['catalogue_feature_count']}; R130 burst features: {report['target_orbit_feature_count']}; acquisition groups: {len(report['acquisition_groups'])}")
    print(f"Observed relative-orbit counts: {report['observed_relative_orbit_counts']}")
    print(f"First catalogue samples: {report['catalogue_burst_id_samples'][:5]}")
    for g in report["acquisition_groups"]:
        print(f"{g['acquisition_datetime_utc']} | bursts={len(g['burst_ids'])} | pols={','.join(g['polarizations'])}")
    print(f"Report: {a.output}")
    return 0

if __name__=="__main__": raise SystemExit(main())
