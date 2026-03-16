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
