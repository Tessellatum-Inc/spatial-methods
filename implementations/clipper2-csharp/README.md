# Clipper2 polygon offsetting and Boolean overlay example (C#)

This .NET 8 console project exercises Clipper2's integer-path APIs for closed
polygon offsetting and general polygon Boolean operations. It complements,
but is deliberately separate from, the dependency-free Python teaching
implementations.

## Run

```bash
dotnet run --project implementations/clipper2-csharp/Clipper2Example.csproj
```

The executable checks:

- positive round offset, negative miter offset and complete collapse;
- intersection, difference and union of a concave U-shaped polygon and a
  horizontal bar;
- the expected two disconnected intersection components;
- independent area identities for the Boolean results.

The concave fixture is important: it cannot be represented by the one-ring
Sutherland–Hodgman API in `implementations/python/polygon-clipping`. Clipper2
returns a collection of paths and handles disconnected output.

## Coordinate scale is your responsibility

Clipper2's `Paths64` uses integer coordinates. If one coordinate unit is
intended to represent one millimetre, encode metres using a scale of 1,000.
Scale all coordinates and offset distances consistently, check integer range,
and document the chosen scale. The sample uses a small integer grid.

## Algorithm and scope

This is a **library-backed general polygon overlay example**, not a from-scratch
Vatti implementation. Clipper2 supplies the scanline Boolean engine; this
repository's code defines fixtures, invokes the API and independently checks
component counts and area conservation. Do not cite this wrapper as an
implementation of Vatti's original algorithm.

The example uses the NonZero fill rule and simple, non-self-intersecting input
rings. More fixtures are required before claiming coverage of self-intersecting
paths, complex hole nesting, all fill rules, touching/coincident boundaries or
production CRS precision policies.

## Source and version

- NuGet package: [Clipper2](https://www.nuget.org/packages/Clipper2/), pinned
  here to 2.0.0.
- [Clipper2 official documentation](https://www.angusj.com/clipper2/Docs/Overview.htm).
- [Clipper API](https://www.angusj.com/clipper2/Docs/Units/Clipper/Functions/Clipper_Intersect.htm).

The package version is explicit so an upgrade can be reviewed and tested.
