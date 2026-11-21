"""Generate annotated visual-review sheets for the HEIG-VD control/checkpoint rehearsal.

The output is a review aid, not a point-visibility approval or accuracy assessment.
Source images remain in the acquired snapshot and are never modified.
"""
from __future__ import annotations

import argparse
import csv
import json
import math
from pathlib import Path
from textwrap import dedent


IMAGE_PREFIX = "EB-02-00761_"
MARKER_COLOR = (245, 190, 35)


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
    from PIL import Image, ImageDraw, ImageFont

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
            unique_points = set()
            ox = (tile_w - resized.width) // 2
            oy = header_h + 6
            for item in rows:
                # Validate membership, but intentionally do not reveal the role.
                roles[item["point_id"]]
                unique_points.add(item["point_id"])
                x = ox + item["x"] * scale
                y = oy + item["y"] * scale
                color = MARKER_COLOR
                radius = 10
                draw.ellipse((x-radius, y-radius, x+radius, y+radius), outline=(0,0,0), width=4)
                draw.ellipse((x-radius+2, y-radius+2, x+radius-2, y+radius-2), outline=color, width=5)
                label = item["point_id"]
                bbox = draw.textbbox((0, 0), label, font=font)
                tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
                lx, ly = x + 12, y - th // 2
                draw.rectangle((lx-2, ly-1, lx+tw+3, ly+th+2), fill=(255,255,255))
                draw.text((lx, ly), label, fill=color, font=font)
            footer = f"observations: {len(rows)} | unique points: {len(unique_points)}"
            draw.text((12, tile_h - 18), footer, fill=(25,25,25), font=font)
            annotated = output / "images" / f"{image_path.stem}-annotated.jpg"
            annotated.parent.mkdir(parents=True, exist_ok=True)
            canvas.save(annotated, quality=88, optimize=True)
            annotated_paths.append(annotated)
            image_summaries.append({"image": image_path.name, "observations": len(rows), "unique_points": len(unique_points)})

    # Two 4x4 sheets; each tile preserves readable image context and point labels.
    for page in range(2):
        sheet = Image.new("RGB", (tile_w * 4, tile_h * 4 + 72), (235, 235, 235))
        draw = ImageDraw.Draw(sheet)
        draw.text((18, 14), "HEIG-VD drone 2019 - annotated image observations", fill=(20,20,20), font=ImageFont.load_default())
        draw.text((18, 38), "Yellow markers = publisher-provided Metashape image picks. Control/checkpoint roles are intentionally hidden in this review aid.", fill=(20,20,20), font=ImageFont.load_default())
        for index, path in enumerate(annotated_paths[page*16:(page+1)*16]):
            with Image.open(path) as tile:
                sheet.paste(tile, ((index % 4) * tile_w, 72 + (index // 4) * tile_h))
        sheet.save(output / f"contact-sheet-{page+1}.jpg", quality=88, optimize=True)

    # Build a role-blind, high-resolution view for each point across all source images.
    image_by_stem = {path.stem: path for path in images}
    observations_by_point: dict[str, list[dict]] = {}
    for stem, rows in observations.items():
        if stem not in image_by_stem:
            raise ValueError(f"Observation image is missing: {stem}")
        for item in rows:
            observations_by_point.setdefault(item["point_id"], []).append({
                **item, "image_path": image_by_stem[stem]
            })

    crop_size = 640
    crop_header = 36
    crop_tile_height = crop_size + crop_header
    point_review_dir = output / "point-review"
    point_review_dir.mkdir(parents=True, exist_ok=True)
    point_review_summaries = []
    for point_id in sorted(observations_by_point):
        point_rows = sorted(
            observations_by_point[point_id],
            key=lambda item: item["image_path"].name,
        )
        columns = 3
        row_count = math.ceil(len(point_rows) / columns)
        sheet = Image.new(
            "RGB",
            (columns * crop_size, row_count * crop_tile_height + 56),
            (238, 238, 238),
        )
        sheet_draw = ImageDraw.Draw(sheet)
        sheet_draw.text(
            (12, 12),
            f"Point {point_id} — {len(point_rows)} source image observations",
            fill=(20, 20, 20),
            font=font,
        )
        sheet_draw.text(
            (12, 32),
            "Role-blind review: yellow ring marks the publisher-provided image pick; role is not shown.",
            fill=(20, 20, 20),
            font=font,
        )
        for index, item in enumerate(point_rows):
            with Image.open(item["image_path"]) as source:
                source = source.convert("RGB")
                width, height = source.size
                left = round(item["x"] - crop_size / 2)
                top = round(item["y"] - crop_size / 2)
                right, bottom = left + crop_size, top + crop_size
                crop = Image.new("RGB", (crop_size, crop_size), (245, 245, 245))
                source_crop = source.crop((
                    max(0, left), max(0, top),
                    min(width, right), min(height, bottom),
                ))
                crop.paste(source_crop, (max(0, -left), max(0, -top)))
            tile = Image.new("RGB", (crop_size, crop_tile_height), (250, 250, 250))
            tile_draw = ImageDraw.Draw(tile)
            tile_draw.text(
                (8, 10),
                f"{item['image_path'].name} | px {item['x']:.1f}, {item['y']:.1f}",
                fill=(20, 20, 20),
                font=font,
            )
            tile.paste(crop, (0, crop_header))
            marker_x = item["x"] - left
            marker_y = item["y"] - top + crop_header
            radius = 13
            tile_draw.ellipse(
                (marker_x-radius, marker_y-radius, marker_x+radius, marker_y+radius),
                outline=(0, 0, 0), width=5,
            )
            tile_draw.ellipse(
                (marker_x-radius+2, marker_y-radius+2, marker_x+radius-2, marker_y+radius-2),
                outline=MARKER_COLOR, width=5,
            )
            tile_draw.line(
                (marker_x-18, marker_y, marker_x+18, marker_y),
                fill=MARKER_COLOR, width=2,
            )
            tile_draw.line(
                (marker_x, marker_y-18, marker_x, marker_y+18),
                fill=MARKER_COLOR, width=2,
            )
            sheet.paste(
                tile,
                ((index % columns) * crop_size, 56 + (index // columns) * crop_tile_height),
            )
        point_path = point_review_dir / f"point-{point_id}.jpg"
        sheet.save(point_path, quality=92, optimize=True)
        point_review_summaries.append({
            "point_id": point_id,
            "observation_count": len(point_rows),
            "review_sheet": str(point_path.relative_to(output)),
        })

    # Machine-readable blank register for a role-blind review of every source pick.
    review_register = output / "observation-review-register.csv"
    with review_register.open("w", newline="", encoding="utf-8") as stream:
        writer = csv.writer(stream)
        writer.writerow([
            "point_id", "image", "source_pixel_x", "source_pixel_y",
            "visibility", "target_identity", "centring", "occlusion",
            "sharpness", "ambiguity", "cross_image_correspondence",
            "decision", "reason", "reviewer", "reviewed_at",
        ])
        for stem in sorted(observations):
            image_name = image_by_stem.get(stem)
            if image_name is None:
                raise ValueError(f"Observation image is missing: {stem}")
            for item in sorted(observations[stem], key=lambda row: row["point_id"]):
                writer.writerow([
                    item["point_id"], image_name, f'{item["x"]:.3f}', f'{item["y"]:.3f}',
                    "", "", "", "", "", "", "", "", "", "", "",
                ])

    instructions = dedent("""# Role-blind point review

    Review the point sheets before consulting the control/checkpoint split key.

    For each point, inspect every source image crop and record:
    - whether the intended target or feature is clearly identifiable;
    - whether the publisher's marker is centred on the intended target;
    - blur, occlusion, shadow, glare, vegetation, repeated patterns or ambiguity;
    - whether the observation should be accepted, questioned or rejected, with a reason.

    The yellow ring marks the publisher-provided Metashape image coordinate. These
    observations have not been independently remeasured. A visible marker does not
    establish survey accuracy or checkpoint independence. Keep reviewer decisions
    and rationale locked before unblinding control/checkpoint roles.
    """).strip() + "\n"
    (point_review_dir / "README.md").write_text(instructions, encoding="utf-8")

    report = {
        "status": "role_blind_visual_review_material_prepared_not_human_approved",
        "source_image_count": len(images),
        "observation_count": sum(len(v) for v in observations.values()),
        "images_with_observations": len(observations),
        "unique_observed_point_count": len({o["point_id"] for rows in observations.values() for o in rows}),
        "point_review_sheet_count": len(point_review_summaries),
        "point_review_crop_size_px": crop_size,
        "point_review_sheets": point_review_summaries,
        "image_summaries": image_summaries,
        "limitations": [
            "Markers reproduce source-provided Metashape image picks; they are not independently remeasured.",
            "Control/checkpoint role assignments are intentionally omitted from the review sheets; keep reviewer decisions locked before consulting the split key.",
            "A visible marker does not establish target-centre quality, survey quality or independent checkpoint status.",
            "High-resolution per-point sheets show 640x640 pixel crops around each observation, with the source-provided pick marked.",
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
