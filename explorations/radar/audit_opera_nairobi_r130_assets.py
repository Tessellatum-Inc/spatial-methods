#!/usr/bin/env python3
"""Audit OPERA R130 HDF5 source metadata and RTC/RTC-STATIC raster grids."""
from __future__ import annotations
import argparse, json, re, sys
from pathlib import Path
import h5py
import numpy as np
import rasterio

SAFE_RE=re.compile(r"S1[ABCD]_IW_SLC__\w+_\d{8}T\d{6}_\d{8}T\d{6}_\d{6}_\w+_\w+\.SAFE",re.I)
KEYS={
 "absolute_orbit":"/identification/absoluteOrbitNumber",
 "track_number":"/identification/trackNumber",
 "burst_id":"/identification/burstID",
 "platform":"/identification/platform",
 "orbit_direction":"/identification/orbitPassDirection",
 "zero_doppler_start":"/identification/zeroDopplerStartTime",
 "zero_doppler_end":"/identification/zeroDopplerEndTime",
 "product_type":"/identification/productType",
 "polarizations":"/data/listOfPolarizations",
 "source_start":"/metadata/sourceData/zeroDopplerStartTime",
 "source_end":"/metadata/sourceData/zeroDopplerEndTime",
 "source_product_level":"/metadata/sourceData/productLevel",
 "source_processing_time":"/metadata/sourceData/processingDateTime",
 "source_acquisition_count":"/metadata/sourceData/numberOfAcquisitions",
 "input_l1_count":"/metadata/processingInformation/inputs/numberOfInputL1Files",
}

def decode(v):
    if isinstance(v,bytes): return v.decode("utf-8","replace")
    if isinstance(v,np.ndarray): return [decode(x) for x in v.tolist()]
    if isinstance(v,np.generic): return v.item()
    if isinstance(v,(list,tuple)): return [decode(x) for x in v]
    return v

def walk_strings(h5):
    found=[]
    def visitor(name,obj):
        if isinstance(obj,h5py.Dataset):
            try:
                if obj.size<=100 and (obj.dtype.kind in "SUO"):
                    for v in np.asarray(obj[()]).reshape(-1):
                        x=decode(v)
                        if isinstance(x,str) and x.strip(): found.append({"path":"/"+name,"value":x})
            except (TypeError,ValueError,OSError): pass
        for key,value in obj.attrs.items():
            x=decode(value)
            vals=x if isinstance(x,list) else [x]
            for v in vals:
                if isinstance(v,str) and v.strip(): found.append({"path":"/"+name+"@"+key,"value":v})
    h5.visititems(visitor)
    for key,value in h5.attrs.items():
        x=decode(value)
        vals=x if isinstance(x,list) else [x]
        for v in vals:
            if isinstance(v,str) and v.strip(): found.append({"path":"/@"+key,"value":v})
    return found

def inspect_h5(path):
    with h5py.File(path,"r") as h:
        metadata={}
        input_dataset_paths=[]
        if "/metadata/processingInformation/inputs" in h:
            def list_inputs(name,obj):
                if isinstance(obj,h5py.Dataset): input_dataset_paths.append("/"+name)
            h["/metadata/processingInformation/inputs"].visititems(list_inputs)
        for key,path_name in KEYS.items():
            if path_name in h:
                metadata[key]=decode(h[path_name][()])
        strings=walk_strings(h)
    safe_names=sorted({m.group(0) for item in strings for m in SAFE_RE.finditer(item["value"])})
    metadata["source_safe_identifiers"]=safe_names
    metadata["input_dataset_paths"]=input_dataset_paths
    if "source_slc_granules" in metadata:
        raw=metadata["source_slc_granules"]
        metadata["source_slc_granules"]=raw if isinstance(raw,list) else [raw]
        safe_names=sorted({m.group(0) for value in metadata["source_slc_granules"] for m in SAFE_RE.finditer(str(value))})
        metadata["source_safe_identifiers"]=safe_names
    metadata["source_file_references"]=[x for x in strings if any(k in x["value"].lower() for k in (".safe","manifest","measurement","annotation","calibration"))]
    return {"file":path.name,"metadata":metadata}

def inspect_raster(path):
    with rasterio.open(path) as ds:
        return {"file":path.name,"crs":ds.crs.to_string() if ds.crs else None,
          "width":ds.width,"height":ds.height,"count":ds.count,"dtype":list(ds.dtypes),
          "transform":list(ds.transform)[:6],"bounds":[ds.bounds.left,ds.bounds.bottom,ds.bounds.right,ds.bounds.top],
          "nodata":ds.nodata,"resolution":list(ds.res),"is_tiled":ds.is_tiled}

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--root",type=Path,default=Path("opera-assets"))
    p.add_argument("--output",type=Path,default=Path("opera-assets-audit.json"))
    a=p.parse_args()
    rtc=sorted((a.root/"rtc").glob("*.h5")); static=sorted((a.root/"static").glob("*.tif")); dynamic=sorted((a.root/"rtc").glob("*.tif"))
    if len(rtc)!=15: raise ValueError(f"Expected 15 HDF5 files, found {len(rtc)}")
    if len(static)!=18: raise ValueError(f"Expected 18 static GeoTIFFs (3 bursts x 6 layers), found {len(static)}")
    if len(dynamic)!=45: raise ValueError(f"Expected 45 dynamic GeoTIFFs (15 products x VV/VH/mask), found {len(dynamic)}")
    h5_reports=[inspect_h5(x) for x in rtc]
    raster_reports=[inspect_raster(x) for x in dynamic+static]
    # Grid equality is assessed within each burst, not across different bursts.
    by_burst={}
    for item in raster_reports:
        m=re.search(r"(T130[-_]\d{6}[-_]IW3)",item["file"])
        if m: by_burst.setdefault(m.group(1).replace("_","-"),[]).append(item)
    grid_checks={}
    for burst,items in by_burst.items():
        signatures={(x["crs"],x["width"],x["height"],tuple(round(v,9) for v in x["transform"])) for x in items}
        grid_checks[burst]={"raster_count":len(items),"unique_grid_count":len(signatures),
            "same_grid_within_burst":len(signatures)==1,"files":[x["file"] for x in items]}
    report={"schema":"tessellatum.opera-nairobi-r130-metadata-raster-audit.v1",
      "counts":{"hdf5":len(h5_reports),"dynamic_rasters":len(dynamic),"static_rasters":len(static)},
      "hdf5":h5_reports,"rasters":raster_reports,"grid_checks":grid_checks,
      "checks":{"all_15_hdf5_have_absolute_orbit":all(x["metadata"].get("absolute_orbit") is not None for x in h5_reports),
        "all_15_hdf5_have_burst_id":all(x["metadata"].get("burst_id") is not None for x in h5_reports),
        "all_15_hdf5_have_source_start":all(x["metadata"].get("source_start") is not None for x in h5_reports),
        "all_three_bursts_have_complete_grid_sets":len(grid_checks)==3 and all(x["raster_count"]==21 for x in grid_checks.values()),
        "each_burst_has_one_shared_grid":len(grid_checks)==3 and all(x["same_grid_within_burst"] for x in grid_checks.values())},
      "limitations":["HDF5 input SAFE references may be absent or represented as input file basenames; report preserves all candidate strings.",
        "Matching absolute orbit, platform, burst and acquisition timing is stronger than matching date/time alone but still does not prove pixel equivalence.",
        "Grid agreement is checked within each OPERA burst; adjacent bursts are intentionally not required to share a grid."]}
    a.output.write_text(json.dumps(report,indent=2,default=str)+"\n",encoding="utf-8")
    print("HDF5 products:",len(h5_reports),"dynamic rasters:",len(dynamic),"static rasters:",len(static))
    for x in h5_reports:
        m=x["metadata"]; print(f"{x['file']} | orbit={m.get('absolute_orbit')} | platform={m.get('platform')} | burst={m.get('burst_id')} | start={m.get('source_start')} | input datasets={m.get('input_dataset_paths')} | source SLC granules={m.get('source_slc_granules')} | source SAFE={m.get('source_safe_identifiers')}")
    for burst,x in grid_checks.items(): print(f"{burst} | rasters={x['raster_count']} | unique grids={x['unique_grid_count']} | same-grid={x['same_grid_within_burst']}")
    print("Checks:",json.dumps(report["checks"],sort_keys=True))
    return 0 if all(report["checks"].values()) else 1

if __name__=="__main__":
    try: raise SystemExit(main())
    except Exception as e: print(f"OPERA asset audit failed: {e}",file=sys.stderr); raise
