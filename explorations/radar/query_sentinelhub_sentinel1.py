#!/usr/bin/env python3
"""Authenticate to CDSE Sentinel Hub and search Sentinel-1 GRD over Nairobi.

This is deliberately separate from the OData SAFE downloader. It retrieves
catalogue metadata only; it does not download a SAFE archive or raster assets.
Credentials are read only from SENTINEL_HUB_CLIENT_ID and
SENTINEL_HUB_CLIENT_SECRET environment variables.
"""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import sys
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from urllib.request import Request, urlopen

TOKEN_URL = (
    "https://identity.dataspace.copernicus.eu/auth/realms/CDSE/"
    "protocol/openid-connect/token"
)
CATALOG_SEARCH_URL = "https://sh.dataspace.copernicus.eu/catalog/v1/search"
NAIROBI_BBOX = [36.65, -1.45, 37.05, -1.15]
DEFAULT_START = "2026-10-01T00:00:00Z"
DEFAULT_END = "2026-11-23T00:00:00Z"


def _read_json_response(raw: bytes, label: str) -> dict:
    try:
        payload = json.loads(raw.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise ValueError(f"{label} returned invalid JSON.") from exc
    if not isinstance(payload, dict):
        raise ValueError(f"{label} response must be a JSON object.")
    return payload


def request_access_token(client_id: str, client_secret: str, timeout: int = 30) -> str:
    """Exchange the OAuth client credentials for a short-lived access token."""
    if not client_id or not client_secret:
        raise ValueError(
            "Set SENTINEL_HUB_CLIENT_ID and SENTINEL_HUB_CLIENT_SECRET."
        )
    body = urlencode({
        "grant_type": "client_credentials",
        "client_id": client_id,
        "client_secret": client_secret,
    }).encode("utf-8")
    request = Request(
        TOKEN_URL,
        data=body,
        headers={
            "Content-Type": "application/x-www-form-urlencoded",
            "Accept": "application/json",
        },
        method="POST",
    )
    try:
        with urlopen(request, timeout=timeout) as response:
            payload = _read_json_response(response.read(), "CDSE token endpoint")
    except HTTPError as exc:
        # Never print response bodies, headers, request bodies, or credentials.
        raise RuntimeError(
            f"CDSE OAuth token request failed with HTTP {exc.code}."
        ) from None
    except (URLError, TimeoutError, OSError) as exc:
        raise RuntimeError(
            f"CDSE OAuth token request could not complete ({type(exc).__name__})."
        ) from None
    token = payload.get("access_token")
    if not isinstance(token, str) or not token:
        error = payload.get("error")
        if isinstance(error, str) and error:
            raise RuntimeError(f"CDSE OAuth response did not contain an access token ({error}).")
        raise RuntimeError("CDSE OAuth response did not contain an access token.")
    return token


def build_search_payload(start: str, end: str, limit: int = 20) -> dict:
    """Build a bounded STAC search for Sentinel-1 GRD over the Nairobi study AOI."""
    try:
        start_dt = datetime.fromisoformat(start.replace("Z", "+00:00"))
        end_dt = datetime.fromisoformat(end.replace("Z", "+00:00"))
    except ValueError as exc:
        raise ValueError("Start and end must be ISO 8601 timestamps.") from exc
    if start_dt.tzinfo is None or end_dt.tzinfo is None:
        raise ValueError("Start and end timestamps must include a timezone.")
    if start_dt >= end_dt:
        raise ValueError("Start timestamp must be earlier than end timestamp.")
    if not 1 <= limit <= 100:
        raise ValueError("--limit must be between 1 and 100.")
    return {
        "bbox": NAIROBI_BBOX,
        "datetime": f"{start_dt.astimezone(timezone.utc).isoformat().replace('+00:00', 'Z')}/"
                    f"{end_dt.astimezone(timezone.utc).isoformat().replace('+00:00', 'Z')}",
        "collections": ["sentinel-1-grd"],
        "limit": limit,
        "filter": "sar:instrument_mode='IW'",
        "filter-lang": "cql2-text",
    }


def search_catalog(access_token: str, payload: dict, timeout: int = 60) -> dict:
    """Search the Sentinel Hub STAC Catalog API using a bearer token."""
    if not access_token:
        raise ValueError("An access token is required.")
    request = Request(
        CATALOG_SEARCH_URL,
        data=json.dumps(payload).encode("utf-8"),
        headers={
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json",
            "Accept": "application/geo+json, application/json",
        },
        method="POST",
    )
    try:
        with urlopen(request, timeout=timeout) as response:
            result = _read_json_response(response.read(), "Sentinel Hub Catalog API")
    except HTTPError as exc:
        raise RuntimeError(
            f"Sentinel Hub Catalog search failed with HTTP {exc.code}."
        ) from None
    except (URLError, TimeoutError, OSError) as exc:
        raise RuntimeError(
            f"Sentinel Hub Catalog search could not complete ({type(exc).__name__})."
        ) from None
    features = result.get("features")
    if not isinstance(features, list):
        raise ValueError("Catalog response did not contain a valid 'features' array.")
    for index, feature in enumerate(features):
        if not isinstance(feature, dict) or not isinstance(feature.get("id"), str):
            raise ValueError(f"Catalog feature at index {index} has no valid id.")
    return result


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--start", default=DEFAULT_START, help="Inclusive ISO 8601 start.")
    parser.add_argument("--end", default=DEFAULT_END, help="Exclusive ISO 8601 end.")
    parser.add_argument("--limit", type=int, default=20)
    parser.add_argument("--timeout", type=int, default=60)
    parser.add_argument("--output-dir", type=Path, default=Path("data/sentinelhub/nairobi"))
    args = parser.parse_args(argv)
    if args.timeout < 1:
        parser.error("--timeout must be at least one second.")
    try:
        payload = build_search_payload(args.start, args.end, args.limit)
        token = request_access_token(
            os.environ.get("SENTINEL_HUB_CLIENT_ID", ""),
            os.environ.get("SENTINEL_HUB_CLIENT_SECRET", ""),
            timeout=min(args.timeout, 30),
        )
        result = search_catalog(token, payload, timeout=args.timeout)
    except (ValueError, RuntimeError) as exc:
        print(str(exc), file=sys.stderr)
        return 2

    retrieved_at = datetime.now(timezone.utc)
    stamp = retrieved_at.strftime("%Y%m%dT%H%M%SZ")
    args.output_dir.mkdir(parents=True, exist_ok=True)
    response_path = args.output_dir / f"sentinelhub_s1_nairobi_{stamp}.geojson"
    metadata_path = args.output_dir / f"sentinelhub_s1_nairobi_{stamp}.metadata.json"
    raw = (json.dumps(result, indent=2, ensure_ascii=False) + "\n").encode("utf-8")
    response_path.write_bytes(raw)
    features = result["features"]
    metadata = {
        "service": "Copernicus Data Space Ecosystem Sentinel Hub Catalog API",
        "token_endpoint": TOKEN_URL,
        "catalog_search_endpoint": CATALOG_SEARCH_URL,
        "authentication": "OAuth2 client_credentials",
        "retrieved_at_utc": retrieved_at.isoformat().replace("+00:00", "Z"),
        "query": payload,
        "feature_count": len(features),
        "feature_ids": [feature["id"] for feature in features],
        "response_file": response_path.name,
        "response_sha256": hashlib.sha256(raw).hexdigest(),
        "next_page_present": bool(
            result.get("context", {}).get("next")
            or any(link.get("rel") == "next" for link in result.get("links", [])
                   if isinstance(link, dict))
        ),
        "scope_note": (
            "Catalogue metadata only. This run does not download SAFE archives or "
            "imagery pixels, and a bounding-box intersection does not prove full "
            "study-area coverage or scientific suitability."
        ),
    }
    metadata_path.write_text(
        json.dumps(metadata, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    print(f"Sentinel Hub OAuth: authenticated.")
    print(f"Sentinel-1 GRD catalogue features: {len(features)}")
    print(f"Catalogue evidence: {response_path}")
    print(f"Run metadata: {metadata_path}")
    print(f"Response SHA-256: {metadata['response_sha256']}")
    if metadata["next_page_present"]:
        print("Additional catalogue pages are available; this run saved the first page only.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
