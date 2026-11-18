#!/usr/bin/env python3
"""Check relative Markdown and notebook links, including GitHub-style heading anchors.

External links are skipped. Markdown heading slug behavior is approximated for the
common GitHub rules (lowercase, punctuation removal, spaces to hyphens, duplicate
suffixes). Explicit HTML anchors are recognized. Unsupported renderer-specific
anchors may require manual inspection.
"""
from __future__ import annotations
import json
import re
import sys
from pathlib import Path
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parents[1]
LINK_RE = re.compile(r"!?(?:\[[^\]]*\])\(([^)]+)\)")
HEADING_RE = re.compile(r"^\s{0,3}(#{1,6})\s+(.+?)\s*#*\s*$")
HTML_ANCHOR_RE = re.compile(r"<a\s+(?:[^>]*?\s)?(?:id|name)=[\"']([^\\"']+)[\\"'][^>]*>", re.I)

def strip_fenced_code(text: str) -> str:
    """Remove fenced code blocks so example URLs/headings are not checked."""
    output = []
    in_fence = False
    fence_char = ""
    fence_length = 0
    for line in text.splitlines():
        match = re.match(r"^\s{0,3}(\x60{3,}|~{3,})", line)
        if match:
            marker = match.group(1)
            if not in_fence:
                in_fence, fence_char, fence_length = True, marker[0], len(marker)
                continue
            if marker[0] == fence_char and len(marker) >= fence_length:
                in_fence = False
                continue
        if not in_fence:
            output.append(line)
    return "\n".join(output)

def markdown_sources(path: Path) -> list[tuple[str, str]]:
    if path.suffix.lower() == ".md":
        return [(str(path.relative_to(ROOT)), strip_fenced_code(path.read_text(encoding="utf-8")))]
    if path.suffix.lower() == ".ipynb":
        notebook = json.loads(path.read_text(encoding="utf-8"))
        sources = []
        for index, cell in enumerate(notebook.get("cells", [])):
            if cell.get("cell_type") == "markdown":
                raw = cell.get("source", [])
                cell_text = "".join(raw) if isinstance(raw, list) else str(raw)
                sources.append((f"{path.relative_to(ROOT)} [markdown cell {index}]", strip_fenced_code(cell_text)))
        return sources
    return []

def resolve_target(source_name: str, raw_target: str) -> Path | None:
    target = raw_target.strip().split()[0].strip("<>")
    if not target:
        return None
    parsed = urlsplit(target)
    if parsed.scheme or parsed.netloc:
        return None
    target_path = unquote(parsed.path)
    source = ROOT / source_name.split(" [markdown cell", 1)[0]
    if not target_path:
        return source.resolve()
    resolved = ROOT / target_path.lstrip("/") if target_path.startswith("/") else source.parent / target_path
    return resolved.resolve()

def resolve_heading_anchor(source_name: str, raw_target: str) -> tuple[Path | None, str]:
    target = raw_target.strip().split()[0].strip("<>")
    parsed = urlsplit(target)
    if parsed.scheme or parsed.netloc:
        return None, ""
    target_path = unquote(parsed.path)
    source = ROOT / source_name.split(" [markdown cell", 1)[0]
    resolved = ROOT / target_path.lstrip("/") if target_path.startswith("/") else (source.parent / target_path if target_path else source)
    return resolved.resolve(), unquote(parsed.fragment)

def github_heading_slug(heading: str) -> str:
    """Approximate GitHub heading slug rules for ordinary Markdown headings."""
    heading = re.sub(r"<[^>]+>", "", heading)
    heading = re.sub(r"\\", "", heading)
    heading = re.sub(r"[\x60*_~]", "", heading).strip().lower()
    heading = re.sub(r"[^\w -]", "", heading, flags=re.UNICODE)
    return re.sub(r"\s+", "-", heading).strip("-")

def heading_anchors(source_text: str) -> set[str]:
    """Collect heading slugs and explicit HTML anchors, including duplicates."""
    anchors = set()
    counts: dict[str, int] = {}
    for line in source_text.splitlines():
        for match in HTML_ANCHOR_RE.finditer(line):
            anchors.add(match.group(1))
        match = HEADING_RE.match(line)
        if not match:
            continue
        slug = github_heading_slug(match.group(2))
        if not slug:
            continue
        duplicate = counts.get(slug, 0)
        counts[slug] = duplicate + 1
        anchors.add(slug if duplicate == 0 else f"{slug}-{duplicate}")
    return anchors

def source_text_for_path(path: Path) -> list[str]:
    if not path.exists():
        return []
    if path.suffix.lower() == ".md":
        return [strip_fenced_code(path.read_text(encoding="utf-8"))]
    if path.suffix.lower() == ".ipynb":
        notebook = json.loads(path.read_text(encoding="utf-8"))
        out = []
        for cell in notebook.get("cells", []):
            if cell.get("cell_type") == "markdown":
                raw = cell.get("source", [])
                out.append(strip_fenced_code("".join(raw) if isinstance(raw, list) else str(raw)))
        return out
    return []

def main() -> int:
    errors = []
    checked = 0
    anchor_checked = 0
    candidates = sorted(
        path for path in ROOT.rglob("*")
        if path.is_file() and ".git" not in path.parts
        and path.suffix.lower() in {".md", ".ipynb"}
    )
    anchor_cache: dict[Path, set[str]] = {}
    for path in candidates:
        for source_name, text in markdown_sources(path):
            for match in LINK_RE.finditer(text):
                raw_target = match.group(1)
                resolved = resolve_target(source_name, raw_target)
                if resolved is None:
                    continue
                checked += 1
                if not resolved.exists():
                    errors.append(f"{source_name}: broken local link -> {raw_target}")
                    continue
                target, anchor = resolve_heading_anchor(source_name, raw_target)
                if not anchor or target is None or target.suffix.lower() not in {".md", ".ipynb"}:
                    continue
                anchor_checked += 1
                if target not in anchor_cache:
                    target_sources = source_text_for_path(target)
                    anchor_cache[target] = set().union(*(heading_anchors(s) for s in target_sources) if target_sources else set())
                if anchor not in anchor_cache[target]:
                    display = target.relative_to(ROOT) if target.is_relative_to(ROOT) else target
                    errors.append(f"{source_name}: missing heading anchor #{anchor} in {display}")
    if errors:
        print("\n".join(errors))
        print(f"\nFound {len(errors)} broken link/anchor(s); checked {checked} local links and {anchor_checked} anchors.")
        return 1
    print(f"Checked {checked} local links and {anchor_checked} heading anchors across {len(candidates)} Markdown and notebook files.")
    return 0

if __name__ == "__main__":
    sys.exit(main())
