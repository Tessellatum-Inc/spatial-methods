#!/usr/bin/env python3
"""Audit Copernicus Sentinel-1 product footprints against the Nairobi study AOI.

Requires Shapely. Catalogue intersection is only a discovery condition; this
audit independently tests whether each returned footprint covers the full
rectangular study AOI.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

from shapely.geometry import box, shape

AOI_BOUNDS = (36.65, -1.45, 37.05, -1.15)
AOI_WKT = (
    "POLYGON((36.65 -1.45,37.05 -1.45,37.05 -1.15,"
    "36.65 -1.15,36.65 -1.45))"
)


def attribute_map(product: dict) -> dict:
    """Return product attributes keyed by their catalogue Name."""
    attributes = product.get("Attributes", [])
    if not isinstance(attributes, list):
        return {}
    return {
        item["Name"]: item.get("Value")
        for item in attributes
        if isinstance(item, dict) and isinstance(item.get("Name"), str)
    }


def audit_product(product: dict, aoi) -> dict:
    """Summarise metadata and test whether the product footprint covers AOI."""
    attrs = attribute_map(product)
    footprint = product.get("GeoFootprint")
    geometry_valid = False
    covers_aoi = False
    geometry_type = None
    if isinstance(footprint, dict):
        try:
            geometry = shape(footprint)
            geometry_type = geometry.geom_type
            geometry_valid = bool(not geometry.is_empty and geometry.is_valid)
            covers_aoi = bool(geometry_valid and geometry.covers(aoi))
        except (TypeError, ValueError):
            pass

    locations = product.get("Locations", [])
    if not isinstance(locations, list):
        locations = []
    location_records = [
        {
            "format_type": item.get("FormatType"),
            "download_link": item.get("DownloadLink"),
            "content_length_bytes": item.get("ContentLength"),
        }
        for item in locations
        if isinstance(item, dict)
    ]

    return {
        "product_id": product.get("Id"),
        "product_name": product.get("Name"),
        "sensing_start_utc": (product.get("ContentDate") or {}).get("Start"),
        "sensing_end_utc": (product.get("ContentDate") or {}).get("End"),
        "content_length_bytes": product.get("ContentLength"),
        "online": product.get("Online"),
        "product_type": attrs.get("productType"),
        "platform": attrs.get("platformSerialIdentifier"),
        "instrument_mode": attrs.get("operationalMode"),
        "swath": attrs.get("swathIdentifier"),
        "orbit_direction": attrs.get("orbitDirection"),
        "relative_orbit": attrs.get("relativeOrbitNumber"),
        "polarisation_channels": attrs.get("polarisationChannels"),
        "product_composition": attrs.get("productComposition"),
        "slice_number": attrs.get("sliceNumber"),
        "total_slices": attrs.get("totalSlices"),
        "timeliness": attrs.get("timeliness"),
        "processing_level": attrs.get("processingLevel"),
        "footprint_type": geometry_type,
        "footprint_valid": geometry_valid,
        "covers_study_aoi": covers_aoi,
        "locations_retrieved": product.get("LocationsRetrieved") is True,
        "locations": location_records,
    }


def build_inventory(enriched_path: Path) -> dict:
    raw = enriched_path.read_bytes()
    payload = json.loads(raw)
    products = payload.get("value") if isinstance(payload, dict) else None
    if not isinstance(products, list):
        raise ValueError("Enriched OData response must contain a 'value' array.")

    metadata_path = enriched_path.with_name(
        enriched_path.name.replace(".with_locations.json", ".metadata.json")
    )
    if not metadata_path.exists():
        raise ValueError(f"Missing provenance sidecar: {metadata_path.name}")
    metadata = json.loads(metadata_path.read_text(encoding="utf-8"))

    aoi = box(*AOI_BOUNDS)
    audited = [audit_product(product, aoi) for product in products]
    candidates = [
        item["product_id"] for item in audited if item["covers_study_aoi"]
    ]
    return {
        "title": "Nairobi Sentinel-1 IW GRD catalogue inventory",
        "generated_from": enriched_path.name,
        "source": metadata.get("source"),
        "retrieved_at_utc": metadata.get("retrieved_at_utc"),
        "query_url": metadata.get("query_url"),
        "raw_response_sha256": metadata.get("response_sha256"),
        "enriched_response_sha256": hashlib.sha256(raw).hexdigest(),
        "product_count": len(audited),
        "locations_requested": metadata.get("locations_requested"),
        "locations_retrieved": metadata.get("locations_retrieved"),
        "next_link_present": metadata.get("next_link_present"),
        "study_aoi": {
            "crs": "EPSG:4326",
            "bounds_west_south_east_north": list(AOI_BOUNDS),
            "wkt": AOI_WKT,
            "coverage_test": "footprint geometry covers the complete rectangle",
        },
        "full_aoi_cover_candidate_ids": candidates,
        "interpretation_limits": [
            "The AOI is a rectangular discovery and exercise boundary, not an official Nairobi administrative boundary.",
            "Footprint coverage is tested against the complete rectangle; it does not certify radiometric quality or scientific suitability.",
            "Online status and catalogue download links do not prove authorized product download; Copernicus download requires an access token.",
            "A Sentinel-1 slice product is not a complete datatake; slice composition and adjoining products must be considered.",
        ],
        "products": audited,
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", required=True, type=Path, help="Enriched .with_locations.json file.")
    parser.add_argument("--output", required=True, type=Path, help="Inventory JSON output path.")
    args = parser.parse_args(argv)
    try:
        inventory = build_inventory(args.input)
    except (OSError, json.JSONDecodeError, ValueError) as exc:
        parser.error(str(exc))
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(inventory, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    print(f"Audited {inventory['product_count']} products.")
    print(f"Full-AOI candidates: {len(inventory['full_aoi_cover_candidate_ids'])}")
    print(f"Inventory: {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
