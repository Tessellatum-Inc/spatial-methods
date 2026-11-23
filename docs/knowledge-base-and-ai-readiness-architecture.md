# Spatial Methods — Complete knowledge base and AI-readiness architecture

**Version:** 0.1  
**Status:** Foundational architecture  
**Scope:** Public knowledge infrastructure, curation, retrieval and future AI interfaces

## 1. Purpose

Spatial Methods is building more than a collection of articles, tutorials or code examples. It is building a maintained, connected knowledge base for understanding, researching, teaching, implementing and applying spatial and related scientific-technological methods.

The knowledge base must serve several interfaces without fragmenting the underlying knowledge:

- people browsing the public GitHub repository;
- learners and practitioners following curated routes;
- researchers and educators tracing sources and relationships;
- Patreon members receiving ongoing editorial curation and guided learning;
- search engines and other discovery systems;
- future AI assistants and applications retrieving grounded, traceable knowledge.

**Maintain one coherent body of knowledge, then expose it through multiple useful experiences.**

AI-readiness is a design requirement, not a reason to turn the repository into a chatbot or to write content for machines at the expense of people.

## 2. The layers and their responsibilities

These layers are connected, but they are not interchangeable.

### 2.1 Spatial Methods: the public knowledge and capability foundation

The four permanent pillars remain the primary organising structure:

1. **Spatial Algorithms** — computational methods and their theory, implementations, assumptions, tests and limitations.
2. **Spatial Recipes** — reproducible workflows combining data, algorithms, tools, parameters and decisions.
3. **Spatial Data Collection** — methods and systems for observing, measuring, sampling, generating, acquiring and transmitting spatial information.
4. **Theoretical Foundations** — mathematics and sciences explaining phenomena, measurements, representations, methods and systems.

Applications are contexts in which the pillars are combined, not a fifth pillar. Software, instruments, data, standards, experiments, research and products connect the pillars.

The existing repository remains the canonical public home for reviewed explanations, technical records, code, tests, experiments, datasets, learning paths and documentation.

### 2.2 The complete knowledge base: the connected knowledge model

The knowledge base is the wider information architecture that connects the repository's resources and subjects. It is not a duplicate directory containing another copy of every article.

It has three complementary parts:

- **Canonical content:** maintained explanations, implementations, experiments, source notes and other substantive resources in their appropriate repository locations.
- **Catalogues and indexes:** subject indexes, record classifications, resource registers, coverage maps and stable identifiers that make the content navigable.
- **Knowledge relationships:** explicit links between concepts, foundations, methods, collection systems, algorithms, implementations, data, workflows, applications, evidence and learning routes.

The master subject index describes the subject universe. Canonical records describe particular knowledge objects. Resource records describe external sources. These must not be collapsed into one type of entry.

### 2.3 Patreon: the continuous curation and membership experience

Patreon is an editorial and learning layer over the knowledge base, not a second canonical technical archive.

Its value comes from ongoing human work:
- selecting and evaluating useful sources;
- explaining why they matter and how they relate;
- organising subject collections and resource shelves;
- creating guided routes for different intentions and levels of depth;
- synthesising research, disagreements, limitations and developments;
- publishing practical companions, walkthroughs and learning activities;
- helping members discover what to read, test, compare or build next.

Publicly licensed material remains governed by its original licence. Membership should charge for original curation, interpretation, structure, guidance, community and companion work—not for exclusive access to material that is already freely available under an open licence.

A Patreon post should link to canonical technical records where possible. Corrections to technical content should be made in the canonical source, with the member-facing post updated or annotated as appropriate.

### 2.4 Products and services: opportunities arising from knowledge and user problems

Products are not a separate knowledge pillar and should not be forced into the architecture prematurely.

Products may emerge from repeated needs, workflow friction, missing integrations, difficult implementation steps, quality-assurance gaps, specialist learning needs or original research.

Examples include software utilities, connectors, APIs, validated workflow packages, datasets, technical publications, training, specialist assistants and professional services.

Record an opportunity as a hypothesis until there is evidence of a real problem, a reachable customer and willingness to pay. Do not describe an identified gap as a market opportunity until it has been investigated.

## 3. Knowledge objects

The architecture must preserve distinctions between different kinds of things. Reuse the existing classification in [Record types and classification](../catalog/record-types.md), rather than inventing a competing taxonomy.

| Object family | Examples | Typical role |
|---|---|---|
| Subject | Geodesy, spatial statistics, radar remote sensing | Organises a territory of knowledge |
| Concept | Datum, spatial autocorrelation, point spread function | Names an idea or principle |
| Technical record | Algorithm, operation, model, statistic, metric, method | Explains a defined technical object |
| Workflow | Survey adjustment, image classification pipeline | Describes a repeatable sequence |
| Collection system | GNSS receiver, LiDAR system, sensor network | Describes how information is acquired |
| Implementation | Library, package, API, software function | Connects a method to executable software |
| Data resource | Dataset, data product, sample collection | Describes information used or produced |
| Evidence resource | Paper, book, standard, official documentation | Supports or qualifies claims |
| Experiment | Reproducible test, simulation, benchmark | Produces evidence under stated conditions |
| Application | Transport accessibility, deformation monitoring | Provides real-world context and requirements |
| Learning resource | Explanation, exercise, learning path, teaching companion | Supports understanding and capability |
| Opportunity | Unmet need, workflow friction, product hypothesis | Connects knowledge to possible offers |

One object may have several relationships but should retain one clear primary identity and classification. Do not create a separate record for every mention of a concept.

## 4. Relationship model

The knowledge base becomes more valuable when relationships are explicit. Use meaningful, directional relationships rather than relying only on tags or incidental links in prose.

| Relationship | Meaning | Example |
|---|---|---|
| explains | Provides theoretical or conceptual explanation for | Geodesy explains reference-frame concepts |
| depends_on | Requires or assumes another object | A least-squares adjustment depends on a stochastic model |
| implements | Realises a method or operation in software | A library implements a geometry operation |
| uses | Employs another object as an input or component | A recipe uses a GNSS observation dataset |
| collects_with | Acquires information using a system or method | A survey uses a total station |
| applies_to | Is relevant to a problem or application | Network analysis applies to route accessibility |
| alternative_to | Offers another approach to a similar task | Two interpolation methods are alternatives |
| validates | Provides a check or validation procedure for | Independent checkpoints validate a surface model |
| benchmarked_by | Has measured performance using a benchmark | An implementation is benchmarked by a defined test suite |
| derived_from | Was derived or adapted from another source or record | A teaching example is derived from a published method |
| cites | Explicitly cites an evidence source | A technical record cites a standard |
| part_of | Belongs to a broader subject, system or workflow | A submethod is part of a workflow |
| supersedes | Replaces an earlier version or record | A revised specification supersedes an older one |

These are relationship semantics, not mandatory fields to add indiscriminately. Use only relationships supported by the content. Record direction and target identity clearly. Add a new relationship type only when a real recurring need cannot be expressed by the existing vocabulary.

## 5. Identity, metadata and provenance

### 5.1 Stable identifiers

Continue using the stable subject identifiers defined in the master subject index, such as SM-FND-001. Subject IDs identify subject areas; they do not identify every article or software package within them.

Canonical records, resources, experiments, datasets and learning objects should have their own stable IDs when cross-referencing and machine retrieval require them. IDs must not depend on a file path, display title or current taxonomy placement.

Do not assign IDs retroactively to every file in one bulk operation. Establish a record-ID convention and apply it as records are reviewed or materially updated.

### 5.2 Minimum metadata for a canonical knowledge record

Where relevant, a canonical record should expose:

- stable record ID;
- canonical title and aliases;
- primary record kind;
- primary subject ID and relevant secondary subjects;
- concise description of the problem or question;
- prerequisites and dependencies;
- inputs, outputs and intended use;
- assumptions, limitations and known failure modes;
- related record IDs and relationship types;
- evidence and source references;
- verification and implementation status;
- author or responsible maintainer where appropriate;
- creation, review and last-verified dates where freshness matters;
- licence and reuse conditions where relevant.

Not every object needs every field. Unknown values should remain unknown, not be inferred. Keep human-readable explanations as the primary content; metadata supports discovery and connection.

### 5.3 Status must describe actual evidence

Use status labels consistently:

- **captured:** identified or imported, not yet assessed;
- **mapped:** scope and relationships outlined;
- **sourced:** relevant references identified;
- **curated:** sources evaluated and organised;
- **researched:** a substantive synthesis exists;
- **implemented:** a reproducible implementation exists;
- **tested:** stated tests have been run and results recorded;
- **validated:** evidence supports the stated validation claim and scope;
- **maintained:** reviewed within a stated maintenance process.

These states are not necessarily a linear maturity ladder. A source can be curated without an implementation; an implementation can be tested without being validated for a real-world use. Do not use a stronger status than the evidence supports.

### 5.4 Evidence and provenance

Important technical claims should be traceable to the sources or experiments supporting them. Preserve source identity, issuing organisation or author, publication or release date, version, URL or DOI, access date when relevant, and the specific claim or section supported.

Distinguish primary evidence, official specifications and documentation, secondary synthesis, community experience, repository-generated experimental results, editorial interpretation, hypotheses and unresolved questions.

A citation does not make a claim automatically correct. Explain conflicts, scope and limitations where they matter. Preserve the difference between synthetic experiments and real-world observations.

## 6. Retrieval and AI-readiness requirements

The repository should be useful to an AI system because it is well-structured and evidence-aware—not because every page is written as a prompt.

### 6.1 Retrieval units

Technical records should have clear headings and self-contained sections so a retrieval system can return a useful passage without losing its meaning. Define specialist terms, identify the subject, state important assumptions near the relevant procedure and keep limitations close to the claims they qualify.

Avoid unexplained abbreviations, headings that only make sense in the surrounding page, giant pages that mix unrelated topics, duplicated facts that drift out of sync, unannotated link lists and claims that omit evidence or scope.

Do not fragment a coherent explanation into dozens of tiny files merely to optimise chunk size. Retrieval design must preserve conceptual context.

### 6.2 Machine-readable discovery

The existing Markdown repository is the canonical source. A future retrieval layer may generate machine-readable indexes from approved records, for example JSON or JSONL containing IDs, titles, kinds, subject IDs, relationships, status, source references, canonical paths and concise descriptions.

Generated indexes must be reproducible from canonical sources and clearly marked as derived outputs. They must not become a second manually maintained truth.

A future search service may index approved public content and expose filtered retrieval by subject, record kind, status, application, software, date or evidence type. The choice of search engine, vector database, graph database or hosting architecture is deliberately deferred until there is a tested need.

### 6.3 Grounded assistant behaviour

Any future Spatial Methods assistant should:

1. Prefer relevant canonical Spatial Methods records over unsupported recollection.
2. Identify the sources and versions used to answer.
3. Distinguish established guidance, experimental results, editorial interpretation and hypotheses.
4. State when the repository has no adequate evidence or coverage.
5. Preserve assumptions, units, coordinate reference details, uncertainty and limitations.
6. Never present synthetic examples as field evidence or simulated performance as real-world validation.
7. Avoid inventing software capabilities, standards requirements, citations, benchmark results or professional authority.
8. Offer useful next steps and original source links.
9. Use general model knowledge to explain and connect material, but identify when a claim is not established by the curated knowledge base.
10. Respect the access and licence conditions of every retrieved resource.

The assistant should be a knowledge interface, not an authority that silently overrides source material or professional judgement.

### 6.4 Future integration options

Potential interfaces include direct repository discovery and retrieval through a connected GitHub experience; a searchable Spatial Methods website; a dedicated retrieval API; an MCP server exposing search, record retrieval and relationship traversal; or a ChatGPT app or other AI assistant built on an approved retrieval service.

These are possible interfaces, not current capabilities or commitments. Build the content and metadata foundation first. Select the integration route only after testing retrieval quality, source attribution, access control, maintenance cost and user demand.

## 7. Quality requirements

A knowledge object is not ready for high-confidence AI retrieval merely because a file exists.

Before promoting a record into an authoritative retrieval collection, check as appropriate:

- identity and classification are clear;
- content is internally coherent and scoped;
- key claims have traceable evidence;
- assumptions and limitations are visible;
- implementation and test claims are reproducible;
- synthetic and real-world evidence are distinguished;
- related records resolve to valid canonical targets;
- source and licence conditions permit the intended use;
- review status and date are accurate.

Low-confidence or incomplete records may still be discoverable, but their status must travel with the retrieved content.

## 8. How the existing repository maps to the knowledge base

The knowledge base is an architectural layer across the repository, not a replacement for its established directories.

| Existing location | Knowledge-base role |
|---|---|
| catalog/ | Subject taxonomy, record classification, source coverage and structured navigation |
| foundations/ | Foundational explanations |
| algorithms/ and methods/ | Canonical technical methods and procedures |
| recipes/ | Reproducible task-oriented workflows |
| implementations/ | Executable realisations and tests |
| experiments/, benchmarks/ and notebooks/ | Experimental evidence, performance and practical investigation |
| data/ | Data resources and supporting datasets, with provenance and licence |
| research/ and explorations/ | Research synthesis and curiosity-led investigations |
| learning-paths/ and learning-packs/ | Guided learning routes and collections |
| guides/ and docs/ | Standards, operating guidance and architecture |
| publishing/ and templates/ | Public distribution and reusable editorial formats |

The catalogue should point to canonical content rather than copying it. A record may appear in several learning routes or collections without creating multiple canonical versions.

## 9. Operating cycle

Use this cycle to grow the knowledge base while continuously looking for useful products and membership value:

1. **Discover:** identify a question, subject, source, technology, dataset, problem or development.
2. **Classify:** decide what kind of knowledge object it is and where it belongs.
3. **Map:** identify its scope, branches, dependencies and relationships.
4. **Curate:** evaluate relevant sources and explain their contribution.
5. **Research:** synthesise evidence, disagreements, assumptions and open questions.
6. **Demonstrate:** implement, test, benchmark or investigate when doing so adds value.
7. **Connect:** link the resulting records to foundations, collection methods, algorithms, recipes, tools and applications.
8. **Publish:** expose the appropriate public technical resource and, where useful, a Patreon curation experience.
9. **Observe:** record questions, recurring friction, unmet needs and requests.
10. **Evaluate opportunities:** test whether a genuine product, integration, training or service could solve a demonstrated problem.

Not every subject needs to pass through every step. Choose the depth that matches its significance and intended use.

## 10. Implementation sequence

Do not begin by building a graph database, vector database, API or chatbot. First make the underlying knowledge reliable and connected.

### Stage 1 — Establish the model
- Adopt this architecture alongside the four-pillar and record-type standards.
- Reconcile existing subject IDs, canonical records and resource registers.
- Define stable IDs for canonical records where cross-linking materially benefits.
- Establish a controlled relationship vocabulary and metadata conventions.

### Stage 2 — Curate a representative connected cluster
- Use the existing reference, positioning and measurement cluster as the first test.
- Connect foundational concepts, measurement systems, standards, methods, implementations, experiments, recipes and applications.
- Verify links, provenance and status rather than merely adding more entries.
- Use the cluster to test whether the model works across different object types.

### Stage 3 — Build machine-readable indexes
- Select a small set of mature records.
- Define a versioned JSON Schema or equivalent record contract.
- Generate a machine-readable index from canonical sources.
- Validate IDs, links, relationship targets and required fields automatically.
- Keep the index derived and reproducible.

### Stage 4 — Test retrieval quality
- Create representative questions from beginner, research, implementation and applied perspectives.
- Check whether retrieval finds the right records, includes relevant caveats and preserves source context.
- Compare retrieval-only answers with general model answers.
- Record missing knowledge, misleading matches and unsupported conclusions.

### Stage 5 — Select integrations
- Test GitHub-connected discovery, a website search experience and an API/MCP interface against the same questions.
- Compare quality, maintenance burden, access control and cost.
- Build a dedicated ChatGPT app only if it provides a demonstrably better experience than simply connecting the repository.

## 11. Success criteria

The knowledge base is becoming useful when:

- a user can enter through a subject, problem, algorithm, instrument, dataset, paper or software tool and discover meaningful routes;
- important concepts connect to the theory, evidence, implementations and applications that explain them;
- canonical records can be found by stable identity and useful metadata;
- sources, versions, assumptions and limitations survive retrieval;
- an assistant can answer representative questions with traceable support and acknowledge gaps;
- curation produces useful Patreon experiences without duplicating or paywalling open material;
- recurring user difficulties lead to tested product and integration hypotheses.

The objective is not to maximise the number of records, links or AI answers. It is to reduce the distance between a question, trustworthy understanding and the ability to do something useful.

---

**Architectural principle:** Spatial Methods maintains the knowledge; catalogues make it navigable; explicit relationships make it connected; curation makes it useful; practical work makes it credible; and future AI interfaces make it easier to access and apply.
