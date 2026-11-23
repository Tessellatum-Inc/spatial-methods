# Application-to-Methods Feedback Loop

**Status:** Foundational operating standard  
**Applies to:** All application investigations, case studies, prototypes, research demonstrations and practical projects  
**Purpose:** Ensure that applications strengthen the reusable Spatial Methods system rather than becoming disconnected project silos.

## 1. Governing principle

An application is both a real-world problem to understand and a test environment for the methods, data pathways, tools and automation used to address it.

Spatial Methods must learn from applications in two directions:

- **Knowledge flows into the application:** foundations, collection methods, algorithms, recipes, datasets, tools and standards are selected and combined to solve the problem.
- **Capability flows back into Spatial Methods:** discoveries, reusable procedures, data-discovery routes, processing components, validation methods, automation and documented limitations are extracted and returned to the appropriate canonical locations.

The application is not the organising centre of the repository. The four pillars remain the organising structure. The application supplies context, constraints, evidence and practical pressure that help improve them.

**A successful application investigation should leave behind more reusable capability than the application-specific deliverable alone.**

## 2. The four-pillar relationship

Every application should be mapped against the four pillars, without forcing artificial completeness:

| Pillar | Questions an application should expose | Reusable contribution |
|---|---|---|
| Theoretical Foundations | Which principles explain the phenomenon, measurement, representation, uncertainty or computation? | Clarified theory, derivations, assumptions, domain-specific extensions and prerequisite links |
| Spatial Data Collection | How is the required information observed, measured, sampled, generated, discovered or acquired? | Sensor/collection methods, source discovery, access procedures, metadata checks and acquisition automation |
| Spatial Algorithms | Which computational procedures transform, analyse, model, compare or optimise the data? | Algorithm records, tested implementations, benchmarks, numerical checks and known failure modes |
| Spatial Recipes | How are the components assembled into a repeatable task? | Workflow stages, decision rules, orchestration, QA gates, project templates and reproducible outputs |

Applications connect these pillars. They do not create a fifth pillar or a separate permanent knowledge silo.

## 3. The application investigation cycle

### Stage 1 — Define the real task

Record the actual problem, intended decision, users, operating context, spatial and temporal scope, required outputs, constraints and consequences of error.

Do not begin with a preferred software package or a technology demonstration. Define what must be known or achieved first.

**Output:** bounded application brief and fitness-for-purpose requirements.

### Stage 2 — Decompose the task into a workflow

Represent the work as stages, inputs, transformations, decisions, outputs and checks.

Typical stages may include:

1. Discover suitable data, sources, instruments or services.
2. Assess access, coverage, licensing, quality and fitness for purpose.
3. Acquire or observe data and preserve raw inputs.
4. Inspect metadata, integrity, coordinate reference, units and temporal coverage.
5. Prepare, clean, transform or harmonise data.
6. Apply algorithms, models or domain methods.
7. Validate intermediate and final outputs.
8. Package results with provenance, limitations and reproducibility information.
9. Deliver, monitor or maintain the result where relevant.

Not every application uses every stage. Add domain-specific stages when the actual process requires them.

**Output:** workflow map with explicit handoffs and decision points.

### Stage 3 — Identify the knowledge and capability dependencies

For each stage, identify:

- the theoretical principles and domain knowledge required;
- the collection or data-discovery method;
- the data model, format, reference system and metadata;
- the algorithms and computational operations;
- the software, instruments, infrastructure and access requirements;
- the quality checks and validation evidence;
- the safety, legal, ethical, privacy and professional constraints.

Link to existing canonical records first. Create new material only for a real gap, correction or useful extension.

**Output:** dependency map across the four pillars.

### Stage 4 — Execute and observe the friction

Carry out a bounded investigation, implementation or rehearsal appropriate to the available evidence and permissions.

Record not only the intended workflow but also what actually happens:

- where data was discovered and how availability was determined;
- what was difficult to access, download, parse or interpret;
- which metadata was missing or misleading;
- which transformations were necessary;
- which operations were repeated manually;
- where failures occurred and how they were detected;
- what could be tested automatically;
- what required human or specialist judgement;
- which assumptions failed under real conditions.

Do not hide failed attempts that materially affect reproducibility. Distinguish a design proposal, synthetic rehearsal, public-data run, prototype, field test and operational deployment.

**Output:** evidence-backed execution record and friction log.

### Stage 5 — Extract reusable capabilities

For each useful finding, determine whether it belongs in one or more of these categories:

- **Data discovery:** source catalogues, APIs, search strategies, query patterns, coverage checks and access conditions.
- **Acquisition:** downloaders, collection protocols, pagination, retries, resumability, checksums and immutable snapshots.
- **Inspection:** file inventories, schema checks, metadata extraction, integrity checks and anomaly detection.
- **Preparation:** format conversion, filtering, reprojection, resampling, harmonisation, tiling and normalisation.
- **Computation:** algorithms, models, processing components and performance improvements.
- **Validation:** independent checks, metrics, tolerances, diagnostics, test data and acceptance gates.
- **Orchestration:** stage sequencing, configuration, workflow state, logging, error handling and reproducible execution.
- **Packaging:** manifests, provenance, reports, exports, documentation and handover structures.

A manual procedure may be a valuable recipe before it is ready for automation. Do not automate an unstable or poorly understood process merely because it is repetitive.

**Output:** candidate reusable assets with a clear proposed home.

### Stage 6 — Classify before promoting

Use four reuse levels:

| Level | Meaning | Repository treatment |
|---|---|---|
| General reusable capability | Applies across multiple domains or application families | Promote to a shared implementation, algorithm, collection method or foundation record |
| Domain reusable capability | Reusable within a coherent domain, such as photogrammetry or hydrology | Maintain as a domain component and link to the shared foundations |
| Application-specific capability | Required by one application or operating context | Keep with that application or recipe; document why it is specific |
| Project-specific configuration | Values, paths, credentials, site conditions, client rules or one-off decisions | Keep in a project record or local configuration; do not promote as general method |

Do not generalise prematurely. A component does not become universal simply because it is useful once. Conversely, a generic data-integrity or provenance requirement should not be buried inside a single project just because that project revealed the need.

### Stage 7 — Return improvements to canonical homes

Place each contribution where future users will naturally find and reuse it:

- principles and explanations → **Theoretical Foundations**;
- observation, sensing, measurement and acquisition → **Spatial Data Collection**;
- computational procedures → **Spatial Algorithms** and their tested implementations;
- repeatable end-to-end workflows → **Spatial Recipes**;
- domain constraints and evidence → the relevant **application record**;
- cross-cutting automation and repository conventions → shared technical documentation.

Use links and stable identifiers to connect records. Avoid copying the same explanation into several folders. The application record should point to canonical components rather than become a duplicate of them.

### Stage 8 — Verify the contribution

A reusable automation or method should, where applicable, have:

- a stated purpose and bounded scope;
- documented inputs, outputs and assumptions;
- explicit dependencies and version information;
- deterministic or explainable behaviour;
- tests for normal, boundary and failure cases;
- meaningful error messages and safe failure behaviour;
- provenance and logging appropriate to the task;
- examples using synthetic or redistributable data;
- clear limitations and non-goals;
- instructions another person can follow;
- a licence and data-rights basis.

A successful run is not the same as scientific validation. Tests establish only the properties they actually test.

**Output:** reviewed, tested and documented canonical contribution.

### Stage 9 — Feed the improved method back into applications

Update the originating recipe or application to use the canonical component. Record what changed, what became easier or more reliable, and what remains specific to the application.

This closes the loop:

**application need → workflow decomposition → reusable capability → canonical method → improved application**

## 4. Automation design principles

Automation should reduce repeated effort while preserving scientific and operational judgement.

1. **Discover before downloading.** Inspect source identity, coverage, dates, licence, access method, formats and metadata before acquisition.
2. **Preserve originals.** Keep raw inputs immutable; process verified working copies.
3. **Make provenance automatic.** Record source identifiers, versions, retrieval time, parameters, software versions and checksums where appropriate.
4. **Prefer explicit configuration.** Avoid hidden defaults for CRS, units, dates, thresholds, resampling, model settings or acceptance criteria.
5. **Separate orchestration from domain logic.** A workflow runner should coordinate tested components rather than duplicate their algorithms.
6. **Make failure visible.** Report missing data, partial success, rejected records, failed checks and skipped stages explicitly.
7. **Use independent validation.** Do not validate a result solely with the same data or assumptions used to create it.
8. **Keep human decisions explicit.** Automation can flag, calculate, compare and organise; consequential interpretation and approval remain assigned to competent people.
9. **Design for reuse without erasing context.** Shared components accept clear inputs and configuration; application-specific constraints remain documented.
10. **Avoid unnecessary infrastructure.** Prefer open standards, public data, local execution and existing CI where they meet the need. Do not introduce paid services or fixed operational dependencies without a justified requirement.

## 5. Minimum application record

Every substantial application investigation should maintain a concise record containing:

- application ID, title and status;
- real-world problem and intended use;
- scope, exclusions and operating context;
- workflow map and stage dependencies;
- linked foundations, collection methods, algorithms and recipes;
- data sources, access conditions and provenance;
- software, instruments and infrastructure;
- automation used and automation opportunities discovered;
- QA, validation and acceptance evidence;
- safety, legal, ethical and specialist requirements;
- failures, friction, unresolved questions and limitations;
- reusable contributions and their canonical repository locations;
- next experiment or implementation step;
- review date and responsible reviewer.

This is a flexible record, not a mandatory long report. Use only the fields relevant to the application.

## 6. How to decide whether an application is worth pursuing

An application investigation is especially valuable when it:

- tests several existing methods together;
- reveals a missing foundation or misunderstood assumption;
- exposes a repeated data-discovery or processing task;
- generates a useful, reusable automation;
- enables comparison of alternative algorithms or instruments;
- creates a realistic validation problem;
- demonstrates a capability that cannot be understood from isolated examples;
- produces reusable teaching, research or implementation assets.

Do not pursue an application merely because it is fashionable, complex or visually impressive. Its value to Spatial Methods lies in the knowledge and capability it helps create.

## 7. Anti-chaos rules

- Keep the application question visible throughout the work.
- Do not let one project redefine the four-pillar architecture.
- Do not create a new folder, taxonomy or framework for every project.
- Do not duplicate canonical methods inside application reports.
- Do not build automation before the procedure and its acceptance criteria are understood.
- Do not mistake a working demonstration for a validated operational system.
- Do not expand into adjacent subjects unless they materially explain, enable or improve the task.
- At each major milestone, ask: **What reusable capability did this application contribute to Spatial Methods?**

## 8. Working example: photogrammetric mapping

Photogrammetry is a useful application testbed because it brings all four pillars together:

- foundations: projective geometry, camera calibration, adjustment, reference systems and measurement uncertainty;
- collection: camera/platform systems, image acquisition, control and field records;
- algorithms: feature matching, bundle adjustment, reconstruction, filtering and orthorectification;
- recipes: requirements, reconnaissance, acquisition design, processing, independent QA and delivery.

The current repository already contains a photogrammetric mapping recipe, flight-design calculations, an OpenDroneMap runner, dataset acquisition and audit utilities, and independent checkpoint statistics. The next task is to integrate and test the handoffs between these capabilities, not to invent a parallel photogrammetry framework.

See the [photogrammetric reusable-capability register](../recipes/photogrammetric-mapping/reusable-capabilities.md).

## 9. Governing test

An application is not complete for Spatial Methods merely because its immediate output exists.

It has made a meaningful contribution when the work has also improved at least one reusable foundation, collection method, algorithm, recipe, dataset pathway, validation procedure or automation—and that improvement has been placed, documented and verified in its canonical home.
