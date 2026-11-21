"""Generate annotated visual-review sheets for the HEIG-VD control/checkpoint rehearsal.

The output is a review aid, not a point-visibility approval or accuracy assessment.
Source images remain in the acquired snapshot and are never modified.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROLES = {
    "control": (230, 126, 34),
    "checkpoint": (30, 144, 255),
    "excluded": (245, 205, 48),
}
IMAGE_PREFIX = "EB-02-00761_"


def load_split(path: Path) -> dict[str, str]:
    split = json.loads(path.read_text(encoding="utf-8"))
    selection = split["selection"]
    roles: dict[str, str] = {}
    for role, key in (
        ("control", "control_points"),
        ("checkpoint", "checkpoint_points"),
    ):
        for point_id in selection[key]:
            if point_id in roles:
                raise ValueError(f"Point {point_id} appears in more than one split")
            roles[point_id] = role
    for point_id in selection.get("excluded_low_observation_points", {}):
        if point_id in roles:
            raise ValueError(f"Excluded point {point_id} also appears in split")
        roles[point_id] = "excluded"
    return roles


def image_stem(label: str) -> str:
    return label if label.startswith(IMAGE_PREFIX) else IMAGE_PREFIX + label


def generate(dataset: Path, split_path: Path, output: Path) -> dict:
    dataset = dataset.resolve()
    output.mkdir(parents=True, exist_ok=True)
    roles = load_split(split_path)
    observations: dict[str, list[dict]] = {}
    with (dataset / "gcp" / "gcp_obs.csv").open(encoding="utf-8-sig") as stream:
        for line_number, line in enumerate(stream, 1):
            if not line.strip() or line.lstrip().startswith("#"):
                continue
            # The publisher's .csv export is whitespace-delimited, not comma-delimited.
            row = line.split()
            if len(row) != 4:
                raise ValueError(f"Observation line {line_number}: expected 4 fields, got {len(row)}")
            point_id, label, x, y = row
            observations.setdefault(image_stem(label), []).append(
                {"point_id": point_id, "x": float(x), "y": float(y)}
            )

    images = sorted((dataset / "images").glob("*.JPG"))
    if len(images) != 32:
        raise ValueError(f"Expected 32 JPG images, found {len(images)}")
    unknown = sorted({o["point_id"] for rows in observations.values() for o in rows} - set(roles))
    if unknown:
        raise ValueError(f"Observations contain points absent from split: {unknown}")

    font = ImageFont.load_default()
    tile_w, tile_h, header_h = 1120, 790, 36
    annotated_paths = []
    image_summaries = []
    for image_path in images:
        with Image.open(image_path) as source:
            source = source.convert("RGB")
            actual_w, actual_h = source.size
            if (actual_w, actual_h) != (5472, 3648):
                raise ValueError(f"{image_path.name}: unexpected dimensions {source.size}")
            scale = min((tile_w - 24) / actual_w, (tile_h - header_h - 20) / actual_h)
            resized = source.resize((round(actual_w * scale), round(actual_h * scale)), Image.Resampling.LANCZOS)
            canvas = Image.new("RGB", (tile_w, tile_h), (245, 245, 245))
            canvas.paste(resized, ((tile_w - resized.width) // 2, header_h + 6))
            draw = ImageDraw.Draw(canvas)
            draw.text((12, 10), image_path.name, fill=(20, 20, 20), font=font)
            rows = observations.get(image_path.stem, [])
            counts = {"control": 0, "checkpoint": 0, "excluded": 0}
            ox = (tile_w - resized.width) // 2
            oy = header_h + 6
            for item in rows:
                role = roles[item["point_id"]]
                counts[role] += 1
                x = ox + item["x"] * scale
                y = oy + item["y"] * scale
                color = ROLES[role]
                radius = 11 if role != "excluded" else 9
                draw.ellipse((x-radius, y-radius, x+radius, y+radius), outline=(0,0,0), width=4)
                draw.ellipse((x-radius+2, y-radius+2, x+radius-2, y+radius-2), outline=color, width=5)
                label = item["point_id"]
                bbox = draw.textbbox((0, 0), label, font=font)
                tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
                lx, ly = x + 12, y - th // 2
                draw.rectangle((lx-2, ly-1, lx+tw+3, ly+th+2), fill=(255,255,255))
                draw.text((lx, ly), label, fill=color, font=font)
            footer = f"observations: {len(rows)} | controls: {counts['control']} | checkpoints: {counts['checkpoint']} | excluded: {counts['excluded']}"
            draw.text((12, tile_h - 18), footer, fill=(25,25,25), font=font)
            annotated = output / "images" / f"{image_path.stem}-annotated.jpg"
            annotated.parent.mkdir(parents=True, exist_ok=True)
            canvas.save(annotated, quality=88, optimize=True)
            annotated_paths.append(annotated)
            image_summaries.append({"image": image_path.name, "observations": len(rows), **counts})

    # Two 4x4 sheets; each tile preserves readable image context and point labels.
    for page in range(2):
        sheet = Image.new("RGB", (tile_w * 4, tile_h * 4 + 72), (235, 235, 235))
        draw = ImageDraw.Draw(sheet)
        draw.text((18, 14), "HEIG-VD drone 2019 - annotated image observations", fill=(20,20,20), font=ImageFont.load_default())
        draw.text((18, 38), "Orange = proposed control | Blue = withheld checkpoint | Yellow = excluded low-observation point. Markers show publisher-provided Metashape picks.", fill=(20,20,20), font=ImageFont.load_default())
        for index, path in enumerate(annotated_paths[page*16:(page+1)*16]):
            with Image.open(path) as tile:
                sheet.paste(tile, ((index % 4) * tile_w, 72 + (index // 4) * tile_h))
        sheet.save(output / f"contact-sheet-{page+1}.jpg", quality=88, optimize=True)

    report = {
        "status": "visual_review_material_prepared_not_human_approved",
        "source_image_count": len(images),
        "observation_count": sum(len(v) for v in observations.values()),
        "images_with_observations": len(observations),
        "point_role_counts": {role: sum(value == role for value in roles.values()) for role in ROLES},
        "image_summaries": image_summaries,
        "limitations": [
            "Markers reproduce source-provided Metashape image picks; they are not independently remeasured.",
            "A visible marker does not establish target-centre quality, survey quality or independent checkpoint status.",
            "Human review must inspect target visibility, centring, occlusion, blur, ambiguity and marker-to-target correspondence.",
        ],
    }
    (output / "visual-review-summary.json").write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    return report


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("dataset_root", type=Path)
    parser.add_argument("split_json", type=Path)
    parser.add_argument("output_dir", type=Path)
    args = parser.parse_args()
    report = generate(args.dataset_root, args.split_json, args.output_dir)
    print(json.dumps({k: v for k, v in report.items() if k != "image_summaries"}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
