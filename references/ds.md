# Design Specification (DS) — Reference

## Purpose

The Design Specification answers **"HOW will the system be built?"** It is the vendor's technical
blueprint — the bridge between the Functional Specification (what the system does) and the actual
implementation. A developer should be able to build from it; an IQ protocol should be able to
verify against it.

Where the FS describes behavior from the user's perspective, the DS describes architecture,
component design, data structures, interfaces, security controls, and technology choices from
the engineer's perspective. The customer's QA team uses the DS to confirm that the vendor has
a defensible, traceable technical plan and to anchor IQ test cases against specific, verifiable
design decisions.

**V-model position:** Left side, below FS. Traces backward to FS requirements; traces forward
to IQ protocol test cases.

**Ownership:** Vendor fully owns. Customer reviews and may comment but does not co-author.

**Key standards:** IEEE 1016, C4 model (Simon Brown), GAMP 5 2nd Ed. Appendix D4,
ISO/IEC/IEEE 42010.

---

## Predecessor Dependencies

| Predecessor | What the DS Needs From It |
|---|---|
| **FS (required)** | Functional requirements to decompose into technical design. Every FS-xxx must trace to at least one DS section or component. |
| **URS (recommended)** | User intent context — helps distinguish "must" constraints from "should" preferences during trade-offs. |
| **Validation Plan (if available)** | GAMP category and risk assessment inform depth of design documentation required. |
| **Discovery outputs** | Technology stack, codebase structure, deployment constraints, integration targets. |

If the FS does not yet exist, the skill can generate a DS from discovery outputs and code
analysis, but it flags every design decision as untraced and recommends backfilling the FS.

---

## Required Sections

### 1. Introduction

Purpose, scope, intended audience, relationship to FS, technical glossary, document conventions.

**Template headings:** 1.1 Purpose, 1.2 Scope, 1.3 Intended Audience (dev team primary,
QA team secondary, customer validation review), 1.4 Relationship to FS (cite FS doc ID,
version, date), 1.5 Glossary, 1.6 Document Conventions (trace format `[DS-NNN] -> [FS-NNN]`,
diagram notation, GAMP annotations `[GAMP-N]`).

**Coaching:** The introduction should orient a new developer joining the project. If someone
reads only section 1, they should understand what is being built and how this document connects
to the rest of the validation package.

### 2. System Architecture (C4 Model)

Progressive zoom from context through containers, components, and (where warranted) code-level
design. See the C4 Model Guidance section below for when each level applies.

**Template headings:** 2.1 Level 1 — System Context (system as black box, users, external
systems; every external system must appear in Interface Inventory), 2.2 Level 2 — Container
Diagram (deployable units with technology choices and communication protocols), 2.3 Level 3 —
Component Diagrams (one per container, with responsibilities and GAMP category per component),
2.4 Level 4 — Code-Level Design (only for safety-critical or algorithmically complex modules).

**Coaching:** Most systems need Levels 1-3. Level 4 is reserved for modules where the algorithm
or state management is itself the regulated behavior (dosage calculation, batch release logic,
audit trail implementation). Over-documenting at Level 4 creates maintenance burden without
validation value.

### 3. Module / Component Design

For each component in the Level 3 diagrams, provide a detailed design description.

**Per-component template:** Header with FS traces, GAMP category, single-sentence
responsibility. Sub-sections: 3.N.1 Behavior (input->output processing, state transitions,
business rules), 3.N.2 Internal Structure (sub-modules/classes/layers), 3.N.3 Error Handling
(detection, reporting, recovery, failure mode impact), 3.N.4 Configuration (parameters,
defaults, valid ranges), 3.N.5 Dependencies (other components, with interface references).

**Coaching:** Each component should pass the "new developer test" — could someone implement it
from the description alone? For GAMP 5 components, the component design IS the specification
that IQ verifies against.

### 4. Interface Definitions

Every interface the system exposes or consumes, with enough detail to verify during IQ.

**Template headings:** 4.1 External Interfaces (from Level 1 context diagram), 4.2 Internal
Interfaces (from Level 3 diagrams), 4.3 User Interfaces (screen inventory, navigation flow;
GxP-critical screens get field-level specs with validation rules), 4.4 API Specifications
(method, path, request/response schema, auth, error codes; reference OpenAPI if maintained
separately).

Use the Interface Inventory Matrix format (see below) to catalog all interfaces.

### 5. Data Design

Logical and physical data models, data flow, storage strategy, and data lifecycle.

**Template headings:** 5.1 Logical Data Model (ER diagram, use Data Dictionary format below),
5.2 Physical Data Model (schemas, tables, indexes, constraints, partitioning/replication),
5.3 Data Flow (ingestion, transformation, storage, retrieval; data flow diagrams for GxP-critical
paths), 5.4 Data Retention and Archival (periods per category, archival mechanism, regulatory
minimums), 5.5 Data Migration (if applicable: mapping, transformation rules, validation).

**Coaching:** The data model is the most stable part of the design and the most scrutinized
during validation. Auditors check that GxP-critical fields are identified, audit trail coverage
is complete, and retention meets regulatory minimums.

### 6. Security Design

Authentication, authorization, audit trail, electronic signatures, data protection. See the
21 CFR Part 11 section below for regulatory specifics.

**Template headings:** 6.1 Authentication (mechanism, MFA, session management, password policy),
6.2 Authorization (RBAC model, role definitions, permission matrix, segregation of duties),
6.3 Audit Trail (captured events, metadata per event, storage, tamper-evidence, ALCOA+ mapping),
6.4 Electronic Signatures (regulated actions requiring e-sig, mechanism, identity binding,
Part 11.50/11.70 compliance), 6.5 Data Protection (encryption at rest/in transit, key management,
PII/PHI handling), 6.6 Network Security (segmentation, firewall rules, API gateway).

### 7. Performance and Scalability

Quantified performance targets traceable to FS requirements, and the architectural mechanisms
that achieve them.

**Template headings:** 7.1 Performance Targets (table: Metric | Target | FS Trace |
Measurement Method), 7.2 Scalability Architecture (horizontal vs vertical, auto-scaling,
bottleneck analysis), 7.3 Capacity Planning (storage growth, compute per workload tier).

**Coaching:** Every performance number must be testable during OQ. Avoid vague targets like
"fast" or "responsive." If the FS says "real-time," the DS must define what that means in
milliseconds.

### 8. Reliability and Availability

**Template headings:** 8.1 Availability Targets (uptime SLA, maintenance windows, RTO, RPO),
8.2 Redundancy and Failover (topology, detection time, switchover time), 8.3 Backup and
Recovery (schedule, retention, location, recovery validation — ties to IQ), 8.4 Disaster
Recovery (DR site, replication, test frequency), 8.5 Monitoring and Alerting (health checks,
metrics, thresholds, escalation).

### 9. Configuration Management

**Template headings:** 9.1 Environment Strategy (dev, staging, validation, production — purpose
and isolation), 9.2 Configuration Parameters (settings, defaults, who can change, which changes
require revalidation), 9.3 Version Control (repo structure, branching, build/release pipeline),
9.4 Change Control Integration (design change flow, impact assessment for validated state).

### 10. Traceability Matrix

| DS Reference | FS Requirement | Design Element | IQ Test Case | Status |
|---|---|---|---|---|
| DS-001 | FS-001 | Section 2.2: API Container | IQ-TBD | Designed |

**Coaching:** This matrix is generated from the manifest, not hand-maintained. Every FS
requirement must map to at least one DS design element. Every DS element should forward-trace
to an IQ test case (populated when IQ is authored). Orphan DS items indicate scope creep or
missing FS requirements.

---

## C4 Model Guidance

Four zoom levels. Use the minimum needed to communicate the design.

**Level 1 — System Context.** Always required. The system as a single box, users, external
systems. Establishes the validation boundary. Diagram: title, system box (highlighted), actors,
external systems (gray), labeled arrows with data flow direction and protocol.

**Level 2 — Container Diagram.** Always for multi-container systems. Deployable units (web
server, database, mobile app, message broker) with technology labels and communication
protocols. Drives IQ verification — each container is a separately installable unit.

**Level 3 — Component Diagram.** For containers with GxP-critical logic, custom code, or
complex integration. Internal modules with responsibilities and dependencies. One diagram per
container, components labeled with GAMP category.

**Level 4 — Code-Level.** Only for safety-critical algorithms, complex state machines, or
regulatory logic where the implementation approach is the controlled element. Class diagrams,
state machines, or structured pseudocode.

**Diagram rendering:** Author in text-based notation (PlantUML, Mermaid, Structurizr DSL),
render to images for published documents. Store source notation alongside rendered images.

---

## UML vs C4 — When to Use Each

C4 is the primary notation for architecture. UML supplements for behavioral and data views.

| Diagram Type | When to Use | DS Section |
|---|---|---|
| **C4 Context** | Always — system boundary | 2.1 |
| **C4 Container** | Multi-container systems | 2.2 |
| **C4 Component** | GxP-critical containers | 2.3 |
| **UML Sequence** | Multi-component interactions, API call chains, e-signature workflows | 3.x, 4.x |
| **UML State Machine** | Regulated state transitions (batch status, approval workflows) | 3.x |
| **UML Activity** | Business processes spanning components, data processing pipelines | 3.x, 5.3 |
| **ER Diagram** | Data model — always for Section 5 | 5.1, 5.2 |
| **UML Class** | Code-level design of complex modules (Level 4 only) | 2.4 |

**Rule of thumb:** Structure -> C4. Behavior over time or data relationships -> UML.

---

## Architecture Decision Records (ADRs)

ADRs provide the rationale trail auditors expect. Record significant decisions when they are
made, not when the auditor asks.

**ADR format:** ADR-NNN title, Status (Proposed | Accepted | Deprecated | Superseded by
ADR-XXX), Date, Context (technical/regulatory problem), Decision (what and why), Alternatives
Considered (with rejection rationale), Consequences (positive, negative, regulatory impact on
validation approach/GAMP category/Part 11), FS Traces.

**When to write:** Technology selection, security architecture, data architecture, integration
patterns (sync vs async, batch vs real-time), decisions driven by regulatory constraints, any
decision where the rejected alternative would produce a materially different system.

---

## Technology Stack Table Format

Every technology component cataloged with its GAMP category. Drives IQ scope: GAMP 1 needs
installation verification, GAMP 4 needs configuration verification, GAMP 5 needs rigorous
testing.

| Component | Technology | Version | GAMP Cat. | Rationale | License | DS Section |
|---|---|---|---|---|---|---|
| Operating System | RHEL | 9.3 | 1 — Infra | Standard OS | Commercial | 2.2 |
| Database | PostgreSQL | 15.4 | 1 — Infra | Standard RDBMS | OSS | 2.2 |
| Web Framework | Express.js | 4.18 | 4 — Configured | Routing/middleware config | OSS (MIT) | 2.2 |
| Audit Trail Module | Custom | 1.0 | 5 — Custom | Vendor-developed | Proprietary | 3.x |
| Auth Provider | Okta | SaaS | 4 — Configured | SSO/MFA config | Commercial SaaS | 6.1 |

**Per-component categorization:** Assign based on how the component is used in this system,
not its inherent nature. A database is GAMP 1 when used as-is, GAMP 4 if stored procedures
implement business logic, GAMP 5 if custom extensions are developed.

---

## Interface Inventory Matrix Format

Single source of truth for integration scope. Directly drives IQ interface verification.

| ID | Name | Source | Destination | Protocol | Format | Direction | Auth | Frequency | GxP Critical | Source Zone | Destination Zone | Conduit SL | FS Trace | DS Section |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| IF-001 | Patient Import | EMR | App API | REST/HTTPS | HL7 FHIR | Inbound | OAuth 2.0 | Real-time | Yes | Zone 4 — Enterprise | Zone 4 — Enterprise | N/A — same zone | FS-012 | 4.1 |
| IF-002 | Report Export | App | File Share | SFTP | PDF | Outbound | Key-based | On-demand | Yes | Zone 4 — Enterprise | Zone 3 — Process Control | SL-2 | FS-015 | 4.1 |

**GxP Critical = Yes** means the interface carries regulated data or controls a regulated
process. These require dedicated IQ test cases for connectivity, data integrity, error handling,
and timeout behavior.

**Zone and Security Level columns** (Source Zone, Destination Zone, Conduit SL) are required
when `regulatory_context` includes IEC 62443 or the system type is OT/SCADA. Zone designations
follow IEC 62443 zone definitions (e.g., Zone 1 — Safety, Zone 2 — Basic Control, Zone 3 —
Process Control, Zone 4 — Enterprise, Zone 5 — DMZ/External). Conduit SL specifies the
required Security Level target (SL-T) for communication between zones per IEC 62443, ranging
from SL 1 (basic) to SL 4 (state-sponsored threat). For IT-only systems, these columns may
be marked N/A.

---

## Data Dictionary with Regulatory Significance Column

The Regulatory Significance column distinguishes a validation-ready data dictionary from a
generic one.

| Entity | Attribute | Type | Constraints | Reg. Significance | Audit Trailed | Retention | FS Trace |
|---|---|---|---|---|---|---|---|
| Patient | patient_id | UUID | PK, NOT NULL | GxP — identity | No (immutable) | 25 years | FS-010 |
| Batch Record | status | ENUM | IN_PROGRESS, COMPLETE, REJECTED | GxP — disposition | Yes | Product life + 1yr | FS-022 |
| Batch Record | released_by | FK->User | NOT NULL when COMPLETE | 21 CFR 11 — e-sig | Yes | Product life + 1yr | FS-023 |
| Audit Event | event_type | VARCHAR(50) | NOT NULL | 21 CFR 11 — trail | N/A (is the trail) | Per policy | FS-030 |

**Regulatory significance values:** GxP (supports quality/safety/efficacy decisions), 21 CFR
Part 11 (electronic records/signatures), PII/PHI (personally identifiable/protected health
information), ALCOA+ (Attributable, Legible, Contemporaneous, Original, Accurate), Operational
(supports system function, not directly regulated).

---

## Security Design for 21 CFR Part 11

When Part 11 applies, the DS must map each requirement to its design mechanism.

| Part 11 Section | Requirement | Design Mechanism | DS Section |
|---|---|---|---|
| 11.10(a) | System validation | V-model package | — |
| 11.10(b) | Accurate/complete copies | Export preserving metadata | 5.4 |
| 11.10(c) | Record protection | RBAC + encryption + backup | 6.2, 6.5, 8.3 |
| 11.10(d) | Access limited to authorized | Authentication + RBAC | 6.1, 6.2 |
| 11.10(e) | Audit trail | Secure, computer-generated, timestamped | 6.3 |
| 11.10(f) | Operational system checks | Workflow engine design, state machine enforcement, business rule validation | 3.x, 6.2 |
| 11.10(g) | Authority checks | Permission matrix, segregation of duties | 6.2 |
| 11.10(h) | Device checks | Input validation, checksums, referential integrity | 3.x, 5.2 |
| 11.10(i) | Training | Policies to hold individuals accountable for actions under e-signatures — vendor provides training documentation and system help; customer owns procedural compliance | Vendor Assessment |
| 11.10(k) | Documentation controls | Version control, change control | 9.3, 9.4 |
| 11.30 | Open system controls | All 11.10 controls plus encryption of records, digital signatures, and standards body controls for systems where content owners do not control access | 6.5, 6.6 |
| 11.50 | Signature manifestations | Signer name, date/time, meaning displayed | 6.4 |
| 11.70 | Signature/record linking | Cryptographic binding | 6.4 |
| 11.100 | E-sig general requirements | Unique, not reused, not reassigned | 6.1, 6.4 |
| 11.200 | E-sig components | Two distinct identification components | 6.4 |
| 11.300 | ID codes/passwords | Password policy, lockout, expiration | 6.1 |

**Coaching:** Not every system requires full Part 11. State which sections apply based on
intended use. Over-claiming creates unnecessary testing burden; under-claiming creates audit
risk.

**Open vs Closed Systems (11.10 / 11.30):** A system is "open" when persons who are
responsible for the content of electronic records do not control access to the system.
Cloud/SaaS deployments where the customer does not control the infrastructure are typically
open systems. For cloud/SaaS deployments, determine whether the system is closed or open per
Part 11 definitions. If open, additional controls (encryption, digital signatures, standards
certification) apply per Section 11.30. The shared responsibility model determines where
these controls are implemented.

---

## EU GMP Annex 11 Design Compliance Matrix

When the system operates within EU GMP scope, Annex 11 requirements must be mapped alongside
21 CFR Part 11. The two frameworks overlap significantly but Annex 11 introduces additional
lifecycle, supplier, and business continuity requirements.

| Annex 11 Clause | Requirement Summary | DS Design Mechanism | DS Section Reference |
|---|---|---|---|
| Clause 1 (Risk Management) | Risk-based approach to computerised system lifecycle | Risk assessment drives design decisions | Risk Assessment, DS Sections 7–8 |
| Clause 3 (Supplier/Service Provider) | Supplier competence and quality system | Vendor QMS, development lifecycle documentation | Vendor Assessment |
| Clause 3.4 (Service Providers/Cloud) | Cloud service provider qualification | SLA definitions, data residency, shared responsibility model | DS Section 4 (Interfaces) |
| Clause 4 (Validation) | Life cycle approach, validation report | V-model lifecycle with full traceability | VP, VSR |
| Clause 5 (Data) | Accuracy checks on data entry | Input validation, business rules, error handling | DS Section 3 (Component Design) |
| Clause 7 (Data Storage) | Damage protection, accessibility, readability | Backup architecture, data format standards, retention design | DS Section 5 (Data Design) |
| Clause 7.1 (Data Protection) | Regular backups, verified restore | Backup jobs, restore testing, RPO/RTO targets | DS Section 8 (Reliability) |
| Clause 8 (Printouts) | Clear indication if data changed since last print | Print timestamp, version marking | DS Section 3 |
| Clause 9 (Audit Trails) | Risk-based audit trail configuration | Audit trail design per data criticality | DS Section 6 (Security) |
| Clause 10 (Change and Configuration Management) | Change control procedures | Configuration management design, version control | DS Section 9 |
| Clause 11 (Periodic Evaluation) | Periodic evaluation mechanism | System health monitoring, compliance dashboard | DS Section 7 (Performance) |
| Clause 12 (Security) | Physical and logical access controls | Authentication, authorization, session management | DS Section 6 |
| Clause 13 (Incident Management) | Incident reporting and assessment | Error logging, alerting, incident workflow | DS Section 3 |
| Clause 14 (Electronic Signature) | Link between signature and record | E-signature binding, non-repudiation | DS Section 6 |
| Clause 16 (Business Continuity) | Alternative arrangements for system breakdown | Failover architecture, disaster recovery | DS Section 8 |
| Clause 17 (Archiving) | Data archival with verified retrieval | Archive format, migration strategy, retrieval verification | DS Section 5 |

**Coaching:** Systems subject to both FDA and EU regulation must address both Part 11 and
Annex 11. Where requirements overlap, a single design mechanism may satisfy both. Where they
diverge (e.g., Annex 11 Clause 3 supplier requirements, Clause 16 business continuity),
separate design treatment is needed.

---

## DS to IQ Traceability

The DS is the primary input to the IQ protocol. Each verifiable design decision should produce
one or more IQ test cases.

| DS Element | IQ Verification Type | Example |
|---|---|---|
| Container (Level 2) | Installation verification | PostgreSQL 15.4 installed, service running |
| Component GAMP category | Verification depth | GAMP 5: code deployment + config check |
| Technology stack entry | Version verification | Each component matches specified version |
| Interface definition | Connectivity test | IF-001 connection + auth succeeds |
| Security controls | Configuration verification | Password policy matches DS section 6.1 |
| Configuration parameter | Setting verification | Params match DS defaults or site values |
| Data model | Schema verification | Tables, columns, constraints match DS section 5.2 |
| Backup/recovery design | Recovery test | Backup completes, restore is consistent |
| Environment strategy | Environment verification | Isolation confirmed, no cross-env access |

**Forward (DS->IQ):** Every installable/configurable design decision must have an IQ test case.
Flag "IQ-verifiable" items during DS authoring.
**Backward (IQ->DS):** Every IQ test must cite its DS section. An IQ test with no DS reference
is an orphan.

---

## Domain-Specific Variations

### Pharma Manufacturing / SCADA
- Level 4 diagrams often required for PLC/SCADA control logic
- ISA-88 batch model and ISA-18.2 alarm management in component design
- Interface inventory must include fieldbus/OPC-UA equipment connections
- Data design addresses historian integration and time-series storage
- Security design addresses OT/IT segmentation (IEC 62443)
- 21 CFR Part 211 retention: batch records 1 year past expiry

### LIMS
- Sample lifecycle state machine is typically a Level 4 element
- Instrument integration: protocol details, data parsing, bidirectional result verification
- Calculation engine: formula specification with precision/rounding rules
- Certificate of Analysis (CoA) generation logic needs explicit design
- Data design must support ALCOA+ for all analytical results

### Enterprise / ERP Integration
- Interface inventory is typically the largest section
- Master data synchronization: explicit source of truth per entity
- Workflow engine: all configurable approval routing documented
- Multi-tenancy/multi-site: data segregation architecture
- Reporting: cross-site aggregation and access controls

### Clinical Trial Systems
- Dual compliance: 21 CFR Part 11 + EU Annex 11 in security design
- Randomization algorithm: Level 4 detail with statistical justification
- Blinding mechanisms with documented unblinding controls
- Data design supports CDISC standards (CDASH, SDTM)
- Audit trail supports full trial data history reconstruction

---

## Cloud and SaaS Considerations (GAMP 5 Appendix D7)

When the system is deployed as cloud (IaaS/PaaS) or SaaS, the DS must address the additional
considerations from GAMP 5 2nd Edition Appendix D7. These supplement — not replace — the
standard DS sections above.

### Shared Responsibility Model

Document the division of responsibilities between the cloud provider, application vendor, and
customer. The responsibility assignment directly affects validation scope — the customer must
validate what they control and verify supplier controls for what they do not.

| Responsibility Area | Cloud Provider (IaaS/PaaS) | Application Vendor (SaaS) | Customer |
|---|---|---|---|
| Infrastructure qualification | Owns — provides compliance certifications | Relies on cloud provider | Verifies certifications |
| OS patching | Owns (PaaS) or shared (IaaS) | Owns | Verifies patching cadence |
| Application deployment | Provides platform | Owns — deploys and maintains | Validates release process |
| Data backup | Provides infrastructure/tools | Configures and executes | Verifies backup adequacy and restore testing |
| Access management | Identity platform primitives | Application-level RBAC | Owns user provisioning, role assignment, periodic review |
| Audit logging | Infrastructure-level logs | Application audit trail | Owns retention policy, review, and archival |
| Network security | VPC, security groups, DDoS | Application firewall, API gateway | Defines requirements, verifies implementation |
| Disaster recovery | Regional redundancy, failover infra | DR configuration, RTO/RPO adherence | Owns DR plan, participates in DR testing |
| Data residency | Provides region selection | Configures per customer requirement | Defines regulatory requirements, verifies compliance |

### Service Level Agreements

The DS must document SLA requirements that drive reliability and availability design:

- **Availability target:** e.g., 99.9% uptime (excludes scheduled maintenance windows)
- **Recovery Point Objective (RPO):** Maximum acceptable data loss (e.g., 1 hour)
- **Recovery Time Objective (RTO):** Maximum acceptable downtime (e.g., 4 hours)
- **Support response times:** Severity-based (e.g., Sev-1: 15 min response, 4 hr resolution)
- **Incident notification timeframes:** Time from detection to customer notification (e.g., 1 hour for data breach, 4 hours for service degradation)

SLA metrics must be measurable and map to DS Section 8 (Reliability and Availability) design
mechanisms. The DS should specify how SLA compliance is monitored and reported.

### Data Residency and Sovereignty

Identify where data is stored, processed, and backed up at each tier:

- **Primary storage:** Geographic region and specific data center (where known)
- **Backup/DR storage:** Geographic region for replicas and backups
- **Processing location:** Where compute operations on the data occur
- **Transit paths:** Data routing between regions or providers

Map each data location to applicable regulatory requirements: EU GDPR data residency
(adequacy decisions, Standard Contractual Clauses), country-specific data localization laws,
and sector-specific requirements (e.g., China PIPL, Russia Federal Law 242-FZ). Document any
restrictions on cross-border data transfer and the legal mechanisms enabling permitted
transfers.

### Multi-Tenancy Considerations

If the system uses a multi-tenant architecture, document tenant isolation mechanisms across
all layers:

- **Data isolation:** Separate databases, shared database with tenant-scoped schemas, or row-level tenant filtering. Specify how cross-tenant data leakage is prevented and verified.
- **Compute isolation:** Shared application instances with tenant context, dedicated containers, or dedicated VM instances. Document resource limits and noisy-neighbor protections.
- **Network isolation:** Virtual network segmentation, tenant-specific endpoints, or shared endpoints with tenant routing. Specify how network-level cross-tenant access is prevented.

For GxP systems, multi-tenancy isolation must be verifiable during IQ and documented in the
security design (DS Section 6).

### Cloud Provider Qualification

Reference the cloud provider's compliance certifications and map them to validation
requirements:

- **SOC 2 Type II:** Covers security, availability, processing integrity, confidentiality, and privacy controls. Map relevant trust service criteria to DS design mechanisms.
- **ISO 27001:** Information security management system certification. Reference applicable controls from Annex A.
- **FedRAMP:** For US federal or regulated workloads. Identify authorization level (Low, Moderate, High).
- **GxP-specific certifications:** AWS GxP compliance packages, Azure Life Sciences compliance, GCP healthcare compliance. Reference specific whitepapers and attestations.

**Important:** Cloud provider certifications supplement but do not replace customer validation
responsibilities. Certifications demonstrate that the provider's environment is qualified, but
the customer must still validate the application layer, configuration, data integrity, and
business processes running on that infrastructure. The DS should reference specific
certification report IDs and review dates, and the validation plan should include periodic
re-review of provider certifications.

---

## Coaching Questions

### Architecture
- Could you swap any technology without changing the FS? If not, the DS may be over-coupled.
- What happens if the most critical external system is unavailable? Is the failure mode documented?
- Are there single points of failure? Are they acknowledged and justified?

### Component Design
- For each GAMP 5 component: could a developer implement from the DS alone?
- Are error handling behaviors specified, or just happy-path logic?
- Which components maintain state? Is the state machine explicitly documented?

### Data Design
- Is every GxP-critical field identified? Would an auditor agree with the significance assignments?
- Are retention periods specified for every data category? Do they meet regulatory minimums?
- Is the audit trail design sufficient to reconstruct who did what, when, and why?

### Security
- Does the Part 11 mapping have a design mechanism for every applicable section?
- Is segregation of duties defined for every GxP-critical operation?
- How are electronic signatures bound to the records they sign?

### Interfaces
- Is every Level 1 context diagram interface in the Interface Inventory?
- For GxP-critical interfaces: what happens when a message is lost, duplicated, or corrupted?
- Are timeout and retry behaviors specified?

### Traceability
- Does every FS requirement have at least one DS design element?
- Does every DS element trace to an FS requirement? If not: scope creep or missing FS?
- Are IQ-verifiable items flagged for the IQ author?

---

## Anti-Patterns

**Architecture Astronaut.** Microservices, event sourcing, CQRS for a 10-user system.
Architecture complexity must be justified by actual requirements — reference the FS requirement
that drives each decision.

**Copy-Paste Architecture Diagram.** Diagrams from framework docs or cloud marketing instead
of the actual system. Every box must correspond to something being built or configured.

**Missing Error Paths.** Component designs describe only happy-path processing. Each component
must document input validation, error detection, error reporting, and recovery/retry behavior.

**GAMP Category Shopping.** Custom code classified as GAMP 4 to reduce testing. Apply the
GAMP 5 decision tree honestly — if vendor developers wrote code, it is GAMP 5.

**Phantom Interfaces.** Interface inventory lists connections absent from diagrams, or diagrams
show arrows with no interface spec. Cross-reference every C4 arrow against the Interface
Inventory. They must match.

**Undated Technology Stack.** "PostgreSQL" without a version. Versions drift between environments
causing IQ failures. Every entry must have a pinned version. "Latest" is not a version.

**Audit Trail Afterthought.** Audit trail mentioned in security as a checkbox but not designed
into data model or component architecture. It must appear in Sections 3, 5, and 6 — it is a
cross-cutting concern, not a bolt-on.

**Data Dictionary Without Regulatory Column.** Types and constraints documented but no
identification of GxP-critical, PII, or Part 11 fields. Use the Regulatory Significance
column so an auditor can scan the system's regulatory data footprint.
