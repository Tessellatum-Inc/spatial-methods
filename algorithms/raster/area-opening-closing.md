# Grayscale area opening and closing

An area opening suppresses bright connected structures whose connected-component area is below a threshold while preserving larger structures. For each gray level, form the upper-level set and identify connected components; a pixel's filtered value is the highest level at which its component satisfies the minimum-area criterion. Area closing is the dual operation on the negated image and fills small dark components.

The implementation uses explicit threshold-stack connected-component traversal with 4- or 8-neighbour connectivity. It is a clear small-raster reference, not an efficient max-tree construction. Runtime scales with the number of unique values times the number of pixels.
