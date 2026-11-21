#!/usr/bin/env python3
"""Grid-safe Sentinel-2 multispectral point-window extraction.

Reads small per-band windows from STAC assets. Native 10 m and 20 m grids are
kept separate: this module never silently resamples 20 m data to 10 m.
"""
from __future__ import annotations

from typing import Any

import numpy as np
import rasterio
from rasterio.warp import transform as transform_coordinates
from rasterio.windows import Window

from stac_imagery_review import rasterio_source

# Aliases cover common Earth Search and Copernicus Data Space STAC conventions.
# Order is intentional: prefer explicit native-resolution assets over generic aliases.
BAND_ALIASES: dict[str, tuple[str, ...]] = {
    "B02": ("B02_10m", "B02", "blue", "blue-jp2"),
    "B03": ("B03_10m", "B03", "green", "green-jp2"),
    "B04": ("B04_10m", "B04", "red", "red-jp2"),
    "B08": ("B08_10m", "B08", "nir", "nir-jp2"),
    "B05": ("B05_20m", "B05", "rededge1", "rededge1-jp2"),
    "B06": ("B06_20m", "B06", "rededge2", "rededge2-jp2"),
    "B07": ("B07_20m", "B07", "rededge3", "rededge3-jp2"),
    "B8A": ("B8A_20m", "B8A", "nir08", "nir08-jp2"),
    "B11": ("B11_20m", "B11", "swir16", "swir16-jp2"),
    "B12": ("B12_20m", "B12", "swir22", "swir22-jp2"),
    "SCL": ("SCL_20m", "SCL", "scl", "scl-jp2"),
}

BAND_GRID = {
    "B02": "10m", "B03": "10m", "B04": "10m", "B08": "10m",
    "B05": "20m", "B06": "20m", "B07": "20m", "B8A": "20m",
    "B11": "20m", "B12": "20m", "SCL": "20m",
}


def asset_for_band(item: dict[str, Any], band: str) -> tuple[str, dict[str, Any]] | None:
    """Select a STAC asset by explicit band aliases, preferring HTTPS per alias."""
    if band not in BAND_ALIASES:
        raise ValueError(f"Unsupported Sentinel-2 band: {band}")
    assets = item.get("assets", {})
    for alias in BAND_ALIASES[band]:
        accepted_names = {alias.lower(), f"{alias.lower()}-jp2"}
        matches = [
            (name, asset)
            for name, asset in assets.items()
            if name.lower() in accepted_names and asset.get("href")
        ]
        if not matches:
            continue
        public = [
            pair for pair in matches
            if str(pair[1].get("href", "")).startswith(("https://", "http://"))
        ]
        return (public or matches)[0]
    return None


def _grid_signature(src: Any) -> tuple[str, tuple[float, ...], int, int]:
    """Return an exact grid signature to prevent accidental pixel misalignment."""
    return (
        src.crs.to_string() if src.crs else "",
        tuple(src.transform),
        int(src.width),
        int(src.height),
    )


def _asset_scale_offset(asset: dict[str, Any]) -> tuple[float, float, str]:
    """Read STAC raster scale/offset when supplied; otherwise preserve raw values."""
    bands = asset.get("raster:bands") or []
    metadata = bands[0] if bands and isinstance(bands[0], dict) else {}
    scale = metadata.get("scale", 1.0)
    offset = metadata.get("offset", 0.0)
    unit = str(metadata.get("unit") or "source_units")
    try:
        return float(scale), float(offset), unit
    except (TypeError, ValueError) as exc:
        raise ValueError("STAC raster:bands scale/offset must be numeric") from exc


def read_multispectral_windows(
    item: dict[str, Any],
    longitude: float,
    latitude: float,
    *,
    bands: tuple[str, ...] = tuple(BAND_ALIASES),
    window_pixels: int = 32,
) -> dict[str, Any]:
    """Read requested bands around a WGS84 point, preserving native grids.

    Returns float32 arrays with nodata represented as NaN, plus per-band source
    metadata. Explicit STAC scale/offset metadata is applied. Bands in the same
    nominal grid group must have exactly matching CRS, affine transform and
    raster dimensions. The 10 m and 20 m groups are deliberately not compared
    or resampled against each other.
    """
    if window_pixels < 1 or window_pixels > 512:
        raise ValueError("window_pixels must be between 1 and 512")
    if not bands:
        raise ValueError("At least one band must be requested")
    unknown = set(bands) - set(BAND_ALIASES)
    if unknown:
        raise ValueError(f"Unsupported Sentinel-2 bands: {', '.join(sorted(unknown))}")

    arrays: dict[str, np.ndarray] = {}
    metadata: dict[str, dict[str, Any]] = {}
    signatures: dict[str, tuple[str, tuple[float, ...], int, int]] = {}
    missing: list[str] = []

    for band in bands:
        selected = asset_for_band(item, band)
        if selected is None:
            missing.append(band)
            continue
        asset_name, asset = selected
        href = str(asset["href"])
        raster_path, env = rasterio_source(href)
        with env:
            with rasterio.open(raster_path) as src:
                if src.crs is None:
                    raise RuntimeError(f"{asset_name} asset has no CRS")
                x, y = transform_coordinates(
                    "EPSG:4326", src.crs, [longitude], [latitude]
                )
                row, col = src.index(x[0], y[0])
                if not (0 <= row < src.height and 0 <= col < src.width):
                    raise RuntimeError(f"Sample point falls outside {asset_name} raster bounds")

                grid_group = BAND_GRID[band]
                signature = _grid_signature(src)
                previous = signatures.get(grid_group)
                if previous is not None and signature != previous:
                    raise RuntimeError(
                        f"{grid_group} assets are not on the same native grid; "
                        "refusing implicit resampling"
                    )
                signatures[grid_group] = signature

                half = window_pixels // 2
                window = Window(
                    col - half, row - half, window_pixels, window_pixels
                )
                masked = src.read(1, window=window, boundless=True, masked=True)
                values = np.asarray(masked.filled(np.nan), dtype=np.float32)
                scale, offset, unit = _asset_scale_offset(asset)
                values = values * np.float32(scale) + np.float32(offset)
                arrays[band] = values
                metadata[band] = {
                    "asset_key": asset_name,
                    "href": href,
                    "grid_group": grid_group,
                    "crs": src.crs.to_string(),
                    "pixel_size_map_units": [abs(src.transform.a), abs(src.transform.e)],
                    "scale": scale,
                    "offset": offset,
                    "unit": unit,
                    "nodata": src.nodata,
                    "window_shape": list(values.shape),
                    "grid_signature": {
                        "transform": list(src.transform),
                        "width": src.width,
                        "height": src.height,
                    },
                }

    return {
        "item_id": item.get("id", ""),
        "collection": item.get("collection", ""),
        "datetime": (
            item.get("properties", {}).get("datetime")
            or item.get("properties", {}).get("start_datetime", "")
        ),
        "longitude": float(longitude),
        "latitude": float(latitude),
        "window_pixels": window_pixels,
        "bands": arrays,
        "band_metadata": metadata,
        "missing_bands": missing,
        "native_grids": sorted(signatures),
    }


__all__ = ["BAND_ALIASES", "BAND_GRID", "asset_for_band", "read_multispectral_windows"]
