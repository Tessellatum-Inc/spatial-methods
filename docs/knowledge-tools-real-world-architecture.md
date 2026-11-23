# Spatial Methods — Knowledge, tools and real-world capability architecture

**Version:** 0.1  
**Status:** Working architecture  
**Purpose:** Define how Spatial Methods connects foundational knowledge, data, methods, technologies, practical tools, experiments and real-world applications.

## 1. Architectural ambition

Spatial Methods is evolving from a primarily spatial and computational learning resource into a connected environment for exploring the sciences, technologies, data and methods through which people understand and interact with the world.

The ambition is not to catalogue every discipline or reproduce every course. It is to make unfamiliar territories navigable, connect ideas that are usually separated, and help people move from curiosity towards meaningful capability.

A person may enter through a mathematical question, a physical phenomenon, a dataset, a scientific instrument, a software tool, a practical problem or an idea for something to build. The architecture must support all these entry points.

**Working promise:** Explore how the world works, understand how it is measured and represented, investigate the methods and technologies involved, and develop the capability to do useful things with that knowledge.

## 2. The definitive structure: four pillars

Spatial Methods is organised around four permanent pillars. These are the top-level structure for the knowledge archive, research, practical work and future products.

### 1. Spatial Algorithms

Reusable computational methods for working with spatial data and spatial problems.

An algorithm record explains:
- the problem it addresses and the task it performs;
- its mathematical and computational foundations;
- inputs, outputs, assumptions and preconditions;
- the procedure, variants and implementation choices;
- complexity, accuracy, performance and limitations;
- tests, benchmarks, example data and suitable applications.

Algorithms are reusable building blocks. One algorithm may support many different recipes and applications. Keep the distinction between an algorithm, a broader method, a statistical model, an operation, a data structure and a software implementation explicit.

### 2. Spatial Recipes

Reproducible, problem-oriented workflows that show how to accomplish something.

A recipe combines the appropriate data, algorithms, software or instruments, parameters, decisions and validation steps into an executable or repeatable procedure. It should explain when the workflow is suitable, what is needed, how to carry it out, how to assess the result and where it can fail.

A recipe may use one algorithm or many. It may also include data acquisition, preprocessing, analysis, modelling, visualisation and delivery. Recipes are not merely tutorials or lists of software steps: they preserve the reasoning and decisions that make a workflow reproducible.

Recipes can be general-purpose, domain-specific or highly specialised. Their depth and validation requirements must match the application.

### 3. Spatial Data Collection

How information about spatial phenomena and systems is observed, detected, measured, sampled, generated, acquired and transmitted.

This pillar covers the complete breadth of collection and measurement—not just drones, satellites or remote sensing. It includes, where relevant:
- terrestrial surveying, GNSS, laser scanning and geophysical measurement;
- satellite and airborne observation, radar, optical imaging and photogrammetry;
- marine, underwater and oceanographic instruments;
- atmospheric, weather and environmental sensor networks;
- laboratory, analytical, biological and medical measurement;
- industrial sensing, machine vision and process telemetry;
- human, administrative, mobility and operational records;
- digital telemetry, network and application data;
- controlled experiments, computational generation and synthetic spatial data.

Distinguish four questions in each relevant record:
1. **Observation and acquisition:** how is the signal, sample, event or record captured?
2. **Measurement:** what quantity is estimated, in what units, with what calibration and uncertainty?
3. **Data generation:** is the information observed, human-recorded, experimentally produced, simulated or computed?
4. **Transmission and infrastructure:** how is it digitised, positioned, timed, communicated, stored and made available?

A collection system may include the phenomenon, sampling interface, sensor, transducer or detector, electronics, signal conditioning, digitisation, positioning and timing, communications, storage and processing. Describe the actual system rather than assuming every device follows one generic pipeline.

### 4. Theoretical Foundations

The knowledge that explains why spatial phenomena, measurements, representations, algorithms and workflows behave as they do.

This includes, as relevant:
- mathematics: geometry, algebra, calculus, linear algebra, probability, statistics, topology, optimisation and numerical analysis;
- spatial science: geodesy, cartography, spatial statistics, geographic theory and spatial cognition;
- physical sciences: mechanics, electromagnetism, optics, thermodynamics, fluid dynamics and wave physics;
- life, environmental and chemical sciences;
- computer science, information theory, data structures, algorithms and complexity;
- engineering principles: electronics, materials, control, measurement and system design.

Foundations are not a compulsory first stage or a single prerequisite ladder. Link the theory that materially explains a method, instrument, dataset or application, and expose deeper routes for people who need them.

## 3. How the four pillars connect

The four pillars are distinct, but they are designed to connect:

- **Foundations explain** the principles behind collection systems, algorithms and recipes.
- **Data collection produces or acquires** observations and measurements that can be represented and investigated.
- **Algorithms transform, analyse or model** data and can be reused across many workflows.
- **Recipes combine** the relevant foundations, collection methods, data, algorithms, tools and decisions to accomplish a task.
- **Applications provide context** for choosing and validating the right combination.

Applications are not a fifth pillar. They are the real-world contexts in which the four pillars are brought together. They range from general-purpose capabilities through domain-specific work to highly specialised, frontier or safety-critical applications.

Data, software, instruments, experiments, research, teaching and products are important resources or outputs that connect the pillars; they are not additional top-level pillars.

## 4. Application specialisation and validation

Applications vary substantially in scope, specialisation, operating context and consequence. Do not present them as though they are all general-purpose tools or interchangeable workflows.

A useful working spectrum is:

- **General-purpose:** data exploration, mapping, visualisation, spatial statistics, modelling, simulation and workflow automation.
- **Domain-specific:** flood modelling, transport planning, precision agriculture, mineral exploration, habitat assessment and spatial public-health analysis.
- **Highly specialised:** seismic inversion, radiotherapy treatment planning, satellite orbit determination, underwater acoustic localisation and industrial non-destructive testing.
- **Frontier and research:** experimental instruments, emerging measurement techniques, novel algorithms and systems whose methods or operational practices are still being established.

This is a spectrum, not a fixed ranking. Specialisation may arise from domain theory, operating conditions, rare equipment, data constraints, safety or regulatory requirements, or the consequences of error.

For each application, make visible where relevant:
- the problem, users, operating environment and intended decision;
- domain knowledge and specialist roles;
- required data, instruments, algorithms, recipes and infrastructure;
- performance criteria, validation evidence, uncertainty and acceptable failure;
- safety, legal, ethical, professional and regulatory obligations;
- whether the work is exploratory, educational, research-grade, operational or safety-critical.

The intended application determines the required depth and validation burden. Do not imply that a general-purpose demonstration is suitable for a specialised or safety-critical deployment.

## 5. Movement is non-linear

People can enter and move between dimensions in any direction.

Examples:
- Start with a drone, then investigate flight dynamics, control theory, embedded computing, GNSS, sensors and navigation.
- Start with electromagnetic theory, then explore antennas, radar architectures, signal processing, detection theory, software-defined radio and operational systems.
- Start with microscopy, then explore optics, detectors, image formation, sampling, reconstruction and quantitative analysis.
- Start with a statistical method, then investigate its probability foundations, numerical implementation, data requirements and uses across several fields.

A practical problem may expose a missing foundation. A mathematical idea may suggest a new instrument. A dataset may raise questions about the physical process that generated it. Preserve these feedback loops.

## 6. Cross-disciplinary demonstration territories

Use diverse territories to test whether the architecture works beyond spatial analysis.

| Territory | Distinctive foundations and systems | Possible practical work |
|---|---|---|
| Drones and autonomous flight | Mechanics, aerodynamics, control, electronics, embedded computing, sensing | Simulation, sensor logging, controller experiments, mapping |
| Radar and electromagnetic systems | Electromagnetism, wave physics, RF engineering, signal processing, detection and estimation | Signal experiments, simulation, waveform analysis, accessible SDR work |
| Microscopy and imaging | Optics, detectors, image formation, sampling, reconstruction | Calibration, image acquisition, quantitative image analysis |
| Robotics | Mechanics, kinematics, control, perception, embedded systems | Simulated manipulation, small robot builds, navigation tests |
| Astronomy and telescopes | Optics, electromagnetism, orbital mechanics, statistics and signal processing | Public observation analysis, image processing, orbit simulation |

These are test cases, not a closed list or a new rigid subject hierarchy. Each territory must retain its own scientific and engineering distinctions. Shared foundations should be linked without flattening differences.

## 7. Tool and instrument records

Create a Tool and Instrument Directory as a connected resource, not a shopping catalogue.

A record should capture, where relevant:
1. Name, category, manufacturer or origin, model/version and canonical references.
2. Purpose: what it observes, measures, manipulates, computes, constructs or controls.
3. Operating principles: the science and engineering behind it.
4. Inputs and outputs: physical quantities, signals, data formats, interfaces or materials.
5. System components and dependencies.
6. Methods, software, standards and other tools it works with.
7. Capabilities, range, resolution, accuracy, precision, bandwidth or other relevant specifications—with provenance.
8. Calibration, uncertainty, limitations, failure modes and maintenance.
9. Access pathway: understand, simulate, use remotely, borrow, hire, purchase, assemble or build.
10. Approximate cost and availability only when verified and dated.
11. Safety, legal, ethical and operational requirements.
12. Experiments and investigations it enables.
13. Related explorations, datasets, implementations and applications.
14. Licensing, documentation and review date.

Do not invent specifications or imply that a tool is suitable for a task without evidence. Separate independent scientific principles from manufacturer claims and marketing language.

## 8. Access and practical engagement levels

Not every capability requires ownership. Record realistic access routes:

- **Conceptual:** understand the instrument and its principles without operating one.
- **Computational:** use simulations, public datasets, emulators or software tools.
- **Accessible hands-on:** use low-cost components, small instruments, open hardware or borrowed equipment.
- **Shared facilities:** access university laboratories, makerspaces, observatories, workshops or institutional equipment.
- **Remote infrastructure:** use remote sensing archives, telescope services, cloud computing, research platforms or instrument networks.
- **Specialist partnership:** collaborate with organisations that operate expensive, regulated or safety-critical systems.

These are access options, not levels of status. Expensive infrastructure should not be treated as the default measure of practical depth.

## 9. Practical investigation records

A practical activity should be designed around a question or capability, not around a product demonstration.

Capture as appropriate:
- investigation question and hypothesis, if applicable;
- relevant foundations and assumptions;
- instrument, equipment, software and data;
- access, cost, time and skill requirements;
- safety, legal and ethical considerations;
- setup and procedure;
- calibration and measurement uncertainty;
- expected observations or outputs;
- validation and quality checks;
- results, deviations and failure modes;
- interpretation and limitations;
- reproducibility information;
- next experiment or extension.

Distinguish simulation from physical measurement, demonstration from validation, and a teaching prototype from a production-ready system.

## 10. Outputs and reusable assets

An exploration may generate one or more reusable outputs:
- explanations, derivations and reference notes;
- annotated bibliographies and research maps;
- code, algorithms, packages and APIs;
- notebooks, simulations and models;
- datasets, synthetic data and metadata;
- experiment protocols and test fixtures;
- hardware designs, prototypes and build instructions;
- calibration and validation procedures;
- teaching resources and workshops;
- software products, services and technical specifications.

Record provenance, version, licence, dependencies, evidence and maintenance expectations. A single investigation may support several outputs, but do not manufacture deliverables where they add no value.

## 11. Relationship model

Connect records with explicit relationships, such as:
- explains foundation of;
- measures or observes;
- generates data for;
- transforms or represents;
- models or simulates;
- implements;
- requires instrument;
- uses method;
- validates;
- applies to;
- extends or adapts;
- contrasts with;
- enables experiment;
- produces artefact;
- raises question about.

Prefer explained relationships over a large flat tag collection.

## 12. Quality and safety principles

- Preserve the distinction between theory, simulation, measurement, observation and interpretation.
- State assumptions, units, uncertainty, calibration and provenance where relevant.
- Verify code, calculations, instrument procedures and experimental results before claiming success.
- Do not imply physical validation from simulated results.
- Respect safety standards, equipment limits, privacy, environmental impacts and applicable laws.
- Treat drones, radio systems, lasers, high voltage, chemicals, biological materials and other potentially hazardous technologies with appropriate controls.
- Avoid giving unsafe operational instructions; route specialist or regulated activities through qualified supervision and official guidance.
- Distinguish open-source designs from permission to operate equipment or transmit signals in a particular jurisdiction.

## 13. How this extends the existing Spatial Methods collection

The spatial and computational archive remains a strong, developed starting territory. It becomes one connected branch within the wider system:
- spatial algorithms become methods with mathematical and computational lineage;
- remote sensing connects to sensing, electromagnetic systems, instruments and data;
- geospatial software connects to computing and engineering;
- field investigations connect methods to instruments, observations and uncertainty;
- spatial applications connect to wider physical, biological, environmental and human systems.

Do not force unrelated subjects into a geospatial workflow. Follow the subject wherever its own foundations, technologies and applications lead.

## 14. Implementation sequence

1. Approve the conceptual model and update the product brief.
2. Add adaptable fields for tools, instruments, experiments and physical outputs to the exploration template.
3. Create a tool and instrument record template.
4. Create a practical investigation template that distinguishes simulation, software implementation and physical experiment.
5. Test the model against drones, radar, microscopy, robotics and astronomy.
6. Link the new records to existing spatial algorithms and Radar material where relationships are genuine.
7. Build indexes only after enough high-quality records exist to justify them.

## 15. Acceptance tests

The architecture is working when:
- someone can enter through a tool, phenomenon, question, dataset, method or application;
- observation and acquisition cover diverse physical, biological, environmental, industrial, human, digital and computational sources—not just drones or remote sensing;
- acquisition, measurement, data generation and transmission are distinguishable and can be traced as a system;
- general-purpose, domain-specific, highly specialised and frontier applications can be represented without forcing them into one workflow;
- specialist prerequisites, validation, safety and consequences of error are visible where relevant;
- observation and acquisition cover diverse physical, biological, environmental, industrial, human, digital and computational sources—not just drones or remote sensing;
- acquisition, measurement, data generation and transmission are distinguishable and can be traced as a system;
- general-purpose, domain-specific, highly specialised and frontier applications can be represented without forcing them into one workflow;
- specialist prerequisites, validation, safety and consequences of error are visible where relevant;
- an exploration can connect foundations to measurement, data, computation and practical work without forcing a linear sequence;
- physical tools are treated as engineered systems, not shopping recommendations;
- people can identify realistic access routes without owning expensive infrastructure;
- simulations, prototypes and real-world validation are clearly distinguished;
- one foundation can connect multiple fields without erasing their differences;
- practical work has observable outputs, limitations and reproducibility details;
- the existing spatial archive fits naturally without dictating the entire scope.

## 11. Applications as capability-building testbeds

Applications bring the four pillars together and test whether their knowledge, data pathways, algorithms and recipes work under real constraints. They must also feed reusable improvements back into the repository.

An application investigation should therefore produce two kinds of value:

1. **Application value:** a useful analysis, prototype, experiment, dataset, decision aid or operationally relevant result.
2. **Methods value:** reusable data-discovery routes, acquisition procedures, processing components, validation patterns, automation, foundations or recipes.

The application remains a context, not a fifth pillar or a new organising silo. Its findings should be decomposed and promoted to the canonical home of each reusable capability. Keep domain-specific components with their domain where appropriate; do not generalise a one-off project configuration into a universal method.

The operating cycle is:

**application need → workflow decomposition → capability extraction → canonical method → improved application**

Use the [Application-to-Methods Feedback Loop](application-to-methods-feedback-loop.md) as the operating standard. The [photogrammetric reusable-capability register](../recipes/photogrammetric-mapping/reusable-capabilities.md) demonstrates how an existing application can expose reusable data acquisition, dataset auditing, processing provenance, orchestration and independent-validation patterns.

The governing question at every major application milestone is:

**What reusable capability did this application contribute to Spatial Methods, and where is that capability maintained and verified?**
