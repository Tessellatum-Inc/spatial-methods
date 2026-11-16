# Greiner–Hormann implementation walkthrough

## Why linked lists?

A polygon is a cyclic sequence. Greiner–Hormann inserts crossing events into
both boundary sequences, preserving their order along each edge. A circular
doubly linked list makes it possible to switch between the two boundaries at a
crossing and to traverse in either direction.

## Event ordering

For segments AB and CD, the crossing parameters t and u locate the same point
on each segment:

```
P = A + t(B - A) = C + u(D - C)
```

Events on each edge are inserted in ascending parameter order. This ordering
is essential: traversing a polygon must encounter crossings in geometric
boundary order, not in the order the nested loops happened to discover them.

## Entry and exit

For an intersection node, inspect a point on the outgoing boundary arc. If
that arc lies inside the other polygon, the event is an entry for intersection
traversal; otherwise it is an exit. The paired event on the other boundary has
the complementary traversal role.

## Traversal

Start at each unvisited entry event on the subject. Follow the subject boundary
to the next crossing, switch to its paired node on the clip boundary, and
continue in the direction implied by that event. Mark both nodes visited to
avoid emitting the same component more than once.

## What is intentionally not hidden

This implementation rejects vertex touches and collinear overlaps instead of
silently treating them as ordinary crossings. It also excludes holes and
self-intersecting rings. These are important parts of production clipping, not
minor details that should be hidden behind a generic "supports arbitrary
polygons" claim.

The test suite combines deterministic topology cases, 1,000 seeded
axis-aligned rectangle pairs checked against interval arithmetic, and 250
seeded rotated rectangle pairs checked against Shapely/GEOS.
