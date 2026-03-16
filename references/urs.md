# URS — User Requirements Specification Reference

## 1. Purpose

The URS defines **what** the system must do from the user's perspective — capabilities, constraints, and conditions — without prescribing **how**. It is the top of the V-model: every downstream document (FS, DS, IQ, OQ, PQ) traces back to URS requirements.

**Vendor role:** You draft a starter URS template pre-populated from discovery. Your customer owns, refines, and approves the final document. Your customer's QA team expects a URS that is auditable, traceable, and free of implementation language. Frame every coaching interaction accordingly: "This is your customer's document — you are making it easy for them to own it."

**Regulatory weight:** Auditors (FDA, EU) start from the URS and trace forward. A weak URS undermines the entire validation package. A strong URS makes every downstream document easier to write and defend.

## 2. Predecessor Dependencies

None. The URS sits at the top of the V-model. It may be informed by discovery outputs, the customer's validation master plan, or applicable regulatory requirements, but no other V-model document is required before drafting.

## 3. Required Sections

Generate all 18 sections below. Each section includes its heading, content guidance, and example content.

### 3.1 Document Control

Revision history table, approval signatures, distribution list. Your customer's QA team expects formal change control from the first approved version.

| Rev | Date | Author | Change Description | Approved By |
|-----|------|--------|--------------------|-------------|
| 0.1 | YYYY-MM-DD | [Author] | Initial draft | — |
| 1.0 | YYYY-MM-DD | [Author] | Approved for validation | [QA Head] |

### 3.2 Purpose and Scope

Why this document exists, what system it covers, what is explicitly out of scope. One paragraph each. Your customer's QA team expects the scope boundary to be unambiguous — auditors look here first to determine what was validated.

> *Example:* "This URS defines the user requirements for [System Name], a [brief description] used to [business process]. This document covers [in-scope items]. The following are explicitly excluded: [out-of-scope items]."

### 3.3 Definitions and Abbreviations

All domain-specific terms, abbreviations, and acronyms. Include both technical and regulatory terms. Reference the project glossary if one exists.

### 3.4 Referenced Documents

Standards, regulations, SOPs, and other documents referenced by requirements. Include document number, title, version, and relevance.

### 3.5 System Overview

High-level description of the system: what it does, where it fits in the customer's process, who uses it. No implementation detail.

### 3.6 Stakeholder Identification

List every role that interacts with or is affected by the system. For each stakeholder, identify their primary concerns. Your customer's QA team expects requirements to be traceable to specific user groups.

| Stakeholder | Role Description | Primary Concerns |
|-------------|-----------------|------------------|
| Production Operator | Executes batch records | Ease of use, GMP compliance |
| QA Reviewer | Reviews and approves records | Audit trail, data integrity |
| System Administrator | Manages users and configuration | Security, maintainability |

### 3.7 Business Process Requirements

Requirements about the business workflows the system must support. These are process-level, not feature-level.

> *Example:* "URS-BPR-001: The system shall support the batch disposition workflow from batch creation through QA release, including all intermediate review and approval steps, within the customer's existing SOP framework."

### 3.8 Functional Requirements

Core capabilities the system must provide. This is typically the largest section. Organize by functional area or user workflow. Every requirement uses the shall-statement format (see Section 4).

### 3.9 Data Requirements

What data the system must capture, store, calculate, and report. Include data types, retention periods, and migration needs.

### 3.10 Interface Requirements

All system interfaces: user interfaces (general expectations, not mockups), system-to-system interfaces, and hardware interfaces. Specify direction, protocol, and frequency.

### 3.11 Regulatory and Compliance Requirements

Requirements driven by regulations: 21 CFR Part 11, EU GMP Annex 11, ALCOA+ data integrity, electronic signatures, audit trails. Your customer's QA team expects these to be explicitly stated, not implied.

> *Example:* "URS-REG-001: The system shall maintain a time-stamped, immutable audit trail for all create, modify, and delete operations on GxP-critical data, capturing the user identity, timestamp, old value, new value, and reason for change."

### 3.12 Security Requirements

Authentication, authorization, role-based access, password policies, session management, data encryption.

### 3.13 Performance Requirements

Response times, throughput, concurrent users, data volumes. Every performance requirement must include a measurable threshold and the conditions under which it applies.

### 3.14 Availability and Reliability Requirements

Uptime targets, maintenance windows, disaster recovery, backup/restore, failover. Specify RPO and RTO.

### 3.15 Usability Requirements

Training expectations, accessibility, language/localization, error message clarity. Quantify where possible.

### 3.16 Migration and Data Conversion Requirements

Data migration from legacy systems: mapping expectations, validation of migrated data, rollback procedures.

### 3.17 Environment and Infrastructure Requirements

Hosting model (cloud, on-premise, hybrid), browser/OS compatibility, network requirements.

### 3.18 Support and Maintenance Requirements

Vendor support expectations, SLAs, upgrade/patch process, change notification, training for new releases.

## 4. Requirement Writing Format

Every requirement follows the **3-Element Model: Capability + Condition + Constraint**.

### Pattern

> **[ID]:** The system **shall** [CAPABILITY] [CONDITION] [CONSTRAINT].

| Element | Definition | Example |
|---------|-----------|---------|
| **Capability** | What the system does (verb + object) | "generate an audit trail entry" |
| **Condition** | When or under what circumstances | "when any GxP-critical field is modified" |
| **Constraint** | Measurable limit or quality bound | "within 1 second of the triggering event" |

### Rules

- **shall** = mandatory requirement (testable, traceable)
- **should** = desirable but not mandatory (use sparingly; auditors may challenge)
- **will** = statement of fact about the system or environment, not a requirement
- **may** = permissive, optional capability
- One requirement per statement. Compound requirements hide untested conditions.
- Every requirement must be verifiable by at least one IATD method (see Section 8).

## 5. NASA Forbidden Words

These words are **prohibited** in requirement statements because they introduce ambiguity, subjectivity, or unverifiable conditions. Flag any requirement containing them during coached refinement.

| Forbidden Word | Why It Fails | Fix Strategy |
|----------------|-------------|--------------|
| **adequate** | Subjective — adequate to whom? | Specify the measurable threshold |
| **as appropriate** | Defers decision to reader | State the specific conditions |
| **as a minimum** | Implies the stated value is negotiable | State the exact requirement |
| **be able to** | Ambiguous capability vs. actual behavior | Use "shall [verb]" directly |
| **but not limited to** | Unbounded scope | List all items explicitly |
| **capability of** | Indirect — state what the system does | Use "shall [verb]" directly |
| **effective** | Subjective measure | Define the measurable outcome |
| **etc.** | Unbounded, untestable | List all items explicitly |
| **if practical** | Escape clause — who decides? | Remove or state the condition |
| **easy** | Subjective | Quantify (e.g., "within 3 clicks") |
| **maximize** | No defined upper bound | State the specific target |
| **minimize** | No defined lower bound | State the specific target |
| **normal** | Undefined baseline | Specify the operating conditions |
| **reasonable** | Subjective judgment | State the measurable threshold |
| **several** | Vague quantity | State the exact number or range |
| **simple** | Subjective | Define the measurable criteria |
| **sufficient** | Subjective — sufficient for what? | State the measurable threshold |
| **support** | Vague capability | Specify the exact behavior |
| **timely** | Unmeasurable | State the time constraint |
| **user-friendly** | Entirely subjective | Specify usability criteria |

## 6. INCOSE 14 Characteristics of Well-Formed Requirements

Use this checklist during coached refinement. Every requirement should satisfy all 14 characteristics.

| # | Characteristic | Test Question |
|---|---------------|---------------|
| 1 | **Necessary** | If removed, would a capability gap exist? |
| 2 | **Appropriate** | Is this the right level of abstraction for a URS (not design)? |
| 3 | **Unambiguous** | Can two independent readers interpret it identically? |
| 4 | **Complete** | Does it contain all information needed to verify it? |
| 5 | **Singular** | Does it state exactly one requirement? |
| 6 | **Feasible** | Can current technology satisfy it within project constraints? |
| 7 | **Verifiable** | Can you write a pass/fail test for it? |
| 8 | **Correct** | Does it accurately reflect the stakeholder's actual need? |
| 9 | **Conforming** | Does it follow the project's requirement writing format? |
| 10 | **Free of implementation** | Does it say "what" without prescribing "how"? |
| 11 | **Traceable** | Does it have a unique ID and known origin? |
| 12 | **Allocated** | Is it assigned to a specific system component or function? |
| 13 | **Consistent** | Does it conflict with any other requirement? |
| 14 | **Non-redundant** | Is this requirement stated only once? |

## 7. Requirement Numbering

### Format

```
URS-[CATEGORY]-[NNN]
```

### Category Prefixes

| Prefix | Category |
|--------|----------|
| BPR | Business Process Requirements |
| FUN | Functional Requirements |
| DAT | Data Requirements |
| INT | Interface Requirements |
| REG | Regulatory and Compliance Requirements |
| SEC | Security Requirements |
| PRF | Performance Requirements |
| AVL | Availability and Reliability Requirements |
| USA | Usability Requirements |
| MIG | Migration and Data Conversion Requirements |
| ENV | Environment and Infrastructure Requirements |
| SUP | Support and Maintenance Requirements |

### Rules

- Numbers start at 001 and increment sequentially within each category.
- Deleted requirements are never reused — mark as "Deleted" with rationale.
- Sub-requirements use dot notation: URS-FUN-003.1, URS-FUN-003.2.
- The prefix is overridable in the project manifest if the customer has an existing convention.

## 8. IATD Verification Methods

Every requirement must be mapped to at least one verification method. The four methods (IATD):

| Method | Abbreviation | When to Use | Example |
|--------|-------------|-------------|---------|
| **Inspection** | I | Visual examination of the system, document review, code review | Verify a label appears on screen |
| **Analysis** | A | Mathematical or statistical evaluation, modeling, simulation | Verify a calculation algorithm |
| **Test** | T | Executing the system under controlled conditions with expected results | Verify a search returns results within 3 seconds |
| **Demonstration** | D | Operating the system to show capability without formal measurement | Verify a workflow can be completed end-to-end |

### Mapping in the URS

Include a verification method column in the requirements table:

| Req ID | Requirement | Priority | Verification |
|--------|------------|----------|-------------|
| URS-FUN-001 | The system shall... | Must | T |
| URS-REG-001 | The system shall... | Must | T, I |

## 9. Examples — Bad vs. Good Requirements

### Pair 1: Vague Performance

- **Bad:** "The system shall respond in a timely manner."
- **Good:** "URS-PRF-001: The system shall display the requested report within 5 seconds of the user submitting the query, when the report dataset contains up to 100,000 records and up to 25 users are concurrently active."
- **Why:** Replaces "timely" (NASA forbidden) with measurable condition and constraint.

### Pair 2: Implementation Leakage

- **Bad:** "The system shall use an Oracle 19c database to store batch records."
- **Good:** "URS-DAT-001: The system shall persistently store all batch records for the retention period defined in SOP-DI-003, with the ability to retrieve any individual record within 3 seconds."
- **Why:** URS states the need (persistent storage, retention, retrieval speed); the FS/DS chooses the database.

### Pair 3: Compound Requirement

- **Bad:** "The system shall enforce unique usernames, require passwords of at least 8 characters, and lock accounts after 3 failed attempts."
- **Good (split into 3):**
  - "URS-SEC-001: The system shall enforce unique user identifiers across all active accounts."
  - "URS-SEC-002: The system shall require passwords of at least 8 characters, containing at least one uppercase letter, one lowercase letter, one digit, and one special character."
  - "URS-SEC-003: The system shall lock a user account after 3 consecutive failed authentication attempts within a 15-minute window."
- **Why:** Each requirement is singular, independently testable, and independently traceable.

### Pair 4: Unbounded Scope

- **Bad:** "The system shall integrate with the customer's existing systems, including but not limited to the ERP, LIMS, and EDMS."
- **Good:** "URS-INT-001: The system shall provide a bidirectional data interface with the customer's ERP system (SAP S/4HANA) for batch record status updates. URS-INT-002: The system shall provide a read-only data interface with the customer's LIMS (LabWare 7) for pulling analytical results. URS-INT-003: The system shall provide a document retrieval interface with the customer's EDMS (Documentum) for linking controlled documents."
- **Why:** Eliminates "but not limited to" (NASA forbidden), specifies direction and scope per interface.

### Pair 5: Subjective Usability

- **Bad:** "The system shall be user-friendly and easy to learn."
- **Good:** "URS-USA-001: A trained operator shall be able to complete the batch record entry workflow within 10 minutes after completing the standard 4-hour training program. URS-USA-002: The system shall provide contextual help text for every data entry field accessible within one click of the field."
- **Why:** Replaces "user-friendly" and "easy" (both NASA forbidden) with measurable outcomes.

### Pair 6: Missing Condition

- **Bad:** "The system shall generate an audit trail."
- **Good:** "URS-REG-002: The system shall generate an audit trail entry for every create, modify, and delete action performed on GxP-critical records, capturing: user identity, date/time (UTC), action performed, field affected, previous value, new value, and reason for change."
- **Why:** Specifies the triggering condition, scope, and required data elements.

## 10. GAMP Category Selection Guidance

The GAMP 5 category determines the rigor of testing and documentation. Coach the customer to classify the system correctly — your customer's QA team expects a justified rationale, not a guess.

| Category | Description | Examples | URS Impact |
|----------|-------------|----------|------------|
| **1 — Infrastructure Software** | Operating systems, databases, middleware | Windows Server, Oracle DB, .NET runtime | Typically no URS needed; covered by IQ |
| **3 — Non-Configured** | Commercial off-the-shelf, used as-is | Standard label printers, barcode scanners | Lightweight URS; focus on intended use |
| **4 — Configured** | Commercial software configured (not coded) to meet user needs | LIMS, ERP modules, configured EDMS | Standard URS; requirements focus on configured behaviors |
| **5 — Custom** | Built to order; custom code | Bespoke applications, custom integrations | Full URS; most rigorous requirements |

Many real systems span categories (e.g., a configured LIMS with custom reports). Coach the customer to classify at the component level: "Your customer's QA team expects the GAMP category to be justified per component, not blanket-applied to the whole system."

## 11. Coaching Prompts

Use these section-by-section during Phase 2 (Coached Refinement). Each prompt targets a specific weakness pattern.

### Scope
- "Can you name one thing the system explicitly does NOT do? Defining the boundary prevents scope creep during validation."
- "If a regulator asked 'was X validated?' — would this scope statement give a clear yes or no?"

### Stakeholders
- "Who will be affected if this system goes down for 4 hours? Those are your stakeholders."
- "Is there a stakeholder who only interacts during exceptions (e.g., deviation handling)? They often get missed."

### Functional Requirements
- "For each requirement, can you describe a pass/fail test? If not, the requirement needs to be more specific."
- "Is this a user need or a design decision? If you're describing HOW the system works, it belongs in the FS."
- "Would a different vendor's system also need to meet this requirement? If yes, it belongs here. If no, it might be implementation."

### Regulatory Requirements
- "Does this system create, modify, store, or transmit GxP-critical electronic records? If yes, 21 CFR Part 11 / Annex 11 requirements are mandatory."
- "Have you stated the audit trail requirement explicitly, or are you assuming the vendor 'just does it'?"

### Performance Requirements
- "What is the worst acceptable response time, not the ideal one? Requirements define the floor."
- "Under what conditions? 10 users or 500? Morning batch processing or end-of-quarter reporting?"

### Data Requirements
- "What is the regulatory retention period for this data? Your customer's QA team will ask."
- "If the system were replaced in 5 years, how would this data be extracted? That is a requirement."

### Interface Requirements
- "For each interface, who initiates the data exchange? What happens when the other system is unavailable?"

## 12. Anti-Patterns

Flag these during coached refinement and reviewer checks.

| Anti-Pattern | Description | Fix |
|-------------|-------------|-----|
| **Wish list** | Requirements that describe nice-to-haves without priority | Assign Must/Should/Could priority per MoSCoW; remove "Could" items unless justified |
| **Copy-paste from vendor brochure** | Requirements that mirror vendor marketing language | Rewrite from the user's perspective — what business outcome is needed? |
| **Regulation by reference only** | "The system shall comply with 21 CFR Part 11" with no specifics | Decompose into testable sub-requirements (audit trail, e-sig, access control) |
| **Gold-plating** | Requirements far exceeding regulatory or business need | Challenge each requirement: "What is the cost of NOT having this?" |
| **Design masquerading as requirement** | "The system shall use REST APIs" or "The system shall use AES-256 encryption" | Rewrite as capability: "The system shall securely transmit data" — let DS/FS choose the mechanism |
| **Orphan requirements** | Requirements with no clear stakeholder or business justification | Trace back to a stakeholder need or remove |
| **Ambiguous priority** | All requirements marked "Must" | Force-rank using MoSCoW; a URS where everything is "Must" provides no guidance |
| **Missing negative requirements** | Only describes what the system does, never what it must NOT do | Add constraints: "The system shall NOT allow deletion of approved batch records" |

## 13. GAMP 5 Addenda

Include these additional sections when the project manifest sets `regulatory_context` to `gamp5`.

### 13.1 Intended Use Statement

A concise statement describing the GxP-regulated use of the system. Required by GAMP 5 as the foundation for risk-based validation.

> *Example:* "[System Name] is intended for use in the electronic creation, review, approval, and storage of batch production records within a GMP-regulated pharmaceutical manufacturing environment."

### 13.2 Initial Risk Assessment

A preliminary risk assessment identifying the GxP impact of each functional area. This feeds the risk-based testing strategy in the Validation Plan. Use a simple High/Medium/Low classification at the URS stage.

| Functional Area | GxP Impact | Rationale |
|----------------|-----------|-----------|
| Batch record entry | High | Direct impact on product quality and patient safety |
| User administration | Medium | Supports data integrity controls |
| Report generation | Low | Informational; not used for release decisions |

### 13.3 Data Integrity (ALCOA+) Requirements

Explicitly map requirements to ALCOA+ principles where applicable:

| Principle | Meaning | URS Requirement Example |
|-----------|---------|------------------------|
| **A**ttributable | Who performed the action and when | Audit trail with user identity and timestamp |
| **L**egible | Data is readable and permanent | Data display and print formatting requirements |
| **C**ontemporaneous | Recorded at time of activity | Real-time data capture, no backdating |
| **O**riginal | First capture or certified copy | Original record preservation, certified copy process |
| **A**ccurate | Error-free, reflecting actual observation | Validation rules, input checks |
| **+Complete** | All data present, no deletions | Append-only audit trail, no record deletion |
| **+Consistent** | Chronological, time-stamped sequence | Synchronized timestamps, ordered event logs |
| **+Enduring** | Retained for required lifetime | Data retention and archival requirements |
| **+Available** | Accessible for review throughout retention | Data retrieval, search, and export requirements |

### 13.4 Supplier Requirements

Requirements the customer places on the vendor as a supplier within the GAMP 5 framework: quality management system documentation, change control and notification process, incident and defect management, release and upgrade procedures, support and service level commitments.

### 13.5 CSA Considerations

When the customer follows FDA's Computer Software Assurance (CSA) guidance (September 2025):

- Risk-rank requirements to enable risk-based testing (critical thinking, not scripted testing for low-risk items)
- Distinguish requirements supporting critical GxP processes vs. supporting/convenience functions
- Critical process requirements warrant full scripted testing (OQ); non-critical may use unscripted/ad hoc approaches

## 14. Override Points

These are locations where company-specific content can be injected via the project manifest's `section_overrides` configuration.

| Override Key | Section Affected | Default Behavior |
|-------------|-----------------|------------------|
| `urs.document_control_template` | 3.1 Document Control | Standard revision history table |
| `urs.custom_sections_after_scope` | After 3.2 | None — insert customer's standard sections (e.g., Quality Risk Management) |
| `urs.requirement_categories` | 7. Requirement Numbering | Default 12 category prefixes |
| `urs.priority_scheme` | Requirement tables | MoSCoW (Must/Should/Could/Won't) |
| `urs.custom_sections_before_appendix` | End of document body | None — insert customer's standard appendices |
| `urs.approval_workflow` | 3.1 Document Control | Single approval signature block |
| `urs.id_prefix` | 7. Requirement Numbering | "URS" — overridable to match customer convention |
| `urs.regulatory_sections` | 13. GAMP 5 Addenda | Included when `regulatory_context: gamp5` |

### Adding Custom Sections

In the project manifest, add entries under `section_overrides.urs.[override_key]` with `heading`, `guidance`, and `required` fields. Custom sections are inserted at the specified override point and follow the same coaching and review rules as standard sections.
