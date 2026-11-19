# Nairobi pilot — reconnaissance and readiness pack

**Status:** Desk preparation only. No field reconnaissance, site access, permissions or field acquisition are authorised or confirmed.  
**Parent workflow:** [Survey-to-spatial-dataset](README.md)  
**Feasibility assessment:** [Nairobi pilot feasibility assessment](feasibility-assessment-nairobi-pilot.md)  
**Project definition:** [Pilot project definition](pilot-project-definition.md)  
**Verification method:** [Positional verification plan](positional-verification-plan.md)

## 1. Purpose

Move from desk feasibility to a defensible site decision without prematurely starting a survey.

The immediate task is to determine whether a short, permissioned corridor can support a small inventory of public-transport stopping locations and selected visible roadside assets. The reconnaissance is not a survey, stop audit, traffic study or determination of legal road boundaries.

The first candidate for desk follow-up is **Ngong Road, Adams Arcade–Prestige Mall**. It is not yet the selected site. The 20 December 2024 Nairobi Gazette lists Adams Arcade and Prestige Mall among stages on a gazetted bus route. This establishes a route reference, not the current operation of a service, the official designation of every visible stopping place, or permission to survey the road reserve.

## 2. Evidence to establish before visiting

### 2.1 Road and transport authority

- [ ] Ask KURA Nairobi Region to confirm whether the exact proposed road section is under its management and identify the responsible operational office.
- [ ] Ask whether a written no-objection, research permission, road-reserve access approval or other authorisation is required for a non-intrusive inventory.
- [ ] Ask whether any current works, restrictions, safety requirements or planned works affect the segment.
- [ ] Ask Nairobi City County Mobility/Transport whether it has a role in confirming the public-transport route/stopping context or any county approval.
- [ ] Ask who can authoritatively confirm whether a particular stopping location is formally designated. Do not infer designation from observed use, a sign, a map or a route stage.

**Starting evidence:** KURA lists Ngong Road among its projects and public works. KURA has also publicly stated that a queried Ngong Road section falls under its jurisdiction. These are good reasons to contact KURA first, but they do not replace confirmation for the exact segment.  
Sources: [KURA official website](https://kura.go.ke/); [KURA public clarification reported in 2025](https://www.kenyans.co.ke/news/114474-kura-announces-plans-build-footbridges-ngong-road-after-public-outcry); [Nairobi Gazette Notice No. 16879, 20 December 2024](https://new.kenyalaw.org/akn/ke/officialGazette/2024-12-20/226/eng%402024-12-20/source).

### 2.2 Site access and safety

- [ ] Define the proposed start/end limits using recognisable public landmarks and a desk map.
- [ ] Confirm lawful public access for a walk-through; obtain written permission before entering private property, restricted facilities or controlled road areas.
- [ ] Identify safe pedestrian routes, crossings, refuge points and places where observers can stand without obstructing passengers, operators, pedestrians or traffic.
- [ ] Exclude carriageway entry, traffic-lane measurement, roadside equipment deployment and any activity requiring traffic control unless separately authorised and professionally planned.
- [ ] Agree a stop-work rule for unsafe traffic, conflict, weather, crowding, security concerns or requests from an authorised officer.
- [ ] Use a buddy system; establish check-in/out, emergency contacts, daylight-only initial visit and transport arrangements.
- [ ] Do not photograph identifiable people, vehicle registration plates or sensitive premises unless there is a documented lawful need and an approved handling procedure.

### 2.3 Measurement capability

- [ ] Identify a competent person who can advise on the measurement method and review its limitations.
- [ ] Confirm whether a suitable GNSS receiver, total station, level, range instrument or other equipment can actually be accessed.
- [ ] Obtain make/model, serial or asset ID, firmware, manuals, configuration details and available calibration/verification records.
- [ ] Confirm operator competence, field procedure, power/battery needs, accessories and any hire/training cost.
- [ ] Decide whether the first pilot needs survey-grade coordinates at all. If no defensible reference and independent check can be arranged, restrict claims and redesign the deliverable rather than imply accuracy.
- [ ] Identify an independent check method and competent reviewer before collecting production observations.

### 2.4 Data governance

- [ ] Define the purpose, intended users and minimum attributes.
- [ ] Use stable feature IDs and preserve raw observations and provenance.
- [ ] Record whether a feature is observed, absent, not assessed, inaccessible or obscured; do not collapse these states.
- [ ] Avoid collecting personal data. If photographs or incidental personal data cannot be avoided, define lawful basis, minimisation, access, retention and deletion before collection.
- [ ] Confirm rights and permissions for any third-party basemap, imagery, route data or reference dataset.
- [ ] Agree storage, backup, access control, publication and redaction rules.

## 3. Reconnaissance protocol

This protocol is for a preliminary, non-intrusive visit only after access and safety conditions are confirmed. It does not authorise measurement or entry into controlled areas.

### Before departure

1. Save the approved corridor extent, contact details and emergency plan offline.
2. Confirm visit date/time, weather, transport, team members and check-in contact.
3. Carry identification and any written permission/authority correspondence.
4. Carry no survey instrument for operational measurement unless that activity is separately authorised and planned.
5. Prepare a simple observation sheet with the categories below.

### At the site

1. Confirm the start/end landmarks and whether the corridor is continuous and safely walkable.
2. Observe only from lawful, safe pedestrian areas.
3. Record broad feature diversity: apparent stopping locations, visible signs/shelters/seating, pedestrian interfaces, crossings, kerbs/ramps, footways and obvious obstructions.
4. Distinguish observed physical evidence from interpretation. Use “apparent stopping location” unless formal designation is verified.
5. Note inaccessible or obscured sections without attempting to enter them.
6. Record environmental and operational constraints that affect safe observation or later measurement.
7. Do not approach, interview, photograph or record passengers/operators for this pilot.
8. Stop if the activity causes obstruction, draws a safety concern or requires access not covered by permission.

### After departure

1. Check that all notes are legible and all records have a time, observer and location/context.
2. Separate direct observations from assumptions and unresolved questions.
3. Record any near miss, safety concern, access restriction or request to stop.
4. Update the corridor scorecard and decision register.
5. Do not convert reconnaissance notes into survey-grade coordinates or publish them as an authoritative inventory.

## 4. Corridor comparison scorecard

Score each criterion from 0 to 3: **0 = unacceptable/unknown; 1 = weak; 2 = workable with conditions; 3 = strong and evidenced.** A score of 0 for authority/access or safety is a hard stop, not something that can be offset by a high total.

| Criterion | Weight | What earns a high score |
|---|---:|---|
| Written authority/access pathway | 5 | Responsible authority identified; written requirements and access pathway clear |
| Pedestrian safety | 5 | Continuous safe observation route; low exposure; safe stopping points |
| Independent reference/check feasibility | 5 | Competent reviewer and suitable independent method realistically available |
| Measurement/equipment access | 4 | Suitable equipment, operator, verification records and support available |
| Feature diversity and pilot value | 3 | Enough relevant features to test the schema without excessive scope |
| Boundedness and logistics | 3 | Short, clearly bounded segment; practical transport and daylight schedule |
| Data/privacy manageability | 2 | Minimal personal data and clear publication/retention rules |
| Stakeholder cooperation | 2 | Constructive response from relevant authority/property/operator contacts |

**Weighted score:** sum(score × weight). Maximum = 87. The score is a decision aid, not a substitute for judgement. A candidate is not field-ready merely because it scores well.

| Candidate | Current status | Main reason to retain | Main unresolved risk |
|---|---|---|---|
| Ngong Road, Adams Arcade–Prestige Mall | Preferred for first desk enquiry; not selected | Gazette route stages include both landmarks; KURA has Ngong Road project/jurisdiction evidence | Exact segment authority/access, pedestrian safety, stop designation and independent check |
| Ngara Road / Forest Road | Reserve candidate only | Potentially useful urban transport and roadside feature diversity | Route/stop evidence, authority, access and safe walkability need stronger confirmation |

Do not assign numeric scores until evidence has been gathered. Unknown is not a neutral 2.

## 5. Initial contacts and enquiry order

### Contact 1 — KURA Nairobi Region

Purpose: confirm exact road authority, access requirements and the correct permission route.

KURA's published contact information includes:
- Nairobi Regional Office: Machakos Road, Industrial Area, Nairobi.
- Email: **nairobi@kura.go.ke**.
- Official website: [kura.go.ke](https://kura.go.ke/).

Ask for written answers to:
1. Is the Adams Arcade–Prestige Mall section of Ngong Road managed by KURA?
2. What permission or no-objection is required for a small, non-intrusive academic/technical inventory from public pedestrian areas?
3. Are there restrictions, active works or safety requirements for this section?
4. Which office/person should review the proposed scope and site plan?

### Contact 2 — Measurement Systems Limited

Purpose: understand equipment access and capability, not purchase hardware.

Published business listing:
- Mukima Estate, opposite Sunstar Hotel, Garden Estate Road, Nairobi.
- Phone: **+254 798 519942**.
- Ask whether short-term hire, supervised demonstration or training is available; verify all details directly.

Ask for:
1. Available GNSS/RTK, total station and levelling equipment suitable for a small urban asset inventory.
2. Hire rates, minimum period, deposit, accessories and operator support.
3. Calibration/verification documentation supplied with the equipment.
4. Whether an experienced operator or training session can be arranged.
5. What site conditions would make each method unsuitable.

This is an enquiry only. No instrument has been reserved or confirmed.

### Contact 3 — University of Nairobi, Geospatial and Space Technology

Purpose: seek methodological discussion, student/research collaboration or independent technical review.

Ask whether an appropriate academic or technical contact can advise on:
- fit-for-purpose method selection;
- reference/control and independent checks;
- supervision and professional boundaries;
- whether the proposed inventory is a suitable small applied learning project.

A conversation or informal interest is not a formal partnership or approval.

### Contact 4 — Nairobi City County Mobility/Transport

Purpose: clarify the public-transport information and stop-designation question, and identify any county coordination needed. Do not assume the County is the road-reserve authority for the selected segment.

## 6. Readiness decision

The pilot may move from desk preparation to a controlled reconnaissance visit only when all of the following are documented:

- [ ] Exact candidate segment and visit purpose defined.
- [ ] Relevant authority and any required permission confirmed in writing.
- [ ] Lawful pedestrian access confirmed.
- [ ] Site-specific safety plan and stop-work procedure approved.
- [ ] Team and responsible lead identified.
- [ ] Data/privacy and photography rules agreed.
- [ ] No measurement or equipment deployment is planned beyond the permission granted.

The pilot may move from reconnaissance to field acquisition only after a separate field plan is approved, including intended use, feature definitions, CRS/reference decision, measurement method, instrument verification, operator competence, independent checks, acceptance criteria, data management, permissions, budget and competent review.

**Current decision: NOT READY for field acquisition.** This is a deliberate control, not a project failure. The immediate next milestone is written authority clarification and capability enquiries.

## 7. Decision register

| Decision / question | Current position | Evidence needed | Owner | Status |
|---|---|---|---|---|
| Is the candidate segment under KURA? | Likely KURA lead based on public evidence; exact segment unconfirmed | Written confirmation from KURA Nairobi Region | Project lead | Open |
| Is reconnaissance permitted? | Unknown | Written permission/requirements | Project lead | Open |
| Are stopping locations formally designated? | Not established | Authoritative county/transport confirmation for each relevant location | Project lead | Open |
| Is there safe pedestrian access? | Not assessed on site | Approved desk plan and controlled reconnaissance | Project lead | Open |
| Can suitable equipment be accessed? | Suppliers identified, no quote or booking | Hire/demo details and instrument records | Project lead | Open |
| Is independent checking available? | Not confirmed | Named competent reviewer and method | Project lead | Open |
| Are acceptance criteria defined? | Not yet; depends on intended use | User need and predeclared quality requirements | Project lead/reviewer | Open |
| Is the pilot funded and scheduled? | Not confirmed | Budget, logistics and agreed timing | Project lead | Open |

## 8. Source notes and limitations

- [Nairobi Gazette Notice No. 16879 (20 December 2024)](https://new.kenyalaw.org/akn/ke/officialGazette/2024-12-20/226/eng%402024-12-20/source): route network reference; does not establish current service operation or official designation of every stop.
- [KURA](https://kura.go.ke/): official authority source and current contact starting point; confirm exact segment and permission requirements directly.
- [KURA public clarification on Ngong Road](https://www.kenyans.co.ke/news/114474-kura-announces-plans-build-footbridges-ngong-road-after-public-outcry): secondary reporting of KURA's jurisdiction statement; not a substitute for a formal response.
- [Land Surveyors' Board register](https://www.lsb.go.ke/register): verify current professional status where regulated surveying work or independent professional review is involved.

All business listings and contacts are leads only. Verify identity, current contact details, scope, competence, pricing and availability directly. No site visit, equipment booking, partnership, permission, survey or field validation is claimed by this document.
