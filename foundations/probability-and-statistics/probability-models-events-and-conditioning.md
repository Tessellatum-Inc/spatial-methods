# Probability models, events and conditioning

**Subject identity:** `SM-FND-004` — Probability and statistical inference  
**Module:** 01  
**Status:** Initial researched teaching resource; independent technical review and learner testing pending.

## 1. Why probability belongs in spatial science

Spatial work repeatedly asks questions whose answers are uncertain:

- What is the chance that a randomly selected building lies inside a flood-exposure zone?
- Given that a classifier marks a pixel as tree cover, how likely is it to be tree cover on the ground?
- How likely is a survey observation to exceed a specified error threshold under a stated measurement model?
- Given an observed pattern of events, how much evidence is there for clustering rather than a spatially uniform process?

These questions are not interchangeable. Each requires a clearly defined event, a population or process, an observation unit and a probability model. A map of probabilities is not simply a map with numbers between zero and one: each value needs a defined interpretation.

Probability is a mathematical model for uncertainty. It can be informed by long-run frequencies, physical mechanisms, expert judgement, prior studies or a statistical model. The numerical value alone does not tell us which basis was used.

## 2. Outcomes, sample spaces and events

A **random experiment** is a process whose outcome is not known with certainty before it is observed. Its **sample space**, written \(\Omega\), is the set of possible outcomes. An **event** is a subset of that sample space.

For a randomly selected mapped cell, one possible sample space might be:

\[
\Omega=\{\text{exposed},\;\text{not exposed}\}.
\]

The event \(A=\{\text{exposed}\}\) is the subset containing the exposed outcome. For a more detailed classification, the sample space might contain several mutually exclusive land-cover classes. The sample space must be defined at the level of the question: a pixel, parcel, road segment, survey station, person or observation are different units.

A probability assignment \(P\) maps events to values between zero and one. The standard probability axioms are:

1. \(P(A)\geq 0\) for every event \(A\);
2. \(P(\Omega)=1\);
3. for pairwise disjoint events \(A_1,A_2,\ldots\), the probability of their union is the sum of their probabilities.

Useful consequences include:

\[
P(A^c)=1-P(A)
\]

and

\[
P(A\cup B)=P(A)+P(B)-P(A\cap B).
\]

Here \(A^c\) is the complement of \(A\), \(A\cup B\) means that at least one of the events occurs, and \(A\cap B\) means both occur.

The shortcut \(P(A\cup B)=P(A)+P(B)\) is valid only when the events are disjoint. If overlap is possible, subtract the intersection once.

### Probability is not automatically a count ratio

For a finite set of equally likely outcomes, a probability can be calculated as the number of favourable outcomes divided by the total number of outcomes. Equal likelihood is an assumption, not a universal property of spatial data.

A randomly selected parcel gives each parcel equal selection chance if the design is uniform over parcels. It does not give each square metre equal selection chance when parcels differ in area. A uniformly selected point over a region, a uniformly selected raster cell, and a uniformly selected address describe different sampling mechanisms. The observation unit and selection design determine what the probability refers to.

## 3. Marginal, joint and conditional probability

The **marginal probability** \(P(A)\) describes the probability of event \(A\) without conditioning on another event.

The **joint probability** \(P(A\cap B)\) describes the probability that both \(A\) and \(B\) occur.

The **conditional probability** of \(A\) given that \(B\) has occurred is:

\[
P(A\mid B)=\frac{P(A\cap B)}{P(B)},\qquad P(B)>0.
\]

Conditioning changes the reference population or information set. It is not a cosmetic addition to the notation. The denominator is the probability of the condition, \(B\), not the probability of the event being investigated.

The multiplication rule follows directly:

\[
P(A\cap B)=P(A\mid B)P(B).
\]

A two-way table is often the clearest way to keep the denominator straight. Row percentages and column percentages answer different conditional questions; always identify which group forms the denominator.

## 4. Independence is not the same as disjointness

Events \(A\) and \(B\) are independent when knowing that one occurred does not change the probability of the other. For events with nonzero probabilities, equivalent statements are:

\[
P(A\mid B)=P(A)
\]

and

\[
P(A\cap B)=P(A)P(B).
\]

**Disjoint events** cannot occur together: \(P(A\cap B)=0\). If both events have positive probability, disjoint events are dependent, because observing one rules out the other.

This distinction matters in spatial analysis. Two map layers may overlap spatially, and two environmental conditions may co-occur. It is not valid to multiply their probabilities merely because they are represented in separate datasets. Independence requires a substantive or statistical justification.

Spatial observations often exhibit dependence because nearby locations share environmental conditions, infrastructure, acquisition conditions or latent processes. Treating adjacent cells as independent replicates can create false precision. The formal theory of spatial dependence and random fields belongs in SM-FND-005, but the warning is essential here.

## 5. Total probability and Bayes' theorem

Suppose \(A_1,\ldots,A_k\) form a partition of the sample space: they are mutually exclusive and collectively exhaustive. For an event \(B\),

\[
P(B)=\sum_{i=1}^{k}P(B\mid A_i)P(A_i).
\]

This is the **law of total probability**. It calculates the overall probability of \(B\) by adding the contributions from every possible partition group.

Bayes' theorem reverses the conditioning:

\[
P(A_j\mid B)=
\frac{P(B\mid A_j)P(A_j)}
{\sum_{i=1}^{k}P(B\mid A_i)P(A_i)}.
\]

The prior probability \(P(A_j)\) is updated using how likely the observed evidence \(B\) would be under each possible state. The denominator normalises the contributions so the posterior probabilities sum to one.

Bayes' theorem does not make weak evidence strong, remove model misspecification or guarantee that a prior is appropriate. Its result depends on the prior probabilities, the likelihood model and the definition of the evidence.

## 6. Worked spatial example: a screening layer

Consider a **hypothetical synthetic** screening model for 10,000 equal-area map cells in a study region. The purpose is to illustrate how a rare condition affects the interpretation of a positive screening result. These values are assumptions for teaching; they are not observed data or performance claims about a real flood model.

Assume:

- 4% of cells are truly exposed under the reference definition;
- the screening layer flags 90% of exposed cells (sensitivity);
- it correctly leaves 92% of unexposed cells unflagged (specificity).

The assumed prevalence is 0.04. The false-positive rate is \(1-0.92=0.08\).

| Reference state | Flagged positive | Flagged negative | Total |
|---|---:|---:|---:|
| Exposed | 360 | 40 | 400 |
| Not exposed | 768 | 8,832 | 9,600 |
| Total | 1,128 | 8,872 | 10,000 |

The probability of a positive flag is:

\[
P(+)=P(+\mid E)P(E)+P(+\mid E^c)P(E^c)
\]

\[
=(0.90)(0.04)+(0.08)(0.96)=0.1128.
\]

The probability that a cell is exposed given that it was flagged positive is:

\[
P(E\mid +)=\frac{P(+\mid E)P(E)}{P(+)}
=\frac{0.90\times0.04}{0.1128}
\approx0.3191.
\]

So the positive predictive value is about **31.9%** under these assumptions. The screen detects most exposed cells, but the relatively low prevalence means false positives outnumber true positives.

This is not a contradiction. Sensitivity asks how often the screen is positive among exposed cells; positive predictive value asks how often exposure is present among positive flags. They condition on different events.

### What changes when prevalence changes?

Keep sensitivity and specificity fixed, but change prevalence. The positive predictive value changes because the prior probability changes.

| Assumed prevalence | Positive predictive value |
|---:|---:|
| 1% | 10.2% |
| 4% | 31.9% |
| 10% | 56.3% |
| 25% | 78.9% |

A screening layer calibrated in one region may not retain the same predictive value in another region if prevalence, land-cover composition, sensor conditions or reference definitions change. A map threshold cannot be interpreted independently of its target population and validation design.

### Spatial-unit caution

The calculation treats 10,000 equal-area cells as the units and uses a common assumed prevalence. If cells have unequal area, a cell-level probability and an area-weighted probability are not the same. If the goal is the probability that a randomly selected building is exposed, the relevant population is buildings, not cells. If cells are spatially dependent, the table may still describe the stated finite set, but ordinary independent-binomial uncertainty calculations would need additional justification.

## 7. Common errors and interpretation checks

1. **Reversing a conditional probability:** \(P(A\mid B)\) is generally not \(P(B\mid A)\).
2. **Ignoring prevalence:** high sensitivity does not guarantee high positive predictive value.
3. **Confusing independence with disjointness:** disjoint positive-probability events are dependent.
4. **Multiplying probabilities without justification:** the product rule for independent events requires independence; otherwise use conditional probability.
5. **Treating every cell as equally likely:** the sampling unit and selection mechanism determine the probability.
6. **Treating neighbouring cells as independent replicates:** spatial dependence can invalidate standard uncertainty calculations.
7. **Confusing association with causation:** conditional probabilities describe relationships under a model; they do not by themselves identify causal effects.
8. **Treating assumed model values as measured facts:** label assumptions, estimated quantities and empirical validation separately.

Before interpreting a probability, ask:

- What is the random unit or process?
- What are the possible outcomes and event definitions?
- What population, region and time period does the model refer to?
- What information is being conditioned upon?
- How were the prior and conditional probabilities obtained?
- Does the sampling design or spatial dependence challenge the model?
- Is the result a probability for a cell, parcel, person, event, area or future observation?

## 8. Short exercises

### Exercise A — overlap and union

Suppose \(P(A)=0.30\), \(P(B)=0.40\), and \(P(A\cap B)=0.12\). Calculate \(P(A\cup B)\). Are the events independent?

**Worked guidance:** \(P(A\cup B)=0.30+0.40-0.12=0.58\). The product \(P(A)P(B)=0.12\), which equals the supplied intersection, so the events satisfy the independence condition.

### Exercise B — conditioning direction

In a reference sample, 20% of cells are exposed. A screening layer flags 80% of exposed cells. What is \(P(+\mid E)\)? Is that enough information to calculate \(P(E\mid +)\)?

**Worked guidance:** \(P(+\mid E)=0.80\). No. The false-positive rate among unexposed cells is also needed to calculate the total positive probability and hence the reverse conditional probability.

### Exercise C — Bayes update

A region has an assumed exposure prevalence of 5%. A screening layer has sensitivity 90% and specificity 95%. Calculate the probability of exposure given a positive flag.

**Worked guidance:**

\[
P(E\mid +)=\frac{0.90(0.05)}
{0.90(0.05)+0.05(0.95)}
=\frac{0.045}{0.0925}
\approx0.4865.
\]

The posterior probability is approximately 48.6%. The result depends on the assumed prevalence and screening performance applying to the target region and reference definition.

## 9. Connections and next steps

- Continue to [random variables and distributions](README.md), where events become numerical quantities with probability distributions.
- Connect covariance and random vectors to [linear algebra and matrix methods](../linear-algebra/README.md).
- Connect spatial dependence to the future SM-FND-005 domain and existing [spatial cross-validation](../../methods/spatial-cross-validation.md).
- Connect uncertainty interpretation to [measurement science](../measurement-science/measurement-principles-and-field-verification.md).
- Connect screening-layer validation to the [photogrammetric checkpoint QA companion](../../implementations/python/photogrammetry-odm/README.md), while keeping classification validation and coordinate checkpoint assessment distinct.

## References

- Diez, D. M., Çetinkaya-Rundel, M., and Barr, C. D. (2019). *OpenIntro Statistics*, 4th ed., Chapter 3, especially Sections 3.1–3.2. [OpenIntro book and companion resources](https://openintro.org/book/os/); [open PDF copy of the fourth edition](https://people.hsc.edu/faculty-staff/blins/books/openintrostats4e.pdf). The book is released under CC BY-SA 3.0 according to [OpenIntro's licence page](https://openintro.org/license/). This module is an original synthesis with original synthetic spatial examples; it does not reproduce the textbook's exercises or figures.

## Evidence and review boundary

The cited textbook's probability chapter was inspected for event definitions, probability rules, conditional probability, independence, tree-diagram reasoning and Bayes' theorem. The synthetic spatial screening example and the pedagogical interpretation are original to this module. No real classification data, flood map, regional prevalence estimate or operational screening system was evaluated. The source supports introductory probability concepts; it does not validate the illustrative model assumptions or any spatial application.
