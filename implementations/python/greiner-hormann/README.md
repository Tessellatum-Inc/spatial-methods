# Greiner–Hormann polygon intersection

A from-scratch Python implementation of the Greiner–Hormann linked-list
polygon intersection method.

## Contract

- One simple, hole-free ring per input.
- Arbitrary concavity is allowed.
- Proper transverse edge crossings are supported.
- Disjoint and containment cases are handled.
- Multiple disconnected output rings are supported.
- Inputs are normalized to counter-clockwise orientation.
- Vertex-touch and collinear/coincident boundary events are explicitly
  rejected; point/line-only output is not represented.
- Coordinates must be finite planar 2D values in the same coordinate system.

This is a teaching implementation, not a robust GIS overlay engine. It uses a
single scale-sensitive epsilon for event classification and does not implement
a precision grid, holes, self-intersecting input, or a full arrangement model.

## Run

```bash
python -m pip install pytest shapely
PYTHONPATH=. pytest -q
```

Shapely is used only by the rotated-rectangle test as an independent oracle;
the algorithm itself uses only the Python standard library.

## Algorithm outline

1. Normalize and validate both simple rings.
2. Find proper segment crossings and compute each crossing's edge parameter.
3. Insert paired intersection nodes in order into both circular linked lists.
4. Mark each crossing as an entry/exit event by testing the following boundary
   arc against the other polygon.
5. Start at each unvisited entry node, follow the current ring, switch to its
   paired node at each crossing, and reverse/continue according to the paired
   event's entry state.
6. Remove duplicate consecutive coordinates and return CCW components.

The key data structure is a pair of circular doubly linked lists. Each
intersection node stores a pointer to its counterpart in the other polygon.

## Complexity

For rings with n and m vertices, this straightforward implementation compares
all edge pairs, so intersection discovery is O(nm). Insertion and traversal
are linear in the number of vertices plus intersections. It is intended for
algorithm study and moderate inputs, not very large production geometries.
