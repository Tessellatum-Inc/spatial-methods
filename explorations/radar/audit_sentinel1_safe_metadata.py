#!/usr/bin/env python3
"""Audit Sentinel-1 IW GRD SAFE metadata and dual-polarisation file presence.

This is a pre-processing gate, not a radiometric or geospatial validation.
It inspects ZIP members without extracting or modifying the source archive.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import re
import sys
import zipfile
import xml.etree.ElementTree as ET

POLARISATIONS = {"vv", "vh"}
MEASUREMENT_RE = re.compile(r"^s1[abcd]-iw-grd-(vv|vh)-.*\.tiff?$", re.IGNORECASE)


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def safe_member_names(archive: zipfile.ZipFile) -> list[str]:
    names = []
    for info in archive.infolist():
        name = info.filename.replace("\\", "/")
        parts = Path(name).parts
        if name.startswith("/") or ".." in parts:
            raise ValueError(f"Unsafe path in SAFE archive: {info.filename}")
        if not info.is_dir():
            names.append(name)
    return names


def pol_from_name(name: str) -> str | None:
    match = re.search(r"-(vv|vh)-", Path(name).name, re.IGNORECASE)
    return match.group(1).lower() if match else None


def xml_root(archive: zipfile.ZipFile, member: str) -> ET.Element:
    info = archive.getinfo(member)
    if info.file_size > 20 * 1024 * 1024:
        raise ValueError(f"XML metadata member exceeds 20 MiB safety limit: {member}")
    return ET.fromstring(archive.read(member))


def local_tag(element: ET.Element) -> str:
    return element.tag.rsplit("}", 1)[-1].lower()


def xml_values(root: ET.Element, wanted: set[str]) -> list[str]:
    values = []
    for element in root.iter():
        if local_tag(element) in wanted and element.text and element.text.strip():
            values.append(element.text.strip())
    return sorted(set(values))


def audit_archive(path: Path, expected_product_name: str | None = None) -> dict:
    if not zipfile.is_zipfile(path):
        raise ValueError("Input is not a ZIP archive.")
    with zipfile.ZipFile(path) as archive:
        corrupt = archive.testzip()
        if corrupt:
            raise ValueError(f"ZIP CRC validation failed: {corrupt}")
        names = safe_member_names(archive)
        lower = [name.lower() for name in names]
        manifests = [name for name in names if name.lower().endswith("/manifest.safe") or name.lower() == "manifest.safe"]
        if len(manifests) != 1:
            raise ValueError(f"Expected exactly one manifest.safe; found {len(manifests)}.")
        manifest = manifests[0]
        root = xml_root(archive, manifest)

        measurements = [name for name in names if "/measurement/" in name.lower()]
        measurement_pols = {
            match.group(1).lower()
            for name in measurements
            if (match := MEASUREMENT_RE.match(Path(name).name))
        }
        annotations = [name for name in names if "/annotation/" in name.lower() and name.lower().endswith(".xml")]
        calibrations = [name for name in names if "/calibration/" in name.lower() and name.lower().endswith(".xml")]
        noises = [name for name in names if "/annotation/" in name.lower() and "noise-" in Path(name).name.lower() and name.lower().endswith(".xml")]
        annotation_pols = {pol_from_name(name) for name in annotations if pol_from_name(name)}
        calibration_pols = {pol_from_name(name) for name in calibrations if pol_from_name(name)}
        noise_pols = {pol_from_name(name) for name in noises if pol_from_name(name)}

        manifest_pols = {
            value.upper()
            for value in xml_values(root, {"transmitterreceiverpolarisation", "polarisation"})
            if value.upper() in {"VV", "VH", "HH", "HV"}
        }
        swaths = xml_values(root, {"swath"})
        modes = xml_values(root, {"mode", "producttype"})
        product_names = [
            Path(name).parts[0]
            for name in names
            if Path(name).parts and Path(name).parts[0].lower().endswith(".safe")
        ]
        root_product_name = product_names[0] if product_names else ""

    checks = {
        "measurement_contains_vv_and_vh": measurement_pols == POLARISATIONS,
        "annotation_contains_vv_and_vh": annotation_pols == POLARISATIONS,
        "calibration_contains_vv_and_vh": calibration_pols == POLARISATIONS,
        "noise_annotation_contains_vv_and_vh": noise_pols == POLARISATIONS,
        "manifest_is_well_formed_xml": True,
    }
    if expected_product_name:
        checks["product_name_matches_expected"] = root_product_name == expected_product_name
    passed = all(checks.values())
    return {
        "archive": path.name,
        "archive_size_bytes": path.stat().st_size,
        "archive_sha256": sha256_file(path),
        "safe_root_name": root_product_name,
        "manifest_member": manifest,
        "manifest_polarisation_values": manifest_pols,
        "manifest_swath_values": swaths,
        "manifest_mode_or_product_type_values": modes,
        "measurement_files": sorted(measurements),
        "measurement_polarisations": sorted(measurement_pols),
        "annotation_file_count": len(annotations),
        "annotation_polarisations": sorted(annotation_pols),
        "calibration_file_count": len(calibrations),
        "calibration_polarisations": sorted(calibration_pols),
        "noise_annotation_file_count": len(noises),
        "noise_annotation_polarisations": sorted(noise_pols),
        "checks": checks,
        "structural_dual_pol_gate": "passed" if passed else "failed",
        "scientific_processing_status": "not_started",
        "limitations": [
            "Filename and XML presence checks do not validate raster readability, pixel values, calibration LUT contents, or geolocation.",
            "Manifest polarisation and swath tags vary by product generation; absent tags are reported, not inferred.",
            "A passing structural gate does not establish complete datatake coverage or radiometric comparability.",
        ],
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("archive", type=Path, help="Downloaded SAFE ZIP archive.")
    parser.add_argument("--expected-product-name")
    parser.add_argument("--output", type=Path, help="Optional JSON report path.")
    args = parser.parse_args(argv)
    try:
        report = audit_archive(args.archive, args.expected_product_name)
    except (OSError, ValueError, zipfile.BadZipFile, ET.ParseError) as exc:
        print(f"SAFE metadata audit failed: {exc}", file=sys.stderr)
        return 2
    rendered = json.dumps(report, indent=2, ensure_ascii=False) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(rendered, encoding="utf-8")
    print(rendered, end="")
    return 0 if report["structural_dual_pol_gate"] == "passed" else 1


if __name__ == "__main__":
    raise SystemExit(main())
