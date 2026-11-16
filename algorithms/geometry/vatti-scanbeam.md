# Native Vatti scanbeam decomposition

Vatti's general polygon clipping method processes polygon contours through
scanbeams, active edges, local minima, horizontal edges and intersection
events. The first native component implemented here extracts the geometric
events and edge bounds needed to initialise that process.

The package
[implementations/python/vatti-scanbeam](../../implementations/python/vatti-scanbeam/README.md)
provides:
- sorted unique scanbeam levels;
- non-horizontal bounds stored lower-to-upper with original traversal winding;
- explicit horizontal-edge records;
- local-minimum pairs, including horizontal bottom plateaus;
- exact rational slope ordering for the two bounds at each minimum.

This is a **partial native implementation**. It does not yet process the
active-edge list, compute edge crossings, apply fill rules or emit Boolean
output. It must not be described as a complete Vatti clipper.

## References

- Vatti, B. R. (1992), "A generic solution to polygon clipping",
  *Communications of the ACM*, 35(7), 56–63.
- Clipper2 overview: https://www.angusj.com/clipper2/Docs/Overview.htm
