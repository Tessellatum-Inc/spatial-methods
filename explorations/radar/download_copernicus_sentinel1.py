#!/usr/bin/env python3
"""Download and structurally validate one Copernicus Sentinel-1 SAFE product.

Credentials are read only from CDSE_USERNAME and CDSE_PASSWORD environment
variables. They are never accepted as command-line arguments or written to disk.
The script downloads the extracted product form as a ZIP archive, validates its
ZIP CRCs and essential SAFE members, then writes a SHA-256 sidecar.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import time
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode, urlparse
from urllib.request import (
    HTTPRedirectHandler,
    Request,
    build_opener,
)
import uuid
import zipfile

TOKEN_URL = (
    "https://identity.dataspace.copernicus.eu/auth/realms/CDSE/"
    "protocol/openid-connect/token"
)
DOWNLOAD_URL = "https://download.dataspace.copernicus.eu/odata/v1/Products"
ALLOWED_HOSTS = {
    "identity.dataspace.copernicus.eu",
    "download.dataspace.copernicus.eu",
    "catalogue.dataspace.copernicus.eu",
}


class DataspaceRedirectHandler(HTTPRedirectHandler):
    """Prevent bearer credentials from following redirects off the CDSE domain."""

    def redirect_request(self, req, fp, code, msg, headers, newurl):
        host = (urlparse(newurl).hostname or "").lower()
        if host not in ALLOWED_HOSTS:
            raise URLError(f"Refusing redirect to untrusted host: {host or '(none)'}")
        return super().redirect_request(req, fp, code, msg, headers, newurl)


def validate_product_id(value: str) -> str:
    """Require a canonical UUID before placing an ID in an OData path."""
    try:
        parsed = uuid.UUID(value)
    except (ValueError, AttributeError) as exc:
        raise ValueError("--product-id must be a valid UUID.") from exc
    if str(parsed) != value.lower():
        raise ValueError("--product-id must use canonical UUID form.")
    return str(parsed)


def request_access_token(username: str, password: str, timeout: int = 60) -> str:
    """Obtain a short-lived CDSE access token without persisting credentials."""
    if not username or not password:
        raise ValueError("CDSE_USERNAME and CDSE_PASSWORD must both be set.")
    body = urlencode({
        "grant_type": "password",
        "client_id": "cdse-public",
        "username": username,
        "password": password,
    }).encode("utf-8")
    request = Request(
        TOKEN_URL,
        data=body,
        headers={"Content-Type": "application/x-www-form-urlencoded"},
        method="POST",
    )
    opener = build_opener(DataspaceRedirectHandler())
    try:
        with opener.open(request, timeout=timeout) as response:
            payload = json.loads(response.read().decode("utf-8"))
    except (HTTPError, URLError, TimeoutError, json.JSONDecodeError) as exc:
        raise RuntimeError(f"Copernicus token request failed: {exc}") from exc
    token = payload.get("access_token") if isinstance(payload, dict) else None
    if not isinstance(token, str) or not token:
        raise RuntimeError("Copernicus token response did not contain access_token.")
    return token


def validate_safe_archive(path: Path) -> dict:
    """Check ZIP integrity and the minimum expected Sentinel-1 SAFE structure."""
    if not zipfile.is_zipfile(path):
        raise ValueError("Downloaded file is not a valid ZIP archive.")
    with zipfile.ZipFile(path) as archive:
        corrupt_member = archive.testzip()
        if corrupt_member is not None:
            raise ValueError(f"ZIP CRC check failed for member: {corrupt_member}")
        names = [name.replace("\\", "/") for name in archive.namelist()]
    lower_names = [name.lower() for name in names]
    manifests = [name for name in lower_names if name.endswith("/manifest.safe") or name == "manifest.safe"]
    measurements = [
        name for name in lower_names
        if "/measurement/" in name and name.endswith((".tif", ".tiff"))
    ]
    annotations = [
        name for name in lower_names
        if "/annotation/" in name and name.endswith(".xml")
    ]
    if len(manifests) != 1:
        raise ValueError(f"Expected exactly one SAFE manifest.safe; found {len(manifests)}.")
    if not measurements:
        raise ValueError("SAFE archive contains no measurement GeoTIFF under measurement/.")
    if not annotations:
        raise ValueError("SAFE archive contains no annotation XML under annotation/.")
    return {
        "manifest": manifests[0],
        "measurement_file_count": len(measurements),
        "annotation_file_count": len(annotations),
        "zip_member_count": len(names),
    }


def download_product(product_id: str, token: str, output_path: Path, timeout: int = 120) -> None:
    """Stream an extracted SAFE product to disk without buffering it in memory."""
    url = f"{DOWNLOAD_URL}({product_id})/$value"
    request = Request(
        url,
        headers={"Authorization": f"Bearer {token}", "User-Agent": "SpatialMethods/1.0"},
    )
    opener = build_opener(DataspaceRedirectHandler())
    output_path.parent.mkdir(parents=True, exist_ok=True)
    partial_path = output_path.with_suffix(output_path.suffix + ".part")
    try:
        with opener.open(request, timeout=timeout) as response, partial_path.open("wb") as target:
            while True:
                chunk = response.read(1024 * 1024)
                if not chunk:
                    break
                target.write(chunk)
        if partial_path.stat().st_size == 0:
            raise RuntimeError("Copernicus returned an empty product download.")
        partial_path.replace(output_path)
    except (HTTPError, URLError, TimeoutError, OSError) as exc:
        partial_path.unlink(missing_ok=True)
        raise RuntimeError(f"Sentinel-1 product download failed: {exc}") from exc


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--product-id", required=True, help="Copernicus product UUID.")
    parser.add_argument("--output-dir", type=Path, default=Path("data/copernicus/nairobi"))
    parser.add_argument("--timeout", type=int, default=120)
    args = parser.parse_args(argv)
    try:
        product_id = validate_product_id(args.product_id)
        if args.timeout < 1:
            raise ValueError("--timeout must be a positive integer.")
        username = os.environ.get("CDSE_USERNAME", "")
        password = os.environ.get("CDSE_PASSWORD", "")
        token = request_access_token(username, password, timeout=min(args.timeout, 60))
        archive_path = args.output_dir / f"sentinel1_{product_id}.SAFE.zip"
        download_product(product_id, token, archive_path, timeout=args.timeout)
        structure = validate_safe_archive(archive_path)
        digest = sha256_file(archive_path)
        manifest = {
            "product_id": product_id,
            "downloaded_at_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
            "download_endpoint": f"{DOWNLOAD_URL}({product_id})/$value",
            "archive_file": archive_path.name,
            "archive_size_bytes": archive_path.stat().st_size,
            "archive_sha256": digest,
            "validation": "passed",
            "safe_structure": structure,
            "limitations": [
                "Structural validation does not establish radiometric correctness or scientific suitability.",
                "No calibration, terrain correction, resampling, or interpretation has been performed.",
            ],
        }
        sidecar = archive_path.with_suffix(archive_path.suffix + ".metadata.json")
        sidecar.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    except (ValueError, RuntimeError, OSError) as exc:
        parser.error(str(exc))
    print(f"Downloaded: {archive_path}")
    print(f"SHA-256: {digest}")
    print(f"SAFE structure: {json.dumps(structure, sort_keys=True)}")
    print(f"Provenance: {sidecar}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
