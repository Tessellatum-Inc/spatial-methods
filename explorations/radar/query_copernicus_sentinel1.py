#!/usr/bin/env python3
"""Discover Sentinel-1 IW GRD products in the Nairobi study window via Copernicus OData.

Catalogue discovery only: intersection is not full-coverage proof, and metadata
availability is not proof that an asset can be downloaded or scientifically used.
"""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import sys
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from urllib.request import Request, urlopen

API_URL = "https://catalogue.dataspace.copernicus.eu/odata/v1/Products"
AOI_WKT = (
    "POLYGON((36.65 -1.45,37.05 -1.45,37.05 -1.15,"
    "36.65 -1.15,36.65 -1.45))"
)
DEFAULT_START = "2026-10-01T00:00:00Z"
DEFAULT_END = "2026-11-22T00:00:00Z"


def _utc_timestamp(value: str, label: str) -> datetime:
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError as exc:
        raise ValueError(f"{label} must be an ISO 8601 timestamp.") from exc
    if parsed.tzinfo is None or parsed.utcoffset() is None:
        raise ValueError(f"{label} must include an explicit UTC offset.")
    return parsed.astimezone(timezone.utc)


def build_query(start: str, end: str, limit: int) -> dict[str, str]:
    """Build a documented OData query for Sentinel-1 IW GRD products."""
    start_dt = _utc_timestamp(start, "Start")
    end_dt = _utc_timestamp(end, "End")
    if start_dt >= end_dt:
        raise ValueError("Start timestamp must be earlier than end timestamp.")
    if not 1 <= limit <= 1000:
        raise ValueError("--limit must be between 1 and 1000.")

    start_value = start_dt.isoformat(timespec="milliseconds").replace("+00:00", "Z")
    end_value = end_dt.isoformat(timespec="milliseconds").replace("+00:00", "Z")
    spatial = (
        "OData.CSC.Intersects(area=geography'SRID=4326;"
        f"{AOI_WKT}')"
    )
    product_type = (
        "Attributes/OData.CSC.StringAttribute/any("
        "att:att/Name eq 'productType' and "
        "att/OData.CSC.StringAttribute/Value eq 'IW_GRDH_1S')"
    )
    filters = (
        "Collection/Name eq 'SENTINEL-1' and "
        f"{product_type} and {spatial} and "
        f"ContentDate/Start ge {start_value} and "
        f"ContentDate/Start lt {end_value}"
    )
    return {
        "$filter": filters,
        "$orderby": "ContentDate/Start asc",
        "$top": str(limit),
        "\u0024expand": "Attributes",
    }


def retrieve(url: str, timeout: int) -> bytes:
    request = Request(
        url,
        headers={
            "Accept": "application/json",
            "User-Agent": "Tessellatum-Spatial-Methods/1.0 (reproducible research)",
        },
    )
    with urlopen(request, timeout=timeout) as response:
        return response.read()


def build_location_query(product_id: str) -> str:
    """Build a separate OData query for one product's available locations."""
    if not isinstance(product_id, str) or not product_id:
        raise ValueError("Product ID must be a non-empty string.")
    params = {
        "$filter": f"Id eq '{product_id}'",
        "$expand": "Locations",
    }
    return f"{API_URL}?{urlencode(params)}"


def attach_product_locations(products: list[dict], timeout: int) -> list[dict]:
    """Attach Locations to catalogue records, preserving per-product failures."""
    errors = []
    for product in products:
        query_url = build_location_query(product["Id"])
        try:
            raw = retrieve(query_url, timeout)
            payload = json.loads(raw)
            matches = payload.get("value") if isinstance(payload, dict) else None
            if not isinstance(matches, list):
                raise ValueError("Location response has no valid 'value' array.")
            match = next(
                (item for item in matches
                 if isinstance(item, dict) and item.get("Id") == product["Id"]),
                None,
            )
            if match is None:
                raise ValueError("Location response did not contain the requested product.")
            locations = match.get("Locations")
            if not isinstance(locations, list):
                raise ValueError("Location response has no valid 'Locations' array.")
            product["Locations"] = locations
            product["LocationsRetrieved"] = True
        except (HTTPError, URLError, TimeoutError, OSError, ValueError) as exc:
            message = f"{type(exc).__name__}: {exc}"
            product["LocationsRetrieved"] = False
            product["LocationsFetchError"] = message
            errors.append({
                "product_id": product["Id"],
                "product_name": product["Name"],
                "error": message,
            })
    return errors


def parse_catalogue_response(raw: bytes) -> dict:
    try:
        payload = json.loads(raw)
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise ValueError("Copernicus response was not valid UTF-8 JSON.") from exc
    if not isinstance(payload, dict):
        raise ValueError("Copernicus OData response must be a JSON object.")
    products = payload.get("value")
    if not isinstance(products, list):
        detail = payload.get("error") or payload
        raise ValueError(f"Copernicus response has no valid 'value' array: {detail}")
    for index, product in enumerate(products):
        if not isinstance(product, dict):
            raise ValueError(f"Product at index {index} is not a JSON object.")
        if not isinstance(product.get("Id"), str) or not product["Id"]:
            raise ValueError(f"Product at index {index} has no usable Id.")
        if not isinstance(product.get("Name"), str) or not product["Name"]:
            raise ValueError(f"Product at index {index} has no usable Name.")
        footprint = product.get("GeoFootprint")
        if footprint is not None and not isinstance(footprint, dict):
            raise ValueError(f"Product at index {index} has an invalid GeoFootprint.")
    return payload


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--start", default=DEFAULT_START, help="Inclusive UTC start.")
    parser.add_argument("--end", default=DEFAULT_END, help="Exclusive UTC end.")
    parser.add_argument("--limit", type=int, default=100)
    parser.add_argument("--timeout", type=int, default=90)
    parser.add_argument("--output-dir", type=Path, default=Path("data/copernicus/nairobi"))
    args = parser.parse_args(argv)
    if args.timeout < 1:
        parser.error("--timeout must be at least 1 second.")
    try:
        params = build_query(args.start, args.end, args.limit)
    except ValueError as exc:
        parser.error(str(exc))

    query_url = f"{API_URL}?{urlencode(params)}"
    try:
        raw = retrieve(query_url, args.timeout)
        payload = parse_catalogue_response(raw)
    except HTTPError as exc:
        print(f"Copernicus HTTP error {exc.code}: {exc.reason}", file=sys.stderr)
        return 2
    except (URLError, TimeoutError, OSError) as exc:
        print(f"Could not retrieve Copernicus catalogue response: {exc}", file=sys.stderr)
        return 2
    except ValueError as exc:
        print(f"Invalid Copernicus catalogue response: {exc}", file=sys.stderr)
        return 3

    retrieved = datetime.now(timezone.utc)
    retrieved_at = retrieved.isoformat(timespec="microseconds").replace("+00:00", "Z")
    stamp = retrieved.strftime("%Y%m%dT%H%M%S%fZ")
    args.output_dir.mkdir(parents=True, exist_ok=True)
    response_path = args.output_dir / f"copernicus_sentinel1_nairobi_{stamp}.json"
    metadata_path = args.output_dir / f"copernicus_sentinel1_nairobi_{stamp}.metadata.json"
    response_path.write_bytes(raw)
    products = payload["value"]
    location_errors = attach_product_locations(products, args.timeout)
    metadata = {
        "source": API_URL,
        "query_url": query_url,
        "query_parameters": params,
        "retrieved_at_utc": retrieved_at,
        "response_file": response_path.name,
        "response_sha256": hashlib.sha256(raw).hexdigest(),
        "product_count": len(products),
        "locations_requested": len(products),
        "locations_retrieved": sum(p.get("LocationsRetrieved") is True for p in products),
        "locations_errors": location_errors,
        "next_link_present": isinstance(payload.get("@odata.nextLink"), str),
        "status": (
            "catalogue_response_saved"
            if not location_errors
            else "catalogue_response_saved_with_location_errors"
        ),
        "interpretation_limit": (
            "Spatial intersection does not establish full AOI coverage. "
            "Product metadata does not establish asset access, full polarisation "
            "requirements, radiometric suitability, or scientific validity."
        ),
    }
    metadata_path.write_text(
        json.dumps(metadata, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    print(f"Saved {len(products)} catalogue product records.")
    print(
        f"Retrieved locations for {metadata['locations_retrieved']}/"
        f"{metadata['locations_requested']} products."
    )
    if location_errors:
        print(f"Warning: location metadata failed for {len(location_errors)} products.")
    print(f"Response: {response_path}")
    print(f"Metadata: {metadata_path}")
    print(f"SHA-256: {metadata['response_sha256']}")
    if metadata["next_link_present"]:
        print("Warning: OData returned a nextLink; additional pages remain.")
    print("Next: inspect full footprints, expanded attributes, polarisation and asset locations.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
