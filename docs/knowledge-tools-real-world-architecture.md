# Spatial Methods — Knowledge, tools and real-world capability architecture

**Version:** 0.1  
**Status:** Working architecture  
**Purpose:** Define how Spatial Methods connects foundational knowledge, data, methods, technologies, practical tools, experiments and real-world applications.

## 1. Architectural ambition

Spatial Methods is evolving from a primarily spatial and computational learning resource into a connected environment for exploring the sciences, technologies, data and methods through which people understand and interact with the world.

The ambition is not to catalogue every discipline or reproduce every course. It is to make unfamiliar territories navigable, connect ideas that are usually separated, and help people move from curiosity towards meaningful capability.

A person may enter through a mathematical question, a physical phenomenon, a dataset, a scientific instrument, a software tool, a practical problem or an idea for something to build. The architecture must support all these entry points.

**Working promise:** Explore how the world works, understand how it is measured and represented, investigate the methods and technologies involved, and develop the capability to do useful things with that knowledge.

## 2. The connected model

The following dimensions are a shared conceptual model, not departments, a taxonomy that every subject must fit, or a mandatory learning sequence.

### A. Phenomena, systems and questions
What exists, happens or needs to be understood? This may include physical phenomena, living systems, human systems, engineered systems, abstract mathematical objects or practical problems.

### B. Foundations
The principles that explain or support investigation:
- mathematics: algebra, calculus, geometry, linear algebra, probability, statistics, topology, optimisation and numerical analysis;
- physical sciences: mechanics, electromagnetism, optics, thermodynamics, fluid dynamics and wave physics;
- life and chemical sciences: biology, chemistry, molecular science and systems biology;
- computational and information sciences: computer science, information theory, logic, algorithms and complexity;
- engineering principles: electronics, materials, control, measurement and system design.

Include foundations when they materially explain the curiosity. Do not force every exploration to begin with prerequisites.

### C. Observation, measurement and sensing
How a phenomenon or system becomes observable:
- measurement theory, uncertainty, calibration and standards;
- sensors, detectors, instruments and experimental design;
- sampling, acquisition, telemetry and signal generation;
- remote, in-situ, laboratory and observational methods.



#### Observation and data-acquisition systems: broad by design

Observation and acquisition must not be reduced to drones, remote sensing or any single instrument family. The scope includes how information about the world is detected, sampled, measured, generated, digitised and transmitted.

Relevant modalities and environments include, without implying an exhaustive taxonomy:

- **Space-based:** Earth-observation satellites, GNSS, space telescopes, radar altimeters, radiometers and atmospheric instruments.
- **Terrestrial and geophysical:** surveying systems, total stations, GNSS receivers, laser scanners, seismic arrays, ground-penetrating radar and geophysical instruments.
- **Atmospheric and environmental:** weather stations, air-quality networks, stream gauges, oceanographic buoys, environmental samplers and distributed sensor networks.
- **Marine and underwater:** sonar, hydrophones, acoustic Doppler current profilers, underwater imaging, remotely operated and autonomous underwater vehicles.
- **Laboratory and analytical:** microscopes, spectrometers, chromatographs, mass spectrometers, thermal analysers and chemical sensors.
- **Industrial and machine systems:** machine vision, vibration and pressure sensors, encoders, RFID, industrial telemetry and process-monitoring systems.
- **Medical and biological:** MRI, CT, ultrasound, EEG, ECG, biosensors, sequencing and other diagnostic or research instruments.
- **Astronomical and particle observation:** optical and radio telescopes, spectrographs, photometers, particle detectors and gravitational-wave observatories.
- **Human and administrative:** surveys, transactions, censuses, operational records, mobility traces and other human-generated observations.
- **Digital systems:** application events, network telemetry, logs, platform monitoring and machine-generated records.
- **Experimental and computational generation:** controlled experiments, simulations, synthetic environments, numerical models and digital twins.

Keep four related but distinct questions visible:

1. **Acquisition:** How is a signal, sample, event or record captured?
2. **Measurement:** What quantity is estimated, in what units, under what calibration and uncertainty?
3. **Data generation:** Is the information observed, human-recorded, experimentally produced, simulated or otherwise computed?
4. **Transmission and acquisition infrastructure:** How is it digitised, synchronised, communicated, stored and made available?

A real acquisition chain may span the phenomenon, sensor or sampling interface, transducer/detector, analogue electronics, signal conditioning, digitisation, timing and positioning, communications, storage and processing. Not every system contains every stage, and some combine several stages in one device. Record the actual chain rather than assuming a generic sensor-to-dataset pipeline.

No modality is inherently the centre of the architecture. Choose examples according to the question being investigated, the evidence available and the capabilities required.

### D. Data and representation
What is produced by observation, computation or human activity, and how it is represented:
- signals, time series, images, spectra, point clouds, tables, graphs, spatial data and event streams;
- data models, coordinate systems, metadata, encoding and schemas;
- provenance, quality, uncertainty, bias, missingness and licensing;
- storage, transmission, interoperability and lifecycle.

Data is not a single kind of object. Its meaning depends on how it was generated, measured, transformed and represented.

### E. Methods, models and computation
How questions are formalised and investigated:
- mathematical and statistical methods;
- algorithms and data structures;
- physical, biological and social models;
- numerical methods, simulation and optimisation;
- signal and image processing;
- machine learning and inference;
- software, databases, distributed systems and computational infrastructure.

### F. Instruments, tools and technologies
What people use to observe, measure, manipulate, compute, construct or operate:
- scientific instruments: microscopes, telescopes, spectrometers and laboratory equipment;
- sensors and measurement systems: GNSS, IMUs, LiDAR, radar and environmental sensors;
- machines and platforms: drones, robots, vehicles and automated systems;
- electronics: microcontrollers, radios, circuits, embedded computers and test equipment;
- software: GIS, CAD, simulation, modelling, analysis and control systems;
- computational infrastructure: GPUs, clusters, cloud systems and remote research platforms;
- field and workshop equipment.

Tools include physical and digital systems. They should be understood as engineered systems with capabilities, operating principles, interfaces, constraints and failure modes—not merely products to buy.

### G. Experiments, construction and practical capability
What can be tested, reproduced, built, configured, operated or improved?
- conceptual and mathematical experiments;
- software implementations and computational notebooks;
- simulations and synthetic data;
- field measurements and laboratory investigations;
- hardware prototypes and instrument integration;
- calibration, validation, testing and troubleshooting;
- comparison, replication and independent verification.

### H. Applications, services and systems

Applications vary substantially in scope, specialisation, operating context and consequence. They should not be presented as though they are all general-purpose tools or interchangeable workflows.

A useful working spectrum is:

- **General-purpose capabilities:** data exploration, mapping, visualisation, statistical analysis, modelling, simulation and workflow automation. These can serve many domains, though still require context and competent use.
- **Domain-specific applications:** flood modelling, medical imaging, precision agriculture, transport planning, mineral exploration, weather forecasting and habitat assessment. They combine shared foundations with domain knowledge, specialised data and context-specific methods.
- **Highly specialised applications:** seismic inversion, radiotherapy treatment planning, satellite orbit determination, underwater acoustic localisation and industrial non-destructive testing. These may require advanced expertise, specialised instruments, rigorous validation, formal standards or regulated practice.
- **Frontier and research applications:** experimental instruments, emerging measurement techniques, novel algorithms and systems whose methods, benchmarks or operational practices are still being established.

This is a spectrum, not a fixed ranking or taxonomy. An application may move along it as technology, evidence and practice mature. Specialisation is not simply a measure of difficulty: it may arise from domain-specific theory, narrow operating conditions, rare equipment, data constraints, safety or regulatory requirements, or the consequences of error.

For each application, make visible where relevant:
- the problem, users, operating environment and intended decision or outcome;
- domain knowledge and prerequisites that cannot be replaced by generic tool proficiency;
- required data, instruments, methods, infrastructure and specialist roles;
- performance criteria, validation evidence, uncertainty and acceptable failure;
- safety, legal, ethical, professional and regulatory obligations;
- whether the work is exploratory, educational, research-grade, operational or safety-critical.

Applications may enable scientific discovery, engineering and product development, environmental observation, infrastructure, transport, health, agriculture, industry, public services and new forms of interaction. Foundational inquiry also has value without an immediate application.

## 3. Movement is non-linear

People can enter and move between dimensions in any direction.

Examples:
- Start with a drone, then investigate flight dynamics, control theory, embedded computing, GNSS, sensors and navigation.
- Start with electromagnetic theory, then explore antennas, radar architectures, signal processing, detection theory, software-defined radio and operational systems.
- Start with microscopy, then explore optics, detectors, image formation, sampling, reconstruction and quantitative analysis.
- Start with a statistical method, then investigate its probability foundations, numerical implementation, data requirements and uses across several fields.

A practical problem may expose a missing foundation. A mathematical idea may suggest a new instrument. A dataset may raise questions about the physical process that generated it. Preserve these feedback loops.

## 4. Cross-disciplinary demonstration territories

Use diverse territories to test whether the architecture works beyond spatial analysis.

| Territory | Distinctive foundations and systems | Possible practical work |
|---|---|---|
| Drones and autonomous flight | Mechanics, aerodynamics, control, electronics, embedded computing, sensing | Simulation, sensor logging, controller experiments, mapping |
| Radar and electromagnetic systems | Electromagnetism, wave physics, RF engineering, signal processing, detection and estimation | Signal experiments, simulation, waveform analysis, accessible SDR work |
| Microscopy and imaging | Optics, detectors, image formation, sampling, reconstruction | Calibration, image acquisition, quantitative image analysis |
| Robotics | Mechanics, kinematics, control, perception, embedded systems | Simulated manipulation, small robot builds, navigation tests |
| Astronomy and telescopes | Optics, electromagnetism, orbital mechanics, statistics and signal processing | Public observation analysis, image processing, orbit simulation |

These are test cases, not a closed list or a new rigid subject hierarchy. Each territory must retain its own scientific and engineering distinctions. Shared foundations should be linked without flattening differences.

## 5. Tool and instrument records

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

## 6. Access and practical engagement levels

Not every capability requires ownership. Record realistic access routes:

- **Conceptual:** understand the instrument and its principles without operating one.
- **Computational:** use simulations, public datasets, emulators or software tools.
- **Accessible hands-on:** use low-cost components, small instruments, open hardware or borrowed equipment.
- **Shared facilities:** access university laboratories, makerspaces, observatories, workshops or institutional equipment.
- **Remote infrastructure:** use remote sensing archives, telescope services, cloud computing, research platforms or instrument networks.
- **Specialist partnership:** collaborate with organisations that operate expensive, regulated or safety-critical systems.

These are access options, not levels of status. Expensive infrastructure should not be treated as the default measure of practical depth.

## 7. Practical investigation records

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

## 8. Outputs and reusable assets

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

## 9. Relationship model

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

## 10. Quality and safety principles

- Preserve the distinction between theory, simulation, measurement, observation and interpretation.
- State assumptions, units, uncertainty, calibration and provenance where relevant.
- Verify code, calculations, instrument procedures and experimental results before claiming success.
- Do not imply physical validation from simulated results.
- Respect safety standards, equipment limits, privacy, environmental impacts and applicable laws.
- Treat drones, radio systems, lasers, high voltage, chemicals, biological materials and other potentially hazardous technologies with appropriate controls.
- Avoid giving unsafe operational instructions; route specialist or regulated activities through qualified supervision and official guidance.
- Distinguish open-source designs from permission to operate equipment or transmit signals in a particular jurisdiction.

## 11. How this extends the existing Spatial Methods collection

The spatial and computational archive remains a strong, developed starting territory. It becomes one connected branch within the wider system:
- spatial algorithms become methods with mathematical and computational lineage;
- remote sensing connects to sensing, electromagnetic systems, instruments and data;
- geospatial software connects to computing and engineering;
- field investigations connect methods to instruments, observations and uncertainty;
- spatial applications connect to wider physical, biological, environmental and human systems.

Do not force unrelated subjects into a geospatial workflow. Follow the subject wherever its own foundations, technologies and applications lead.

## 12. Implementation sequence

1. Approve the conceptual model and update the product brief.
2. Add adaptable fields for tools, instruments, experiments and physical outputs to the exploration template.
3. Create a tool and instrument record template.
4. Create a practical investigation template that distinguishes simulation, software implementation and physical experiment.
5. Test the model against drones, radar, microscopy, robotics and astronomy.
6. Link the new records to existing spatial algorithms and Radar material where relationships are genuine.
7. Build indexes only after enough high-quality records exist to justify them.

## 13. Acceptance tests

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
