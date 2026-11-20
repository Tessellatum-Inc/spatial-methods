# Mathematics for spatial science

Mathematics is the language used to describe quantities, relationships, change, structure and uncertainty. Spatial science uses it to represent locations, measure distances and areas, describe surfaces and networks, transform coordinates, analyse patterns, model processes and make decisions.

This collection builds the mathematical ideas needed across geoinformatics. It is not intended to be a generic school-mathematics textbook: each topic is connected to spatial questions, data and methods.

**Subject identity:** `SM-FND-001` — Mathematics for spatial science.

## Learning architecture

The sequence below moves from mathematical language toward structures and methods used repeatedly in spatial work. It is a suggested progression; readers may enter through a relevant application and follow its prerequisites.

| Module | Topic | Main spatial connections |
|---|---|---|
| 01 | [Mathematical language, quantities and spatial models](mathematical-language-quantities-and-spatial-models.md) | Variables, units, functions, coordinate pairs, scale, area, density and modelling |
| 02 | [Number systems, arithmetic and numerical representation](number-systems-arithmetic-and-numerical-representation.md) | Measurement values, precision, rounding, significant figures and numerical data |
| 03 | [Ratios, proportions, rates and logarithms](ratios-proportions-rates-and-logarithms.md) | Map scale, resolution, density, rates of change, decibels and spectral transforms |
| 04 | [Equations, inequalities and mathematical reasoning](equations-inequalities-and-mathematical-reasoning.md) | Thresholds, constraints, classification rules and solving spatial problems |
| 05 | [Functions and relationships](functions-and-relationships.md) | Transformations, distance functions, terrain surfaces and spatial models |
| 06 | [Coordinate geometry and reference frames](coordinate-geometry-and-reference-frames.md) | Cartesian coordinates, lines, planes, coordinate transformations and geometric interpretation |
| 07 | [Vectors and vector operations](vectors-and-vector-operations.md) | Displacement, direction, velocity, gradients and 3D geometry |
| 08 | [Sequences, series and approximation](sequences-series-and-approximation.md) | Iterative algorithms, discretisation and convergence |
| 09 | [Mathematical modelling and dimensional analysis](mathematical-modelling-and-dimensional-analysis.md) | Model construction, assumptions, units, scaling, sensitivity and plausibility checks |
| 10 | [Trigonometry for spatial science](trigonometry-for-spatial-science.md) | Angles, radians, trigonometric functions, bearings, azimuths, slopes and planar geometry |\n| 11 | Introductory discrete mathematics and logic *(planned)* | Sets, relations, graphs, Boolean operations and spatial predicates |

## Coverage audit

The eight existing modules have received an initial coverage audit. The [mathematics gap register](gap-register.md) records missing concepts, priorities, dependencies and the recommended treatment for each gap. It deliberately distinguishes material that belongs in this domain from topics that should be developed in specialist foundations. This is an editorial planning review, not independent technical certification.

## What this domain covers—and what it does not

This domain establishes the common mathematical language. More specialised theory has its own home:

- Matrix algebra, vector spaces, eigenvalues and decompositions belong in [Linear algebra and matrix methods](../README.md#subject-map) under `SM-FND-002`.
- Derivatives, integrals, gradients, differential equations and continuous change belong in `SM-FND-003`.
- Probability and statistical inference belong in `SM-FND-004`; spatial stochastic processes belong in `SM-FND-005`.
- Geometric structures and topology receive deeper treatment under `SM-FND-006` and `SM-FND-007`.
- Floating-point error, conditioning and numerical stability belong in `SM-FND-016`.

A module may introduce a concept needed to understand a later subject, but it should link to the canonical deeper treatment rather than reproduce it.

## Competency goals

A learner completing this domain should be able to:

1. Translate a spatial question into defined quantities, variables and relationships.
2. Distinguish a number from the quantity, unit, reference and measurement process it represents.
3. Use ratios, rates, functions and coordinate relationships correctly.
4. Check equations and results using dimensions, units, limiting cases and physical interpretation.
5. Recognise when a mathematical representation is an approximation and state its assumptions.
6. Identify the mathematical prerequisites of a spatial algorithm or measurement method.

## Development and review standard

Each module should include, where relevant:

- clear definitions and consistent mathematical notation;
- inline mathematics using single dollar delimiters, for example `$x^2+y^2=r^2$`;
- display mathematics using double dollar delimiters on their own lines, for example `$$` on a line before and after the expression;
- units typeset upright with `\mathrm{}` and symbols defined;
- intuitive explanation followed by formal treatment;
- derivations or justification of important relationships;
- worked spatial examples with units;
- common errors and boundary cases;
- exercises that require interpretation, not only calculation;
- connections to algorithms, data collection, recipes and applications;
- relevant references for technical claims, linked to stable records in the source register;
- an explicit evidence/review state and scope limitations.

Do not mistake a long list of formulas for a foundation. The aim is to teach how to select, interpret and question a mathematical model.

## Current status

Modules 01–10 have initial public content and have received notation, source and initial coverage audits. Independent technical review and targeted expansion remain necessary. Module 11 remains planned, not yet written or reviewed. The gap register guides the next work; coverage will expand only when each module has meaningful explanatory content.
