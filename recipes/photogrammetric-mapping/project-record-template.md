# Photogrammetric project record and QA checklist

Use one copy per project. Replace bracketed prompts; write **Not applicable** with a reason rather than deleting required fields. Attach source records and reports where needed. This template records decisions; it does not certify compliance or accuracy.

## A. Project identity and requirements

- Project name/ID: [ ]
- Client / responsible organisation: [ ]
- Project lead / responsible operator: [ ]
- Version and date: [ ]
- Study area / boundary / buffer: [ ]
- Intended use and user decision: [ ]
- Target surface/features: [ ]
- Required deliverables and formats: [ ]
- Required coverage/completeness: [ ]
- Required GSD / feature visibility (if specified): [ ]
- Horizontal accuracy requirement and basis: [ ]
- Vertical accuracy requirement and basis: [ ]
- Coordinate reference system / realisation / epoch: [ ]
- Vertical datum / height type / geoid model: [ ]
- Units and axis order: [ ]
- Independent validation design and acceptance criteria: [ ]
- Exclusions and unresolved requirements: [ ]

**Requirements gate:** [Approved / Not approved / Conditional]  
Approver, date, evidence and conditions: [ ]

## B. Reconnaissance, feasibility and safety

- Desk reconnaissance sources and dates: [ ]
- Site reconnaissance date/team: [ ]
- Terrain, structures, vegetation and occlusion: [ ]
- Surface texture, reflectance, movement and lighting: [ ]
- Access and site consent: [ ]
- Applicable aviation/airspace permissions checked by whom and when: [ ]
- Privacy/data protection considerations: [ ]
- Environmental and site restrictions: [ ]
- Risk assessment and emergency arrangements: [ ]
- Weather/operating limits and stop-work triggers: [ ]
- Alternative methods considered: [ ]

**Feasibility gate:** [Approved / Not approved / Conditional]  
Decision and evidence: [ ]

## C. Sensor and acquisition design

- Platform / sensor / camera make and model: [ ]
- Sensor dimensions / pixel pitch (source): [ ]
- Focal length / lens / focus: [ ]
- Shutter type / exposure / image format: [ ]
- Calibration information and date: [ ]
- Navigation/trajectory system and time synchronisation: [ ]
- Planned height above ground and basis: [ ]
- Planned GSD and calculation: [ ]
- Approximate footprint and calculation: [ ]
- Forward/side overlap and project-specific rationale: [ ]
- Flight strips / cross-strips / obliques / camera stations: [ ]
- Speed / image interval / blur considerations: [ ]
- Boundary margin / terrain-following considerations: [ ]
- Planned image count / storage / battery / logistics: [ ]
- Control point IDs and distribution: [ ]
- Check point IDs and independent survey method: [ ]
- Control/check uncertainty and reference: [ ]
- Acquisition plan version: [ ]

**Design gate:** [Approved / Not approved / Conditional]  
Reviewer, date and conditions: [ ]

## D. Field acquisition log

For each mission/session record:

| Session ID | Date/time and timezone | Area/strip | Conditions | Deviations/incidents | Operator |
|---|---|---|---|---|---|
| [ ] | [ ] | [ ] | [ ] | [ ] | [ ] |

- Actual camera/platform settings and changes: [ ]
- Control/check observations completed: [ ]
- Image completeness and coverage inspected: [ ]
- Blur/exposure/sharpness sample inspected: [ ]
- Missing strips or gaps: [ ]
- Reflight or remedial action: [ ]
- Raw media preserved: [ ]
- Backup copies verified: [ ]

**Field gate:** [Accepted / Conditional / Rejected]  
Outstanding actions: [ ]

## E. Data ingest and provenance

- Raw-data location and access control: [ ]
- File inventory / count / size: [ ]
- Checksum algorithm and manifest location: [ ]
- Copy verification: [ ]
- Image metadata / EXIF preserved: [ ]
- Trajectory and field logs present: [ ]
- Control/check files and coordinate definitions present: [ ]
- Missing, corrupt, excluded or transformed files: [ ]
- Working-copy location: [ ]
- Data retention/backup policy: [ ]

## F. Processing record

- Software, version, operating environment: [ ]
- Project CRS and units verified: [ ]
- Image exclusions and reasons: [ ]
- Alignment settings and results: [ ]
- Camera model/calibration diagnostics: [ ]
- Tie-point distribution and issues: [ ]
- Control points, weights and residuals: [ ]
- Bundle-adjustment reports: [ ]
- Dense reconstruction settings: [ ]
- Surface/classification method: [ ]
- Orthorectification/DEM source: [ ]
- Export settings, pixel size and NoData: [ ]
- Processing log and intermediate reports: [ ]

## G. Quality assessment

### Internal diagnostics
- [ ] Image coverage and alignment reviewed
- [ ] Tie-point distribution reviewed
- [ ] Camera calibration and bundle adjustment reviewed
- [ ] Point-cloud/surface completeness and artefacts reviewed
- [ ] Orthomosaic seams, blur, gaps and displacement reviewed
- [ ] CRS, vertical reference, units and export metadata reviewed

### Independent checks
- Check point set and survey provenance: [ ]
- Confirmed not used in adjustment/tuning: [ ]
- Sample size and spatial/elevation distribution: [ ]
- Bias and statistics by coordinate component: [ ]
- Outliers/exclusions and rationale: [ ]
- Reference uncertainty and limitations: [ ]
- Acceptance criteria and result: [ ]
- Independent reviewer: [ ]

**Quality decision:** [Accept / Conditional accept / Reprocess / Reacquire / Reject]  
Decision authority, date and supporting report: [ ]

## H. Delivery and closure

- [ ] Deliverables match approved specification
- [ ] Coordinate/vertical reference and units documented
- [ ] Metadata and acquisition summary included
- [ ] Processing method and software versions documented
- [ ] Independent validation report included, or limitation stated
- [ ] Known limitations, omissions and exclusions stated
- [ ] Provenance, file inventory and checksums included
- [ ] Readme and folder structure included
- [ ] Licence, ownership and access conditions addressed
- [ ] Archive and retention location recorded

- Delivery date/version: [ ]
- Recipient / handover record: [ ]
- Outstanding conditions: [ ]
- Final sign-off and role: [ ]

## I. Lessons and change record

- What failed or required rework? [ ]
- Which assumptions were confirmed or disproved? [ ]
- What should change in the next acquisition? [ ]
- What changes require a new specification or approval? [ ]
- Record version, author, date and change: [ ]
