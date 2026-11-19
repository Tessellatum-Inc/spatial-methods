# Pilot project definition — urban public-transport stop and roadside-asset inventory

**Status:** Proposed application for G0 desk design. Not a selected site or authorised field assignment.  
**Parent workflow:** [Survey-to-spatial-dataset](README.md)  
**Pillar integration:** Spatial Recipes, Spatial Data Collection, Spatial Algorithms and Theoretical Foundations  
**Geographic context:** Nairobi, Kenya; exact study area intentionally undecided.

## 1. Why this is a useful first application

A small inventory of public-transport stops and immediately associated roadside/pedestrian assets is a bounded, understandable spatial information problem. It combines:

- point positioning and spatial reference;
- field observation and attribute capture;
- feature identification and classification;
- completeness, positional and thematic quality checks;
- spatial data modelling and interoperable delivery.

It is useful to transport planners, operators, accessibility researchers and local infrastructure assessments. It also provides a realistic path from measurement science to a dataset someone can inspect and use.

This pilot is an inventory and data-quality exercise. It is **not** a route redesign, traffic study, engineering design, accessibility certification, legal survey or claim that any stop is officially designated.

## 2. Proposed study question

**Can we create a traceable, quality-assessed spatial inventory of public-transport stopping locations and selected visible roadside assets along one short, permissioned urban corridor?**

The first study area should be small enough to complete carefully and independently check. Select it only after reviewing access, safety, feature density, data sensitivity, transport relevance, equipment and the availability of suitable reference/check observations.

## 3. Initial scope

### Core feature classes

1. **Stop location** — an observed public-transport boarding/alighting location, with its identification status recorded.
2. **Stop infrastructure** — visible shelter, seating, sign, lighting and other selected facilities.
3. **Pedestrian interface** — visible footway connection, kerb/ramp, crossing and obstruction indicators in the immediate stop context.
4. **Observation/control point** — only where required by the chosen measurement design; distinguish control from ordinary inventory features.

Do not assume that every observed stopping place is formally designated, legally authorised or served by a particular route. Record the evidence and confidence for its classification.

### Explicit exclusions for the pilot

- Parcel boundaries, cadastral claims or property ownership.
- Detailed engineering levels, design grades or construction set-out.
- Traffic counts, passenger counts or service-frequency claims unless separately designed.
- Personal identification, identifiable passenger imagery or unnecessary personal data.
- Hidden utility assets or intrusive investigation.
- Formal accessibility compliance determinations.

## 4. Draft feature data model

Use a relational model rather than one overloaded flat layer. The tables below describe the minimum conceptual model; field names and types must be finalised against the chosen data format and collection tooling.

### 4.1 `stop` — one record per observed stopping location

| Field | Type | Required | Meaning |
|---|---|---:|---|
| stop_id | text/UUID | Yes | Stable project identifier; not an official stop code |
| geometry | Point | Yes | Observed location with declared CRS |
| observed_name | text | No | Name displayed or locally used; provenance recorded |
| stop_status | coded text | Yes | observed_stop / signed_stop / designated_verified / uncertain |
| evidence_basis | text | Yes | What supports the stop classification |
| route_reference | text | No | Route label/reference as observed; not proof of official service |
| side_of_road | coded text | No | north/east/south/west/median/unknown where meaningful |
| observation_datetime | timestamp | Yes | Local time with timezone |
| positional_method | coded text | Yes | Method actually used |
| position_quality_class | coded text | Yes | Project-defined quality category; not a fabricated accuracy value |
| source_observer | text | Yes | Observer/team identifier or pseudonymous code |
| notes | text | No | Concise relevant observations |

### 4.2 `asset` — one record per associated physical asset

| Field | Type | Required | Meaning |
|---|---|---:|---|
| asset_id | text/UUID | Yes | Stable asset identifier |
| stop_id | foreign key | Conditional | Associated stop, if applicable |
| geometry | Point | Yes | Asset position if separately captured |
| asset_type | coded text | Yes | shelter, seat, sign, light, kerb_ramp, crossing, footway_link, obstruction, other |
| presence | boolean/coded | Yes | Present, absent after inspection, not assessed, or obscured |
| condition | coded text | No | Good / fair / poor / damaged / unknown, with definitions |
| accessibility_observation | coded text | No | Observed feature only; not a compliance verdict |
| observation_datetime | timestamp | Yes | Local time with timezone |
| evidence_ref | text | No | Photo or field-record identifier, subject to privacy controls |
| notes | text | No | Relevant detail and uncertainty |

### 4.3 `survey_observation` — measurement provenance

| Field | Type | Required | Meaning |
|---|---|---:|---|
| observation_id | text/UUID | Yes | Unique observation identifier |
| feature_id | text/UUID | Yes | Related stop or asset |
| raw_record_ref | text | Yes | Link to immutable original observation |
| method | coded text | Yes | GNSS, total_station, tape_offset, image_derived, digitised_reference, other |
| instrument_id | text | No | Equipment register reference |
| setup_id | text | No | Setup/session reference |
| observed_at | timestamp | Yes | Time of observation |
| operator_id | text | Yes | Observer/team code |
| reference_id | text | No | Control/reference source |
| processing_status | coded text | Yes | raw / processed / checked / rejected |
| rejection_reason | text | No | Required if rejected |

### 4.4 `quality_check` — independent checks and decisions

| Field | Type | Required | Meaning |
|---|---|---:|---|
| check_id | text/UUID | Yes | Unique check identifier |
| feature_id | text/UUID | Yes | Checked feature |
| check_type | coded text | Yes | independent_position / attribute_recheck / completeness / topology / metadata |
| check_method | text | Yes | How the check was performed |
| reference_source | text | Conditional | Independent reference and its provenance |
| result | numeric/text | Yes | Observed discrepancy or categorical result |
| acceptance_rule | text | Yes | Predeclared criterion and source |
| decision | coded text | Yes | pass / fail / conditional / not_assessed |
| checked_at | timestamp | Yes | Check date/time |
| reviewer_id | text | Yes | Reviewer/team code |

### 4.5 Supporting tables

- `equipment_register`: equipment ID, make/model, serial/asset identifier, firmware, configuration, verification/calibration evidence and limitations.
- `control_reference`: point/source ID, coordinates, CRS/epoch/height reference, provenance, uncertainty and permitted use.
- `data_dictionary`: field definitions, allowed values, units, null semantics and version.
- `processing_run`: input hashes/references, software/version, parameters, operator, timestamp and output references.

Keep raw records immutable. Store processed values and corrections as new records or versioned outputs, not destructive edits to the original.

## 5. Collection design principles

- Separate the location of a stop from the location of each associated asset when the distinction matters.
- Record whether a location was directly observed, derived, digitised from imagery or supplied by another source.
- Distinguish an absent feature from one that was not assessed, was inaccessible or was obscured.
- Use stable IDs and explicit relationships; do not rely on row order or names as identifiers.
- Record local observation time with timezone and preserve original timestamps where available.
- Define condition and accessibility observation categories before collection, with examples and observer guidance.
- Capture only photographs needed to evidence assets; avoid identifiable people and sensitive information.
- Do not attach a numerical positional accuracy to a feature unless the method, reference, checks and uncertainty support it.

## 6. Measurement and validation strategy — to be selected after feasibility review

Candidate positioning approaches include GNSS in suitable environments, total-station observations tied to suitable control, or a documented combination. Phone-derived or imagery-digitised coordinates may be useful for reconnaissance or preliminary mapping, but must not be presented as survey-grade positions without supporting evidence.

The selected design must answer:

1. What positional quality does the intended use require?
2. What reference frame, coordinate epoch and vertical reference are appropriate?
3. Which equipment and correction services are actually available?
4. What independent check source can test the result?
5. What environmental conditions may degrade observations?
6. How will repeated observations, setup changes and systematic effects be handled?
7. What sample of features will be independently re-observed and why?

Do not use the same observations both to fit and independently validate a result. Predefine acceptance criteria before examining check discrepancies.

## 7. Proposed deliverables

1. Study-area and scope note.
2. Feature inventory and coded data dictionary.
3. Equipment, reference and observation register.
4. Immutable raw observation package and field log.
5. Processed geospatial dataset with CRS and lineage.
6. Independent quality-check report.
7. Map and concise handover note.
8. Limitations, unresolved issues and recommendations for further collection.

A GeoPackage is a candidate delivery container for vector layers and related tables, subject to compatibility and project requirements. Preserve raw instrument-native files separately where needed.

## 8. G0 feasibility gate — no fieldwork before resolution

| Decision | Current state | Evidence needed |
|---|---|---|
| Exact corridor/site | Open | Candidate site, boundary and rationale |
| Access and permission | Open | Written/otherwise valid permission and responsible contact |
| Safety | Open | Field risk assessment, safe observation locations and operating plan |
| Equipment | Open | Available instrument, manuals, verification status and competent operator |
| Reference/control | Open | Suitable authoritative source, CRS/epoch and independent-check plan |
| Scope and acceptance | Draft | User requirement and agreed quality criteria |
| Data/privacy | Open | Photography rules, data minimisation, licence and publication constraints |
| Supervision/review | Open | Competent reviewer independent of the primary observations |
| Budget/logistics | Open | Transport, equipment, connectivity, time and contingency |

**Gate decision:** not authorised for field execution. Progress to a field protocol only when the material dependencies have evidence-backed answers.

The initial implementation is now available in the [synthetic rehearsal directory](synthetic/README.md). It tests the draft tables and referential checks with invented local-plane values; it is not a geospatially referenced sample or field dataset.

## 9. Synthetic rehearsal opportunity

Before any field activity, create a small synthetic dataset to test:

- stable identifiers and table relationships;
- coded values and null semantics;
- geometry/CRS handling;
- import/export to the proposed delivery format;
- completeness and topology checks;
- reproducible processing and report generation.

Label every generated record as synthetic. Do not mix synthetic and observed data without explicit provenance fields and clear separation.

## 10. Next actions

1. Review this draft schema for scope creep and unnecessary fields.
2. Identify one feasible candidate corridor and verify its access/safety conditions.
3. Decide whether the first pilot is stop-only or stop-plus-selected-roadside-assets.
4. Confirm equipment and independent-check options.
5. Freeze the feature dictionary and acceptance criteria.
6. Produce the detailed field protocol and synthetic test fixture.

The project remains a proposed G0 design. It does not claim that a corridor, stop inventory, equipment or field access has been confirmed.
