# Ratios, proportions, rates and logarithms

**Foundation domain:** Mathematics for spatial science  
**Subject ID:** SM-FND-001  
**Module:** 03  
**Status:** Initial public foundation; further technical review and expansion required

## 1. Why these ideas matter

Spatial work repeatedly compares quantities that differ in scale, unit, area, time or magnitude. Examples include converting map distances into ground distances, comparing raster cell areas, expressing population per square kilometre, describing environmental change, comparing sensor measurements and expressing signal ratios in decibels.

The arithmetic is often simple. The difficult part is choosing the correct numerator, denominator, units, reference quantity and interpretation.

A ratio compares quantities; a rate compares quantities with a specified denominator, often time or area; a logarithm expresses multiplicative relationships on an additive scale. They are related, but not interchangeable.

## 2. Ratios

A ratio compares two quantities by division. For non-zero b:

\[
a:b=\frac{a}{b}.
\]

The quantities must be identified before the ratio is interpreted. They may be counts, lengths, areas, masses or other compatible quantities. If the numerator and denominator have different dimensions, the result retains a unit.

### 2.1 Equivalent ratios

Multiplying or dividing both terms of a ratio by the same non-zero number preserves the ratio:

\[
\frac{2}{5}=\frac{4}{10}=\frac{40}{100}.
\]

This is useful when converting a ratio into a convenient form, but it does not change the underlying relationship.

### 2.2 Ratios with units

Suppose a field team records 18 km of surveyed road over 6 hours of productive observation time:

\[
\frac{18\;\mathrm{km}}{6\;\mathrm{h}}
=3\;\mathrm{km\,h^{-1}}.
\]

The result has dimensions of length per time. It is an average rate over the stated interval, not a guarantee that the team moved at a constant speed or that every kilometre had equal difficulty.

### 2.3 Ratios are directional

The ratio of A to B is not generally the same as the ratio of B to A:

\[
\frac{A}{B}\ne\frac{B}{A}.
\]

Always state what is being compared and in which order.

## 3. Proportions and percentages

A proportion expresses a part relative to a defined whole:

\[
p=\frac{\text{part}}{\text{whole}}.
\]

When the part is included in the whole and both are counted on the same basis, the proportion lies between 0 and 1. A percentage is the proportion multiplied by 100:

\[
P=100p\%.
\]

### 3.1 Worked example: land-cover composition

Suppose a mapped study area contains 240 km² of woodland within a total mapped area of 800 km².

\[
p=\frac{240}{800}=0.30
\]

\[
P=0.30\times100=30\%.
\]

Woodland occupies 30% of the stated mapped area, under the classification and area-measurement method used. This does not establish that the classification is correct, that the map boundary is complete, or that the area calculation is suitable for a legal or cadastral purpose.

### 3.2 Denominators matter

Consider two districts:

| District | Woodland | Total area | Woodland share |
|---|---:|---:|---:|
| A | 120 km² | 400 km² | 30% |
| B | 180 km² | 900 km² | 20% |

District B has more woodland area, but District A has the larger woodland proportion. The two measures answer different questions.

In spatial reporting, specify whether the denominator is total administrative area, land area excluding water, valid classified pixels, sampled observations, population within a boundary or another explicitly defined population or area.

### 3.3 Percentage change is not percentage-point change

If a proportion rises from 20% to 25%, the change is 5 percentage points, because 25 − 20 = 5. The relative increase is 25%, because (25 − 20) / 20 = 0.25.

For a quantity changing from an initial value x₀ ≠ 0 to a final value x₁, relative change is:

\[
r=\frac{x_1-x_0}{x_0}.
\]

The percentage change is 100r%. The sign indicates increase or decrease under the chosen convention.

## 4. Proportional relationships

Two quantities are directly proportional when one is a constant multiple of the other:

\[
y=kx,
\]

where k is a constant of proportionality.

If x doubles, y doubles, provided the model and its conditions remain valid.

### Example: map scale

A representative fraction (RF) of 1:50,000 means that one unit on the map represents 50,000 of the same units on the ground, under the map's stated scale model.

\[
\text{Ground distance}
=\text{Map distance}\times50{,}000.
\]

A map distance of 4 cm represents:

\[
4\;\mathrm{cm}\times50{,}000
=200{,}000\;\mathrm{cm}
=2{,}000\;\mathrm{m}
=2\;\mathrm{km}.
\]

Conversely, a ground distance of 1 km is represented by:

\[
\frac{1{,}000\;\mathrm{m}}{50{,}000}
=0.02\;\mathrm{m}
=2\;\mathrm{cm}.
\]

The scale denominator is dimensionless because the numerator and denominator use the same unit before conversion.

**Important limitation:** a nominal or representative map scale does not establish positional accuracy. Map projection, local scale variation, source accuracy, generalisation, reproduction and display zoom all affect how a map should be interpreted. A web map viewed at an arbitrary zoom level does not have one fixed physical scale on the screen.

## 5. Inverse proportionality

Two quantities are inversely proportional when their product is constant:

\[
y=\frac{k}{x},\qquad x\ne0.
\]

If x doubles, y halves, all else being equal.

### Example: pixel count and cell area

For a raster with square cells of side length s, the area of one cell is:

\[
A_c=s^2.
\]

For a fixed total area Aₜ, the approximate number of cells required is:

\[
N=\frac{A_T}{s^2}.
\]

If cell width is halved, each cell has one quarter of the area, so approximately four times as many cells are required to cover the same area.

This relationship assumes square cells, a consistent grid and a suitable planar area calculation. For non-square cells, use \(A_c=\Delta x\,\Delta y\). For geographic coordinates in angular units, degree differences cannot be treated as constant ground lengths or areas without an appropriate geodetic or projection treatment.

## 6. Rates

A rate expresses how one quantity changes or accumulates relative to another quantity. The denominator determines the meaning and units.

\[
\text{Average rate}
=\frac{\text{change in quantity}}{\text{change in reference quantity}}.
\]

The reference quantity may be time, area, distance, population or another meaningful exposure.

### 6.1 Temporal rates

If a measured quantity changes from x₀ at time t₀ to x₁ at time t₁, the average rate of change is:

\[
\bar r=\frac{x_1-x_0}{t_1-t_0}.
\]

For a shoreline-position estimate changing by 12 m over 4 years:

\[
\bar r=\frac{12\;\mathrm{m}}{4\;\mathrm{yr}}
=3\;\mathrm{m\,yr^{-1}}.
\]

This is an average over the interval. It does not prove that the shoreline moved at a constant rate or explain the physical causes. The result also depends on how the shoreline indicator, reference frame, dates, tide or water level, uncertainty and comparison method were defined.

### 6.2 Spatial density

A density is a quantity divided by an area or volume:

\[
D=\frac{Q}{A}.
\]

If a hypothetical district has 96,000 residents over 120 km²:

\[
D=\frac{96{,}000\;\text{people}}{120\;\mathrm{km^2}}
=800\;\text{people}\,\mathrm{km^{-2}}.
\]

This is an area-wide average. It does not mean residents are distributed uniformly. Boundary choices, population reference dates, land-area definitions and treatment of uninhabited land can change the result.

### 6.3 Rates of observation and operational productivity

A field team that captures 150 asset records in 5 hours has a mean capture rate of:

\[
30\;\text{records}\,\mathrm{h^{-1}}.
\]

This rate can help with planning, but it is not a universal productivity benchmark. Travel, access, feature complexity, revisit requirements, quality control and breaks affect the denominator and the meaning of the rate.

### 6.4 Units reveal the rate's meaning

Examples include metres per second (speed), square kilometres per year \(area-change rate\), people per square kilometre (population density), observations per site (sampling intensity) and bytes per second (data throughput).

If the units do not match the question, the rate is probably not the one needed.

## 7. Growth and compounding

A constant absolute increment produces a linear model:

\[
x_n=x_0+nd,
\]

where d is the increment per period.

A constant proportional growth rate produces a compound model:

\[
x_n=x_0(1+g)^n,
\]

where g is the growth rate per period expressed as a decimal and n is the number of periods.

### Worked example

Suppose a hypothetical mapped asset inventory starts with 1,000 records and grows by 5% per year under a constant proportional-growth assumption:

\[
x_3=1{,}000(1.05)^3\approx1{,}157.63.
\]

A real inventory contains discrete records, so an operational forecast needs an explicit rule for rounding, additions, removals, duplicate resolution and changing coverage. This is a model illustration, not evidence that an inventory will grow at a constant rate.

For a continuously compounded model, the corresponding exponential form is:

\[
x(t)=x_0e^{kt},
\]

where k is a continuous proportional growth parameter per unit time. The discrete and continuous models are related but are not identical for a finite period.

## 8. Logarithms

A logarithm answers the question: to what power must a base be raised to obtain a given positive number?

\[
\log_b(x)=y\quad\Longleftrightarrow\quad b^y=x,
\]

where \(b>0\), \(b\neq1\) and \(x>0\).

Common bases include base 10 (common logarithm), base e (natural logarithm, ln) and base 2 (binary logarithm).

### 8.1 Logarithm rules

For positive x and y and a valid base b:

\[
\log_b(xy)=\log_b(x)+\log_b(y)
\]

\[
\log_b\left(\frac{x}{y}\right)=\log_b(x)-\log_b(y)
\]

\[
\log_b(x^a)=a\log_b(x)
\]

\[
\log_b(1)=0,\qquad \log_b(b)=1.
\]

These identities turn multiplication into addition and powers into multiplication. They are useful for analysing multiplicative processes and quantities spanning several orders of magnitude.

A logarithm is defined only for a positive argument in ordinary real arithmetic. In physical interpretation, its argument should be dimensionless. If a measured quantity has units, form a ratio against a reference quantity with the same units before taking its logarithm.

### 8.2 Logarithmic scales and decibels

The decibel expresses a logarithmic ratio. For a power ratio:

\[
L_{\mathrm{dB}}=10\log_{10}\left(\frac{P_2}{P_1}\right).
\]

For an amplitude ratio, when power is proportional to the square of the amplitude under the relevant conditions:

\[
L_{\mathrm{dB}}=20\log_{10}\left(\frac{A_2}{A_1}\right).
\]

The factor is 10 for a power ratio and 20 for an amplitude ratio under that square-law relationship. These formulas must not be mixed without checking what the measured quantity represents.

For a power ratio of 100:

\[
10\log_{10}(100)=20\;\mathrm{dB}.
\]

For an amplitude ratio of 10 under the stated square-law condition:

\[
20\log_{10}(10)=20\;\mathrm{dB}.
\]

The decibel value describes a ratio, not an absolute power or amplitude unless a reference level is specified. This distinction matters in acoustics, radar, communications and sensor systems.

### 8.3 Logarithmic transformations in spatial analysis

A logarithmic transformation can make a highly skewed positive variable easier to visualise or model. It may reduce the influence of very large values and turn some multiplicative relationships into additive ones.

For a model of the form \(y=ax^b\), with positive \(x\) and \(y\):

\[
\ln(y)=\ln(a)+b\ln(x).
\]

This is a mathematical transformation, not a guarantee that the transformed relationship is statistically appropriate. Zeros, negative values, measurement error, sampling design and interpretation on the original scale require attention. Adding an arbitrary constant to make zeros loggable changes the model and must be justified.

In remote sensing and geospatial imaging, logarithmic displays may be used to visualise values with a wide dynamic range. A display stretch is not automatically a physical calibration or a valid substitute for radiometric processing.

## 9. Choosing the right measure

Before calculating a ratio, proportion, rate or logarithm, ask:

1. What exact quantities are being compared?
2. What is the numerator and what is the denominator?
3. Are the units compatible, and what units should the result have?
4. What is the reference population, area, time interval or baseline?
5. Is the relationship direct, inverse, additive, multiplicative or logarithmic?
6. Are the inputs measured, estimated, modelled or stipulated?
7. What assumptions make the calculation meaningful?
8. What important variation is hidden by the average or transformation?

A correct calculation can still answer the wrong question if its denominator or reference is poorly chosen.

## 10. Common errors

- Reporting a percentage without defining the whole or denominator.
- Confusing percentage change with percentage-point change.
- Comparing absolute quantities when the question concerns relative proportions, or vice versa.
- Treating an average spatial density as a uniform local distribution.
- Calling a ratio a rate without stating the reference quantity and units.
- Treating a map scale as positional accuracy.
- Assuming halving cell width merely doubles raster size; for square cells over fixed area, the cell count is approximately quadrupled.
- Applying logarithms to zero or negative values without a justified model.
- Taking the logarithm of a dimensional quantity without defining a reference ratio.
- Using the decibel power formula for an amplitude ratio, or the reverse.
- Interpreting a fitted growth rate as a causal explanation or guaranteed forecast.
- Ignoring uncertainty, boundary definitions, time alignment or changes in data coverage.

## 11. Exercises

Use explicit units and show the reasoning. State assumptions where the question does not provide enough information.

### Exercise 1 — Map scale

A paper map has a representative fraction of 1:25,000. A road segment measures 7.2 cm on the map.

1. Calculate the represented ground distance in metres and kilometres.
2. Calculate the map distance representing 850 m on the ground.
3. Explain why these calculations do not establish the road's positional accuracy.

### Exercise 2 — Proportions and percentage points

A land-cover assessment reports woodland increasing from 18% to 23% of the valid mapped area.

1. Calculate the change in percentage points.
2. Calculate the relative percentage increase in woodland share.
3. Explain why the valid mapped area and classification method should be checked before interpreting the change.

### Exercise 3 — Density and denominator choice

Two hypothetical wards have the following data:

- Ward A: 42,000 residents; 35 km² total area; 28 km² land area.
- Ward B: 55,000 residents; 50 km² total area; 40 km² land area.

1. Calculate population density using total area.
2. Calculate population density using land area.
3. Explain why the two definitions may produce different comparisons.

### Exercise 4 — Raster resolution

A square-cell raster covers approximately 900 km² using 30 m cells.

1. Calculate the area of one cell in square metres and hectares.
2. Estimate the number of cells needed to cover the area, ignoring boundary effects.
3. Estimate the cell count if cell width is reduced to 15 m.
4. Explain why actual raster dimensions may differ from the simple area ratio.

### Exercise 5 — Change rate

A hypothetical mapped wetland area changes from 84 km² to 72 km² over 6 years.

1. Calculate the average absolute rate of change in km² per year.
2. Calculate the relative change over the full interval.
3. Explain why the average rate does not establish that the loss occurred uniformly each year or identify its cause.

### Exercise 6 — Logarithms

1. Evaluate log₁₀\(1,000\).
2. Evaluate log₂(64).
3. Calculate the decibel level for a power ratio of 10.
4. Calculate the decibel level for an amplitude ratio of 10 when power is proportional to amplitude squared.
5. Explain why a logarithm should be applied to a ratio against a reference quantity rather than to a dimensional measurement by itself.

### Exercise 7 — Model selection

A team wants to forecast the number of field assets recorded in a database over the next five years.

1. Describe a situation in which a constant-addition model could be reasonable.
2. Describe a situation in which a constant-proportional-growth model could be reasonable.
3. Identify at least four real-world factors that could make either model unreliable.
4. Explain what evidence would be needed before treating either model as a forecast rather than an illustration.

## 12. Answers and checks

1. **Map scale:** 7.2 cm × 25,000 = 180,000 cm = 1,800 m = 1.8 km. For 850 m, 850 m ÷ 25,000 = 0.034 m = 3.4 cm. Scale alone says nothing about source or positional accuracy.
2. **Proportions:** change = 5 percentage points. Relative increase = (23 − 18) ÷ 18 × 100 ≈ 27.8%. Check whether the valid-area denominator and class definitions remained comparable.
3. **Density:** Ward A is 1,200 people/km² by total area and 1,500 people/km² by land area. Ward B is 1,100 people/km² by total area and 1,375 people/km² by land area. The denominator changes the meaning; use the definition that matches the question and disclose it.
4. **Raster:** 30 m × 30 m = 900 m² = 0.09 ha. 900 km² = 900,000,000 m², giving approximately 1,000,000 cells. At 15 m, cell area is 225 m² and the estimate is approximately 4,000,000 cells. Grid alignment, shape, masking and boundary effects change actual counts.
5. **Change rate:** (72 − 84) ÷ 6 = −2 km²/year. Relative change = (72 − 84) ÷ 84 × 100 ≈ −14.3%. This is an interval average, not a trajectory or causal analysis.
6. **Logarithms:** log₁₀\(1,000\) = 3; log₂(64) = 6; power ratio 10 gives 10 dB; amplitude ratio 10 under the square-law condition gives 20 dB. The reference ratio makes the logarithm's argument dimensionless and interpretable.
7. **Model selection:** constant addition may suit a stable annual survey programme with similar coverage; proportional growth may suit an expanding system where new records arise in proportion to the existing inventory. Coverage changes, funding, duplicate removal, asset retirement, policy, population change, data quality and access can invalidate either assumption. Historical observations, a defined process, uncertainty analysis and out-of-sample evaluation are needed for a defensible forecast.

## 13. Connections across Spatial Methods

- **Spatial algorithms:** density estimation, map-scale operations, raster resampling, change metrics, image transforms and normalisation.
- **Spatial data collection:** sampling intensity, survey productivity, sensor dynamic range and temporal observation rates.
- **Spatial recipes:** area and population summaries, resolution selection, change reporting, monitoring and data-volume planning.
- **Theoretical foundations:** measurement uncertainty \(SM-FND-011\), geodesy and reference systems \(SM-FND-008\), calculus and differential methods \(SM-FND-003\), probability and statistical inference \(SM-FND-004\), remote sensing physics \(SM-FND-012\) and signal processing \(SM-FND-014\).

Related subjects are not substitutes for one another. Map scale, raster cell size, positional accuracy, measurement resolution and uncertainty describe different properties.

## 14. Scope and limitations

This module establishes introductory mathematical relationships. It does not provide a complete treatment of cartographic scale variation, geodesic distance and area, statistical rate estimation, time-series modelling, radiometric calibration, logarithmic signal processing or uncertainty propagation. Those subjects require their own models, assumptions and domain-specific methods.

Worked values are hypothetical teaching examples, not observations from a field survey, official population dataset or operational monitoring programme.

## 15. Further development

The next module develops equations, inequalities and mathematical reasoning: rearranging relationships, solving constraints, interpreting solution sets and checking whether a mathematical solution is meaningful in a spatial context.


## References and further reading

The explanations and worked spatial examples are original Spatial Methods teaching material. The following sources support the mathematical relationships and selected GIS applications.

1. **OpenStax.** *Algebra and Trigonometry 2e*. [Chapter 4: Linear Functions](https://openstax.org/books/algebra-and-trigonometry-2e/pages/4-introduction-to-linear-functions) and [Chapter 6: Exponential and Logarithmic Functions](https://openstax.org/books/algebra-and-trigonometry-2e/pages/6-introduction-to-exponential-and-logarithmic-functions). Used for proportional relationships, rates, exponential growth and logarithm properties.
2. **Esri.** [Explore imagery — Spatial resolution](https://learn.arcgis.com/en/projects/explore-imagery-spatial-resolution/). Used for the applied discussion of raster cell size, represented detail and resolution trade-offs. This is a software-vendor tutorial, not a universal resolution standard.
3. **BIPM.** (2026). *The International System of Units (SI Brochure)*, 9th edition, version 4.01. [Official publication]\(https://www.bipm.org/en/si-brochure-9\). Used for unit expression and dimensional consistency when defining rates and densities.

**Limitations:** A mathematical relationship such as proportionality or exponential growth is not evidence that a particular spatial process follows that model. Model choice requires domain knowledge and appropriate data.
