# Validation Plan (VP) — Reference File

## 1. Purpose

The Validation Plan defines the **what, who, when, and how** of the validation effort for a
specific computerized system. It governs all subsequent qualification activities and deliverables.

### VP vs VMP

| Document | Scope | Owner | Lifespan |
|---|---|---|---|
| **Validation Master Plan (VMP)** | Enterprise-wide validation policy across all systems | Customer QA | Persistent; updated annually |
| **Validation Plan (VP)** | Single-system project plan for one software implementation | Customer Validation Lead (with vendor input) | Project lifecycle; archived after VSR |

The VMP says "all systems shall be validated per GAMP 5." The VP says "here is how we
validate *this* system."

**Vendor framing:** The customer owns the VP. The vendor provides the **system-specific input
section** — system description, GAMP classification, recommended approach, test strategy, and
deliverables list. The customer wraps this into their corporate VP framework alongside SOPs,
organizational roles, and acceptance criteria. The vendor does **not** define acceptance
criteria, assign customer roles, or determine the overall validation strategy.

---

## 2. Predecessor Dependencies

**None.** The VP is written early to set scope. It benefits from these inputs when available:
- **URS** — sharpens scope with defined requirements
- **Vendor Assessment** — confirms vendor capability and GAMP assignment
- **Customer's VMP** — provides the corporate framework for alignment
- **Risk Assessment** — drives risk-based testing strategy

When generating before the URS exists, mark scope sections with
`<!-- TODO: Update after URS approval -->` and proceed.

---

## 3. Vendor's Deliverable Sections

### 3.1 System Description

```markdown
**System Name:** {system_name}  |  **Version:** {version}  |  **Vendor:** {vendor_name}

#### Overview
{2-3 paragraphs: purpose, primary functions, intended use in regulated environment.}

#### Architecture Summary
- **Deployment:** {on-premise | cloud | hybrid}
- **Architecture:** {client-server | web app | microservices}
- **Database:** {type and version}
- **Integrations:** {external systems}
- **Access method:** {browser | desktop | API | mobile}

#### Intended Use
{Regulated business processes supported. Reference 21 CFR Part 11, EU GMP Annex 11
only where the system directly supports compliance.}

#### System Boundaries
- **In scope:** {modules, functions, interfaces included}
- **Out of scope:** {excluded components, separately validated systems}
```

> **Coaching:** "If an auditor read only this section, would they understand what the system
> does, where it runs, and what regulated processes it touches?"

### 3.2 GAMP Classification

Per-component category assignment with rationale. See Section 8 for the assessment table.

### 3.3 Recommended Validation Approach

```markdown
Based on GAMP {category} classification and {low|medium|high} risk profile, the vendor
recommends a {prospective|concurrent} strategy:
- **Risk-based testing:** Effort concentrated on {high-risk areas}
- **Leveraged vendor testing:** {vendor test artifacts customer can leverage}
- **Critical thinking:** Per GAMP 5 2nd Ed / FDA CSA, testing prioritizes
  {patient safety | data integrity | product quality} over exhaustive coverage

#### Vendor Testing Already Performed
{Summary of internal testing — unit, integration, regression, performance — scope
and coverage. Do not share proprietary test cases.}
```

### 3.4 Suggested Test Strategy

| Qualification | Scope | Vendor Role | Customer Role |
|---|---|---|---|
| IQ | Installation, infrastructure, prerequisites | Author protocol, support execution | Execute, document, approve |
| OQ | Functional requirements, configurations, interfaces | Author protocol, provide expected results | Execute, document, approve |
| PQ | Business workflows, end-to-end in production | Provide scenario guidance | Author, execute, approve |

### 3.5 Vendor Deliverables List

| # | Deliverable | Format | Timing |
|---|---|---|---|
| 1 | Functional Specification | .docx | Before OQ |
| 2 | Design Specification | .docx | Before IQ |
| 3 | IQ Protocol | .docx | Before IQ execution |
| 4 | OQ Protocol | .docx | Before OQ execution |
| 5 | PQ Guidance | .docx | Before PQ authoring |
| 6 | Traceability Matrix | .docx/.xlsx | With protocols |
| 7 | Vendor Assessment Package | .docx | During vendor qualification |
| 8 | Release Notes | .pdf | Per release |

> **Coaching:** "Is every deliverable the customer expects listed? Are there gaps?"

---

## 4. GAMP 5 2nd Edition — The CSA Shift

GAMP 5 2nd Edition (2022) and FDA CSA guidance (September 2025) shift from **exhaustive
scripted testing** to **risk-based critical thinking**.

| Aspect | Traditional CSV | GAMP 5 2nd Ed / CSA |
|---|---|---|
| Testing philosophy | Test everything with scripted cases | Focus on patient safety, product quality, data integrity risk |
| Evidence model | Formal pre-approved protocol for every test | Exception-based: document deviations, not expected results |
| Vendor leverage | Customer re-tests everything | Leverage vendor testing; avoid redundancy |
| Documentation | More = more compliant | Right-sized; value over volume |
| Unscripted testing | Not acceptable | Explicitly encouraged |
| Risk assessment | Optional / checklist | Central driver of scope and depth |

The VP must explicitly state **CSA-aligned or traditional CSV**. This cascades to every
downstream document. When CSA-aligned: risk assessment drives scoping, unscripted testing
sections are permitted, evidence scales by risk not feature count, and vendor artifacts are
leveraged rather than duplicated.

> **Coaching:** "Has the customer adopted CSA? This fundamentally shapes the VP. Ask if unsure."

---

## 5. Annex 11 Clause Coverage in the VP

For customers subject to EU GMP, the VP must demonstrate traceability to all applicable
EU GMP Annex 11 clauses. The mapping below identifies how each key clause is addressed
within the VP and its referenced deliverables.

| Annex 11 Clause | Requirement | VP Section Addressing It | Notes |
|---|---|---|---|
| **Clause 1** — Risk Management | Integrate risk management throughout the computerized system lifecycle | VP risk assessment methodology; risk-based test scoping (Sections 3.3, 4) | The VP must reference the risk assessment methodology used and describe how risk drives validation scope, depth, and testing priority |
| **Clause 2** — Personnel | Trained personnel with defined roles and responsibilities | VP Roles and Responsibilities / RACI Matrix (Section 10) | Vendor provides system-specific training materials; the VP should reference training requirements and how competence is assured |
| **Clause 3** — Supplier/Service Provider | Supplier assessment, formal agreements, and documented responsibilities | VP references the Vendor Assessment deliverable (Section 3.5) | The VP should confirm that vendor qualification is complete or planned; formal quality agreements should be referenced |
| **Clause 4** — Validation | Life cycle approach, change control, and validation report | VP defines the lifecycle approach and references all V-model deliverables (Sections 3–4, 9) | The VP is itself the primary response to Clause 4; it must describe the full lifecycle from planning through summary report |
| **Clause 7** — Data Storage | Data protection, backup, and restore procedures | VP Test Strategy must include data integrity verification (Sections 3.4, 11) | IQ/OQ should verify backup configuration; PQ or operational procedures should verify restore capability and data integrity |
| **Clause 10** — Change and Configuration Management | Documented change control procedures | VP Post-Go-Live section addresses change control (Section 11) | The VP must reference the customer's change control SOP and describe how changes to the validated system are assessed and documented |
| **Clause 11** — Periodic Evaluation | Regular evaluation to confirm the system remains in a validated state | VP Periodic Review section defines review frequency and scope (Section 12) | The VP must state the periodic review frequency, scope, and responsible parties |
| **Clause 16** — Business Continuity | Arrangements for system breakdown or failure | VP should reference DR/BC testing requirements (Section 11) | The VP should describe or reference disaster recovery and business continuity testing; for cloud/SaaS, see Section 6 |

> **Note:** For customers subject to EU GMP, the VP must demonstrate compliance with ALL
> applicable Annex 11 clauses. This mapping ensures no clause is overlooked during validation
> planning. Clauses not listed above (e.g., Clause 5 — Data, Clause 6 — Accuracy Checks,
> Clause 8 — Printouts, Clause 9 — Audit Trails) should be addressed in the relevant
> downstream deliverables (FS, DS, IQ, OQ) and traced via the Traceability Matrix.

> **Coaching:** "Walk through each Annex 11 clause with the customer. Can they point to a
> specific VP section or deliverable that addresses it? If not, add it."

---

## 6. Cloud and SaaS Validation Considerations (GAMP 5 Appendix D7)

Cloud and SaaS deployments introduce a shared responsibility model where validation
activities are distributed across the cloud infrastructure provider, the application vendor,
and the customer. The VP must clearly document this division.

### 6.1 Shared Responsibility Model

The following table defines the typical division of validation responsibilities. The VP must
include a project-specific version adapted to the actual deployment model.

| Validation Activity | Cloud Provider | Application Vendor | Customer |
|---|---|---|---|
| Infrastructure qualification | Certifications (SOC 2, ISO 27001) | Deployment verification on provider platform | Acceptance of provider certifications; gap assessment |
| Application validation | N/A | IQ, OQ protocol authoring and support | PQ, VP, VSR authoring and approval |
| Security controls | Physical security, network infrastructure | Application-level security, access control framework | User management, security policies, access reviews |
| Backup and DR | Infrastructure-level backup and redundancy | Application data backup procedures | Verification of backup/restore, DR testing |
| Patch management | OS and infrastructure patching | Application patching and updates | Impact assessment, regression testing |
| Audit trail | Infrastructure logs (access, availability) | Application audit trails (data changes, user actions) | Review, retention, periodic audit trail assessment |

### 6.2 Cloud-Specific Validation Activities

The VP must address or reference the following cloud-specific validation activities:

- **Data residency verification:** Where is data stored, processed, and backed up? Confirm compliance with regional data sovereignty requirements.
- **Multi-tenancy isolation verification:** Confirm that data is logically or physically isolated from other tenants. Reference provider documentation and, where possible, include in OQ testing.
- **Service Level Agreement (SLA) validation:** Validate provider and vendor SLAs against the VP acceptance criteria for availability, performance, and support response.
- **Provider compliance certification review:** Review and document provider certifications (SOC 2 Type II, ISO 27001, ISO 27018, etc.) and assess coverage against validation requirements.
- **Network connectivity and latency validation:** Verify that network performance meets requirements for GxP-critical workflows, particularly for real-time data entry and electronic signatures.

> **Note:** Cloud provider certifications (SOC 2, ISO 27001) supplement but do NOT replace
> customer validation responsibilities per GAMP 5 Appendix D7. The customer must still
> perform risk-based validation of the application layer and business processes.

### 6.3 SaaS Update Management

SaaS delivery models mean the vendor or provider may initiate updates without the customer's
direct control. The VP must address how the validated state is maintained through updates:

- **Vendor-initiated updates:** Define the process for how the customer assesses the impact of vendor-initiated updates on the validated state. Reference the vendor's release notes and change classification process.
- **Regression testing strategy:** Define the customer's approach to regression testing after SaaS updates — full regression, risk-based targeted regression, or leverage of vendor regression evidence.
- **Communication protocol:** Document the notification process for updates affecting GxP-critical functionality, including advance notice period, change classification, and customer approval gates (where applicable).
- **Release notes template:** Reference the Vendor Assessment release notes template as the standard format for communicating changes, their classification, and their potential impact on the validated state.

> **Coaching:** "For SaaS systems, the VP must answer: 'What happens to our validated state
> when the vendor pushes an update?' If the answer is unclear, the VP has a gap."

---

## 7. Strategy Type Selection Table

| Strategy | When Used | VP Implications |
|---|---|---|
| **Prospective** | New implementation or major upgrade; system not yet live | Full IQ/OQ/PQ before production. Default for new systems. |
| **Concurrent** | Time-critical deployment with risk controls; phased rollout | Interim controls documented. Per-phase acceptance criteria. Justification required. |
| **Retrospective** | Legacy system in production with no prior validation | Operational data as evidence. Gap analysis drives scope. Document what cannot be verified retroactively. |

```
Is the system in production?
├── No → Time-critical with risk controls? → Yes: Concurrent / No: Prospective
└── Yes → Previously validated? → Yes but outdated: Re-validate / No: Retrospective
```

> **Coaching:** "Prospective is the default. Concurrent or retrospective requires documented
> justification — an auditor will ask for it."

---

## 8. GAMP Category Assessment Table

Each component receives an independent GAMP 5 category. A single system often spans
multiple categories.

| Category | Description | Examples | Validation Effort |
|---|---|---|---|
| **Cat 1** | Infrastructure software — OS, DB, middleware | Windows Server, Oracle DB | Verify installation and configuration only |
| **Cat 3** | Non-configured COTS used as-is | PDF viewers, file transfer tools | Verify installation; minimal functional testing |
| **Cat 4** | Configured products | LIMS workflows, ERP custom reports | Test configured functions against requirements |
| **Cat 5** | Custom applications | Custom integrations, bespoke engines | Full lifecycle; test all requirements; source review |

> **Note:** GAMP 5 2nd Ed discontinued **Category 2 (Firmware)**. Firmware is now Cat 1 or 3.
> Flag if the customer's VMP still references Cat 2.

**Per-component template:**

| Component | GAMP Cat | Rationale | Configured? | Custom Code? |
|---|---|---|---|---|
| {component} | Cat {n} | {justification} | Yes/No | Yes/No |

> **Coaching:** "Classify each component independently. The database may be Cat 1 while a
> custom integration is Cat 5. Blanket classification is an anti-pattern."

---

## 9. Deliverables Scaled by Category

| Deliverable | Cat 1 | Cat 3 | Cat 4 | Cat 5 |
|---|---|---|---|---|
| VP vendor input | Minimal | Brief | Standard | Comprehensive |
| URS | N/A | Reference vendor docs | Required | Required (detailed) |
| FS | N/A | Vendor datasheet | Required | Required (detailed) |
| DS | N/A | N/A | If complex config | Required |
| Traceability Matrix | N/A | Minimal | Required | Required (full) |
| Risk Assessment | Reference platform | Brief | Required | Required (detailed) |
| IQ Protocol | Checklist | Brief | Standard | Comprehensive |
| OQ Protocol | N/A | Spot-check | Full functional | Full + boundary + negative |
| PQ Protocol | N/A | Optional | Recommended | Required |

**Vendor deliverable scope indicators** (test cases and document pages the vendor will author — customer-side effort depends on their organization and integrator):

| Category | Vendor Test Cases | Vendor Doc Pages |
|---|---|---|
| Cat 1 | 5-15 | 10-20 |
| Cat 3 | 10-25 | 20-40 |
| Cat 4 | 20-60 | 50-120 |
| Cat 5 | 40-150+ | 100-300+ |

> **Coaching:** "If the customer wants Cat 5 deliverables for a Cat 3 product, flag
> over-validation. Cat 3 deliverables for Cat 5? Flag the gap. Note: timeline and
> total effort estimation is the integrator's or customer's responsibility, not the vendor's."

---

## 10. RACI Matrix Template

**R** = Responsible | **A** = Accountable | **C** = Consulted | **I** = Informed

### Vendor Deliverable Activities (vendor authors this section)

| Activity | Vendor PM | Vendor SME | Customer Reviewer |
|---|---|---|---|
| FS Authoring | A | R | C |
| DS Authoring | A | R | C |
| IQ Protocol Authoring | A | R | C |
| OQ Protocol Authoring | A | R | C |
| Traceability Matrix | R | C | A |
| Risk Assessment (initial) | R | R | A |
| Vendor Assessment Package | R | R | I |
| URS Starter Template | R | C | A |
| PQ Recommended Scenarios | C | R | A |

### Suggested Customer Activities (provided as a starting point — customer adapts to their organization)

The following is a template the customer's validation team can use as a starting point. The vendor does not assign roles within the customer's organization — this is the customer's decision.

| Activity | Val Lead | QA | IT | End Users |
|---|---|---|---|---|
| Validation Plan | R | A | I | I |
| URS Approval | R | A | I | C |
| IQ Execution | R | A | R | — |
| OQ Execution | R | A | I | C |
| PQ Execution | R | A | C | R |
| Deviation Management | R | A | C | I |
| Validation Summary | R | A | I | I |
| Change Control | R | A | C | I |

**Adapt for:** small orgs (merge Val Lead + QA but preserve A/R split), cloud/SaaS (add
Vendor Ops column), multi-site (add per-site PQ rows).

> **Coaching:** "Exactly one A per row. The vendor section is authoritative — you own those assignments. The customer section is a suggestion — present it as 'here's a typical RACI your validation team can adapt.'"

---

## 11. Post-Go-Live

Validation is a maintained state, not a one-time event.

### Periodic Review — Vendor Input

```markdown
- **Release frequency:** {quarterly major, monthly patches}
- **Release communication:** {notification method and timing}
- **Impact assessments:** {provided per release? Yes/No}
- **Regression evidence:** {summaries available for customer leverage? Yes/No}
- **Critical patch SLA:** {response time}
```

### Revalidation Triggers

| Trigger | Scope | Vendor Role |
|---|---|---|
| Major version upgrade | Full/partial revalidation per impact | Updated FS/DS, revised protocols |
| Minor update / patch | Regression; targeted revalidation | Release notes with change classification |
| Infrastructure change | IQ re-execution; targeted OQ | Compatibility statement |
| Customer config change | Targeted OQ; PQ if workflows affected | Consult on impact |
| Regulatory change | Gap assessment | Compliance statement |
| Security incident | Impact assessment; re-test if modified | Incident report, remediation summary |

### Change Communication

```markdown
- **Release notes:** {format, timing, distribution}
- **Advance notification:** {lead time for major changes}
- **Emergency notifications:** {process for urgent security/compliance issues}
```

---

## 12. Periodic Review Requirements

### 12.1 Regulatory Basis

- **EU GMP Annex 11 Clause 11:** "Computerised systems should be periodically evaluated to confirm that they remain in a valid state and are compliant with GMP."
- While **21 CFR Part 11** does not explicitly mandate periodic review, it is a widely adopted industry practice and GMP expectation. FDA investigators routinely ask for evidence that validated systems remain under control.

### 12.2 Vendor's Role

The vendor supports the customer's periodic review process by providing:

- **Periodic review guidance template** — a recommended structure and checklist the customer can adapt to their SOPs
- **System health metrics and diagnostics data** — performance data, error rates, and system availability statistics for the review period
- **Release notes and change log** — a consolidated summary of all changes (patches, updates, configuration changes) applied during the review period
- **Support for post-change review** — assistance in evaluating whether vendor-initiated changes have affected the validated state

### 12.3 Recommended Periodic Review Content

The following items should be evaluated at each periodic review. The VP must define which
items apply and who is responsible for each.

1. Review of all changes (vendor-initiated and customer-initiated) since last review or initial validation
2. Assessment of open deviations and CAPAs related to the system
3. Evaluation of system performance against PQ baseline metrics
4. Review of audit trail for anomalies (unauthorized access, unexplained data changes, failed login patterns)
5. Assessment of vendor support and patch status (are all critical patches applied?)
6. Review of user access list and role assignments (are accounts current? Are terminated users removed?)
7. Confirmation that SOPs remain current and aligned with system functionality
8. Review of training records (are all active users trained on the current version?)
9. Review of backup and restore verification records
10. Assessment of any regulatory changes that affect the system's compliance posture

**Recommended frequency:** Annually or after major releases — whichever is sooner. The VP
must state the chosen frequency and the rationale.

> **Coaching:** "Periodic review is not optional for EU GMP-regulated systems. Even for FDA-only
> customers, it is best practice. The VP must define the cadence — do not leave this to be
> decided after go-live."

---

## 13. System Retirement and Decommissioning

### 13.1 When This Section Applies

This section applies when a validated system reaches end-of-life, is replaced by a successor
system, or when the organization decides to discontinue use. The VP should address
decommissioning expectations at the planning stage — not as an afterthought when the system
is being retired.

### 13.2 Vendor's Role in Decommissioning

The vendor supports system retirement by providing:

- **Data export in open, readable formats** — all GxP-relevant data must be exportable in non-proprietary formats (e.g., CSV, XML, PDF/A) to ensure long-term accessibility independent of the vendor's application
- **Data structure and schema documentation** — complete documentation of database schemas, data relationships, and field definitions to enable future data access and interpretation without the original application
- **Decommissioning guidance document** — a vendor-authored guide describing the recommended decommissioning sequence, data export procedures, and verification steps
- **Data migration support** — assistance with migrating data to a successor system, including field mapping, data transformation, and migration verification (reference the Data Migration Protocol)

### 13.3 Key Decommissioning Requirements

- **Data Archival:** All GxP data must be archived in a format that remains accessible and readable for the entire regulatory retention period. Retention periods vary by predicate rule — typically 7-15 years post last use, but specific requirements depend on the applicable regulations (e.g., 21 CFR 211, EU GMP Chapter 4).
- **Archive Verification:** The decommissioning protocol must include verification that archived data is complete, readable, and retrievable. This means executing test retrievals and confirming data integrity against source records before the system is deactivated.
- **Continued Access:** Regulatory record retention requirements survive system retirement. The customer must maintain the ability to produce records for inspections regardless of whether the originating system is still operational.
- **Audit Trail Preservation:** Audit trail data must be archived alongside primary records. The audit trail must remain readable and attributable — meaning each audit trail entry must clearly identify the user, action, timestamp, and before/after values without requiring the original application to interpret it.
- **Reference Standards:** 21 CFR Part 11.10(c) (record retrieval), EU GMP Annex 11 Clause 7 (data storage), GAMP 5 Appendix D5 (operation and retirement).

> **Coaching:** "Decommissioning is a validation activity. The VP should address it even for
> new systems — auditors want to see that data lifecycle planning extends beyond go-live.
> Ask: 'If this system were retired tomorrow, could you produce every GxP record for an
> inspector?'"

---

## 14. Coaching Prompts

Organized by section for Phase 2 (Coached Refinement).

**System Description:** "Would an auditor understand purpose, scope, and regulated context?
Are boundaries explicit? All integration points listed?"

**GAMP Classification:** "Classified per-component or blanket? Any custom code hiding in a
Cat 4 system that should be Cat 5? Can you defend each classification to an auditor?"

**Validation Approach:** "CSA-aligned or traditional CSV? Leveraging vendor test evidence?
Approach proportionate to risk — not over- or under-validating?"

**Test Strategy:** "Does the IQ/OQ/PQ split match this system? High-risk functions getting
extra coverage? For concurrent: what interim controls are in place?"

**Deliverables:** "List matches customer expectations? Any gaps the customer needs that you
cannot provide? Timing realistic — protocols approved before execution?"

**Post-Go-Live:** "How will you communicate changes affecting validated state? Customer
understands their change control responsibility? Obligation if customer delays critical patch?"

**Annex 11 Compliance:** "Can the customer trace every applicable Annex 11 clause to a VP
section or deliverable? Are there gaps in the mapping?"

**Cloud/SaaS:** "Is the shared responsibility model clearly documented? Does the customer
understand what the provider certifications cover and what they must validate themselves?
How are vendor-initiated SaaS updates assessed for impact on validated state?"

**Periodic Review:** "Is the periodic review frequency defined? Does the customer know what
is evaluated at each review? Who owns the review — and is that person named?"

**Decommissioning:** "Has the VP addressed data lifecycle beyond go-live? Can GxP data be
exported in open formats? Will audit trails survive system retirement?"

---

## 15. Anti-Patterns

### AP-1: Blanket GAMP Classification
"The system is GAMP Category 4." Systems span categories. Classify per component (Section 8).

### AP-2: Copy-Paste VP with No System Specifics
Generic template with visible placeholders. Every section must contain system-specific content.

### AP-3: Vendor Overstepping Ownership
Vendor defines customer acceptance criteria or assigns customer roles. Use "vendor recommends"
language. Never write "the customer shall" in vendor input sections.

### AP-4: Missing CSA/CSV Stance
No explicit statement on CSA vs CSV approach. This decision shapes every downstream document.

### AP-5: No Revalidation Triggers
VP covers initial validation but nothing post-go-live. Include the triggers table (Section 11).

### AP-6: Deliverables Without Timing
Document names with no delivery timeline. Add timing column with at least relative milestones.

### AP-7: RACI with No Single Accountable Party
Rows with zero or multiple A assignments. Exactly one A per activity row.

### AP-8: Over-Validation of Low-Risk Components
Cat 1 with full OQ, or Cat 3 with Cat 5 documentation. Scale per Section 9.

### AP-9: No Annex 11 Clause Mapping
VP for EU GMP-regulated customer with no traceability to Annex 11 clauses. Use Section 5 mapping.

### AP-10: Undefined Shared Responsibility for Cloud/SaaS
Cloud-deployed system with no documented division of validation responsibilities between provider, vendor, and customer. Use Section 6 model.

### AP-11: No Periodic Review Plan
VP defines initial validation but does not address how the validated state is maintained over time. Include periodic review requirements (Section 12).

### AP-12: No Decommissioning Consideration
VP ignores data lifecycle and system retirement. Even for new systems, the VP should address how GxP data will be preserved when the system is eventually retired (Section 13).
