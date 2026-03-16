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

### The Predicate Rule Concept

Part 11 is one of the most commonly misunderstood FDA regulations. Many vendors incorrectly treat 21 CFR Part 11 as a standalone regulation — it is not. Part 11 applies **only** when existing ("predicate") regulations already require records to be maintained or submitted electronically. Part 11 supplements those predicate rules; it does not create independent requirements.

**What are predicate rules?** Predicate rules are the underlying GxP regulations that govern a customer's operations. Examples:

| Predicate Rule | Scope |
|----------------|-------|
| 21 CFR Part 211 | Current Good Manufacturing Practice for finished pharmaceuticals |
| 21 CFR Part 820 | Quality System Regulation for medical devices |
| 21 CFR Part 606 | Current Good Manufacturing Practice for blood and blood components |
| 21 CFR Part 58 | Good Laboratory Practice for nonclinical laboratory studies |

**Why this matters for vendors:**

- The scope of Part 11 compliance depends entirely on which predicate rules apply to the customer's operations. A vendor's system may be subject to different Part 11 requirements depending on the customer's regulatory context.
- If a predicate rule does not require records to be maintained electronically, Part 11 does not apply to those records — even if the system stores them electronically by choice.
- Vendors should identify the customer's applicable predicate rules during discovery (URS phase) to correctly scope Part 11 requirements in the FS and DS.
- Do not make blanket "Part 11 compliant" claims without understanding the predicate rule context. An auditor will ask which predicate rules drive the Part 11 requirements — have the answer ready.

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

### ISO 12207 Process-to-V-Model Document Mapping

This table maps ISO/IEC/IEEE 12207 lifecycle processes to the V-model documents produced by this skill. Use this mapping to demonstrate standards alignment in vendor assessments and validation plans.

| ISO 12207 Process | Process Category | V-Model Document(s) | Notes |
|--------------------|------------------|----------------------|-------|
| Stakeholder Requirements Definition | Technical | URS | Captures user needs, business requirements, and regulatory requirements from all stakeholders |
| System/Software Requirements Analysis | Technical | FS | Transforms stakeholder requirements into system-level technical requirements |
| Architectural Design | Technical | DS | Defines system structure, component interfaces, and technology stack decisions |
| Implementation | Technical | *Vendor's internal development — outside validation scope* | Vendor SDLC produces the software; validation documents verify the output, not the coding process |
| Integration | Technical | OQ (integration test cases within OQ) | Integration verification is embedded in OQ test cases that exercise cross-component interactions |
| Verification | Technical | IQ, OQ | IQ verifies installation against DS; OQ verifies system behavior against FS |
| Validation | Technical | PQ | PQ confirms the system meets user needs and intended use per the URS |
| Transition | Technical | IQ (installation verification), Data Migration Protocol | IQ covers deployment to the target environment; data migration protocol covers legacy data transfer |
| Maintenance | Technical | VP post-go-live section | VP defines the ongoing maintenance, change control, and periodic review strategy |
| Supply | Agreement | Vendor Assessment | Vendor assessment evaluates the supplier's QMS, development practices, and support capability |
| Acquisition | Agreement | URS, VP (customer-owned) | Customer-side documents defining what is being acquired and how it will be validated |
| Risk Management | Technical Management | Risk Assessment | FMEA-based risk assessment drives testing depth and scope across all qualification protocols |
| Configuration Management | Technical Management | DS Section 9, VP | DS documents configuration baselines; VP defines configuration management procedures for the validation lifecycle |
| Quality Assurance | Organizational | Vendor Assessment QMS sections, VP | Vendor assessment covers supplier QMS; VP defines quality assurance activities for the validation project |
| Decision Management | Technical Management | DS ADRs (Architecture Decision Records) | ADRs capture and justify significant design decisions with rationale and alternatives considered |
| Measurement | Technical Management | Traceability Matrix metrics, VSR | TM provides coverage metrics; VSR summarizes quantitative validation outcomes |

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
| CSA | Computer Software Assurance | FDA's risk-based alternative to traditional CSV. Emphasizes critical thinking over scripted testing. **Caveat:** The FDA CSA final guidance publication date should be verified against the Federal Register before citing in regulatory submissions. Dates referenced in this skill (e.g., "September 2025") reflect the status at the time of authoring. Always confirm the current publication status and use the official Federal Register citation — guidance versions evolve and draft dates may shift. |
| SLC | Software Lifecycle | The full lifecycle of a software product from concept through retirement |
| SDLC | Software Development Lifecycle | The development portion of the SLC: requirements through release |
| UAT | User Acceptance Testing | Testing performed by end users to confirm the system meets their requirements |
| FAT | Factory Acceptance Testing | Testing performed at the vendor's site before delivery to the customer's environment |
| SAT | Site Acceptance Testing | Testing performed at the customer's site after installation |
| VP | Validation Plan | Document defining the validation strategy, scope, roles, and deliverables |
| VMP | Validation Master Plan | Corporate-level document governing validation across multiple systems (customer-owned) |
| VSR | Validation Summary Report | Final document summarizing validation activities, results, and the validation decision |

### International Regulatory Context

This skill focuses on FDA (21 CFR Part 11) and EU GMP (Annex 11) as the two most commonly encountered frameworks for computerized system validation. Vendors serving additional markets should consult local guidance, including:

- **Japan PMDA** — ERES Guidelines (Electronic Records and Electronic Signatures). Japan's equivalent framework for electronic records, closely aligned with Part 11 concepts but with PMDA-specific interpretation.
- **China NMPA** — GMP Annex on Computerised Systems. China's evolving requirements for computerized systems within pharmaceutical manufacturing.
- **Brazil ANVISA** — RDC 658/2022 (GMP for medical devices) and related guidance. Brazil's regulatory framework incorporates computerized system requirements within its GMP regulations.
- **Australia TGA** — PIC/S guidance (aligned with EU GMP Annex 11). Australia adopts PIC/S guidelines, making Annex 11 alignment the practical path for TGA compliance.
- **WHO** — Technical Report Series on computerised systems. Relevant for vendors supplying to WHO-prequalified manufacturing sites or emerging markets that adopt WHO guidance.

PIC/S (Pharmaceutical Inspection Co-operation Scheme) provides harmonized GMP inspection guidance adopted by 54 participating authorities. Vendors targeting multiple international markets can use PIC/S alignment as a baseline that satisfies most participating regulatory bodies.

The V-model documentation approach in this skill is generally compatible with these frameworks. Adjustments may be needed for jurisdiction-specific requirements — particularly around local language translation, national data residency rules, and market-specific submission formats.

---

## Part 11 vs Annex 11 Divergences

Vendors serving both US and EU customers encounter significant differences between 21 CFR Part 11 and EU GMP Annex 11. These divergences affect system design, documentation, and validation scope.

| Topic | 21 CFR Part 11 | EU GMP Annex 11 | Implication for Vendors |
|-------|----------------|-----------------|-------------------------|
| **Periodic evaluation** | No explicit mandate for periodic revalidation. Systems remain in a validated state until a change triggers revalidation. | Clause 11 requires periodic evaluation confirming the system remains in a validated state. | EU customers will expect scheduled periodic reviews. Build reporting and review workflows into the system or documentation. |
| **Business continuity** | No Part 11 equivalent. Business continuity is addressed by other regulations or left to the organization. | Clause 16 requires arrangements for system breakdown, including manual fallback processes and data recovery. | Vendors must document continuity and recovery procedures for EU-facing deployments. DS and VP should address failure scenarios. |
| **Audit trails** | 11.10(e) requires audit trails for all electronic record changes. Broad, prescriptive requirement. | Clause 9 takes a risk-based approach. Configuration changes and GxP-critical data require audit trails; not every interaction needs full audit trailing. | Design audit trails to cover all record changes (satisfying Part 11), but allow risk-based configuration of audit trail scope to avoid audit fatigue for EU customers. |
| **Cloud/hosted systems** | Addressed via the open/closed system framework (11.10 for closed systems, 11.30 for open systems). No cloud-specific provisions. | Clause 3.4 has specific requirements for service providers, including contracts, audits, and data availability guarantees. | Cloud-deployed systems need explicit service provider qualification documentation for EU customers. Include cloud architecture and SLA details in the DS. |
| **Training** | 11.10(i) requires training for individuals who develop, maintain, or use electronic record/signature systems. | Clause 2 also requires training but scopes it to include education, training, and experience appropriate to the task. Broader competency framing. | Training documentation must cover both technical system training (Part 11) and role-appropriate competency (Annex 11). Vendor training materials should address both angles. |
| **Risk management** | Does not prescribe a specific risk methodology. Risk-based approaches are endorsed by FDA CSA guidance but not mandated by Part 11 itself. | Clause 1 explicitly requires risk management throughout the computerized system lifecycle. Risk assessment is a formal prerequisite. | Always perform and document risk assessment. For EU customers it is mandatory; for US customers it is best practice and supports CSA alignment. |
| **Data storage/archival** | 11.10(c) covers protection of records to enable accurate and ready retrieval throughout the retention period. | Clause 7 has specific requirements for damage protection, accessibility, readability, and accuracy checks throughout the retention period. More prescriptive on storage conditions. | Design data archival with Annex 11 Clause 7 as the baseline — it is the more detailed requirement. Address format migration, media integrity, and periodic readability verification. |

> **Note:** Vendors serving both US and EU customers must design for the **more restrictive** requirement in each area, or implement configurable controls that satisfy both frameworks. When in doubt, Annex 11 is generally the more prescriptive framework — designing to Annex 11 requirements typically satisfies Part 11 as well, but not always in reverse.

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
