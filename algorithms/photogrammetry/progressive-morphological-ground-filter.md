# Progressive morphological ground filtering

Progressive morphological filtering (PMF) estimates terrain from a point cloud
by applying grayscale morphological openings with progressively larger
structuring elements. The opening suppresses elevated objects at scales
smaller than the current window; a height threshold controls which returns
remain candidate ground.

## Rasterised reference workflow

The teaching implementation rasterises the minimum elevation among current
ground candidates, fills empty cells using nearest valid neighbours, and
applies a square grayscale opening at each configured odd window width.
Candidate points are retained when their height above the opened surface is
no greater than

    d(w) = min(d_max, d_0 + s * c * (w - 1)),

where c is horizontal cell size, s is a slope factor and d0/dmax are vertical
tolerances. The candidate set is progressively reduced across windows.

## Implementation and limitations

See [the Python package](../../implementations/python/progressive-morphological-filter/README.md).
This is a rasterised baseline, not a claim of exact equivalence to every PMF
paper or commercial implementation. It does not solve all terrain,
vegetation, bridge and building-edge cases. Validate parameter schedules and
classification accuracy against independent ground labels. Use projected
coordinates and consistent horizontal/vertical units.
