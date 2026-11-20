# Introductory discrete mathematics and logic for spatial science

**Subject:** SM-FND-001 — Mathematics for spatial science  
**Module:** 11  
**Status:** Initial public teaching module; technical review remains necessary.

## Purpose

Spatial information is not only continuous geometry. Many spatial tasks operate on discrete objects, categories, conditions, memberships, links and decisions. A GIS query selects features satisfying conditions. A land-cover layer partitions a study area into classes. A topology model records which objects touch or contain others. A transport network is represented by vertices and edges. A data pipeline applies logical rules to decide which records pass validation.

Discrete mathematics supplies the language for these structures. This module introduces:

- sets and set operations;
- Cartesian products, ordered pairs and relations;
- functions as mappings;
- propositions, connectives, truth tables and quantifiers;
- Boolean expressions and spatial query conditions;
- basic proof, counterexample and mathematical induction;
- introductory graph vocabulary.

It is a foundation, not a complete course in discrete mathematics. Advanced graph theory, combinatorics, formal logic, database theory, algorithms and computational complexity belong in specialist foundations.

## 1. Discrete and continuous representations

A continuous model allows quantities to vary over a continuum, such as a terrain elevation surface represented as a function of location. A discrete model represents objects or states as distinct elements, such as individual buildings, road segments, raster cells, land-cover classes or sensor records.

The distinction is about representation and mathematical structure, not about whether the real world itself is continuous or discrete. A raster discretises space into cells; a vector dataset represents selected entities as features; a network represents selected connections. These are modelling and data-structure choices.

A spatial workflow often combines both:
- continuous coordinates describe where a feature is;
- discrete identifiers distinguish records;
- set operations select groups of features;
- logical predicates determine which records qualify;
- relations represent connections among features;
- algorithms operate over the resulting structures.

## 2. Sets: collections of distinct elements

A **set** is a collection of distinct elements. Order does not matter, and repeating an element does not create a new member.

For example, let the set of mapped road segments be:

$$
R=\{r_1,r_2,r_3,r_4\}
$$

Let the set of road segments intersecting a study boundary be:

$$
I=\{r_2,r_4\}
$$

Membership is written (r_2\in I); non-membership is written (r_1\notin I).

A set can be described by listing its elements or by a rule:

$$
I=\{r\in R\mid r\text{ intersects the study boundary}\}
$$

The vertical bar means “such that”. The rule must be precise enough to determine membership.

### Subsets and equality

A is a subset of B, written (A\subseteq B), if every element of A is also in B. Two sets are equal if they contain exactly the same elements:

$$
A=B\iff(A\subseteq B)\land(B\subseteq A)
$$

The empty set, written \(\varnothing\), has no elements. It is a subset of every set.

The **power set** \(\mathcal P(A)\) is the set of all subsets of A. If A has n elements, a finite set has (2^n) subsets. For example, the set \(\{a,b\}\) has four subsets: \(\varnothing\), \(\{a\}\), \(\{b\}\), and \(\{a,b\}\).

The **cardinality** \(|A|\) is the number of elements in a finite set. Do not confuse the number of features with their total length, area or population.

## 3. Set operations

For sets A and B within a declared universe U:

**Union** contains elements in A, B or both:

$$
A\cup B=\{x\mid x\in A\lor x\in B\}
$$

**Intersection** contains elements in both:

$$
A\cap B=\{x\mid x\in A\land x\in B\}
$$

**Difference** contains elements in A but not B:

$$
A\setminus B=\{x\mid x\in A\land x\notin B\}
$$

**Complement** contains elements in the universe U that are not in A:

$$
A^c=U\setminus A
$$

The universe matters. “All features” could mean all features in a layer, all features in a study area, or all features in a database. A complement without a declared universe is ambiguous.

### Worked example 1 — combine spatial selections

A city asset inventory contains a set U of 500 recorded assets. Let:
- A be assets within 100 m of a mapped road;
- B be assets marked as requiring field verification.

Suppose (|A|=180), (|B|=90), and (|A\cap B|=35).

Then the number satisfying at least one condition is:

$$
|A\cup B|=|A|+|B|-|A\cap B|
$$

$$
|A\cup B|=180+90-35=235
$$

The number satisfying both conditions is 35. The number satisfying the road-proximity condition but not the verification flag is:

$$
|A\setminus B|=180-35=145
$$

These counts assume both selections use the same asset universe, unique identifiers and consistent filtering rules. If records are duplicated, missing or drawn from different snapshots, the set calculation may be mathematically correct but operationally misleading.

### Useful set identities

For sets A, B and C:

$$
A\cup B=B\cup A
\qquad
A\cap B=B\cap A
$$

$$
A\cup(A\cap B)=A
\qquad
A\cap(A\cup B)=A
$$

De Morgan's laws connect complements with union and intersection:

$$
(A\cup B)^c=A^c\cap B^c
$$

$$
(A\cap B)^c=A^c\cup B^c
$$

These identities are useful when simplifying query logic. They do not determine what a spatial predicate means; that meaning comes from the data model and predicate definition.

## 4. Ordered pairs and Cartesian products

An ordered pair records two values in a particular order. In general, ((a,b)\ne(b,a)).

For sets A and B, the Cartesian product is:

$$
A\times B=\{(a,b)\mid a\in A,\ b\in B\}
$$

If A contains three zones and B contains four sensor types, (A\times B) contains 12 possible zone–sensor-type pairs. A pair can represent a possible combination even when no observation exists for that combination.

This distinction matters in data modelling:
- a set of observed zone-sensor pairs records combinations that actually occur;
- the Cartesian product describes all possible pairs;
- a missing pair may mean “not observed”, “not applicable” or “data missing”—not necessarily zero.

An ordered pair of coordinates such as ((x,y)) also depends on a declared axis order and coordinate reference system. Swapping easting and northing changes the represented location.

## 5. Relations: describing connections

A **binary relation** from A to B is any subset of (A\times B). If the relation is from A to itself, it is a relation on A.

Let S be a set of spatial features. A relation T might contain ordered pairs ((a,b)) when feature a touches feature b under a specified topology model:

$$
T\subseteq S\times S
$$

If ((a,b)\in T), we say a is related to b. The relation's definition must specify the predicate, geometry model, tolerance or topology rules where relevant.

Relations can have important properties:

- **Reflexive:** every element is related to itself.
- **Irreflexive:** no element is related to itself.
- **Symmetric:** if a is related to b, then b is related to a.
- **Antisymmetric:** if a is related to b and b to a, then a = b.
- **Transitive:** if a is related to b and b to c, then a is related to c.

Do not assume a relation has one of these properties just because its name sounds familiar. Test the formal definition.

### Equivalence relations and partitions

A relation is an equivalence relation if it is reflexive, symmetric and transitive. It groups elements into equivalence classes: members of one class are equivalent under the defined relation.

For example, records could be grouped by a normalised administrative-area code. “Same administrative area” is an equivalence relation if every record is assigned exactly one valid area and equality of codes is used. A fuzzy “near the same area” relation may fail transitivity and therefore may not define equivalence classes.

A **partition** of a set is a collection of non-empty, pairwise disjoint subsets whose union is the whole set. A mutually exclusive and exhaustive land-cover classification aims to form a partition of the classified cells, provided every cell is assigned exactly one class.

## 6. Functions as mappings

A function (f:A\to B) assigns each element of domain A exactly one output in codomain B. Each input must have one defined output; different inputs may share an output.

- **Domain:** permitted inputs.
- **Codomain:** declared output set.
- **Image/range:** outputs actually attained.
- **Injective (one-to-one):** different inputs have different outputs.
- **Surjective (onto):** every element of the codomain is attained.
- **Bijective:** both injective and surjective.

### Spatial examples

- A valid feature identifier function maps each feature record to its unique identifier. If two records share an identifier, the mapping from records to identifiers is not injective.
- A coordinate transformation maps coordinates from one reference system to another, but its valid domain, parameters, axis order and operation must be specified. Not every numeric pair is a valid coordinate.
- A classification function maps each eligible cell to one class label. If some cells have no output, the function is partial unless missingness is explicitly represented as an output state.

A function is not the same as a relation in general. A relation may associate one input with several outputs or none; a function must assign exactly one output to every input in its declared domain.

## 7. Propositions and logical connectives

A **proposition** is a declarative statement that has a truth value: true or false under a stated interpretation. A question, command or vague claim is not a proposition until it is made precise.

Let:
- P: “the asset is within the study boundary”;
- Q: “the asset has passed positional quality review”.

Logical connectives combine propositions:

- Negation \(\neg P\): not P.
- Conjunction \(P\land Q\): P and Q.
- Disjunction \(P\lor Q\): P or Q, or both (inclusive OR).
- Implication \(P\Rightarrow Q\): if P, then Q.
- Biconditional \(P\Leftrightarrow Q\): P if and only if Q.

### Truth tables

| P | Q | ¬P | P ∧ Q | P ∨ Q | P ⇒ Q |
|---|---|---|---|---|---|
| T | T | F | T | T | T |
| T | F | F | F | T | F |
| F | T | T | F | T | T |
| F | F | T | F | T | T |

An implication is false only when its premise is true and its conclusion is false. When P is false, (P\Rightarrow Q) is true in classical logic. This can feel unintuitive in ordinary language, but it is essential to formal reasoning.

The converse (Q\Rightarrow P) is not generally equivalent to (P\Rightarrow Q). For example, “if a cell is classified as water, then its spectral rule was satisfied” does not imply that every cell satisfying the spectral rule must be classified as water if other conditions or precedence rules apply.

## 8. Predicates and quantifiers

A **predicate** is a statement whose truth depends on one or more variables. For example:

$$
P(x): x\text{ is a building footprint intersecting the study area}
$$

The predicate becomes a proposition when a value is substituted or when variables are quantified.

Two common quantifiers are:

- Universal: \(\forall x\), “for every x”.
- Existential: \(\exists x\), “there exists at least one x”.

For a finite set of features F:

$$
\forall x\in F,\ P(x)
$$

means every feature satisfies P, while:

$$
\exists x\in F,\ P(x)
$$

means at least one feature satisfies P.

Negating quantified statements changes the quantifier:

$$
\neg(\forall x\in F\ P(x))
\equiv
\exists x\in F\ \neg P(x)
$$

$$
\neg(\exists x\in F\ P(x))
\equiv
\forall x\in F\ \neg P(x)
$$

In words: “not every feature passed” means at least one feature did not pass. It does not mean no feature passed.

### Worked example 2 — quality acceptance

Let F be the set of 120 surveyed asset records and let V(x) mean “record x passed the required positional and attribute checks”.

The statement:

$$
\forall x\in F,\ V(x)
$$

claims all 120 records passed. If one record fails, the statement is false.

The statement:

$$
\exists x\in F,\ \neg V(x)
$$

claims at least one record failed. It is the logical negation of the universal acceptance claim.

A report should distinguish:
- all records passed;
- at least one record passed;
- at least one record failed;
- no records passed.

These are not interchangeable summaries.

## 9. Boolean logic and spatial queries

Boolean logic is the foundation of many selection expressions. A query such as “select assets within the study area and marked for inspection, unless their status is retired” can be represented:

$$
I(x)\land W(x)\land\neg R(x)
$$

where I means inside the study area, W means inspection is required, and R means retired.

Parentheses matter when expressions combine AND and OR. For example:

$$
(A\land B)\lor C
$$

is not generally equivalent to:

$$
A\land(B\lor C)
$$

A query should be written with explicit parentheses whenever precedence might be misunderstood. Also account for null or missing values: SQL's three-valued logic (TRUE, FALSE, UNKNOWN) differs from the two-valued propositional truth tables above. A NULL comparison is not simply true or false; database-specific semantics must be understood.

Spatial predicates such as intersects, contains, within, touches, overlaps and disjoint are defined by geometry/topology models. Their exact behaviour can depend on geometry validity, boundary rules, dimensionality, precision and software implementation. Boolean logic combines predicate results; it does not itself define the geometry semantics.

### Worked example 3 — express a GIS selection

Suppose a layer contains road-adjacent assets. Select records that:
1. lie within the project boundary;
2. have a verification flag;
3. are not marked as decommissioned;
4. and either have a missing photograph or a positional QA warning.

Let B, V, D, P and Q denote those predicates. Then:

$$
B\land V\land\neg D\land(\neg P\lor Q)
$$

The parentheses make clear that the final OR applies only to the photograph and QA conditions. Before implementation, define what counts as “within”, what a missing photograph means, and how NULL values are treated.

## 10. Introductory graph language

A graph is a structure consisting of vertices (nodes) and edges (links). A simple undirected graph can be written:

$$
G=(V,E)
$$

where V is a set of vertices and E is a set of unordered pairs of distinct vertices. In a directed graph, edges are ordered pairs.

Spatial examples include:
- intersections as vertices and road segments as edges;
- stops as vertices and transit connections as directed edges;
- facilities as vertices and service or communication links as edges;
- geographic entities as nodes in a relationship graph.

A graph's edges need not represent physical lines in geographic space. They can represent movement, accessibility, dependency, adjacency, communication or another defined relationship.

Basic terms:
- **Adjacent vertices:** connected by an edge.
- **Degree:** number of incident edges in an undirected graph.
- **Path:** a sequence of vertices connected by edges.
- **Cycle:** a path that returns to its starting vertex without repeating intermediate vertices in a simple cycle.
- **Connected graph:** every pair of vertices is joined by a path (for an undirected graph).

A road network graph is a model, not automatically a faithful copy of the road system. One-way restrictions, turn restrictions, access permissions, time dependence, vehicle type, topology errors and edge costs may all matter. A geometric intersection is not necessarily a routable connection (for example, a bridge crossing another road without a junction).

Graph algorithms, shortest paths, network flow, centrality, graph databases and spatial network analysis require dedicated treatment in the computer-science, optimisation and GIScience foundations.

## 11. Proof, counterexamples and induction

Mathematics is not only a collection of calculations. A proof is a reasoned argument that establishes a claim from definitions, assumptions and previously established results. A few successful examples can suggest a pattern but do not prove a statement for every possible input.

### Direct reasoning

To show that a property follows from a definition, begin with the assumptions and apply valid steps.

For example, if A is a subset of B, and B is a subset of C, then A is a subset of C. For any x in A, the first assumption gives x in B; the second gives x in C. Therefore every x in A is in C.

### Counterexamples

A single valid counterexample disproves a universal claim.

Claim: “If two polygons intersect, one must contain the other.”

Counterexample: two polygons can overlap partially, with neither containing the other. Therefore the claim is false.

Counterexamples are particularly useful when reviewing GIS assumptions, algorithm specifications and data-quality rules.

### Contrapositive and contradiction

The implication (P\Rightarrow Q) is logically equivalent to its contrapositive:

$$
\neg Q\Rightarrow\neg P
$$

It is not generally equivalent to its converse (Q\Rightarrow P).

A proof by contradiction assumes the claim is false and derives a contradiction with the assumptions or an established result. The method requires a genuine contradiction, not merely an implausible outcome.

### Mathematical induction

Induction proves a statement for all integers from a starting value by:
1. proving the base case;
2. assuming the statement holds for an arbitrary n in the required range;
3. proving it then holds for n+1.

Example: the sum of the first n positive integers is:

$$
1+2+\cdots+n=\frac{n(n+1)}{2}
$$

Base case n = 1:

$$
1=\frac{1(1+1)}{2}
$$

Assume the formula holds for n. Then:

$$
1+2+\cdots+n+(n+1)
=\frac{n(n+1)}{2}+(n+1)
$$

$$
=(n+1)\left(\frac{n}{2}+1\right)
=\frac{(n+1)(n+2)}{2}
$$

This is the formula with n replaced by n+1, so the statement holds for all positive integers n.

Induction is useful when proving properties of iterative procedures, recursively defined structures and discrete sequences. It does not by itself prove that a spatial algorithm is correct for every real-world dataset; the algorithm's assumptions and input domain must also be established.

## 12. A practical reasoning workflow

When constructing a spatial query, data model or algorithm:

1. Define the universe of objects and the relevant domain.
2. State what each set, predicate, relation or function means.
3. Specify identifiers, units, coordinate reference and geometry semantics where relevant.
4. Write the logic in symbols or carefully structured language.
5. Use truth tables or small test cases to check logical combinations.
6. Test boundary cases, missing values, duplicates and empty sets.
7. Search for counterexamples to universal claims.
8. Distinguish a mathematical proof from empirical validation on a finite dataset.
9. Record the assumptions and the data/software version to which the result applies.

## 13. Exercises

1. Let U = {a,b,c,d,e,f}, A = {a,b,c,d} and B = {c,d,e}. Find A ∪ B, A ∩ B, A \ B and U \ A.
2. A = {north,south} and B = {road,rail,bus}. List A × B and state its cardinality.
3. Let R be the relation “shares a boundary segment with” on a set of polygon features. Is R necessarily reflexive, symmetric or transitive? Explain using the stated relation.
4. A function maps every raster cell to its land-cover class. What condition makes it a function? Give an example of a data problem that would violate the condition.
5. Write the negation of “every road segment in the study area passed QA”. Explain the quantifier change.
6. Translate this rule into logic: select a feature if it is inside the boundary, is not retired, and either requires inspection or has a QA warning.
7. Explain why the converse of “if a feature is a road, it has a road-class attribute” need not be true.
8. Give a counterexample to the claim “if two road lines cross in a 2D map, vehicles can turn from one to the other”.
9. A directed network has vertices A, B, C and edges (A,B), (B,C). Is there a directed path from A to C? Is there necessarily one from C to A?
10. Use induction to show that the sum of the first n odd positive integers is n².
11. Explain why SQL conditions involving NULL cannot always be reasoned about using only TRUE and FALSE.
12. A layer is partitioned into three land-cover classes. State the two conditions required for the classes to form a partition of all valid cells.

## 14. Exercise answers

1. A ∪ B = {a,b,c,d,e}; A ∩ B = {c,d}; A \ B = {a,b}; U \ A = {e,f}.
2. {(north,road),(north,rail),(north,bus),(south,road),(south,rail),(south,bus)}; cardinality is 2 × 3 = 6.
3. It is symmetric if “shares a boundary segment” is defined symmetrically. It is not reflexive under the literal distinct-feature boundary-sharing interpretation. It is not necessarily transitive: A may share a boundary with B, and B with C, while A and C do not share one.
4. Every cell in the function's domain must map to exactly one class value. A cell assigned two conflicting class labels violates uniqueness; an unassigned cell violates totality unless the domain excludes it or a missing/unknown class is explicitly included.
5. “There exists at least one road segment in the study area that did not pass QA.” Formally, ∃x in R such that ¬Q(x).
6. Let I = inside, D = retired, W = requires inspection, and Q = QA warning. The expression is I ∧ ¬D ∧ (W ∨ Q).
7. A non-road feature might also carry a road-class attribute due to a data-entry error, a broad schema or an overloaded field. The original implication does not establish its converse.
8. A bridge and a surface road can cross in 2D without a junction. Geometric intersection alone does not establish a traversable connection.
9. Yes, A → B → C is a directed path. No directed path from C to A follows from the given edges.
10. Base case n = 1: 1 = 1². Assume 1+3+…+(2n−1) = n². Add the next odd number 2(n+1)−1 = 2n+1: n²+2n+1 = (n+1)². Thus the result holds for every positive integer n.
11. In SQL, comparisons with NULL generally evaluate to UNKNOWN, and WHERE retains only rows for which the condition is TRUE. Explicit IS NULL / IS NOT NULL checks and the database's three-valued logic must be considered.
12. The classes must be pairwise disjoint and their union must equal the set of all valid cells. No valid cell is in more than one class, and none is left out.

## 15. Boundaries and connections

This module establishes a common language; it does not replace specialist treatments.

- **Module 04 — Equations, inequalities and mathematical reasoning:** algebraic conditions and constraints; this module adds formal propositions, quantifiers, sets and relations.
- **Module 05 — Functions and relationships:** function notation and mathematical mappings.
- **Module 06 — Coordinate geometry and reference frames:** geometric objects and coordinate representations.
- **Module 07 — Vectors and vector operations:** spatial direction and geometric quantities.
- **SM-FND-015 — Computer science, algorithms and complexity:** data structures, algorithm correctness, computational logic and complexity.
- **SM-FND-018 — Geographic information science and spatial thinking:** spatial predicates, topology, representation and geographic meaning.
- **SM-FND-006 — Geometry and computational geometry:** formal geometric relationships and spatial operations.
- **SM-FND-017 — Optimisation and operations research:** graph optimisation, routing and network flow.
- **SM-FND-007 — Topology and spatial relations:** deeper theory of spatial relationships and topological structure.

The mathematics of a predicate and the semantics of a spatial operation must be kept distinct. Boolean logic can combine the outputs of predicates, but it does not define what “contains”, “intersects”, “connected” or “accessible” means for a particular data model.

## References

- Levin, Oscar. *Discrete Mathematics: An Open Introduction*, 4th edition (2025). [Official textbook](https://discrete.openmathbooks.org/dmoi4.html). Chapters on logic and proofs, sets, functions, relations and graphs. The book is licensed CC BY-NC-SA 4.0; this module provides original explanations and examples and does not reproduce the textbook's text, figures or exercises. Source record: SM-SRC-000028.
- Koroteev, Peter. University of California, Berkeley, MATH 55 course outline. [Discrete Mathematics](https://math.berkeley.edu/~pkoroteev/math55.html). Used as a secondary reference for the scope and conventional sequencing of logic, proof, sets, relations and functions.

**Review limitation:** this is an initial educational module, not an independently peer-reviewed mathematical text. Spatial examples are illustrative. Database three-valued logic is introduced conceptually; SQL dialect-specific details require checking against the relevant database documentation. Graph theory is introductory only.
