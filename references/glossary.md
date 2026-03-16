# Glossary Reference

Reference file for the v-model-docs skill. Loaded into context when generating or reviewing validation documents. Definitions are written for software vendors delivering to life sciences customers.

---

## GAMP 5 Software Categories

Categories define the expected validation effort. From GAMP 5 Second Edition (ISPE, 2022).

| Cat | Name | Description | Validation Approach |
|-----|------|-------------|---------------------|
| 1 | Infrastructure Software | OS, databases, middleware, firmware. No business logic configuration. | Record version, verify installation. Minimal testing. |
| 2 | *(Discontinued)* | Formerly "firmware." Merged into Cat 1 in GAMP 5 First Edition (2008). Referenced in legacy documents only. Do not assign Cat 2 to new systems. | N/A |
| 3 | Non-Configured Product | Commercial off-the-shelf (COTS) used as-is. No user-configurable business rules. | Verify installation, confirm intended use. Leverage vendor testing. |
| 4 | Configured Product | COTS with user-configurable business rules, workflows, or parameters. | Verify configuration matches requirements. Test configured functions. Risk-based scope. |
| 5 | Custom Application | Bespoke software or heavily customized product. Full SDLC applies. | Full V-model lifecycle: URS, FS, DS, IQ, OQ, PQ. Highest validation burden. |

**Skill usage:** GAMP category drives template scaling throughout the skill. Cat 3 projects get lighter IQ/OQ protocols; Cat 5 gets full depth.

---

## 21 CFR Part 11 Key Terms

FDA regulation governing electronic records and electronic signatures for predicate rule compliance.

- **Electronic Record** — Any combination of text, graphics, data, audio, or pictorial information in digital form that is created, modified, maintained, archived, retrieved, or distributed by a computer system.
- **Electronic Signature** — A computer data compilation of any symbol or series of symbols executed, adopted, or authorized by an individual to be the legally binding equivalent of a handwritten signature.
- **Audit Trail** — Secure, computer-generated, time-stamped record that independently records the date and time of operator entries and actions that create, modify, or delete electronic records. Must capture who, what, when, and why.
- **Authority Check** — System control ensuring only authorized individuals can use the system, electronically sign a record, access the operation or device, or alter a record.
- **Closed System** — An environment in which system access is controlled by persons responsible for the content of electronic records on that system.
- **Open System** — An environment in which system access is NOT controlled by persons responsible for the content of electronic records. Requires additional controls (encryption, digital signatures).

---

## ISO/IEC/IEEE 12207 Lifecycle Process Terms

International standard for software lifecycle processes. Provides the generic V-model backbone.

- **Acquirer** — Organization that obtains a system or software product. In pharma context: the regulated customer.
- **Supplier** — Organization that provides a system or software product. In pharma context: the software vendor.
- **Stakeholder Requirements Definition** — Process of defining requirements from the perspective of all stakeholders. Maps to URS in pharma.
- **System Requirements Analysis** — Transforming stakeholder requirements into a set of system technical requirements. Maps to FS.
- **Architectural Design** — Defining the structure and interfaces of system components. Maps to DS.
- **Verification** — Confirmation through objective evidence that specified requirements have been fulfilled. ("Did we build the thing right?")
- **Validation** — Confirmation through objective evidence that the requirements for a specific intended use have been fulfilled. ("Did we build the right thing?")
- **Integration** — Combining software units and components and verifying their interaction.
- **Qualification Testing** — Testing to demonstrate the integrated system meets its requirements in the target environment.
- **Baseline** — A formally approved version of a configuration item, regardless of media, formally designated and fixed at a specific time during the item's lifecycle.
- **Configuration Item** — An entity within a configuration that satisfies an end-use function and can be uniquely identified at a given reference point.

---

## V-Model Naming Map

The same testing levels have different names in pharma and software engineering. This table maps equivalents.

| V-Model Level | Pharma / GxP Term | Software Engineering Term | Verifies Against |
|---------------|-------------------|--------------------------|------------------|
| Unit level | Component Testing | Unit Testing | Code / detailed design |
| Installation level | IQ (Installation Qualification) | Installation Verification / SAT | Design Specification |
| System level | OQ (Operational Qualification) | System Testing / FAT | Functional Specification |
| Acceptance level | PQ (Performance Qualification) | UAT (User Acceptance Testing) | User Requirements (URS) |

**Important distinctions:**
- **IQ** focuses on verified installation in the target environment (infrastructure, versions, configuration). **SAT** (Site Acceptance Testing) is the closest industrial equivalent but emphasizes site-specific conditions.
- **OQ** tests that the system operates according to its functional specification across defined operating ranges. **FAT** (Factory Acceptance Testing) is performed at the vendor site before delivery.
- **PQ** tests that the system performs as intended in actual use with real workflows and production-like data. **UAT** is the closest software equivalent but PQ often includes reproducibility requirements (e.g., 3 consecutive successful runs).

---

## Verification vs Validation

These terms are frequently conflated. The distinction matters for document scoping.

| | Verification | Validation |
|---|---|---|
| **Question** | Did we build the thing right? | Did we build the right thing? |
| **Compares** | Output against its input specification | System against user needs and intended use |
| **Performed by** | Development team (often vendor) | End users or their delegates (often customer) |
| **V-model side** | Left side (descending: URS -> FS -> DS) | Right side (ascending: IQ -> OQ -> PQ) |
| **Example** | Code review confirms DS section 3.2 is implemented correctly | PQ confirms the system supports the customer's actual workflow |
| **FDA language** | "Confirmation that design outputs meet design inputs" | "Confirmation that user needs and intended uses are met" |

---

## Regulatory Acronyms

| Acronym | Full Term | Context |
|---------|-----------|---------|
| FDA | Food and Drug Administration | US regulatory body for drugs, biologics, devices, food |
| GxP | Good _x_ Practice | Umbrella term: GMP, GLP, GCP, GDP, etc. The "x" is a placeholder. |
| GMP | Good Manufacturing Practice | Regulations ensuring products are consistently produced and controlled to quality standards |
| GAMP | Good Automated Manufacturing Practice | ISPE guidelines for validation of computerized systems in pharma. Current: GAMP 5 2nd Ed (2022) |
| CSV | Computer System Validation | Traditional approach: validate the system through documented evidence of testing. Being superseded by CSA. |
| CSA | Computer Software Assurance | FDA's risk-based alternative to traditional CSV. Emphasizes critical thinking over scripted testing. Verify the current guidance version and Federal Register citation for your regulatory submission — guidance versions evolve. |
| SLC | Software Lifecycle | The full lifecycle of a software product from concept through retirement |
| SDLC | Software Development Lifecycle | The development portion of the SLC: requirements through release |
| UAT | User Acceptance Testing | Testing performed by end users to confirm the system meets their requirements |
| FAT | Factory Acceptance Testing | Testing performed at the vendor's site before delivery to the customer's environment |
| SAT | Site Acceptance Testing | Testing performed at the customer's site after installation |
| VP | Validation Plan | Document defining the validation strategy, scope, roles, and deliverables |
| VMP | Validation Master Plan | Corporate-level document governing validation across multiple systems (customer-owned) |
| VSR | Validation Summary Report | Final document summarizing validation activities, results, and the validation decision |

---

## Risk Assessment Terms

Used in risk-based validation planning and deviation handling.

- **FMEA** — Failure Mode and Effects Analysis. Systematic method for evaluating where and how a process or design might fail and the relative impact of those failures.
- **Severity (S)** — Rating (typically 1-5 or 1-10) of how serious the consequence of a failure mode would be. Patient safety impact raises severity to maximum.
- **Occurrence (O)** — Rating of how likely the failure mode is to occur, based on design controls and historical data.
- **Detectability (D)** — Rating of how likely the failure would be detected before it reaches the end user. Lower detectability = higher risk.
- **RPN** — Risk Priority Number. Calculated as S x O x D. Used to prioritize which risks require mitigation. Higher RPN = higher priority.
- **AP** — Action Priority. FMEA supplement (AIAG/VDA, 2019) replacing RPN with a structured priority matrix. Produces High / Medium / Low action priority without the mathematical flaws of RPN multiplication.

**Skill usage:** Risk assessment determines testing depth per requirement. High-severity items require explicit test cases; low-risk items may use verification by inspection under CSA.

---

## Data Integrity: ALCOA+

Framework for data integrity in regulated environments. Originally FDA guidance; now globally adopted.

### Core ALCOA

| Letter | Principle | Definition |
|--------|-----------|------------|
| **A** | Attributable | Data must identify who performed an action and when. Every entry traceable to the person who created it. |
| **L** | Legible | Data must be readable and permanently recorded. Entries must remain legible throughout the retention period. |
| **C** | Contemporaneous | Data must be recorded at the time the activity is performed. No backdating, no retrospective entries. |
| **O** | Original | Data must be the first recording (or a certified true copy). Source data preserved; no undocumented transcription. |
| **A** | Accurate | Data must be correct, truthful, and free from errors. Editing must not obscure original entries (no deletion without audit trail). |

### The "+" Additions

| Principle | Definition |
|-----------|------------|
| **Complete** | All data must be present, including any repeat or reanalysis results. No selective reporting. |
| **Consistent** | Data elements must be internally consistent with timestamps and event sequences. No contradictions. |
| **Enduring** | Data must be durable and available for the entire retention period. Media, format, and storage must ensure long-term accessibility. |
| **Available** | Data must be accessible for review and audit throughout its lifecycle. Retrievable when needed. |

**Skill usage:** OQ protocol test scripts must satisfy ALCOA+ — each test step captures who, what, when, expected result, actual result, and pass/fail.

---

## Change Control Terms

- **CR** — Change Request. Formal proposal to modify a validated system. Initiates impact assessment and approval workflow.
- **CAPA** — Corrective and Preventive Action. Corrective: eliminates the cause of an existing nonconformity. Preventive: eliminates the cause of a potential nonconformity.
- **Deviation** — Departure from an approved instruction or established standard. Requires documentation, root cause analysis, and impact assessment.
- **Revalidation** — Partial or full re-execution of validation activities after a change to a validated system. Scope determined by change impact assessment.
- **Baseline** — The approved, frozen configuration of a system at a point in time. All changes are measured against the baseline. Post-IQ baseline capture is mandatory.

---

## Commonly Confused Terms

### CSV vs CSA
- **CSV (Computer System Validation):** Traditional approach. Heavy documentation, scripted test protocols for every requirement, comprehensive IQ/OQ/PQ. Driven by GAMP 5.
- **CSA (Computer Software Assurance):** FDA's risk-based evolution. Critical thinking over rote scripting. High-risk functions get rigorous testing; low-risk functions may use ad hoc or unscripted testing. Does not eliminate documentation — redirects effort to where risk exists.
- **Key difference:** CSV asks "did we document everything?" CSA asks "did we test the right things?"

### URS vs FS
- **URS (User Requirements Specification):** What the user needs the system to do, stated in user language. Business requirements, process requirements, regulatory requirements. Owned by the customer.
- **FS (Functional Specification):** How the system will fulfill those requirements, stated in technical/system language. System behaviors, interfaces, data handling, error handling. Owned by the vendor.
- **Key difference:** URS says "the system shall allow authorized users to electronically sign batch records." FS says "the system shall present a signature dialog requiring user ID, password, and signing meaning from a configurable list per 21 CFR 11.50."

### IQ vs SAT
- **IQ (Installation Qualification):** Pharma protocol verifying that the system is installed correctly per the design specification. Documented with pre-approved test scripts.
- **SAT (Site Acceptance Testing):** Industrial/engineering test verifying that equipment functions correctly at the customer's site. Less formal documentation framework.
- **Key difference:** IQ is a GxP-regulated activity with formal protocol approval, execution, and deviation handling. SAT is a contractual milestone.

### Validation vs Compliance
- **Validation:** Documented evidence that a system consistently produces results meeting predetermined specifications and quality attributes.
- **Compliance:** State of conforming to applicable regulations, standards, and guidelines.
- **Key difference:** A system can be validated but non-compliant (e.g., validated system lacking adequate access controls under Part 11). Validation is a subset of compliance.

### Risk-Based vs Reduced Testing
- **Risk-based testing:** Allocating testing effort proportional to risk. High-risk items get more test cases, more rigor, more independence. Low-risk items get leaner but still documented testing.
- **Reduced testing:** Simply doing less testing. No risk justification.
- **Key difference:** CSA promotes risk-based testing, not reduced testing. An auditor will accept risk-justified lean testing but will not accept unjustified gaps.

---

## IEC 62443 Security Terms

Industrial automation and control systems security. Relevant when the validated system operates in an industrial environment or processes data crossing network boundaries.

### Security Levels (SL)

| Level | Name | Protection Against |
|-------|------|-------------------|
| SL 0 | None | No specific requirements |
| SL 1 | Casual | Casual or coincidental violation (unintentional errors) |
| SL 2 | Intentional (Low) | Intentional violation using simple means, low resources, generic skills |
| SL 3 | Intentional (Sophisticated) | Intentional violation using sophisticated means, moderate resources, IACS-specific skills |
| SL 4 | State-Sponsored | Intentional violation using sophisticated means with extended resources and nation-state capabilities |

### Zone and Conduit Model

- **Zone** — A logical or physical grouping of assets that share common security requirements. Each zone is assigned a target security level.
- **Conduit** — A logical grouping of communication channels connecting zones. Each conduit must meet the security level of the higher-risk zone it connects.
- **Security context for validation:** When a validated system spans multiple zones (e.g., manufacturing floor + enterprise network), the DS must document zone boundaries, conduit protections, and the target SL per zone. IQ verifies that network segmentation and access controls match the DS.

---

## Quick Reference: Document Abbreviations Used in This Skill

| Abbreviation | Document |
|--------------|----------|
| URS | User Requirements Specification |
| FS | Functional Specification |
| DS | Design Specification |
| VP | Validation Plan |
| IQ | Installation Qualification Protocol |
| OQ | Operational Qualification Protocol |
| PQ | Performance Qualification Protocol |
| TM | Traceability Matrix |
| VSR | Validation Summary Report |
| VA | Vendor Assessment Package |
| ADR | Architecture Decision Record |
