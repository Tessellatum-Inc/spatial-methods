# Spatial Methods — Experience and information architecture

**Version:** 0.1  
**Status:** Foundation specification  
**Purpose:** Define how people enter, navigate, use and continue curiosity-led explorations.

## 1. The organising model

The primary unit is an **Exploration**: a durable, evolving investigation that begins with a curiosity, question, method, technology, source, application or problem.

An Exploration is not necessarily a course, article, research paper or project. It is a connected container for the knowledge and activities that help someone take the subject further.

An exploration may contain:
- a short orientation;
- a map of concepts, branches and applications;
- multiple optional routes for different intentions;
- an annotated resource shelf;
- one or more practical activities;
- research or technical artefacts;
- connections to other explorations;
- a record of findings, open questions and next actions.

The editor selects the components that fit the subject. Do not force every exploration into the same long-form format.

## 2. Entry points

People may arrive through:
- a question they cannot yet phrase precisely;
- a term, role, technology or method they have encountered;
- a paper, book, lecture, dataset, software package or repository;
- a real-world problem or decision;
- a subject they want to learn, research, teach, practise or build with;
- a link from another Spatial Methods exploration.

The first experience should clarify, not interrogate. Ask for additional detail only when it changes the direction materially.

### Intake interpretation

For each new curiosity, establish as needed:
1. What does the person mean by the term or question?
2. Is there ambiguity or a similarly named subject?
3. What do they seem to want to accomplish now?
4. What relevant context or prerequisites are apparent?
5. What would be a useful first result?

Do not require a user to select from a long form before receiving value. Offer a useful orientation first, then let them choose a direction.

## 3. The exploration journey

The experience is a loop, not a linear funnel.

### Step 1 — Orient
Restate the curiosity in clear language. Define the scope, identify ambiguity and distinguish neighbouring concepts that are often conflated.

**Output:** a clear question and a useful framing.

### Step 2 — Reveal the territory
Show the major concepts, branches, methods, applications and relationships. Identify common foundations and where specialisations diverge.

**Output:** a navigable subject map, not an exhaustive taxonomy.

### Step 3 — Choose a route
Offer relevant routes according to intention. Typical routes include:
- Understand a concept.
- Build foundational knowledge.
- Investigate research and evidence.
- Practise with an exercise or dataset.
- Implement or build something.
- Teach or communicate the subject.
- Apply it to a real problem.
- Follow a related curiosity.

These are optional route labels, not user types. One person may choose several or switch as their purpose changes.

**Output:** a personally useful next direction.

### Step 4 — Use curated resources
Present a resource shelf with editorial annotations. A resource record should explain:
- what it is and who produced it;
- what it contributes to this exploration;
- which route or question it supports;
- expected prerequisites and effort where known;
- whether it is primary, introductory, reference, implementation or commentary material;
- access constraints, date sensitivity and licence or reuse notes where relevant;
- why it was selected and any important caveat.

Do not rank resources by popularity alone. A small number of well-chosen resources with clear explanations is preferable to an indiscriminate link dump.

**Output:** a credible, understandable route into existing knowledge.

### Step 5 — Take action
Offer a proportionate first action. Examples include reading one foundational section, inspecting a real dataset, reproducing a figure, running a small notebook, comparing two methods, solving an exercise, teaching a concept or drafting a research question.

The action must match the subject and the user's apparent intention. Do not invent a lab where reading or conceptual clarification is the more useful next step.

**Output:** an observable action and, where possible, an artefact or finding.

### Step 6 — Reflect and preserve
Provide a lightweight way to capture:
- what I explored;
- what I understood;
- what I tried;
- what I observed or produced;
- what surprised me;
- what remains uncertain;
- what I want to do next.

This is an optional continuity aid, not compulsory homework.

**Output:** a record that makes returning easier.

### Step 7 — Connect and continue
Suggest related explorations, foundational concepts, contrasting methods and adjacent disciplines. Explain the relationship rather than merely listing tags.

**Output:** meaningful next doors into the wider knowledge environment.

## 4. Editorial destinations

The member-facing experience uses five destinations. These are navigation surfaces, not separate products or audiences.

### Start Here
Purpose: orient new visitors and members.
Contains:
- the product promise and boundaries;
- how to begin with a curiosity;
- how to use the Exploration Library;
- how to submit a suggestion;
- where practical work and research dispatches live;
- how public GitHub resources and Patreon benefits relate.

### Exploration Library
Purpose: discover and resume durable explorations.
Contains:
- exploration landing pages and indexes;
- topic and method maps;
- annotated resource shelves;
- routes and related explorations;
- status and last-reviewed information.

The library should be navigable by subject, question, method, application and intention. No single taxonomy should be the only way in.

### Curiosity Desk
Purpose: collect, clarify and triage questions and interests.
Contains:
- submission guidance and examples;
- current suggestions and status where appropriate;
- polls or prioritisation requests;
- responses and links to resulting resources.

Submissions inform editorial priorities; they do not create a guarantee of individual research or publication.

### Laboratory
Purpose: make practical work discoverable.
Contains:
- guided investigations;
- exercises and worked examples;
- notebooks, code and datasets;
- setup and reproducibility instructions;
- observations, results and troubleshooting notes.

A lab may be linked from an Exploration and indexed here. Avoid duplicating canonical technical material.

### Research Dispatches
Purpose: surface developments and useful discoveries.
Contains:
- selected papers, tools, datasets and releases;
- short evidence-led explanations of why they matter;
- comparisons, debates and emerging questions;
- links to relevant explorations.

A dispatch is timely editorial discovery, not a substitute for a durable exploration.

## 5. Information model

Keep the metadata model deliberately small. Use relationships and free-text summaries before creating a complex controlled vocabulary.

### Core records

| Record | Purpose | Required fields |
|---|---|---|
| Exploration | Durable investigation | Stable ID, title, central question, summary, status, created/updated date |
| Resource | External or internal source | Title, source/creator, URL or location, resource type, annotation, date checked |
| Route | Optional way through an exploration | Name, intention served, prerequisites or starting point, linked resources/actions |
| Activity | Practical or reflective action | Goal, instructions, requirements, expected output, verification notes where relevant |
| Artefact | Produced output | Name, description, location, provenance, licence/reuse terms |
| Connection | Relationship between records | Source record, target record, relationship explanation |
| Suggestion | Curiosity Desk intake | Submitted question, date, status, triage note, resulting record if any |

### Recommended exploration metadata

- Stable ID / slug.
- Title.
- Central question.
- Short summary.
- Scope and exclusions.
- Domain and optional subject terms.
- Related concepts, methods and applications.
- Supported intentions.
- Prerequisites, if any.
- Status: proposed, researching, active, published, needs review, archived.
- Created date, updated date and last-reviewed date.
- Canonical location.
- Contributors and provenance.
- Licence and reuse notes for original assets.

### Resource types

Use practical labels such as:
- primary research;
- review or textbook;
- official documentation;
- lecture or course;
- dataset;
- software or repository;
- case study;
- reference or standard;
- expert or institution;
- news or release note.

These labels describe what a resource is, not whether it is automatically trustworthy. Quality is assessed separately.

### Intention labels

Use only when helpful:
- understand;
- learn;
- research;
- practise;
- build;
- teach;
- apply;
- explore further.

An exploration can have multiple labels. Do not infer a person's identity from the labels they select.

## 6. Relationship model

The architecture should support many-to-many connections:
- one exploration can involve several subjects and methods;
- one method can support many applications;
- one resource can support several explorations;
- one activity can be useful for more than one route;
- one exploration can connect to another through a named relationship.

Prefer explicit relationships such as:
- requires foundation in;
- applies to;
- uses method;
- contrasts with;
- extends;
- provides data for;
- implements;
- is evidence for;
- raises question about.

Avoid a flat tag cloud as the only representation of knowledge connections.

## 7. Canonical locations and platform responsibilities

### GitHub — durable technical source of truth
Use for technical explanations, code, tests, notebooks, reproducibility instructions, structured references, research notes, corrections and version history.

### Patreon — member experience
Use for welcome and navigation, editorial framing, curated routes, companion guidance, member discussions, polls, dispatches, workshops and member-only services or original materials.

### Newsletter and public publishing
Use for discovery, concise editorial interpretation and invitations into relevant explorations. Link to canonical sources.

### Files and downloadable assets
Use when portability, printing or offline use adds value. Every asset needs provenance, version and reuse information.

Do not create competing copies of canonical technical material. A platform-specific post should explain the value and route the reader to the maintained source.

## 8. Search and discovery

Support several discovery modes:
- browse by broad subject;
- search by natural-language question;
- find a method or technology;
- browse by application or problem;
- filter by intention or resource type;
- follow connections from an exploration already open.

Search should tolerate imperfect vocabulary. Where a query is ambiguous, explain the likely interpretations and offer a useful starting point rather than silently choosing one.

Do not build advanced search infrastructure before there is enough well-described content to justify it. Start with consistent titles, summaries, metadata and cross-links.

## 9. Continuity and progression

The experience should preserve continuity at the exploration level and, where the platform supports it, at the individual member level.

A person's progress record may include:
- exploration opened;
- route selected;
- resources consulted;
- activities attempted or completed;
- notes and artefacts created;
- open questions;
- next action.

Avoid reducing progress to a single percentage or beginner/intermediate/advanced badge. Research, teaching, application and exploration do not share one universal completion scale.

For the initial release, continuity can be supported through downloadable notes, GitHub issues/discussions where suitable, member posts or a simple personal exploration log. Do not promise an automated personal dashboard until it exists.

## 10. Editorial quality rules

- A territory map must show meaningful distinctions, not just broad labels.
- A route must have a purpose and a useful next action.
- A resource recommendation must explain why it is included.
- A practical activity must state prerequisites, requirements and expected output.
- A connection must explain the relationship.
- An exploration must state scope and important omissions.
- Timely dispatches must include dates and be reviewed for freshness.
- Every substantial asset must respect licensing and attribution.
- Corrections should update the canonical record and linked derivatives.

## 11. First-release scope

Build the first experience with existing tools. Do not begin by commissioning a custom platform or building a complex database.

Initial release requires:
1. A Start Here page/post.
2. A browsable Exploration Library index.
3. A Curiosity Desk intake and triage process.
4. A Laboratory index linking practical work.
5. A Research Dispatches index or consistent post format.
6. One complete flagship Exploration (Radar) with multiple routes.
7. Consistent metadata, annotations and cross-links.
8. A simple continuity record that members can use without special software.

## 12. Working templates and operating standards

- [Exploration template](../templates/exploration-template.md) — adaptable structure for a curiosity-led investigation.
- [Research and source evaluation standard](research-and-source-evaluation.md) — source discovery, annotation, evidence, verification and licensing checks.
- [Curiosity Desk operating guide](curiosity-desk.md) — intake, triage, prioritisation and member-facing submission copy.

## 13. Acceptance tests

The architecture is usable when:
- A visitor can arrive with an imprecise question and understand the first useful direction.
- A visitor can tell apart related but distinct branches of a subject.
- A person seeking explanation is not forced into a lab.
- A person seeking implementation can find practical material without reading every introductory item.
- A researcher can identify source quality, evidence and open questions.
- An educator can find reusable teaching material and understand its licence.
- A person can discover related explorations through explained connections.
- A new member can find where to begin, how to submit a curiosity and where to find practical work.
- The same exploration can support several intentions without duplicating its canonical content.

