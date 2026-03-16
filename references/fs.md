# Functional Specification (FS) — Reference

## 1. Purpose

The Functional Specification is the vendor's primary promise of system behavior. It answers: "What will the system observably do?" — without prescribing how.

The FS decomposes every URS requirement into concrete, testable system behaviors. Each FS requirement must be specific enough to write an OQ test script against, yet abstract enough that swapping the underlying technology would not invalidate the specification.

**Audience:** Customer QA, validation leads, subject matter experts, auditors.
**Ownership:** Vendor-owned, customer-approved.
**V-model pairing:** FS requirements are verified by OQ (Operational Qualification) test scripts. Every FS requirement must have at least one OQ test case; every OQ test case must trace to at least one FS requirement.

**GAMP 5 context:** For Category 4 (configured products), the FS documents configurable parameters and their expected behaviors. For Category 5 (custom applications), the FS is the most scrutinized vendor deliverable — auditors will read it line by line.

---

## 2. Predecessor Dependencies

| Document | Relationship |
|---|---|
| **URS (required)** | Every FS requirement must trace backward to one or more URS requirements. The URS is the input; the FS is the decomposition. |
| **Validation Plan (recommended)** | Provides scope boundaries, GAMP category, and regulatory context that shape FS depth. |
| **Vendor Assessment (optional)** | GAMP category justification per component may influence how deeply the FS specifies behavior. |

If the URS does not exist, the skill will offer to backfill one from FS content. This is a red flag — document the gap in the traceability matrix.

---

## 3. Required Sections

### 3.1 Document Control
Document ID, version, date, author, reviewer, approver. Revision history table. Distribution list. Signature block with date fields.

### 3.2 Purpose and Scope
What the document covers and explicitly excludes. System/module identity. Governing URS reference (document ID + version). Regulatory context (21 CFR Part 11, EU GMP Annex 11, or both).

### 3.3 References
URS, Validation Plan, applicable standards (GAMP 5, 21 CFR Part 11, EU GMP Annex 11, ICH Q7/Q9/Q10), vendor internal standards.

### 3.4 Glossary
Every domain-specific term, units of measure with precision, cross-reference to project glossary.

### 3.5 System Overview
High-level system description and purpose. Context diagram (boundaries, external interfaces, user roles). Logical deployment topology (physical belongs in DS). Operating environment assumptions.

### 3.6 Functional Decomposition
Break the system into functional blocks/modules/subsystems. For each: name, purpose, URS requirements addressed, interfaces to other blocks. Use one of the three decomposition patterns (Section 6). This is the structural backbone — every requirement in 3.7 must belong to a block defined here.

### 3.7 Detailed Functional Requirements
One requirement per ID (FS-NNN). Follow the Testable Requirement Pattern (Section 8). Group by functional block. Each requirement: ID, description, acceptance criteria, URS trace, priority.

### 3.8 Interface Specifications
System-to-system and user interfaces per Section 10 format. Data direction, protocol category, frequency, error handling.

### 3.9 Data Requirements
Entities (CRUD), retention/archival rules, ALCOA+ data integrity attributes, calculated fields (formula + precision + rounding), migration requirements.

### 3.10 Alarm and Exception Handling
Per alarm: trigger, classification, message, operator response, escalation. Per exception: system behavior on failure. For process environments, align with ISA-18.2: priority levels (emergency/high/medium/low/diagnostic), shelving, suppression, acknowledgment, return-to-normal.

#### 3.10.1 ISA-18.2 Alarm Management Requirements

For systems subject to ISA-18.2, the following subsections apply. Non-process systems may exclude this content via the project manifest (see Override Points).

**Alarm Philosophy Input (ISA-18.2 Section 6):**
The FS should document the vendor's recommended alarm philosophy inputs for the customer's Alarm Philosophy Document. At minimum:
- Alarm classification scheme: Emergency, High, Medium, Low, Diagnostic (per ISA-18.2). Each priority level must have a defined response time expectation and escalation path.
- Alarm type classification: Process alarms (deviation from process setpoint or range), equipment alarms (mechanical or electrical fault conditions), safety alarms (conditions requiring immediate operator action to prevent harm), environmental alarms (emissions, containment, environmental limit violations), system health alarms (communication failures, controller faults, I/O errors).
- For each alarm type, the FS must specify: which priority levels are applicable, the default notification mechanism (visual, audible, or both), and whether the alarm type is subject to suppression or shelving.

**Alarm Identification and Rationalization (ISA-18.2 Sections 7-8):**
For each alarm point, the FS must specify or provide a structure that captures:
- Alarm tag (unique identifier, cross-referenced to P&ID or system tag)
- Description (plain-language description of the alarm condition)
- Setpoint (trigger value with engineering units)
- Deadband (value below/above setpoint required to clear the alarm, preventing chatter)
- Priority (Emergency/High/Medium/Low/Diagnostic, with justification)
- Consequence of missing (what happens if the operator does not respond in time)
- Response time (maximum time the operator has to take corrective action)
- Corrective action (documented operator response procedure or SOP reference)

Rationalization criteria — the FS should document how each alarm satisfies all four tests:
1. Is this alarm necessary? (Does the condition require awareness or action?)
2. Does it require operator action? (If not, it may be a status indicator, not an alarm.)
3. Is the response time achievable? (Can the operator realistically respond within the required window?)
4. Is it independent of other alarms? (Or is it a consequential alarm that should be suppressed or grouped?)

The FS must specify the Master Alarm Database (MAD) structure requirements: required fields, approval workflow for alarm additions/changes/deletions, version control, and export format. The MAD is the single source of truth for alarm rationalization and must be maintained throughout the system lifecycle.

**Alarm Design Requirements (ISA-18.2 Section 9):**

*Shelving:*
- Maximum shelve duration (configurable per site policy, default recommendation, and hard upper limit)
- Re-notification mechanism (how the system alerts operators when a shelved alarm's shelve timer expires)
- Audit trail of shelving actions (who shelved, when, duration, reason, alarm tag)

*Suppression:*
- State-based suppression rules (which alarms are suppressed during which operating states — e.g., startup, shutdown, cleaning, maintenance)
- Documentation requirements (each suppression rule must be rationalized and recorded in the MAD)
- Automatic re-enablement (suppressed alarms must automatically re-enable when the triggering state ends; manual suppression overrides must have a maximum duration)

*Flood Management:*
- Alarm flood definition: >10 alarms per 10 minutes per operator position (per EEMUA 191)
- Flood suppression strategy: how the system prioritizes and presents alarms during a flood (e.g., show highest priority first, suppress consequential alarms, aggregate related alarms)
- Post-flood analysis: the system must log flood events for subsequent review and alarm rationalization

*Alarm Grouping and Correlation:*
- Related alarm consolidation (grouping alarms with a common root cause into a single operator notification with drill-down capability)
- First-out logic (for trip or interlock events, clearly identifying the initiating alarm vs consequential alarms)

*Return-to-Normal (RTN):*
- RTN behavior per alarm type (does the alarm clear automatically when the condition returns to normal, or does it require explicit acknowledgment first?)
- Latched vs unlatched alarms: latched alarms remain active after the condition clears until explicitly acknowledged; unlatched alarms clear automatically. The FS must specify which alarm types use each behavior.

*Acknowledgment:*
- Acknowledgment requirements per priority level (e.g., Emergency alarms may require acknowledgment within 60 seconds with escalation if unacknowledged)
- Remote acknowledgment controls (whether alarms can be acknowledged from remote stations, and any restrictions or additional authentication required for remote acknowledgment)

#### 3.10.2 Alarm Performance KPI Specifications

The FS should specify target alarm performance metrics that the system must support measuring. These are KPIs the SYSTEM must be able to MEASURE and REPORT — not the FS's own performance targets.

| KPI | Description | Target (per EEMUA 191 / ISA-18.2) |
|---|---|---|
| Average alarm rate | Alarms per operator per 10 minutes during normal operations | ≤1 per EEMUA 191 "manageable" |
| Peak alarm rate | Maximum alarm rate during upsets, measured per operator position | Defined per site (document threshold) |
| Standing alarm count | Number of alarms continuously active without operator action | <5 per operator position |
| Stale alarm identification | Alarms active >24 hours without operator action | System must flag and report |
| Chattering alarm detection | Alarms with >3 activations in 60 seconds | System must detect and report |
| Nuisance alarm rate | Percentage of total alarms classified as nuisance after review | System must track for trending |

The system must provide configurable reporting against these KPIs with export capability for periodic alarm management review meetings.

### 3.11 Security and Access Control
Roles + permissions (CRUD matrix per function). Authentication method. Session management (timeout, concurrent sessions, lock-out). Electronic signature triggers per 21 CFR Part 11. Audit trail access restrictions.

### 3.12 Reporting and Audit Trail
Every report: name, trigger, content, output format. Audit trail: events logged, data per event (old/new value, user, timestamp, reason). Append-only, non-editable. Export formats and scheduling.

### 3.13 Performance Requirements
Response time thresholds (operation + data volume + latency). Throughput. Concurrent user capacity. Behavior at capacity limits.

### 3.14 Regulatory Requirements
Specific regulations imposing system behaviors. 21 CFR Part 11 and EU GMP Annex 11 compliance matrices (if applicable). ALCOA+ mapping.

#### 3.14.1 EU GMP Annex 11 Functional Considerations

For systems subject to EU GMP Annex 11, the FS must address the following clauses with specific functional requirements. These complement the 21 CFR Part 11 requirements elsewhere in this document. For dual-regulated systems, the FS must address both frameworks. Where they diverge (see glossary: Part 11 vs Annex 11 Divergences), design for the more restrictive requirement.

**Clause 5 — Data (Accuracy Checks on Manual Data Entry):**
The FS must specify accuracy checks on manual data entry for all GxP-critical input fields:
- Input validation rules: field-level format validation (e.g., date format, numeric range, enumerated values), cross-field validation (e.g., expiry date must be after manufacturing date), and business rule validation (e.g., batch size within product specification range).
- Double-entry requirements where applicable: identify which data elements require independent dual entry with comparison (e.g., analytical results, critical process parameters, material quantities). Specify system behavior on mismatch (reject, flag for review, require third verification).
- Range checks: for numeric fields, specify acceptable ranges with engineering units. The system must reject or flag out-of-range entries with a clear error message identifying the violated constraint.
- Format validation: specify acceptable input formats, character sets, and maximum lengths. The system must prevent entry of data that does not conform to the defined format.

**Clause 9 — Audit Trails:**
The FS must define which data elements require audit trailing and at what granularity. Apply a risk-based approach:
- GxP-critical data (e.g., batch records, test results, release decisions): full CRUD audit trails capturing who, what, when, old value, new value, and reason for change.
- Operational data (e.g., equipment schedules, resource assignments): change-only audit trails capturing modifications and deletions with user, timestamp, and old/new values.
- Reference data (e.g., product specifications, method parameters, user role assignments): approval audit trails capturing change requests, approvals, and effective dates.

For each audit trail category, the FS must specify: retention period (aligned with data retention policy), search and filter capabilities, export format, and access restrictions (who can view, who cannot modify).

**Clause 10 — Change and Configuration Management:**
The FS must specify how the system handles configuration changes:
- Version control of configurations: every configuration change must be versioned, with the ability to retrieve and compare any previous version.
- Approval workflows for configuration changes: specify which configuration categories require formal approval before activation (e.g., calculation parameters, alarm setpoints, user roles) vs which are effective immediately (e.g., display preferences, report formatting).
- Rollback capabilities: the system must support reverting to a previous configuration version with audit trail documentation of the rollback action, the user who initiated it, and the reason.

**Clause 13 — Incident Management:**
The FS must specify error handling, logging, and incident reporting capabilities:
- System error classification: define error severity levels (e.g., critical/major/minor/informational) and the system behavior for each level (e.g., critical errors halt processing and notify administrators; minor errors log and continue).
- Notification mechanisms: specify how errors and incidents are communicated to users and administrators (on-screen alerts, email notifications, SMS, integration with incident management systems).
- Escalation rules: define time-based and severity-based escalation paths (e.g., critical errors unacknowledged after 15 minutes escalate to site management).

**Clause 16 — Business Continuity:**
The FS must specify system behavior during degraded operations:
- Graceful degradation: define which functions remain available when dependent systems or components are unavailable (e.g., if the historian is offline, the system continues batch execution and buffers data locally).
- Data buffering during outages: specify how the system handles data that cannot be transmitted to its destination (buffer size, buffer persistence, overflow behavior, data integrity during buffering).
- Recovery procedures: define the system's behavior when normal operations resume (automatic reconnection, data synchronization sequence, conflict resolution rules).
- Data reconciliation after restoration: specify how buffered data is reconciled with the target system (chronological replay, duplicate detection, integrity verification, reconciliation report generation).

### 3.15 Traceability Matrix
Forward trace (URS -> FS) and backward trace (FS -> URS). Flag gaps (URS with no FS decomposition) and orphans (FS with no URS parent).

### 3.16 Open Issues
Each: ID, description, owner, target date, impact on FS content.

### 3.17 Appendices
Supplementary diagrams, data dictionaries, screen mockups, extended examples.

---

## 4. The Cardinal Sin: Parroting the URS

The most common FS failure is restating the URS in slightly different words. This adds no value and creates a false sense of decomposition.

**Detection:** (1) If you can delete the FS and write OQ tests from the URS alone, the FS added nothing. (2) If a URS requirement maps to exactly one FS requirement with the same vocabulary, it was not decomposed.

**Prevention:** Apply the 6-Question Checklist (Section 5) to every URS requirement. Each should yield 2+ FS requirements, or the FS requirement must add measurable acceptance criteria absent from the URS. The FS must introduce system-specific vocabulary (screen names, field names, calculation rules, error codes) not in the URS.

**Parroting example:**
> URS-005: "The system shall allow authorized users to approve batch records electronically."
> FS-010: "The system shall provide electronic approval of batch records by authorized users." ← *Same words, zero decomposition.*

**Real decomposition of the same URS requirement:**
> FS-010: "The Batch Review screen shall display: batch number, product name, timestamps, yield %, deviation count."
> FS-011: "Approve button enabled only when user holds Batch Approver role and all review checkboxes are checked."
> FS-012: "Approve triggers e-signature prompt (user ID + password + meaning) per 21 CFR Part 11.50."
> FS-013: "Successful signature sets status to Approved, records signature in audit trail, locks record."
> FS-014: "Three consecutive signature failures lock the user account and generate a high-priority alarm."

---

## 5. Six-Question Decomposition Checklist

For each URS requirement, ask these six questions. If any question reveals detail not already captured, it becomes one or more FS requirements.

| # | Question | What It Exposes |
|---|---|---|
| 1 | **What does the user see?** | Screen layout, fields, labels, navigation, visual feedback |
| 2 | **What triggers this behavior?** | User action, scheduled event, system event, data condition, external signal |
| 3 | **What data moves, and where?** | Inputs, outputs, transformations, storage, external system exchanges |
| 4 | **What are the boundary conditions?** | Min/max values, empty states, maximum volumes, timeout thresholds |
| 5 | **What happens when it fails?** | Error messages, fallback behavior, retry logic, alarm generation, data rollback |
| 6 | **Who is allowed, and how is it proven?** | Roles, permissions, authentication, electronic signatures, audit trail entries |

If a URS requirement survives all six questions with only one FS requirement, it was likely already at FS-level specificity. Document the analysis in the traceability matrix notes column to show the decomposition was attempted.

---

## 6. Three Decomposition Patterns

Choose the pattern that best fits the system or subsystem being specified. Mixing patterns across subsystems is acceptable.

### 6.1 Functional Block Decomposition

**Best for:** Systems with separable modules (LIMS, ERP, document management). Decompose by subsystem; each block gets its own requirements section.

```
Electronic Batch Record
  Block: Recipe Management       -> FS-001..003 (versioning, parameter ranges, approval)
  Block: Batch Execution         -> FS-010..012 (sequencing, data capture, deviations)
  Block: Review and Release      -> FS-020..022 (review display, e-signature, disposition)
```

### 6.2 Use Case Decomposition

**Best for:** Workflow-heavy systems (clinical trials, regulatory submissions). Decompose by actor-goal pairs with normal, alternate, and exception flows.

```
Use Case: Analyst Submits Sample Results (Actor: Lab Analyst)
  Normal:    FS-040 select sample | FS-041 display tests | FS-042 enter results
             FS-043 validate vs spec | FS-044 flag OOS
  Alternate: FS-045 attach chromatogram | FS-046 add comment (audit-trailed)
  Exception: FS-047 reject if past stability date | FS-048 alert if calibration expired
```

### 6.3 Data Flow / State Transition Decomposition

**Best for:** Complex data lifecycles (document control, deviation tracking). Each transition specifies trigger, guard, action, and audit capture.

```
Deviation Record: Draft -> Under Review -> Approved -> CAPA Assigned -> Closed

FS-060: Draft -> Under Review
  Trigger: Submit | Guard: mandatory fields + root cause | Action: notify + start timer | Audit: submitter + snapshot
FS-061: Under Review -> Approved
  Trigger: Approve | Guard: reviewer != author + e-sig | Action: approve + assign CAPA if Major | Audit: reviewer + meaning
FS-062: Under Review -> Draft (rejection)
  Trigger: Return | Guard: reason mandatory | Action: revert + notify + reset timer | Audit: reviewer + reason
```

---

## 7. Technology Swap Test

The Technology Swap Test defines the boundary between FS and DS. Apply it to every requirement:

> **"If I replaced the technology stack (e.g., swapped React for Angular, PostgreSQL for Oracle, AWS for Azure), would this requirement still be valid?"**

- **Yes** -> It belongs in the FS. It describes *what* the system does.
- **No** -> It belongs in the DS. It describes *how* the system does it.

**Examples:**

| Requirement | Swap Test | Belongs In |
|---|---|---|
| "The system shall calculate yield as (actual output / theoretical output) x 100, rounded to 2 decimal places." | Technology-independent calculation | **FS** |
| "Yield calculation shall use PostgreSQL ROUND() function with HALF_EVEN rounding." | Specific to PostgreSQL | **DS** |
| "The login screen shall lock the account after 5 failed attempts." | Any technology can implement this | **FS** |
| "Account lockout shall be enforced via Spring Security's LockoutPolicy bean with a Redis-backed attempt counter." | Specific to Spring + Redis | **DS** |
| "The system shall export reports in PDF format." | Technology-independent output format | **FS** |
| "PDF generation shall use iText 7 library with the company's XSL-FO template." | Specific to iText 7 + XSL-FO | **DS** |

When in doubt, ask: "Would the customer's QA team care about this detail during OQ testing?" If yes, it is FS. If only the development team cares, it is DS.

---

## 8. Testable Requirement Pattern

Every FS requirement must be testable. Use this structure:

```
[Actor/System] shall [observable action] when [trigger/condition],
resulting in [measurable outcome] within [time constraint, if applicable].
```

**Testability checklist for each requirement:**
- Can a tester determine pass/fail without asking the developer?
- Is the expected result specific enough to compare against actual result?
- Are all numeric thresholds, tolerances, and units of measure explicit?
- Is the trigger condition unambiguous (not "when appropriate" or "as needed")?

**Examples:**

| Bad (untestable) | Good (testable) |
|---|---|
| "The system shall respond quickly." | "The Search Results screen shall display results within 3 seconds for queries returning up to 10,000 records." |
| "The system shall handle errors gracefully." | "When a database connection fails during report generation, the system shall display error code ERR-DB-001, log the exception with stack trace, and retain the user's report parameters for retry." |
| "The system shall support concurrent users." | "The system shall support 50 concurrent users performing sample entry without response time exceeding 5 seconds per transaction." |
| "Data shall be backed up regularly." | "The system shall initiate automated database backup daily at 02:00 UTC, completing within 60 minutes for databases up to 500 GB." |

---

## 9. Forbidden Language

The following words and phrases make requirements untestable, ambiguous, or unverifiable. Flag them during coached refinement.

| Forbidden | Why | Replace With |
|---|---|---|
| "appropriate" / "as appropriate" | Undefined decision criteria | Specific condition and action |
| "etc." / "and so on" | Open-ended scope | Exhaustive enumeration |
| "user-friendly" / "intuitive" | Subjective | Specific UI behaviors or task completion criteria |
| "real-time" | Undefined latency | Maximum latency in ms/s |
| "fast" / "quickly" / "efficient" | Subjective | Numeric threshold with units |
| "support" (verb) | Vague | Concrete verb: display, calculate, transmit, store |
| "may" / "might" / "could" | Ambiguous obligation | "shall" (mandatory), "should" (recommended), or omit |
| "minimize" / "maximize" / "optimize" | No pass/fail target | Target value + acceptable range |
| "seamless" / "transparent" | Marketing | Specific integration behavior |
| "robust" / "reliable" | Undefined resilience | Failure modes + recovery + availability targets |
| "adequate" / "sufficient" | No threshold | Specific quantity or measure |
| "all applicable regulations" | Unbounded scope | Named regulations (21 CFR Part 11, Annex 11, etc.) |

---

## 10. Interface Specification Table Format

### 10.1 System-to-System Interfaces

Each interface entry (ID: IF-NNN) must specify:

**Identity:** Name, source system, destination system, direction (uni/bidirectional).
**Behavior:** Protocol category (REST/SOAP/HL7 FHIR/file transfer — specific endpoints in DS), trigger (event/schedule/manual), frequency, expected volume.
**Data:** Elements exchanged (reference data dictionary), validation rules applied before/after transfer.
**Failure:** Error handling behavior (retry, queue, alert, manual fallback).
**Non-functional:** Security (encryption, authentication method), SLA (latency, availability).
**Traceability:** Parent URS requirement(s).

### 10.2 User Interface Specifications

Each screen entry (ID: SCR-NNN) must specify:

**Identity:** Name, purpose, access roles, navigation path.
**Display fields:** Name, data type, source, format.
**Input fields:** Name, data type, validation rules, mandatory/optional, default value.
**Actions:** Buttons/links and their behavior (Save, Submit, Approve, etc.).
**Business rules:** Calculated fields, conditional visibility, cross-field validation.
**Error display:** Location and format of validation errors.
**Traceability:** Parent URS requirement(s).

---

## 11. FS vs DS Boundary Table

| Aspect | FS (What) | DS (How) |
|---|---|---|
| **Core question** | What does the system do? | How is it built? |
| **Audience** | Customer QA, auditors | Development team |
| **Technology** | Neutral (passes swap test) | Specific (frameworks, libraries, infra) |
| **Data** | Logical entities + relationships | Physical schema, tables, indexes |
| **Interfaces** | Protocol category, content, error behavior | Endpoints, payload schemas, auth tokens |
| **UI** | Screen purpose, fields, validation rules | Components, CSS, responsive breakpoints |
| **Performance** | User-observable thresholds | Caching, query optimization, pooling |
| **Security** | Roles, permissions, auth method | OAuth2 flows, token lifecycle, algorithms |
| **Calculations** | Formula, precision, rounding | Algorithm, library dependencies |
| **V-model pairing** | Verified by OQ | Verified by IQ + code review |
| **Change impact** | Customer re-approval | Vendor-internal (may trigger FS assessment) |

---

## 12. Example: Bad vs Good Decomposition

### URS Requirement
> URS-012: "The system shall generate a Certificate of Analysis (CoA) for each released batch, containing all test results, specifications, and a pass/fail determination."

### Bad Decomposition (parroting)
> FS-030: "The system shall generate a Certificate of Analysis for released batches with test results, specifications, and pass/fail status."

This adds nothing. A tester reading FS-030 still does not know what "generate" means, what the CoA looks like, or what triggers it.

### Good Decomposition

> **FS-030:** When a batch reaches status "Released," the CoA Generation function shall be available on the Batch Summary screen to users with Quality Reviewer or Quality Approver role.

> **FS-031:** The CoA shall contain: header (batch number, product name/code, manufacturing date, expiry date), results table (test name, method, spec limit, result, unit, pass/fail per test), summary determination, and footer (user name, timestamp, e-signature fields).

> **FS-032:** Overall determination shall be "Pass" only if every test result falls within spec. Any OOS result sets determination to "Fail" with watermark "FOR INVESTIGATION ONLY — NOT FOR RELEASE."

> **FS-033:** CoA output shall be PDF with document number pattern CoA-{ProductCode}-{BatchNumber}-{Version}, incrementing Version on regeneration.

> **FS-034:** If any assigned test has no result, the system shall block generation and display: "Cannot generate CoA: missing results for tests [list]."

> **FS-035:** CoA generation shall be audit-trailed: batch number, document number, user, timestamp, included test IDs.

Each requirement is independently testable. FS-032 is verified by submitting a batch with one OOS result and checking the watermark. FS-034 is tested by attempting generation with missing data. One vague URS requirement became six testable FS requirements.

---

## 13. Coaching Prompts

### For the Author (during draft generation)
- "This requirement uses '{forbidden word}.' What specific condition determines the action?"
- "URS-{NNN} maps to only one FS requirement. Walk through the 6-Question Checklist."
- "This interface lists data content but not error handling. What happens if the destination is unreachable?"
- "This requirement names a specific technology. Apply the Swap Test — move to DS if it fails."
- "The alarm section has no priorities. Classify each per ISA-18.2 (emergency/high/medium/low/diagnostic)."
- "This screen has 15 fields but no validation rules. For each input: type, range, mandatory/optional, error message."

### For the Author — Alarm Management (ISA-18.2)
- "Does each alarm require a documented operator action? If not, it may be a status indicator, not an alarm."
- "Is the alarm rate achievable? EEMUA 191 defines >1 alarm/min as 'overloaded'. Most ISA-18.2-compliant systems target ≤1 alarm/10min under normal operations."
- "Are there state-based suppression rules? Alarms that are valid during one operating state but nuisance during another need state-based logic."
- "Is there a Master Alarm Database requirement? The MAD is the single source of truth for alarm rationalization."

### For the Reviewer
- "Flag any requirement containing Forbidden Language (Section 9)."
- "Verify each URS requirement decomposes to 2+ FS requirements, or the FS requirement adds measurable criteria absent from the URS."
- "Run the Technology Swap Test on all detailed requirements. Flag technology-specific content."
- "Check for orphan FS requirements — is the URS missing something, or is this scope creep?"
- "Could an OQ tester write a test case from this requirement alone, without calling the vendor?"

### For the Approver
- "Does the traceability matrix show full URS coverage with no gaps?"
- "Does the FS introduce un-requested capabilities? Justified or scope creep?"
- "Is the FS technology-neutral? Could a customer approve it without knowing the tech stack?"
- "Could your QA team write an OQ protocol from this FS alone?"

---

## 14. Anti-Patterns

### 14.1 The Mirror FS
**Symptom:** One-to-one mapping between URS and FS requirements with no additional detail.
**Impact:** No value added; OQ tests will be as vague as the URS.
**Fix:** Apply the 6-Question Checklist to every requirement. If a URS requirement truly cannot be decomposed further, add measurable acceptance criteria.

### 14.2 The Design Specification in Disguise
**Symptom:** FS contains database table names, API endpoint URLs, class names, framework references, or deployment scripts.
**Impact:** Customer approval is now tied to implementation details. Any technology change forces an FS revision and re-approval cycle.
**Fix:** Apply the Technology Swap Test. Move all technology-specific content to the DS.

### 14.3 The Requirements Novel
**Symptom:** FS requirements are written as multi-paragraph narratives instead of discrete, testable statements.
**Impact:** Testers cannot isolate individual pass/fail criteria. Review cycles drag on because reviewers cannot pinpoint what they disagree with.
**Fix:** One requirement, one ID, one testable behavior. If a requirement contains "and" joining two distinct behaviors, split it.

### 14.4 The Missing Failure Path
**Symptom:** FS specifies normal-flow behavior only. No error messages, no boundary conditions, no alarm handling.
**Impact:** Developers invent error handling ad hoc. OQ tests pass on happy path but the system is unvalidated for failure scenarios — the scenarios that matter most in regulated environments.
**Fix:** For every FS requirement, ask question 5 from the decomposition checklist: "What happens when it fails?" Document the answer as an explicit FS requirement.

### 14.5 The Orphan Interface
**Symptom:** Interfaces mentioned in requirements but absent from the Interface Specifications section.
**Fix:** Every external system referenced must have a full interface table entry.

### 14.6 The Assumed Security Model
**Symptom:** "Only authorized users" with no role definitions, CRUD matrix, or authentication spec.
**Fix:** Define every role, its permissions per function, authentication method, and e-signature triggers.

### 14.7 The Audit Trail Afterthought
**Symptom:** Generic "the system shall maintain an audit trail" with no event-level specifics.
**Fix:** For every CUD and approve action, specify: event, fields recorded (old/new value, user, timestamp, reason), retention.

### 14.8 The Scope Creep Specification
**Symptom:** FS requirements that trace to no URS requirement.
**Fix:** Every FS requirement needs a URS parent. If genuinely needed, add the URS requirement first.

---

## Override Points

Customizable via project manifest:

- **Section ordering** — rearrange to match customer template
- **Section inclusion** — exclude optional sections (e.g., ISA-18.2 for non-process systems)
- **Requirement ID prefix** — override "FS-" with project-specific prefix
- **Interface table columns** — add/remove per project
- **Regulatory context** — include/exclude Part 11 and Annex 11 matrices
- **GAMP addenda** — auto-included for Category 4 or 5

---

## GAMP 5 Addenda

**Category 4 (Configured Products):** Document every configuration parameter and selected value. Distinguish vendor-configurable vs customer-configurable. Specify expected behavior per option.

**Category 5 (Custom Applications):** Full decomposition required for every requirement (no pass-through). Test data requirements per functional area. Calculation verification with sample data and expected results. Finer acceptance criteria granularity than Category 4.
