using Clipper2Lib;
using Tessellatum.SpatialAnalysis;

static void Require(bool condition, string message)
{
    if (!condition) throw new InvalidOperationException(message);
}

static Path64 Ring(params (long X, long Y)[] points)
{
    var path = new Path64();
    foreach (var (x, y) in points) path.Add(new Point64(x, y));
    return path;
}

static double Area(Paths64 paths) => Math.Abs(Clipper.Area(paths));

var rectangle = Ring((0, 0), (1000, 0), (1000, 600), (0, 600));
var input = new Paths64 { rectangle };
var expanded = Offsetter.OffsetClosedPaths(input, 100, JoinType.Round);
Require(expanded.Count == 1, "Expected one expanded rectangle path.");
Require(expanded[0].Count > rectangle.Count, "Round joins should add arc vertices.");

var contracted = Offsetter.OffsetClosedPaths(input, -100, JoinType.Miter);
Require(contracted.Count == 1, "Expected one contracted rectangle path.");
var collapsed = Offsetter.OffsetClosedPaths(input, -400, JoinType.Miter);
Require(collapsed.Count == 0, "A contraction larger than the half-width should collapse this rectangle.");

// A concave U intersected by a horizontal bar produces two disconnected
// components. This exercises general polygon Boolean overlay, not just offsets.
var uShape = new Paths64
{
    Ring((0, 0), (10, 0), (10, 10), (7, 10), (7, 3), (3, 3), (3, 10), (0, 10))
};
var bar = new Paths64
{
    Ring((-1, 5), (11, 5), (11, 8), (-1, 8))
};
var intersection = Clipper.Intersect(uShape, bar, FillRule.NonZero);
var difference = Clipper.Difference(uShape, bar, FillRule.NonZero);
var union = Clipper.Union(uShape, bar, FillRule.NonZero);

Require(intersection.Count == 2, "Concave intersection should produce two disconnected components.");
Require(Math.Abs(Area(intersection) - 18.0) < 1e-9, "Unexpected U/bar intersection area.");
Require(Math.Abs(Area(difference) - 54.0) < 1e-9, "Unexpected U-minus-bar area.");
Require(Math.Abs(Area(union) - 90.0) < 1e-9, "Unexpected U/bar union area.");
Require(Math.Abs(Area(intersection) + Area(difference) - Area(uShape)) < 1e-9,
    "Intersection and difference should partition the subject area.");

Console.WriteLine("Clipper2 offset and general polygon overlay checks passed.");
Console.WriteLine($"Round-offset vertices: {expanded[0].Count}; disconnected intersection components: {intersection.Count}");
