# Mathematical language, quantities and spatial models

**Foundation domain:** Mathematics for spatial science  
**Subject ID:** `SM-FND-001`  
**Module:** 01  
**Status:** Initial public foundation; further technical review and expansion required

## 1. Why spatial science needs mathematical language

A spatial problem often begins as an ordinary question:

- How far apart are two locations?
- How much land is inside a boundary?
- How many people live within a service area?
- How steep is a section of terrain?
- How does the position of an object change over time?
- Which candidate site best satisfies a set of requirements?

To reason about these questions, we must decide what quantities matter, how they relate, how they will be represented and what assumptions make the representation useful.

Mathematics gives us a disciplined language for doing this. It lets us move between a real-world situation, a conceptual model, a symbolic expression, a numerical calculation and an interpretation.

The calculation is only one part of that chain. A mathematically correct answer to a poorly specified question can still be useless.

## 2. Quantities, values, units and references

A **quantity** is a property that can be expressed as a number and a reference. Examples include length, area, elapsed time, temperature, population count and elevation.

A **numerical value** is not the whole quantity. The statement `250` is incomplete if we do not know whether it means 250 metres, 250 square metres, 250 people or something else.

A useful spatial statement identifies at least:

- the quantity being described;
- its numerical value;
- its unit, where the quantity has a unit;
- the object, location, interval or population to which it applies;
- the relevant reference, epoch or conditions where these matter.

For example:

> The mapped road segment has a calculated planar length of 250 metres in the stated projected coordinate system.

This is more informative than “the road is 250 long”. It also avoids claiming that a planar GIS length is automatically the same as a ground distance.

### 2.1 Dimensions and units

A **dimension** describes the physical nature of a quantity. Length, time and mass are examples of base dimensions. Area has dimension length squared; speed has dimension length divided by time.

A **unit** is a defined magnitude used to express a quantity. Metre, second and kilogram are examples.

Dimensions help us check whether a mathematical expression is meaningful. Units help us communicate and calculate actual values.

For instance, if a vehicle travels 12 kilometres in 20 minutes, its average speed is:
$$
v = rac{d}{t}
  = rac{12 \mathrm{km}}{20 \mathrm{min}}
  = 0.6 \mathrm{km/min}
$$

Converting minutes to hours:
$$
0.6 \mathrm{km/min}\times60 \mathrm{min/h}
=36 \mathrm{km/h}
$$

The unit conversion is part of the calculation, not cosmetic formatting.

### 2.2 Coordinate values are not self-describing

A coordinate pair such as `(36.8, -1.3)` has no reliable spatial meaning without knowing its coordinate reference system, axis order, units and interpretation. It might be longitude/latitude in degrees, but that should not be guessed.

Likewise, `(250000, 9850000)` might be projected coordinates in metres, but the values alone do not identify the projection, datum, zone or coordinate epoch.

A coordinate is a numerical representation tied to a reference system. It is not simply “the location”.

This distinction matters whenever coordinates are transformed, compared, measured or combined from different sources. See the geodesy and reference-system foundations and the CRS transformation material for the deeper treatment.

## 3. Variables, parameters and observations

A **variable** is a symbol representing a quantity that can take different values within a model. We often use $x$, $y$, $t$, $d$ or $A$, but notation should be defined rather than assumed.

A **parameter** is a quantity treated as fixed within a particular model or calculation, even though it may be estimated or changed in another context.

An **observation** is a value obtained through an observing or measurement process. It may contain error and uncertainty; it is not automatically identical to the true value of the quantity.

Consider a simple model for travel distance:
$$
d = vt
$$

where:

- $d$ is distance travelled;
- $v$ is average speed over the interval;
- $t$ is elapsed time.

If $v=30\,\mathrm{km/h}$ and $t=0.5\,\mathrm{h}$, then $d=15\,\mathrm{km}$.

The equation is simple, but its use assumes that the average speed is meaningful for the interval and that distance is the intended quantity. It does not describe the route geometry, stops, acceleration or variation in speed.

## 4. Mathematical expressions and relationships

An **expression** combines numbers, variables and operations. For example, (2x+5).

An **equation** states that two expressions are equal. For example:
$$
2x+5=17
$$

Solving gives $x=6$.

A **formula** expresses a general relationship between quantities. For a rectangle:
$$
A = lw
$$

where $A$ is area, $l$ is length and $w$ is width.

A **model** is a mathematical representation of some aspect of a system or problem. A formula may form part of a model, but a model also requires definitions, assumptions, scope and an interpretation of its variables.

### 4.1 The same formula can answer different questions

For a rectangle with length $l=40\,\mathrm{m}$ and width $w=25\,\mathrm{m}$:
$$
A=lw=40\times25=1000 \mathrm{m^2}
$$

This computes the planar area of the rectangle under the chosen geometry.

It does not, by itself, establish:
- that the boundary represents a legally recognised parcel;
- that the dimensions were measured accurately;
- that the surface is level;
- that the area is a ground area rather than a grid or map-plane area;
- that the shape is actually rectangular.

The mathematical relationship is exact for an ideal rectangle. Its application to a real feature depends on how the feature and inputs are defined.

## 5. Functions: mapping inputs to outputs

A **function** assigns exactly one output to each input in its specified domain.

We write:
$$
y=f(x)
$$

Here, $x$ is the input, $f$ is the rule and $y$ is the output.

For example:
$$
f(x)=2x+3
$$

If $x=4$, then $f(4)=11$.

A spatial example is a simple planar distance from a fixed point $(x_0,y_0)$ to a point $(x,y)$:
$$
d(x,y)=\sqrt{(x-x_0)^2+(y-y_0)^2}
$$

For this expression to represent a Euclidean planar distance, the coordinates must be in a suitable common Cartesian plane with compatible linear units. Applying it directly to longitude and latitude in degrees does not produce a distance in metres.

A function's **domain** is the set of permitted inputs. Its **codomain** is the declared set of possible outputs. Its **range** is the set of outputs it actually attains.

Defining the domain is not a technical afterthought. A model may only be meaningful within a certain spatial extent, time period, value range or set of conditions.

## 6. Ratios, rates and scale

A **ratio** compares two quantities by division. The quantities must be expressed in compatible units if the ratio is to be dimensionless.

A **rate** compares quantities with different dimensions, such as distance per unit time or population per unit area.

A map scale of 1:50,000 means that one unit of map length represents 50,000 of the same units on the represented ground-distance basis, subject to the map projection and scale interpretation.

For example:
$$
2 \mathrm{cm}\times50{,}000
=100{,}000 \mathrm{cm}
=1{,}000 \mathrm{m}
=1 \mathrm{km}
$$

This is a scale relationship, not a guarantee that every map distance equals the corresponding ground distance everywhere. Projection scale distortion and the map's intended scale basis matter.

A density is another rate:
$$
ho=rac{N}{A}
$$

If 12,000 people are associated with an area of $3\,\mathrm{km}^2$, the average density is:
$$
ho=rac{12{,}000}{3}=4{,}000 \mathrm{people\,km^{-2}}
$$

The result depends on the population definition, the spatial boundary and the time to which the count applies. An average density does not imply that people are uniformly distributed.

## 7. Sets and spatial collections

A **set** is a collection of distinct objects. Sets are useful for describing groups of features, candidate locations, observations or cells.

If $A$ is the set of schools and (B) is the set of health facilities, then:

- ($A\cup B$) is the union: objects in either set;
- ($A\cap B$) is the intersection: objects in both sets;
- ($A\setminus B$) is the difference: objects in $A$ but not (B).

In a GIS, these ideas appear in selection, overlay, filtering and spatial queries. The mathematical set operation and a particular GIS operation are related, but real data operations also depend on geometry models, topology rules, precision and software behaviour.

A **subset** contains only elements of another set. If every feature in $A$ also belongs to (B), then ($A\subseteq B$).

Sets provide a language for defining what is included in an analysis. A spatial query is only as clear as its membership rules.

## 8. Discrete and continuous representations

Some spatial quantities are naturally treated as discrete: a count of buildings, a list of road segments or a finite set of sample locations.

Other quantities are modelled as continuous: elevation over a surface, temperature through space, or a position that can vary continuously.

The distinction is about the mathematical representation, not a claim that the real world is perfectly discrete or continuous.

A raster represents a spatial domain using a finite grid of cells. It can store samples or summaries of a continuous phenomenon, but the grid is a representation with a chosen cell size, alignment, extent and value interpretation.

A vector dataset represents features using points, lines and polygons or related structures. Its finite coordinates approximate or encode selected aspects of spatial objects. The geometry model and data specification determine what those coordinates mean.

A representation must not be confused with the phenomenon it represents.

## 9. Dimensional analysis and plausibility checks

Dimensional analysis checks whether the dimensions on both sides of a relationship are consistent.

For example:
$$
A=lw
$$

has dimensions:
$$
[L^2]=[L][L]
$$

which is consistent.

But the expression $A=l+w$ is dimensionally inconsistent if $A$ is area and $l,w$ are lengths.

Dimensional consistency is necessary for a physically meaningful equation, but it is not sufficient to prove that the equation is correct.

Useful checks include:

1. **Units:** Do the units match the intended output?
2. **Dimensions:** Are the physical dimensions consistent?
3. **Magnitude:** Is the result plausible for the context?
4. **Limiting cases:** Does the model behave sensibly when an input approaches zero or another meaningful limit?
5. **Reference:** Are the coordinates, time, datum or spatial boundary appropriate?
6. **Assumptions:** Are the conditions under which the model is valid satisfied?

### Example: area scaling

If both sides of a square are doubled, its perimeter doubles but its area becomes four times as large.

For side length $s$:
$$
$P=4s,\qquad A=s^2$
$$

After scaling by factor $k$:
$$
$P'=kP,\qquad A'=k^2A$
$$

This distinction matters when changing map scale, raster resolution, grid dimensions or the size of a study region.

## 10. From a real question to a mathematical model

A disciplined modelling sequence is:

1. **State the question.** What do we need to know or decide?
2. **Define the target quantity.** What exactly is to be estimated, calculated or compared?
3. **Set the spatial and temporal scope.** Where and when does the question apply?
4. **Identify inputs.** Which observations, data, parameters and assumptions are needed?
5. **Choose relationships.** What mathematical structure connects the inputs to the output?
6. **Check units and references.** Are quantities compatible and spatially aligned?
7. **Solve or compute.** Apply the mathematical procedure.
8. **Interpret.** Explain what the output means in the original problem.
9. **Evaluate limitations.** Identify uncertainty, omitted processes and conditions where the model may fail.

### Worked example: a simple service-area density

Suppose a hypothetical study area has 18,000 residents and an area of $4.5\,\mathrm{km}^2$.

The question is: what is the mean population density over the study area?

Define:

- $N=18{,}000$ residents, for a specified population reference date;
- $A=4.5\,\mathrm{km}^2$, for a defined study boundary;
- (ho=N/A), mean population density.

Then:
$$
ho=rac{18{,}000}{4.5}
=4{,}000 \mathrm{residents\,km^{-2}}
$$

Interpretation: the total population divided by the total area is 4,000 residents per square kilometre.

This does not mean every square kilometre contains 4,000 residents. It does not describe within-area variation, population distribution, daytime population, access to services or the effect of boundary choice. Those require additional data and models.

## 11. Common mathematical and spatial reasoning errors

| Error | Why it matters | Better practice |
|---|---|---|
| Treating a number as a complete quantity | Units, reference and meaning are missing | State quantity, unit, object and reference |
| Treating coordinates as self-describing | CRS, axis order and units may be unknown | Preserve and inspect coordinate reference metadata |
| Mixing degrees and metres | Arithmetic may be numerically possible but meaningless | Transform or use an appropriate geodetic method |
| Confusing a formula with a model | Assumptions and scope remain unstated | Document definitions, assumptions and validity |
| Assuming an average describes every location | Spatial variation is hidden | Inspect distributions and local patterns |
| Treating a raster cell as the real-world object | Resolution and cell semantics affect interpretation | State what each cell represents |
| Reporting excessive decimal places | Numerical formatting can imply unsupported precision | Match reporting precision to data and uncertainty |
| Checking arithmetic but not interpretation | A correct calculation may answer the wrong question | Translate the result back into the original context |

## 12. Exercises

### Exercise 1 — Quantity and unit

A dataset contains the value `125` for a field called `length`.

1. List at least four pieces of information needed before interpreting the value.
2. Give two different valid interpretations that would lead to different conclusions.
3. Explain why a field name alone is insufficient metadata.

### Exercise 2 — Map scale

A line measures 7.2 cm on a map at 1:25,000.

1. Calculate its represented length in metres and kilometres.
2. State two reasons why this may differ from a ground distance measured in the field.
3. Explain why the answer should not be reported with unjustified precision.

### Exercise 3 — Density and boundaries

Two wards have the following hypothetical data:

| Ward | Population | Area |
|---|---:|---:|
| A | 24,000 | 6 km² |
| B | 15,000 | 2.5 km² |

1. Calculate the mean population density for each ward.
2. Which ward has the higher mean density?
3. Explain why this does not establish which ward has greater congestion or worse access to services.
4. Name two boundary or population-definition issues that could affect comparison.

### Exercise 4 — Function domain

A simplified planar distance function is defined from a fixed point $(x_0,y_0)$.

1. Write the function.
2. State the assumptions needed for the output to be interpreted as a distance in metres.
3. Explain why longitude and latitude in degrees cannot be inserted and treated as metre coordinates.

### Exercise 5 — Model critique

A report states: “The service area has 5,000 people per square kilometre, therefore all residents are within walking distance of the facility.”

1. Identify the mathematical result that may have been calculated.
2. Explain why the conclusion does not follow.
3. Identify at least three additional spatial variables or analyses needed to evaluate walking access.

## 13. Connections to the rest of Spatial Methods

- **Linear algebra:** coordinate transformations, least-squares adjustment, raster operations and multivariable models.
- **Calculus:** terrain gradients, continuous surfaces, rates of change, flow and physical processes.
- **Probability and statistics:** measurement uncertainty, sampling, inference and spatial variation.
- **Geometry and topology:** distances, intersections, boundaries, connectivity and spatial relationships.
- **Geodesy:** coordinate reference systems, Earth geometry and physical reference frames.
- **Numerical analysis:** finite precision, stable computation and approximation.
- **Spatial algorithms:** computational procedures that operationalise mathematical relationships.
- **Spatial data collection:** measurement, sampling and observation that supply model inputs.
- **Spatial recipes:** repeatable workflows that connect a real question to data, methods and an interpretable result.

## 14. Summary

Mathematics for spatial science begins with disciplined definitions. Quantities need units and references; variables need meanings; functions need domains; equations need assumptions; and numerical outputs need interpretation.

The central habit is to move deliberately between the real-world question and its mathematical representation. Before asking whether a calculation is correct, ask whether it represents the right quantity, in the right reference, for the intended purpose.

## Further reading and related resources

- [Theoretical foundations collection](../README.md)
- [Master subject index](../../catalog/master-subject-index.md)
- [Measurement models and measurand definition](../measurement-science/measurement-models-and-measurand-definition.md)
- [Coordinate transformation and CRS axis order](../../algorithms/geodesy/crs-transformation.md)
- [Measurement science and survey adjustment learning path](../../learning-paths/measurement-science-and-survey-adjustment.md)

This module introduces mathematical language and modelling habits. It is not a substitute for the deeper treatment of linear algebra, calculus, statistics, geometry, geodesy or numerical analysis in their respective foundation domains.


## References and further reading

The explanations, spatial examples and exercises in this module are original Spatial Methods teaching material. These references support the mathematical language, quantity and coordinate-system concepts introduced here.

1. **Bureau International des Poids et Mesures (BIPM).** (2026). *The International System of Units (SI Brochure)*, 9th edition, version 4.01. [Official publication and current version](https://www.bipm.org/en/si-brochure-9). Relevant sections: 2.3.3–2.3.4 on dimensions and derived units; 5.4 on expressing quantity values and units. Primary international reference for SI quantities and units.
2. **OpenStax.** *Algebra and Trigonometry 2e*. [Chapter 2: Equations and Inequalities](https://openstax.org/books/algebra-and-trigonometry-2e/pages/2-introduction-to-equations-and-inequalities); [Chapter 3: Functions](https://openstax.org/books/algebra-and-trigonometry-2e/pages/3-introduction-to-functions); [Chapter 12: Analytic Geometry](https://openstax.org/books/algebra-and-trigonometry-2e/pages/12-introduction-to-analytic-geometry). Used for elementary algebraic language, functions and coordinate geometry.
3. **Esri.** [Coordinate systems, map projections, and transformations](https://doc.esri.com/en/arcgis-pro/latest/help/mapping/properties/coordinate-systems-and-projections.html). Used as applied GIS documentation for coordinate reference frames, geographic versus projected coordinates and projection distortion. It is product documentation, not a substitute for geodetic standards.

**Source register:** `SM-SRC-000021`, `SM-SRC-000022`, `SM-SRC-000024`.

**Limitations:** The sources above do not establish the legal or geodetic status of any particular national coordinate reference system. Coordinate examples in this module are illustrative and should not be treated as operational CRS definitions.
