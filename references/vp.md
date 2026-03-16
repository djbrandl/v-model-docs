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

Per-component category assignment with rationale. See Section 6 for the assessment table.

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

## 5. Strategy Type Selection Table

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

## 6. GAMP Category Assessment Table

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

## 7. Deliverables Scaled by Category

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

## 8. RACI Matrix Template

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

## 9. Post-Go-Live

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

## 10. Coaching Prompts

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

---

## 11. Anti-Patterns

### AP-1: Blanket GAMP Classification
"The system is GAMP Category 4." Systems span categories. Classify per component (Section 6).

### AP-2: Copy-Paste VP with No System Specifics
Generic template with visible placeholders. Every section must contain system-specific content.

### AP-3: Vendor Overstepping Ownership
Vendor defines customer acceptance criteria or assigns customer roles. Use "vendor recommends"
language. Never write "the customer shall" in vendor input sections.

### AP-4: Missing CSA/CSV Stance
No explicit statement on CSA vs CSV approach. This decision shapes every downstream document.

### AP-5: No Revalidation Triggers
VP covers initial validation but nothing post-go-live. Include the triggers table (Section 9).

### AP-6: Deliverables Without Timing
Document names with no delivery timeline. Add timing column with at least relative milestones.

### AP-7: RACI with No Single Accountable Party
Rows with zero or multiple A assignments. Exactly one A per activity row.

### AP-8: Over-Validation of Low-Risk Components
Cat 1 with full OQ, or Cat 3 with Cat 5 documentation. Scale per Section 7.
