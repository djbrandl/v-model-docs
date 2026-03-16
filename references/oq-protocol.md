# OQ Protocol — Reference File

## 1. Purpose

The Operational Qualification (OQ) protocol is the vendor's verification deliverable that directly mirrors the Functional Specification (FS). Where the FS declares "the system shall do X," the OQ proves it does. Every testable FS requirement must have at least one corresponding OQ test case executed under controlled conditions.

**Vendor framing:** You author this protocol; your customer executes it. The customer's QA team will use OQ to confirm that every functional requirement performs as specified before accepting the system into their validated environment. A well-written OQ lets the customer execute without calling you for clarification.

**V-model position:** OQ sits on the right side of the V, directly across from the FS. It verifies functional behavior — not installation (IQ) and not business workflow fitness (PQ).

**Regulatory basis:** GAMP 5 2nd Ed (2022) — OQ verifies operation across specified ranges. FDA CSA (Sept 2025) — OQ test cases are candidates for risk-based streamlining. 21 CFR Part 11 — electronic records/signatures claimed in the FS must be verified. EU GMP Annex 11 Clause 4.6 — evidence of correct operation across anticipated operating ranges.

---

## 2. Predecessor Dependencies

| Predecessor | Why Required | What to Pull |
|---|---|---|
| **Functional Specification (FS)** | OQ is the direct verification of the FS | Requirement IDs, acceptance criteria, operating ranges, error handling behavior |
| **IQ Protocol (executed, passed)** | System must be installed before functional testing | IQ completion confirmation, baseline configuration, environment details |
| **Validation Plan (VP)** | Defines OQ scope and risk assessment approach | Risk classification per requirement, testing strategy, deviation process |
| **Design Specification (DS)** | Informs test environment setup | Architecture context, component boundaries, integration points |

**Hard gate:** Do not author OQ until the FS is approved. Do not execute OQ until IQ is complete and approved.

---

## 3. Required Sections

### 3.1 Protocol Header

Document ID, title, system name/version, document version with change history, author, reviewer(s), approver(s) — customer QA must approve before execution — effective date, and reference documents (FS version, IQ protocol ID, VP ID, DS version).

### 3.2 Purpose and Scope

State what the protocol verifies and explicitly exclude IQ scope (installation), PQ scope (business process fitness), performance under production load, and infrastructure qualification.

### 3.3 Roles and Responsibilities

| Role | Responsibility |
|---|---|
| Test Executor | Executes steps, records actual results, captures evidence |
| Test Reviewer | Reviews executed cases for completeness and accuracy |
| QA Approver | Approves protocol, reviews deviations, approves completion |
| System Administrator | Test environment access, test data resets |
| Vendor SME (if needed) | Technical questions only — does not execute tests |

### 3.4 Test Environment

Document: server/hosting (hardware, OS, cloud instance), exact application version/build, database type/version/baseline dataset, browser/client versions, connected systems with test vs. production endpoints, network configuration, test accounts with roles/permissions, and test data source and handling.

### 3.5 Prerequisites

IQ approved, test environment provisioned, test accounts created, test data loaded, personnel trained, deviation forms available, protocol approved by QA.

### 3.6 Test Cases

The body of the protocol. See Sections 4-6.

### 3.7 Deviation Log

See Section 10.

### 3.8 Results Summary

Total test cases, passed, failed, deviations raised, deviations resolved, deviations with CAPA.

### 3.9 Conclusion and Approval

Statement of completion, deviation disposition, and recommendation for PQ. Signatures: Test Lead, QA Approver, System Owner.

---

## 4. Test Design Techniques

Apply at least two techniques per FS requirement. All examples below reference: *"The system shall accept batch sizes between 100 and 10,000 units (FS-042)."*

### 4.1 Boundary Value Analysis (BVA)

Test at exact edges of valid ranges. For [min, max], test: min-1, min, min+1, max-1, max, max+1.

| Input | Expected | Rationale |
|---|---|---|
| 99 | Rejected with error | Below minimum |
| 100 | Accepted | Minimum boundary |
| 101 | Accepted | Just above minimum |
| 9,999 | Accepted | Just below maximum |
| 10,000 | Accepted | Maximum boundary |
| 10,001 | Rejected with error | Above maximum |

### 4.2 Equivalence Partitioning

Divide the input domain into classes with identical expected behavior. Test one representative per partition.

| Partition | Representative | Expected |
|---|---|---|
| Below range (< 100) | 50 | Reject |
| Valid low (100-1,000) | 500 | Accept |
| Valid mid (1,001-5,000) | 3,000 | Accept |
| Valid high (5,001-10,000) | 8,000 | Accept |
| Above range (> 10,000) | 15,000 | Reject |
| Non-numeric | "abc" | Reject with type error |
| Negative | -100 | Reject |
| Null / empty | (blank) | Reject with required field error |

### 4.3 Negative Testing

Provide invalid, unexpected, or malformed inputs. Confirm graceful rejection with no data corruption.

| Scenario | Input | Expected |
|---|---|---|
| Decimal | 100.5 | Reject or accept per FS |
| Special characters | `100; DROP TABLE` | Reject, no DB impact |
| Extreme value | 999,999,999 | Reject, no overflow |
| Leading/trailing spaces | " 100 " | Accept as 100 or reject per FS |

### 4.4 Error Recovery

Induce failure during critical operations. Verify recovery without data loss.

| Failure | Test Action | Expected Recovery |
|---|---|---|
| Network interruption | Disconnect mid-transaction | Rollback, user notified, no partial records |
| Session timeout | Let session expire with unsaved data | Draft preserved or user warned |
| Concurrent edit | Two users edit same record | Second save blocked or merged per FS |
| Database unavailable | Simulate DB down | Graceful error, retry option, no corruption |

### 4.5 State Transition Testing

Map the state diagram from the FS. Test every valid transition and at least one invalid transition per state.

**Example — Batch Record Workflow:**

| Current State | Action | Expected | Valid? |
|---|---|---|---|
| Draft | Submit | Submitted | Yes |
| Draft | Approve | Error: cannot approve from Draft | No |
| Under Review | Approve | Approved | Yes |
| Under Review | Reject | Rejected | Yes |
| Approved | Reject | Error: cannot reject after approval | No |
| Released | Edit | Error: released records immutable | No |

---

## 5. Test Case Format

Step-level detail is mandatory. An executor who has never seen the system must follow the steps without interpretation.

```markdown
### Test Case OQ-{NNN}: {Descriptive Title}

**Traces to:** FS-{NNN}, FS-{NNN}
**Risk Level:** High / Medium / Low
**Technique(s):** BVA, Negative Testing
**Prerequisites:** {Setup beyond protocol-level prerequisites}
**Test Data:** {Reference to test data set ID}

| Step | Action | Expected Result | Actual Result | Pass/Fail | Executed By | Date |
|---|---|---|---|---|---|---|
| 1 | Navigate to {Module} > {Screen} | {Screen title} displayed with {elements} | | | | |
| 2 | Enter "{value}" in {Field Name} | Field displays "{value}" | | | | |
| 3 | Click {Button Name} | {Observable outcome: message text, screen change} | | | | |
| 4 | Verify {element} in {location} | {Element} displays "{value}" in {format} | | | | |

**Evidence:** {Screenshot/log reference IDs}
**Deviation(s):** {ID or "None"}
**Overall Result:** Pass / Fail
```

**Step writing rules:** One action per step. Name every UI element explicitly. Specify exact values, never "a valid value." State the observable outcome, not "system confirms." Include navigation from a known location. Number sequentially — no sub-steps.

### 5.1 Alarm System Verification Test Cases (ISA-18.2)

The following test cases verify alarm management functionality per ISA-18.2 / IEC 62682. These cases apply when the FS defines alarm setpoints, priorities, shelving, suppression, or flood-handling behavior. Each test case follows the format in Section 5.

#### Test Case OQ-ALM-001: Alarm Generation at Setpoint Boundaries

**Traces to:** FS alarm setpoint requirements
**Risk Level:** High
**Technique(s):** Boundary Value Analysis (BVA)
**Prerequisites:** Alarm setpoints configured per FS; process variable simulator available
**Test Data:** Setpoint value, deadband value from alarm configuration

| Step | Action | Expected Result | Actual Result | Pass/Fail | Executed By | Date |
|---|---|---|---|---|---|---|
| 1 | Drive process variable to setpoint - 1 | Alarm does not activate; no annunciation | | | | |
| 2 | Drive process variable to setpoint | Alarm activates; annunciation displayed with correct priority color/symbol and timestamp | | | | |
| 3 | Drive process variable to setpoint + 1 | Alarm remains active; no duplicate alarm generated | | | | |
| 4 | Return process variable to setpoint - deadband + 1 | Alarm remains active (within deadband) | | | | |
| 5 | Return process variable below setpoint - deadband | Alarm returns to normal (RTN); RTN timestamp recorded | | | | |

**Evidence:** Screenshot of alarm banner at each step; alarm historian log entries
**Deviation(s):** {ID or "None"}
**Overall Result:** Pass / Fail

#### Test Case OQ-ALM-002: Alarm Priority Routing

**Traces to:** FS alarm priority and routing requirements
**Risk Level:** High
**Technique(s):** Equivalence Partitioning
**Prerequisites:** Alarm philosophy document approved; operator positions configured; audible annunciation hardware available
**Test Data:** One alarm tag per priority level (Emergency, High, Medium, Low)

| Step | Action | Expected Result | Actual Result | Pass/Fail | Executed By | Date |
|---|---|---|---|---|---|---|
| 1 | Generate Emergency priority alarm | Alarm displays with Emergency color/symbol per alarm philosophy; audible pattern matches Emergency annunciation; operator notification sent to designated position | | | | |
| 2 | Generate High priority alarm | Alarm displays with High color/symbol per alarm philosophy; audible pattern matches High annunciation; operator notification sent to designated position | | | | |
| 3 | Generate Medium priority alarm | Alarm displays with Medium color/symbol per alarm philosophy; audible pattern matches Medium annunciation; operator notification per alarm philosophy | | | | |
| 4 | Generate Low priority alarm | Alarm displays with Low color/symbol per alarm philosophy; audible pattern matches Low annunciation; operator notification per alarm philosophy | | | | |
| 5 | Verify alarm summary display | All four alarms appear in alarm summary with correct priority indicators, timestamps, and tag descriptions | | | | |

**Evidence:** Screenshot of each alarm annunciation; screenshot of alarm summary; audio confirmation log (if applicable)
**Deviation(s):** {ID or "None"}
**Overall Result:** Pass / Fail

#### Test Case OQ-ALM-003: Alarm Shelving Duration Limits

**Traces to:** FS alarm shelving requirements
**Risk Level:** High
**Technique(s):** State Transition Testing
**Prerequisites:** Alarm shelving function enabled; maximum shelve duration configured per FS
**Test Data:** Active alarm tag; configured maximum shelve duration value

| Step | Action | Expected Result | Actual Result | Pass/Fail | Executed By | Date |
|---|---|---|---|---|---|---|
| 1 | Generate an active alarm | Alarm activates and annunciates normally | | | | |
| 2 | Shelve the active alarm | Alarm suppressed from annunciation; shelve action recorded in audit trail with user ID, timestamp, and alarm tag | | | | |
| 3 | Verify alarm status during shelve period | Alarm shows "Shelved" status in alarm summary; no annunciation during shelve period | | | | |
| 4 | Wait for maximum shelve duration to elapse | Alarm re-appears with active annunciation; re-notification generated to operator position | | | | |
| 5 | Verify audit trail | Shelve action, shelve duration, and automatic unshelve event recorded with timestamps | | | | |

**Evidence:** Screenshot of shelved alarm status; screenshot of re-activated alarm; audit trail extract
**Deviation(s):** {ID or "None"}
**Overall Result:** Pass / Fail

#### Test Case OQ-ALM-004: Alarm Suppression Logic

**Traces to:** FS state-based alarm suppression requirements
**Risk Level:** High
**Technique(s):** State Transition Testing
**Prerequisites:** State-based suppression rules configured per FS; ability to change system operating state
**Test Data:** Alarm tag with state-based suppression rule; system states where alarm is suppressed and active

| Step | Action | Expected Result | Actual Result | Pass/Fail | Executed By | Date |
|---|---|---|---|---|---|---|
| 1 | Place system in state where alarm is configured as suppressed | System state change confirmed | | | | |
| 2 | Drive process variable to alarm setpoint | Alarm does not annunciate; suppression status visible in alarm summary | | | | |
| 3 | Verify audit trail for suppression | Suppression event logged with system state, alarm tag, user ID, and timestamp | | | | |
| 4 | Change system to state where alarm is active | System state change confirmed | | | | |
| 5 | Verify alarm annunciates in active state | Alarm activates and annunciates normally; unsuppression event logged in audit trail | | | | |

**Evidence:** Screenshot of suppressed alarm status; screenshot of active alarm annunciation; audit trail extract showing suppression/unsuppression events
**Deviation(s):** {ID or "None"}
**Overall Result:** Pass / Fail

#### Test Case OQ-ALM-005: Concurrent Alarm Handling (Alarm Flood)

**Traces to:** FS alarm flood handling requirements
**Risk Level:** High
**Technique(s):** Negative Testing, Error Recovery
**Prerequisites:** Alarm flood scenario defined; >10 alarm tags available for simultaneous triggering; HMI response time measurement tool available
**Test Data:** Alarm flood scenario triggering >10 alarms in <10 minutes

| Step | Action | Expected Result | Actual Result | Pass/Fail | Executed By | Date |
|---|---|---|---|---|---|---|
| 1 | Trigger alarm flood scenario (>10 alarms in <10 minutes) | All alarms generated and logged in alarm historian with correct timestamps | | | | |
| 2 | Verify alarm historian completeness | All triggered alarms recorded; no alarm data loss; timestamps sequential and accurate | | | | |
| 3 | Verify HMI responsiveness during flood | HMI response time <2 seconds; operator can navigate screens without degradation | | | | |
| 4 | Verify alarm summary accessibility | Alarm summary displays all active alarms; sorting and filtering functions operational | | | | |
| 5 | Verify alarm flood indicator | Flood indicator activates per alarm philosophy when alarm rate exceeds configured threshold | | | | |

**Evidence:** Alarm historian export showing all triggered alarms; HMI response time measurements; screenshot of alarm summary during flood; screenshot of flood indicator
**Deviation(s):** {ID or "None"}
**Overall Result:** Pass / Fail

#### Test Case OQ-ALM-006: Alarm Acknowledgment Workflow

**Traces to:** FS alarm acknowledgment requirements
**Risk Level:** High
**Technique(s):** Negative Testing, State Transition Testing
**Prerequisites:** Alarm acknowledgment rules configured per FS; authorized and unauthorized user accounts available
**Test Data:** Active alarm tag; authorized user credentials; unauthorized user credentials

| Step | Action | Expected Result | Actual Result | Pass/Fail | Executed By | Date |
|---|---|---|---|---|---|---|
| 1 | Generate an active alarm | Alarm activates and annunciates normally | | | | |
| 2 | Attempt acknowledgment by unauthorized user | Acknowledgment rejected; alarm remains unacknowledged; rejection event logged | | | | |
| 3 | Attempt acknowledgment by authorized user | Acknowledgment accepted; alarm visual state changes to acknowledged | | | | |
| 4 | Verify audit trail for acknowledgment | Acknowledging user, timestamp, and alarm state (unacknowledged to acknowledged) recorded in audit trail | | | | |
| 5 | Verify alarm remains visible until RTN | Acknowledged alarm remains in alarm summary until process variable returns to normal | | | | |

**Evidence:** Screenshot of rejected acknowledgment attempt; screenshot of successful acknowledgment; audit trail extract
**Deviation(s):** {ID or "None"}
**Overall Result:** Pass / Fail

---

## 6. Expected Result Quality

### The Four Qualities

| Quality | Bad | Good |
|---|---|---|
| **Unambiguous** | "System responds correctly" | "Green banner displays: 'Record saved successfully'" |
| **Observable** | "Data is stored in database" | "Screen displays Record ID REC-00042 with timestamp" |
| **Toleranced** | "Report generates quickly" | "Report renders within 30 seconds" |
| **Complete** | "Error is shown" | "Red banner: 'Batch size must be between 100 and 10,000.' Field highlighted red. No record created." |

**Tolerance rules:** Time: "within 30 seconds" not "quickly." Numeric: "42.5 +/- 0.1" not "approximately." Counts: "exactly 15 rows" not "all records." Timestamps: "within +/- 2 minutes of wall clock" not "correct."

---

## 7. Traceability

### 7.1 FS-to-OQ Mapping

The relationship is one-to-many. A single FS requirement may need multiple test cases (BVA, negative, error recovery). Every FS requirement maps to at least one OQ test case. No OQ test case exists without an FS trace.

```
FS-042 (Batch size range)
├── OQ-031: Boundary values (BVA)
├── OQ-032: Invalid input handling (Negative)
└── OQ-033: Error recovery on save failure

FS-043 (Batch status workflow)
├── OQ-034: Valid transitions (State Transition)
├── OQ-035: Invalid transitions (State Transition)
└── OQ-036: Concurrent access (Error Recovery)
```

### 7.2 Coverage Verification

Before approval: every FS ID appears in at least one "Traces to" field; no orphan test cases; high-risk requirements use at least two techniques; critical requirements include negative testing and error recovery.

### 7.3 Risk-Based Grouping

Organize by risk classification from the VP, not by FS section order.

| Group | Risk Level | Testing Depth |
|---|---|---|
| 1 | High (GxP-critical, patient safety, data integrity) | BVA + Negative + Error Recovery + State Transition |
| 2 | Medium (Core functional, regulatory non-safety) | BVA + Equivalence Partitioning + Negative |
| 3 | Low (Administrative, non-GxP) | Equivalence Partitioning + targeted Negative |

---

## 8. Test Data Management

### 8.1 Required Elements Per Data Set

| Element | Guidance |
|---|---|
| **Description** | What the data represents and why selected |
| **Source** | Synthetic, anonymized production copy, or reference standard |
| **Location** | File path, database schema, or test data system reference |
| **Preservation** | Retention period (match customer policy — typically 1 year beyond product lifecycle) |
| **Sensitive data** | If PII/PHI present: anonymization method, access controls, disposal procedure |

### 8.2 Integrity Rules

- Load fresh or verify unchanged from documented baseline before execution
- Document sequence dependencies or reset procedures between cases that modify shared data
- Never use production data directly — anonymize or use synthetic
- Document anonymization tool and procedure

---

## 9. Pass/Fail Criteria

### 9.1 Step Level

Actual result matches expected result exactly (within tolerances). Any discrepancy is a failure. Record actual result regardless of outcome.

### 9.2 Test Case Level

| Outcome | Criteria |
|---|---|
| **Pass** | All steps pass |
| **Fail** | One or more steps fail; deviation raised |
| **Pass with Deviation** | Steps pass after deviation resolution |
| **Blocked** | Cannot execute; blocking reason documented |

### 9.3 Protocol Level

| Outcome | Criteria |
|---|---|
| **Pass** | All test cases pass (including Pass with Deviation, deviations closed) |
| **Conditional Pass** | High/medium-risk pass; low-risk deviations open with risk acceptance and CAPA timeline; QA approved |
| **Fail** | Any high/medium-risk test case has unresolved deviation |

---

## 10. Deviation Handling

Every departure from an expected result is a deviation. No exceptions.

### Five-Step Process

**Step 1 — Record immediately.** Stop. Document: deviation ID, test case, step, expected result, actual result, date/time, executor. Capture evidence.

**Step 2 — Classify severity.**

| Severity | Definition | Example |
|---|---|---|
| Critical | GxP data integrity or patient safety impact | Audit trail missing entries; wrong calculation |
| Major | Incorrect function, workaround exists | Wrong date format; export omits field |
| Minor | Cosmetic, no regulatory impact | Misspelled label; alignment issue |

**Step 3 — Investigate root cause.** Categories: (a) software defect, (b) test procedure error, (c) environment issue, (d) FS specification error, (e) test data issue.

**Step 4 — Determine resolution.** Software defect: fix and retest. Procedure error: amend protocol, re-execute. Environment: fix and re-execute. Spec error: amend FS via change control, update OQ. Data issue: correct and re-execute.

**Step 5 — Determine CAPA need.** Critical/Major: document corrective and preventive actions. Minor: corrective action sufficient.

### Deviation Log Fields

Dev ID, Test Case, Step, Severity, Description, Root Cause, Resolution, CAPA Ref, Retest Ref, Status, Closed By, Date.

---

## 11. Retesting Rules

1. **Root cause confirmed before retest.** Never retest hoping the problem resolved itself.
2. **Documented separately.** New execution record (OQ-031-R1), referencing deviation ID and fix applied.
3. **Both results preserved.** Original failure and retest result both appear in the final protocol. Never overwrite.
4. **QA approves retest scope.** QA determines which cases to re-execute and whether regression testing is needed.

Retest records include: original test case reference, deviation reference, root cause, fix description with version/change control reference, regression scope with QA justification, and full step-level re-execution table.

---

## 12. Evidence Capture

### 12.1 GAMP 5 2nd Ed — Exception-Based Approach

Capture evidence to document what happened, not to prove every micro-step.

- **Capture:** Screenshots of final results, error messages, system responses at verification points, log excerpts, generated reports
- **Do not capture:** Every navigation click, typing values, clicking buttons — the recorded actual result is sufficient
- **Scale by risk:** High — evidence at every verification step. Medium — evidence at final verification step. Low — evidence by exception only (unexpected results or deviations).

### 12.2 ALCOA+ Compliance

| Principle | OQ Application |
|---|---|
| **Attributable** | Every entry signed with executor name and date/time |
| **Legible** | Printed (not cursive) handwriting; readable screenshots at print resolution |
| **Contemporaneous** | Recorded at execution time; evidence timestamps match execution dates |
| **Original** | First-capture evidence, not copies of copies |
| **Accurate** | Actual results describe observation, not expectation |
| **+Complete** | No blank fields; unexecuted steps documented as N/A or Blocked with reason |
| **+Consistent** | Uniform date formats, naming conventions, reference numbering |
| **+Enduring** | Stored in accessible format for retention period; no ephemeral links |
| **+Available** | Retrievable by authorized personnel within reasonable time for audit |

### 12.3 Evidence Labeling

Each evidence item labeled with: Evidence ID (EVD-OQ-{NNN}-S{NN}), test case, step, description, captured by, date/time, system name/version, environment identifier.

---

## 13. Coaching Questions

### Coverage and Traceability
- "Which OQ test case verifies FS-{NNN}? A missing test case is an audit finding."
- "This FS requirement has one test case. Given its risk level, should we add negative testing or BVA?"
- "Are 'future release' FS requirements explicitly excluded from OQ scope?"

### Expected Result Quality
- "Could someone who has never seen the system determine pass or fail from this expected result?"
- "This says 'data is saved correctly.' What specifically would the executor observe?"
- "What tolerance applies here? 'Quickly' is not testable."

### Test Design Completeness
- "What happens when the user enters nothing in this required field?"
- "The FS defines five workflow states. I see happy path tests but not invalid transitions."
- "This integration sends data to an external system. What if that system is unavailable?"

### Execution Practicality
- "How long will execution take? If over three days, split into independent modules."
- "This test requires a locked-out user. How does the executor set that up?"
- "These five cases modify the same record. What is the sequence? Does data reset between them?"

### Evidence and Deviations
- "If this fails, what evidence beyond a screenshot would you want? Logs? Database state?"
- "Fifteen steps in this case. Where are the verification points for evidence capture?"

---

## 14. Anti-Patterns

| Anti-Pattern | Why It Fails | Fix |
|---|---|---|
| **"Verify system works correctly"** | No objective pass/fail criterion | Specify observable outcome: message text, field value, record count |
| **Copy-paste from FS** | FS says "shall"; OQ says "executor observes" | Rewrite as executor perspective: "Screen displays..." |
| **Happy path only** | Auditors look for negative tests | Two+ techniques per high-risk requirement; always include negatives |
| **Orphan test cases** | No traceability to FS requirement | Every case populates "Traces to"; remove or justify untraced tests |
| **Vague test data** | "Enter a valid value" introduces variability | Specify exact values; reference test data sets |
| **Missing error text** | "Error displayed" — which one? | Quote exact expected message text |
| **Giant test cases** | 40 steps; failure at step 35 wastes everything | 5-15 steps per case; one verification objective |
| **No deviation section** | Implies deviations won't happen | Always include deviation log and process |
| **Overwriting failures** | Destroys quality record | Preserve originals; add retest records separately |
| **Screenshot every click** | Hundreds of unreviewed pages | Exception-based evidence per GAMP 5 2nd Ed |
| **Testing config, not function** | "Field exists" is IQ, not OQ | OQ tests behavior: enter value, verify system response |
| **Untimed performance** | FS claims "within 5 seconds" but OQ has no timing | Add step measuring response time against tolerance |

---

## Override Points

| Key | Controls | Default |
|---|---|---|
| `oq.evidenceApproach` | Full vs. exception-based evidence | `exception-based` |
| `oq.riskLevels` | Risk group count and naming | 3: High, Medium, Low |
| `oq.deviationSeverities` | Severity classification | Critical, Major, Minor |
| `oq.testCasePrefix` | Test case ID prefix | `OQ` |
| `oq.retestNaming` | Retest naming convention | `{TestID}-R{N}` |
| `oq.passCriteria` | Protocol-level pass criteria | Per Section 9.3 |
| `oq.signatureBlock` | Approval roles and order | Test Lead, QA, System Owner |

---

## GAMP 5 Addenda

### Category-Scaled Testing Depth

| GAMP Category | OQ Approach | Typical Test Count |
|---|---|---|
| **Cat 3** (Non-configured) | Verify configured parameters within ranges; limited functional testing | 5-15 |
| **Cat 4** (Configured) | All configured functions: business rules, workflows, calculations, interfaces, access controls | 15-40 |
| **Cat 5** (Custom) | Full functional verification; every FS requirement tested; high-risk requirements get multiple techniques | 30-100+ |

### FDA CSA Alignment

Under FDA CSA guidance (September 2025), OQ testing is risk-stratified:

- **High risk (direct GxP):** Fully scripted test cases, step-level detail, full evidence
- **Medium risk (indirect GxP):** Scripted test cases, exception-based evidence
- **Low risk (no direct GxP):** Unscripted acceptable — document objective, approach, result, and deviations

The vendor should provide scripted test cases for all risk levels but note which the customer may execute as unscripted per their CSA policy. Reduced documentation burden does not mean untested.

### EU GMP Annex 11 OQ Considerations

For systems subject to EU GMP, OQ test cases must address the following Annex 11 clauses. These supplement — not replace — the FDA Part 11 requirements covered elsewhere in this protocol.

**Clause 5 — Data:** OQ must verify accuracy checks on data entry. Test input validation rules for all GxP-critical fields: boundary values for numeric data fields, format enforcement (date formats, unit-of-measure constraints), rejection of invalid entries with user-visible error messages, and correct handling of mandatory vs. optional fields. Where the FS defines data accuracy checks (e.g., second-person verification, range limits), include explicit OQ test cases for each.

**Clause 9 — Audit Trails:** OQ must verify that audit trail configuration matches the risk-based design documented in the FS. Test cases must confirm: GxP-critical data changes are fully audit trailed (create, modify, delete); audit trail entries capture who (user ID), what (field, old value, new value), when (system-generated timestamp), and why (reason for change, where configured); audit trails cannot be disabled by any user role, including administrators; and audit trail records cannot be modified or deleted. Where the FS defines risk-based audit trail scope (i.e., certain non-GxP fields excluded), verify that the exclusion matches the documented rationale.

**Clause 12 — Security:** OQ must verify logical access controls as defined in the FS. Test cases must cover: role-based access control (RBAC) — each role can access only permitted functions; separation of duties — users cannot perform conflicting actions (e.g., create and approve the same record); session timeout — inactive sessions terminate after the configured duration; and failed login lockout — accounts lock after the configured number of failed attempts, with lockout event logged.

**Clause 14 — Electronic Signature:** OQ must verify e-signature binding per Annex 11 and 21 CFR Part 11. Test cases must confirm: signed records display signer identity, date/time of signature, and meaning of signature (e.g., "Approved," "Reviewed"); signed records cannot be modified without invalidating the signature; and re-signing after modification requires a new signature event with full audit trail.

**Clause 16 — Business Continuity:** OQ must verify system behavior during degraded operations. Test cases should cover: graceful degradation scenarios (e.g., loss of a non-critical integration, reduced network bandwidth) — system continues to function with appropriate user notification; data integrity during failover — no data loss or corruption during switchover to backup systems; and recovery procedures — system restores to a known good state per documented recovery time objectives.

> **Dual-regulation note:** For dual-regulated systems (FDA + EU), ensure OQ test cases cover both Part 11 and Annex 11 requirements. Where requirements diverge (e.g., Annex 11 Clause 9 risk-based audit trails vs. Part 11 11.10(e) comprehensive audit trails), test against the more restrictive requirement.
