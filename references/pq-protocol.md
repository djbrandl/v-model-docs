# PQ Protocol — Reference File

> **Ownership model:** Customer-assist. The vendor provides a recommended PQ template with workflow-driven test scenarios; the customer's validation team adapts it to their production environment and executes it.

> **Framing note:** This PQ template is provided as a recommendation. Your customer's validation team should adapt it to their production environment.

---

## 1. Purpose

Performance Qualification (PQ) is the final qualification stage in the V-model. It answers one question: **does the system perform as intended under real production conditions, with real users, real data, and real workflows?**

PQ mirrors the URS. Where OQ verifies the FS (does each function work correctly?), PQ verifies the URS (does the system meet the user's actual needs in their actual environment?). Every URS requirement should trace forward to at least one PQ test scenario.

### Vendor's Role

The vendor provides a recommended PQ template pre-populated with workflow scenarios derived from the URS and FS, suggested acceptance criteria based on system capabilities, performance baselines from vendor OQ results, and guidance on statistical methods and duration requirements.

The customer owns: adapting scenarios to their SOPs and organizational structure, executing PQ in their production environment, documenting deviations with root cause analysis, and final PQ approval and sign-off.

---

## 2. Predecessor Dependencies

| Predecessor | Status Required | Why |
|---|---|---|
| URS | Approved | PQ traces directly back to URS — without approved requirements, nothing to qualify against |
| FS | Approved | PQ scenarios reference functional behaviors defined in the FS |
| DS | Approved | Environmental and configuration details inform production conditions |
| IQ | Executed, deviations resolved | System must be correctly installed before performance testing |
| OQ | Executed, deviations resolved | Functional correctness must be proven before workflow-level qualification |
| Traceability Matrix | Current | Confirms every URS requirement has a corresponding PQ scenario |

**Hard gate:** IQ and OQ must be complete with all critical and major deviations resolved. Minor OQ deviations may remain open if they do not affect PQ workflow scenarios, but this must be documented with a risk justification.

---

## 3. How PQ Differs from OQ

| Dimension | OQ | PQ |
|---|---|---|
| **Traces to** | Functional Specification (FS) | User Requirements Specification (URS) |
| **Environment** | Validated test environment | Production environment |
| **Data** | Synthetic test data, boundary values | Real or representative production data |
| **Users** | Testers (often vendor personnel) | Actual end users in assigned roles |
| **Focus** | Individual functions work correctly | End-to-end workflows meet business needs |
| **Test design** | Technique-driven (BVA, equivalence partitioning) | Workflow-driven (complete business processes) |
| **Duration** | Single execution per test case | Multiple consecutive executions for reproducibility |
| **Acceptance** | Pass/fail per function | Cumulative performance, often with statistical criteria |
| **Owned by** | Vendor | Customer |

**Key principle:** OQ asks "does each feature work?" PQ asks "does the whole system work for our people, with our data, in our environment?"

---

## 4. Recommended Protocol Sections

### 4.1 Header Block (Required)

Document ID, system name, version, GAMP category, protocol version, prepared by (vendor), adapted by and approved by (customer TODOs), execution date.

### 4.2 Purpose and Scope (Required)

State that PQ demonstrates the system performs as intended under production conditions. Reference the approved URS by document ID and version. Define in-scope workflows and explicit exclusions.

### 4.3 Prerequisites (Required)

IQ/OQ executed and approved, production environment configured per DS, user accounts provisioned with production roles, production data available, SOPs reviewed, testers trained.

### 4.4 System Description (Required)

Brief description from manifest and URS. Include production environment configuration (hardware, OS, network, integrations).

### 4.5 Test Strategy (Required)

Workflow-driven testing approach, consecutive execution count (minimum 3), production conditions maintenance, statistical methods (if applicable), deviation handling procedures.

### 4.6 Traceability Summary (Required)

Table mapping each PQ scenario to source URS requirements. Every URS requirement must appear at least once.

### 4.7 Test Scenarios (Required)

Complete workflow scenarios — not isolated function tests. See Section 5 for design methodology, Section 6 for examples.

### 4.8 Acceptance Criteria Summary (Required)

Consolidated table of all acceptance criteria with pass/fail thresholds.

### 4.9 Deviation Log (Required)

Template with columns: Deviation #, PQ Scenario, Description, Severity (Critical/Major/Minor), Root Cause, Impact Assessment, CAPA, Resolution.

### 4.10 Environmental Conditions Record (Recommended)

System version, configuration parameters, network conditions, concurrent user load, database size, integration endpoint status during execution.

### 4.11 Signatures and Approvals (Required)

Executed By, Reviewed By, QA Approved By — each with date fields.

### 4.12 Appendices (Recommended)

Raw test data/screenshots, performance measurement logs, statistical analysis worksheets, deviation resolution evidence.

---

## 5. Workflow-Driven Scenario Design

PQ scenarios must represent complete business workflows. Use this 5-step process:

**Step 1 — Harvest Workflows from the URS.** Group URS requirements by business process. A single workflow scenario typically covers 3-8 requirements. Example: "create batch record," "assign reviewer," "apply electronic signature," and "generate audit trail" belong to one "batch record lifecycle" scenario.

**Step 2 — Map the Happy Path.** Document the complete step sequence from trigger to outcome, including all system interactions, decision points, and expected outputs.

**Step 3 — Identify Workflow Variations.** Different user roles performing the same workflow, different data volumes, different data types, concurrent access, workflows spanning shifts or calendar days.

**Step 4 — Add Negative Workflow Paths.** Scenarios where the workflow should be blocked: insufficient permissions, incomplete prerequisites, data validation failures, segregation of duties enforcement. Note: PQ negative paths test workflow-level controls, not individual input validation (that belongs in OQ).

**Step 5 — Define Measurable Acceptance Criteria.** Every criterion must be specific (numeric thresholds, not "quickly"), measurable (pass/fail deterministic), traceable (linked to a URS requirement), and reproducible (consistent across 3 executions).

---

## 6. Example Test Scenarios

### 6.1 Batch Record Workflow (PQ-001)

**Traces to:** URS-005, URS-008, URS-012, URS-015 | **Consecutive Executions:** 3

| Step | Action | Expected Result |
|---|---|---|
| 1 | Production operator logs in with assigned credentials | Dashboard displays operator role view |
| 2 | Operator creates batch record using production template | Record created with auto-generated ID; required fields displayed |
| 3 | Operator enters production batch data | Validation rules enforce required fields and format constraints |
| 4 | Operator submits for review | Status changes to "Pending Review"; reviewer notified |
| 5 | Reviewer (different user) opens and approves with e-signature | Signature captured per 21 CFR Part 11; audit trail updated |
| 6 | Verify audit trail completeness | Entries for each action with user ID, timestamp, description |
| 7 | Generate batch record report | Report produced within performance threshold; content matches record |

**Acceptance criteria:** All steps succeed across 3 executions. Segregation of duties enforced. Audit trail ALCOA+ compliant. Report generation within URS-015 threshold.

### 6.2 Access Control and Segregation (PQ-002)

**Traces to:** URS-002, URS-003, URS-019 | **Consecutive Executions:** 3

| Step | Action | Expected Result |
|---|---|---|
| 1 | Log in as each production role (operator, reviewer, admin, read-only) | Each role sees only permitted functions |
| 2 | As operator, attempt admin access | Blocked; event logged in audit trail |
| 3 | As operator, create record then attempt self-approval | Self-approval prevented; segregation enforced |
| 4 | As read-only, attempt record modification | Blocked; no data changes persist |
| 5 | Verify all access control events in audit trail | Denied actions logged with user, timestamp, reason |

**Acceptance criteria:** Zero unauthorized actions across 3 executions. Every blocked action generates audit trail entry.

### 6.3 Performance Under Production Load (PQ-003)

**Traces to:** URS-020, URS-021, URS-022 | **Consecutive Executions:** 3

| Step | Action | Expected Result |
|---|---|---|
| 1 | Establish expected concurrent user load | All sessions connect successfully |
| 2 | Execute primary workflow under load | Completes within response time thresholds |
| 3 | Generate report with production-scale data | Within URS time limit |
| 4 | Search across full production data volume | Within URS response time |
| 5 | Calculate mean, stddev, P95 across all executions | All metrics within URS thresholds |

**Acceptance criteria:** Mean response times within URS thresholds. P95 does not exceed specification. No degradation trend across executions. Zero timeouts or failures under load.

---

## 7. Performance Criteria Categories

### 7.1 Functional Performance
End-to-end workflows complete correctly. All business rules enforced. Outputs match expected results. **Threshold:** 100% correct results across all consecutive executions.

### 7.2 Response Time Performance
Operations complete within URS-defined time limits. If the URS lacks response time thresholds, coach the customer to add them before PQ. **Typical defaults:** interactive operations < 3s, reports < 30s, searches < 5s, batch processing per URS.

### 7.3 Data Integrity
Data stored accurately, displayed correctly, survives complete workflows without corruption. Audit trails complete and ALCOA+ compliant. Electronic signatures meet 21 CFR Part 11. **Threshold:** Zero data integrity failures — non-negotiable.

### 7.4 Reproducibility
Same workflow, multiple executions, consistent results. **Threshold:** Results consistent across all consecutive executions; performance metrics within defined tolerance intervals.

---

## 8. Statistical Methods

Apply statistical rigor to PQ scenarios with quantitative performance criteria rather than relying on single-point pass/fail.

### When to Use

Systems with URS performance requirements, load-sensitive workflows, time-dependent functions, or when the customer's quality framework requires statistical demonstration.

### Recommended Calculations

| Metric | Purpose |
|---|---|
| Mean | Central tendency — "typical" performance |
| Standard Deviation | Variability — how much performance fluctuates |
| 95th Percentile (P95) | Worst realistic case — occasional user experience |
| Min / Max | Range check for outliers |

### Tolerance Intervals

Estimate the range containing a specified proportion of future measurements with a given confidence. Example: "With 95% confidence, 99% of report generation times will fall below 28 seconds" is stronger than "all three test runs were under 30 seconds."

### Process Capability (Cpk)

For tight specifications with sufficient data (25+ points): Cpk >= 1.33 is capable, 1.0-1.33 is marginal, < 1.0 is not capable. Recommend only for high-criticality requirements or when the customer's framework mandates it.

Include raw data in appendices. Summarize statistics in scenario results. Flag measurements exceeding P95, even if the mean passes.

---

## 9. Duration Guidance

### 3 Consecutive Executions

Each scenario executed minimum 3 times consecutively. Demonstrates reproducibility, not one-time success. If any execution fails, all three repeat after root cause resolution — partial passes are not acceptable.

### Operational Period Coverage

| Function Type | Minimum Duration |
|---|---|
| Shift-based workflows | One complete shift cycle |
| Daily batch processes | 3 consecutive days |
| Weekly reporting | One complete cycle |
| Month-end processing | One complete cycle |
| Scheduled maintenance | One complete execution |

### Time-Dependent Functions

Scheduled tasks, timeout handlers, token expiration, and session management require PQ scenarios that exercise the time boundaries — not just normal operation within them.

> "Three consecutive successful executions is the widely accepted minimum. If your customer mandates 5 or 10, follow their standard. If they have no standard, recommend 3 and document the rationale."

---

## 10. Production Conditions

PQ must execute under conditions representing actual production use. Testing in a sanitized lab environment is OQ, not PQ.

| Condition | PQ Requirement |
|---|---|
| **Infrastructure** | Production servers/network/database, or production-equivalent with documented equivalence justification |
| **Data** | Real production data or representative set matching production volume and complexity. Synthetic only if production data cannot be used (document equivalence) |
| **User accounts** | Real production accounts with assigned roles — not shared test accounts |
| **Integrations** | Production instances of upstream/downstream systems (or validated stubs with documented equivalence) |
| **Concurrent load** | Other users performing normal work during PQ execution |
| **Configuration** | Production parameters — not elevated timeouts, reduced security, or debug modes |

### Segregation of Duties

The person who creates a record cannot approve it. The person who configured the system cannot execute PQ unsupervised. QA review of PQ results is independent of execution.

### Production Data Considerations

If using actual production data: confirm no patient safety or privacy implications, document that test activities will not corrupt data, define rollback procedures. If using representative data: document representativeness criteria and include comparison to production characteristics in the appendix.

---

## 11. How PQ Feeds the VSR

| VSR Section | PQ Contribution |
|---|---|
| Qualification Summary | Scenarios executed, pass/fail count, deviation count |
| Requirements Coverage | URS-to-PQ traceability with pass status per requirement |
| Deviation Summary | All deviations with severity, root cause, CAPA, resolution |
| Performance Evidence | Statistical summaries for performance scenarios |
| Residual Risk | URS requirements not fully verified, with risk justification |
| Conclusion Support | Statement that system performs as intended under production conditions |

**Vendor evidence package:** Completed PQ protocol with results, deviation log, traceability matrix (URS-to-PQ with pass/fail), performance data, environmental conditions record, screenshots and raw data.

---

## 12. FDA CSA Alignment (2025)

The FDA's Computer Software Assurance guidance (September 2025) shifts from exhaustive scripted testing toward risk-based, critical thinking approaches.

| CSA Principle | PQ Impact |
|---|---|
| **Risk-based testing** | Focus PQ depth on high-risk workflows (patient safety, data integrity) |
| **Intended use** | Test the system as actually used — reinforces workflow-driven approach |
| **Critical thinking** | Testers understand *why* each scenario matters, not just follow steps |
| **Unscripted testing** | Exploratory testing permitted for lower-risk functions — document observations |
| **Proportionate documentation** | Depth proportionate to risk — Cat 3 needs less rigor than Cat 5 |

### GAMP Category Scaling

| Category | PQ Approach |
|---|---|
| **3** (non-configured) | Light PQ: 3-5 scenarios, may leverage vendor OQ for low-risk functions |
| **4** (configured) | Standard PQ: 8-20 scenarios covering configured business processes |
| **5** (custom) | Comprehensive PQ: 15-40+ scenarios, performance validation, statistical methods |

> "CSA does not eliminate PQ — it makes PQ smarter. The shift is from 'test everything with scripts' to 'test what matters, test it thoroughly, and explain your rationale.'"

---

## 13. Coaching Questions

Use during Phase 2 (Coached Refinement), section by section.

**Scope:** "Which workflows are most critical to your customer's regulated operations?" / "Has the URS defined performance thresholds? Without them, PQ criteria lack measurable targets." / "Does the customer have a corporate standard for consecutive executions?"

**Scenario design:** "This tests a function, not a workflow — can we expand to the full business process?" / "Who are the actual production users? Name their roles." / "What happens when this workflow fails midway? Do you have an error recovery scenario?"

**Acceptance criteria:** "This says 'system responds promptly' — an auditor will ask 'how promptly?'" / "Are there data integrity checks at each handoff point?" / "If scenario fails on execution 2 of 3, what is the retest procedure?"

**Production conditions:** "Actual production or production-equivalent? Document equivalence if the latter." / "Will other users be working during PQ? Do not lock everyone out." / "Are integrations connected to production instances?"

**Traceability:** "Every URS requirement should appear in at least one PQ scenario — run the gap check." / "This scenario traces to no URS requirement — is the URS missing something, or is this an orphan test?"

---

## 14. Anti-Patterns

**Feature checklist disguised as PQ.** PQ scenarios test individual functions in isolation. Fix: restructure around complete business workflows from trigger to outcome.

**Synthetic environment.** PQ runs in a test environment with test accounts and test data. Fix: execute in production with real accounts and representative data.

**Single execution.** Each scenario run once — no reproducibility evidence. Fix: minimum 3 consecutive executions, documented independently.

**Vague acceptance criteria.** Words like "acceptable," "timely," "reasonable." Fix: measurable thresholds traceable to URS requirements.

**Missing traceability.** PQ scenarios do not reference URS requirements, or URS requirements have no PQ coverage. Fix: build traceability table first, run gap analysis after design.

**Vendor executes PQ.** Vendor team runs PQ in the customer's environment. Fix: customer's trained users execute and sign. Vendor may observe and assist.

**Ignoring time-dependent functions.** PQ runs in a single afternoon; scheduled tasks never tested. Fix: extend duration to cover relevant time cycles.

**Copy-paste from OQ.** PQ test steps are identical to OQ with "PQ" in the header. Fix: PQ tests workflows (not functions), uses production conditions (not test environments), demonstrates reproducibility (not single-pass correctness).

---

## Override Points

| Override Point | Default |
|---|---|
| `consecutive_executions` | 3 |
| `statistical_methods` | mean, stddev, P95 |
| `deviation_severity_scheme` | Critical / Major / Minor |
| `approval_signatures` | Executed / Reviewed / QA Approved |
| `appendix_structure` | Data, performance logs, statistics, deviation evidence |
| `performance_thresholds` | From URS |
| `scenario_count_minimum` | By GAMP category (see Section 12) |

---

## GAMP 5 Addenda

When the manifest indicates GAMP 5 regulatory context:

- **Leveraging supplier testing:** GAMP 5 2nd Edition emphasizes leveraging vendor OQ evidence to reduce PQ burden, particularly for Cat 3/4. Document which OQ results the customer leverages and why additional PQ is or is not needed.
- **Risk-based approach:** Scale PQ effort to impact on patient safety, product quality, and data integrity. Document the risk assessment that determined PQ scope.
- **Critical thinking:** Testers document observations beyond scripted steps. Mechanical compliance is insufficient.
- **Data integrity focus:** ALCOA+ applies to PQ test data itself — records must be attributable, legible, contemporaneous, original, and accurate.

### Requirement Format

```
ID:                 PQ-{NNN}
Title:              [Concise scenario title]
Traces to:          [URS-{NNN}, URS-{NNN}]
Workflow:           [Business process name]
Preconditions:      [What must be true before execution]
Steps:              [Numbered sequence]
Expected Results:   [Per step]
Acceptance Criteria:[Measurable thresholds]
Consecutive Runs:   [Number required]
```

Each PQ item must trace to at least one URS requirement. Orphan PQ items are flagged as informational gaps by the traceability engine.
