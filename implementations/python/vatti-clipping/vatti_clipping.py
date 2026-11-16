"""Integer-scaled polygon Boolean operations backed by Clipper's Vatti engine."""
from __future__ import annotations
from dataclasses import dataclass
from math import isfinite
from collections.abc import Sequence
import pyclipper

Point = tuple[float, float]

@dataclass(frozen=True)
class Polygon:
    """One polygon component: a counter-clockwise shell and clockwise holes."""
    shell: list[Point]
    holes: list[list[Point]]

_OPERATIONS = {"intersection": pyclipper.CT_INTERSECTION, "union": pyclipper.CT_UNION,
               "difference": pyclipper.CT_DIFFERENCE, "xor": pyclipper.CT_XOR}
_FILL_RULES = {"even_odd": pyclipper.PFT_EVENODD, "non_zero": pyclipper.PFT_NONZERO,
               "positive": pyclipper.PFT_POSITIVE, "negative": pyclipper.PFT_NEGATIVE}
_COORD_LIMIT = 2**61

def _to_path(ring: Sequence[Point], scale: int, name: str):
    if len(ring) > 1 and tuple(ring[0]) == tuple(ring[-1]):
        ring = ring[:-1]
    if len(ring) < 3:
        raise ValueError(f"{name} needs at least three vertices")
    path = []
    for point in ring:
        if len(point) != 2:
            raise ValueError(f"{name} coordinates must be 2D")
        x, y = float(point[0]), float(point[1])
        if not isfinite(x) or not isfinite(y):
            raise ValueError(f"{name} coordinates must be finite")
        ix, iy = round(x * scale), round(y * scale)
        if abs(ix) >= _COORD_LIMIT or abs(iy) >= _COORD_LIMIT:
            raise ValueError(f"{name} exceeds the safe scaled integer range")
        if not path or (ix, iy) != path[-1]:
            path.append((ix, iy))
    if len(path) > 1 and path[0] == path[-1]:
        path.pop()
    if len(set(path)) < 3:
        raise ValueError(f"{name} collapses on the selected precision grid")
    return path

def _paths(rings, scale, name):
    return [_to_path(ring, scale, f"{name}[{i}]") for i, ring in enumerate(rings)]

def _from_path(path, scale):
    return [(x / scale, y / scale) for x, y in path]

def _simplify_paths(paths, fill_type):
    """Node self-crossings into simple contours under the selected fill rule."""
    result = []
    for path in paths:
        simplified = pyclipper.SimplifyPolygon(path, fill_type)
        result.extend(simplified or [path])
    return result


def _components(tree, scale):
    result = []
    def visit(node):
        for child in node.Childs:
            if child.IsHole:
                visit(child)
                continue
            holes = [_from_path(h.Contour, scale) for h in child.Childs if h.IsHole]
            result.append(Polygon(_from_path(child.Contour, scale), holes))
            for hole in child.Childs:
                if hole.IsHole:
                    visit(hole)
    visit(tree)
    result.sort(key=lambda p: -abs(pyclipper.Area(
        [(round(x * scale), round(y * scale)) for x, y in p.shell])))
    return result

def boolean_clip(subjects: Sequence[Sequence[Point]], clips: Sequence[Sequence[Point]],
                 operation: str, *, scale: int = 1_000_000,
                 fill_rule: str = "even_odd") -> list[Polygon]:
    """Run intersection, union, difference or XOR on ring collections.

    Coordinates are rounded to an integer grid; one grid unit equals 1/scale
    input units. The fill rule applies independently to subject and clip rings.
    Returns Polygon components with shell/hole hierarchy. This is an adapter
    to Clipper's Vatti-family engine, not a from-scratch Vatti implementation.
    """
    if operation not in _OPERATIONS:
        raise ValueError(f"operation must be one of {', '.join(_OPERATIONS)}")
    if fill_rule not in _FILL_RULES:
        raise ValueError(f"fill_rule must be one of {', '.join(_FILL_RULES)}")
    if not isinstance(scale, int) or isinstance(scale, bool) or scale <= 0:
        raise ValueError("scale must be a positive integer")
    subject_paths = _simplify_paths(_paths(subjects, scale, "subjects"), _FILL_RULES[fill_rule])
    clip_paths = _simplify_paths(_paths(clips, scale, "clips"), _FILL_RULES[fill_rule])
    if not subject_paths and not clip_paths:
        return []
    engine = pyclipper.Pyclipper()
    if subject_paths:
        engine.AddPaths(subject_paths, pyclipper.PT_SUBJECT, True)
    if clip_paths:
        engine.AddPaths(clip_paths, pyclipper.PT_CLIP, True)
    tree = engine.Execute2(_OPERATIONS[operation], _FILL_RULES[fill_rule],
                           _FILL_RULES[fill_rule])
    return _components(tree, scale)
