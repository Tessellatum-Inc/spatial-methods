#!/usr/bin/env python3
"""Download selected OPERA RTC-S1 and RTC-STATIC assets with an Earthdata token."""
from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import shutil
import sys
from urllib.error import HTTPError, URLError
from urllib.parse import urlparse
from urllib.request import Request, urlopen

ALLOWED_HOSTS = {"cumulus.asf.earthdatacloud.nasa.gov", "datapool.asf.alaska.edu"}
RTC_SUFFIXES = (".h5", ".iso.xml", "_VV.tif", "_VH.tif", "_mask.tif")
STATIC_SUFFIXES = (
    ".iso.xml",
    "_local_incidence_angle.tif",
    "_mask.tif",
    "_number_of_looks.tif",
    "_rtc_anf_gamma0_to_beta0.tif",
    "_rtc_anf_gamma0_to_sigma0.tif",
)


def select_assets(report: dict) -> list[dict]:
    """Select required science assets only; never download browse images or checksums."""
    rtc = report.get("matched_features", [])
    static = report.get("static_layer_query", {}).get("features", [])
    if len(rtc) != 8:
        raise ValueError(f"Expected eight time-matched RTC burst products, found {len(rtc)}")
    if len(static) != 2:
        raise ValueError(f"Expected two matching RTC-STATIC burst products, found {len(static)}")

    assets = []
    for product_type, features, suffixes in (
        ("rtc", rtc, RTC_SUFFIXES),
        ("static", static, STATIC_SUFFIXES),
    ):
        for feature in features:
            props = feature["properties"]
            candidates = list(props.get("additionalUrls", []))
            if product_type == "rtc" and props.get("url"):
                candidates.append(props["url"])
            selected = set()
            for url in candidates:
                parsed = urlparse(url)
                if parsed.scheme != "https" or parsed.hostname not in ALLOWED_HOSTS:
                    continue
                filename = Path(parsed.path).name
                if any(filename.endswith(suffix) for suffix in suffixes):
                    selected.add(url)
            sizes = props.get("bytes", {})
            product_id = feature.get("file_id") or props.get("fileID") or props.get("sceneName")
            for url in sorted(selected):
                filename = Path(urlparse(url).path).name
                size_record = sizes.get(filename, {})
                assets.append({
                    "product_type": product_type,
                    "product_id": product_id,
                    "url": url,
                    "filename": filename,
                    "expected_size_bytes": size_record.get("bytes"),
                    "format": size_record.get("format"),
                })
    if not assets:
        raise ValueError("No OPERA science assets were selected")
    names = [x["filename"] for x in assets]
    if len(names) != len(set(names)):
        raise ValueError("Selected OPERA assets contain duplicate filenames")
    return assets


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def download_assets(assets: list[dict], output_dir: Path, token: str) -> list[dict]:
    if not token or not token.strip():
        raise ValueError("EARTHDATA_TOKEN is required; configure it as a GitHub Actions secret")
    manifest = []
    for asset in assets:
        folder = output_dir / asset["product_type"]
        folder.mkdir(parents=True, exist_ok=True)
        destination = folder / asset["filename"]
        request = Request(asset["url"], headers={
            "Authorization": f"Bearer {token.strip()}",
            "User-Agent": "Tessellatum-Spatial-Methods/1.0",
        })
        try:
            with urlopen(request, timeout=180) as response, destination.open("wb") as stream:
                shutil.copyfileobj(response, stream)
        except HTTPError as exc:
            raise RuntimeError(
                f"Earthdata download failed for {asset['filename']}: HTTP {exc.code} {exc.reason}. "
                "Check that the Earthdata token is valid and has not expired."
            ) from exc
        except (URLError, TimeoutError, OSError) as exc:
            raise RuntimeError(f"Download failed for {asset['filename']}: {exc}") from exc
        actual_size = destination.stat().st_size
        expected_size = asset.get("expected_size_bytes")
        if expected_size is not None and actual_size != expected_size:
            raise RuntimeError(
                f"Size mismatch for {asset['filename']}: expected {expected_size}, got {actual_size}"
            )
        manifest.append({
            **asset,
            "local_path": str(destination),
            "actual_size_bytes": actual_size,
            "sha256": sha256_file(destination),
            "status": "downloaded_and_size_verified",
        })
        print(f"Downloaded {asset['product_type']}/{asset['filename']} ({actual_size:,} bytes)")
    return manifest


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--report", type=Path, default=Path(
        "data/asf/surat_r009_opera/surat_r009_opera_rtc_catalogue_discovery.json"
    ))
    parser.add_argument("--output-dir", type=Path, default=Path(
        "data/asf/surat_r009_opera/downloaded"
    ))
    args = parser.parse_args(argv)
    try:
        report = json.loads(args.report.read_text(encoding="utf-8"))
        assets = select_assets(report)
        manifest = download_assets(assets, args.output_dir, os.environ.get("EARTHDATA_TOKEN", ""))
    except (OSError, ValueError, json.JSONDecodeError, RuntimeError) as exc:
        print(f"OPERA asset download failed: {exc}", file=sys.stderr)
        return 2

    output = {
        "schema": "tessellatum.opera-surat-r009-download-manifest.v1",
        "source_discovery_report": str(args.report),
        "asset_count": len(manifest),
        "assets": manifest,
        "interpretation_limits": [
            "Successful downloads and size checks do not establish raster-grid alignment or radiometric equivalence.",
            "The RTC-S1 products are 30 m burst-based gamma0 power products; reconcile CRS, transform, source acquisition, mask and effective resolution before comparison.",
            "RTC-STATIC masks are ancillary geometry masks; use each acquisition's RTC product mask to screen the corresponding dynamic RTC raster.",
            "The ellipsoid incidence-angle layer is taken from the separately interpolated source GRD angle grids; the RTC-STATIC local incidence angle is not a substitute for ellipsoid incidence angle.",
        ],
    }
    args.output_dir.mkdir(parents=True, exist_ok=True)
    manifest_path = args.output_dir / "download_manifest.json"
    manifest_path.write_text(json.dumps(output, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"Downloaded and verified {len(manifest)} OPERA assets. Manifest: {manifest_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
