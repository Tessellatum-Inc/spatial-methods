#!/usr/bin/env python3
"""Inventory the CEOS SAR Cal/Val Surat Basin corner-reflector coordinates."""
from __future__ import annotations
import argparse, json, sys
from datetime import datetime, timezone
from pathlib import Path
from urllib.request import Request, urlopen
from xml.etree import ElementTree as ET

KML_URL="https://calvalportal.ceos.org/documents/10136/26472/CEOS-reference-targets.kml/be2807cf-2b33-45ca-932f-a91ddc0d2cb1"
CEOS_SITE_URL="https://calvalportal.ceos.org/surat-basin-queensland-australia"

def local_name(tag:str)->str: return tag.rsplit("}",1)[-1]

def parse_surat_targets(kml_bytes:bytes)->list[dict]:
    root=ET.fromstring(kml_bytes); targets=[]
    for placemark in root.iter():
        if local_name(placemark.tag)!="Placemark": continue
        values={}
        for child in placemark.iter():
            name=local_name(child.tag)
            if name in ("name","description","coordinates") and child.text:
                values.setdefault(name,child.text.strip())
        name=values.get("name","")
        if "surat basin" not in name.lower(): continue
        coordinate_text=values.get("coordinates","").strip()
        if not coordinate_text: continue
        first=coordinate_text.split()[0].split(",")
        if len(first)<2: continue
        try: lon,lat=float(first[0]),float(first[1])
        except ValueError: continue
        if not (-28.5<=lat<=-25.0 and 149.0<=lon<=153.0):
            raise ValueError(f"Surat target outside expected regional bounds: {name} ({lon},{lat})")
        targets.append({"name":name,"longitude":lon,"latitude":lat})
    targets.sort(key=lambda x:x["name"])
    names=[t["name"].lower() for t in targets]
    if len(targets)!=40: raise ValueError(f"Expected 40 CEOS Surat Basin targets; parsed {len(targets)}")
    if len(set(names))!=40: raise ValueError("Duplicate Surat Basin target names in CEOS KML")
    if len({(t["longitude"],t["latitude"]) for t in targets})!=40:
        raise ValueError("Duplicate Surat Basin target coordinates in CEOS KML")
    return targets

def fetch_kml(timeout:int=60)->bytes:
    request=Request(KML_URL,headers={"User-Agent":"Tessellatum-Spatial-Methods/1.0","Accept":"application/vnd.google-earth.kml+xml, application/xml, text/xml"})
    with urlopen(request,timeout=timeout) as response:
        body=response.read()
    if not body: raise ValueError("CEOS target KML response was empty")
    return body

def build_report(targets,kml_bytes):
    lons=[x["longitude"] for x in targets]; lats=[x["latitude"] for x in targets]
    return {"schema":"tessellatum.ceos.surat-basin-corner-reflectors.v1",
        "source":"CEOS SAR Subgroup Point and Distributed Targets Database",
        "source_kml_url":KML_URL,"source_site_url":CEOS_SITE_URL,
        "retrieved_at_utc":datetime.now(timezone.utc).isoformat().replace("+00:00","Z"),
        "source_kml_bytes":len(kml_bytes),"target_count":len(targets),"targets":targets,
        "extent_wgs84":{"west":min(lons),"south":min(lats),"east":max(lons),"north":max(lats)},
        "limitations":["Coordinates are reproduced from the CEOS target database KML; verify against the latest Geoscience Australia survey record before precision geolocation work.",
            "A reflector coordinate is not itself a radiometric measurement; target orientation, maintenance state, acquisition geometry and point-target extraction still require validation."],
        "analysis_ready":False}

def main(argv=None):
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--output",type=Path,default=Path("data/sentinelhub/surat_basin/ceos_surat_basin_corner_reflectors.json"))
    p.add_argument("--timeout",type=int,default=60)
    a=p.parse_args(argv)
    if a.timeout<1: p.error("--timeout must be positive")
    try:
        body=fetch_kml(a.timeout); targets=parse_surat_targets(body); report=build_report(targets,body)
    except Exception as exc:
        print(f"CEOS Surat target inventory failed: {type(exc).__name__}: {exc}",file=sys.stderr); return 2
    a.output.parent.mkdir(parents=True,exist_ok=True); a.output.write_text(json.dumps(report,indent=2)+"\n",encoding="utf-8")
    extent=report["extent_wgs84"]
    print(f"CEOS Surat Basin targets: {len(targets)}")
    print(f"WGS84 extent: {extent['west']:.6f},{extent['south']:.6f},{extent['east']:.6f},{extent['north']:.6f}")
    print(f"Report: {a.output}; analysis_ready=false")
    return 0
if __name__=="__main__": raise SystemExit(main())
