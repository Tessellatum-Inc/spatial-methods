# Intern walkthrough: Euclidean distance on a raster grid

## 1. Define what a cell represents

A raster is an array, but its indices are not map coordinates. Each cell represents an area; this method measures between cell centres. The spacing must be supplied in row and column order, with both values expressed in the same map unit.

## 2. Mark the target cells

The Boolean mask uses True for target cells. The implementation creates a sampled cost array with zero at target cells and positive infinity elsewhere. Each target contributes a parabola to the one-dimensional squared-distance transform.

## 3. Supply physical cell spacing

For square cells of 10 metres, use (10, 10). For a grid with 10-metre rows and 20-metre columns, use (10, 20). The resulting diagonal distance is:

$$
d=\sqrt{(10)^2+(20)^2}=22.36\text{ m (approximately)}
$$

Passing only array indices would silently assume square unit cells.

## 4. Build the lower envelope of parabolas

For one dimension, the algorithm computes
\[
D(q)=\min_i\{f(i)+s^2(q-i)^2\}.
\]
Each finite input sample defines a parabola. The algorithm stores the indices of parabolas on the lower envelope and the intersection coordinates where the winning parabola changes. Both construction and evaluation take linear time. Positive-infinity samples are skipped; a line with no finite samples remains infinite.

The two-dimensional squared Euclidean distance is separable. First apply the one-dimensional transform across each row using column spacing; then apply it down each column using row spacing. Take the square root only after both passes.

## 5. Understand the output

Each output cell stores its Euclidean distance to the nearest target cell. Target cells have distance zero. This is not a path distance: the calculation does not route around barriers, follow terrain or accumulate travel cost.

## 6. Validate the grid assumptions

Tests cover target cells, multiple targets, rectangular cell spacing, diagonal distances, random masks, brute-force comparisons and invalid inputs. The implementation does not infer NoData semantics. Decide whether NoData cells should be included, excluded or masked in downstream analysis.

## 7. Know which algorithm is being used

This package directly implements the Felzenszwalb–Huttenlocher algorithm. The one-dimensional lower-envelope routine is independently tested against brute-force minimisation, and the two-dimensional separable result is tested against direct nearest-target distances.
