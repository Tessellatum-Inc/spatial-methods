#!/usr/bin/env python3
"""Local tile alignment and radiometric consistency screening for Sentinel-1 stacks.

Diagnostic only: tile phase correlation is not a substitute for validated
SAR co-registration using precise orbit information, DEM-assisted processing,
or independently identified stable tie points.
"""
from __future__ import annotations
import argparse
from datetime import datetime, timezone
import json
from pathlib import Path
import numpy as np
import rasterio


def read_raster(path):
    with rasterio.open(path) as ds:
        if ds.count < 3:
            raise ValueError(f"{path}: expected VV, VH, dataMask bands")
        vv = ds.read(1).astype(np.float32)
        vh = ds.read(2).astype(np.float32)
        mask = (ds.read(3) > 0.5) & np.isfinite(vv) & np.isfinite(vh) & (vv > 0) & (vh > 0)
        grid = {"crs": ds.crs.to_string() if ds.crs else None, "width": ds.width,
                "height": ds.height, "transform": list(ds.transform)[:6],
                "bounds": [float(x) for x in ds.bounds]}
    return vv, vh, mask, grid


def _phase_shift(ref, mov, valid):
    if valid.mean() < 0.75 or valid.sum() < 1024:
        return None
    a = np.zeros(ref.shape, np.float64); b = np.zeros(mov.shape, np.float64)
    ar = np.log10(ref[valid]); br = np.log10(mov[valid])
    a[valid] = np.log10(ref[valid]) - ar.mean()
    b[valid] = np.log10(mov[valid]) - br.mean()
    if a[valid].std() < 1e-4 or b[valid].std() < 1e-4:
        return None
    win = np.outer(np.hanning(ref.shape[0]), np.hanning(ref.shape[1]))
    a *= win; b *= win
    cross = np.fft.fft2(a) * np.conj(np.fft.fft2(b))
    cross /= np.maximum(np.abs(cross), 1e-12)
    corr = np.abs(np.fft.ifft2(cross))
    py, px = np.unravel_index(np.argmax(corr), corr.shape)
    def sub(v, i):
        p, c, n = v[(i-1)%len(v)], v[i], v[(i+1)%len(v)]
        d = p - 2*c + n
        return float(0.5*(p-n)/d) if abs(d)>1e-12 else 0.0
    dy = float(py if py <= ref.shape[0]//2 else py-ref.shape[0]) + sub(corr[:,px],py)
    dx = float(px if px <= ref.shape[1]//2 else px-ref.shape[1]) + sub(corr[py,:],px)
    side = corr.copy()
    for y in range(max(0,py-2), min(corr.shape[0],py+3)):
        for x in range(max(0,px-2), min(corr.shape[1],px+3)):
            side[y,x] = 0
    ratio = float(corr[py,px] / max(side.mean(), 1e-15))
    return {"shift_x_pixels": dx, "shift_y_pixels": dy,
            "shift_magnitude_pixels": float(np.hypot(dx,dy)),
            "peak_to_mean_sidelobe_ratio": ratio,
            "valid_fraction": float(valid.mean()), "valid_pixels": int(valid.sum())}


def _stats(arr, mask):
    v = arr[mask].astype(np.float64)
    if not len(v): return {"valid_pixels": 0}
    q = np.percentile(v, [1,5,25,50,75,95,99])
    return {"valid_pixels": int(len(v)), "mean_linear": float(v.mean()),
            "p01_linear": float(q[0]), "p05_linear": float(q[1]),
            "p25_linear": float(q[2]), "median_linear": float(q[3]),
            "p75_linear": float(q[4]), "p95_linear": float(q[5]),
            "p99_linear": float(q[6]),
            "median_db": float(10*np.log10(q[3]))}


def compare(ref_path, mov_path, tile_size=256, stride=256):
    rvv, rvh, rm, rg = read_raster(ref_path)
    mvv, mvh, mm, mg = read_raster(mov_path)
    if rg != mg: raise ValueError(f"Grid mismatch: {ref_path.name} / {mov_path.name}")
    common = rm & mm
    tiles=[]
    h,w=common.shape
    for y in range(0, h-tile_size+1, stride):
        for x in range(0, w-tile_size+1, stride):
            sl=np.s_[y:y+tile_size,x:x+tile_size]
            result=_phase_shift(rvv[sl],mvv[sl],common[sl])
            if result is not None:
                result.update({"row_offset":y,"col_offset":x})
                tiles.append(result)
    good=[t for t in tiles if t["peak_to_mean_sidelobe_ratio"] >= 5.0 and t["shift_magnitude_pixels"] <= 5.0]
    shifts=np.array([[t['shift_x_pixels'],t['shift_y_pixels']] for t in good],dtype=float)
    local_summary=None
    if len(shifts):
        mags=np.linalg.norm(shifts,axis=1)
        local_summary={"accepted_tile_count":len(good),
          "median_shift_x_pixels":float(np.median(shifts[:,0])),
          "median_shift_y_pixels":float(np.median(shifts[:,1])),
          "median_shift_magnitude_pixels":float(np.median(mags)),
          "p90_shift_magnitude_pixels":float(np.percentile(mags,90)),
          "p95_shift_magnitude_pixels":float(np.percentile(mags,95)),
          "max_shift_magnitude_pixels":float(mags.max())}
    rstats_vv=_stats(rvv,common); mstats_vv=_stats(mvv,common)
    rstats_vh=_stats(rvh,common); mstats_vh=_stats(mvh,common)
    def delta(a,b):
        return {k.replace('_linear','_percent_change'):float((b[k]/a[k]-1)*100)
                for k in ('mean_linear','median_linear','p05_linear','p95_linear') if a.get(k,0)>0}
    return {"reference_file":ref_path.name,"moving_file":mov_path.name,"grid":rg,
      "common_valid_fraction":float(common.mean()),"common_valid_pixels":int(common.sum()),
      "tile_size_pixels":tile_size,"tile_stride_pixels":stride,"eligible_tile_count":len(tiles),
      "tiles":tiles,"local_alignment_summary":local_summary,
      "radiometry_common_mask":{"VV":{"reference":rstats_vv,"moving":mstats_vv,"relative_change":delta(rstats_vv,mstats_vv)},
                                "VH":{"reference":rstats_vh,"moving":mstats_vh,"relative_change":delta(rstats_vh,mstats_vh)}},
      "interpretation":"screening_only; tile shifts and distribution changes are diagnostics, not validated co-registration or calibrated temporal change"}


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--rasters',nargs='+',type=Path,required=True)
    p.add_argument('--output',type=Path,required=True)
    p.add_argument('--tile-size',type=int,default=256)
    p.add_argument('--stride',type=int,default=256)
    a=p.parse_args()
    if len(a.rasters)<2: p.error('At least two rasters required')
    if a.tile_size<64 or a.stride<32: p.error('tile-size must be >=64 and stride >=32')
    if any(not f.is_file() for f in a.rasters): p.error('Every raster must exist')
    try:
        comparisons=[compare(a.rasters[0],f,a.tile_size,a.stride) for f in a.rasters[1:]]
    except (ValueError,OSError,rasterio.errors.RasterioError) as e:
        p.exit(2,f'QA failed: {e}\\n')
    report={"schema":"tessellatum.sentinel1.temporal-qa-screen.v1",
      "created_at_utc":datetime.now(timezone.utc).isoformat().replace('+00:00','Z'),
      "reference_file":a.rasters[0].name,"comparison_count":len(comparisons),
      "comparisons":comparisons,"status":"screening_only_not_analysis_ready",
      "analysis_ready":False,
      "limitations":["Tile phase correlation is local image-content matching, not independent stable-feature tie-point validation.",
        "Scene-wide shifts can hide local distortions; tile estimates can be affected by temporal change, speckle, layover and shadow.",
        "Backscatter distribution differences can reflect real change, incidence geometry, moisture, processing or calibration effects.",
        "No precise-orbit verification, DEM-assisted geometric validation, border-noise assessment or absolute geolocation accuracy test is performed.",
        "Radiometric statistics are descriptive and are not a radiometric normalization or calibration validation."]}
    a.output.parent.mkdir(parents=True,exist_ok=True); a.output.write_text(json.dumps(report,indent=2)+'\\n')
    print(f"Wrote {a.output}; {len(comparisons)} comparisons; analysis_ready=false")

if __name__=='__main__': main()
