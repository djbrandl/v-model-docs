# Risk Assessment — Reference File

## 1. Purpose

The risk assessment is the architectural backbone of a GAMP 5 validation effort. It answers the question every auditor asks first: "How did you decide what to test, and how deeply?" Without a formal risk assessment, the vendor cannot justify testing decisions — and unjustified testing decisions are the fastest way to an audit finding.

Risk drives testing depth. A high-risk function (patient safety impact, data integrity exposure) demands dedicated scripted OQ test cases with boundary analysis and negative testing. A low-risk function (cosmetic display preference, internal logging) may be covered by vendor standard testing or visual inspection. This proportionality is the core principle of GAMP 5 2nd Edition and FDA CSA guidance — but it only works when the risk assessment exists, is documented, and is traceable to every downstream testing decision.

**Vendor framing:** The vendor performs the initial risk assessment based on intimate knowledge of the system's architecture, failure modes, and component interactions. The vendor knows where the system is fragile, where custom code introduces uncertainty, and where infrastructure components are battle-tested. The customer's QA team then reviews and may add risks related to their specific operational environment — workflows, user populations, adjacent systems, and site-specific regulatory exposure. The final risk assessment is a collaborative artifact, but the vendor provides the technical foundation.

The risk assessment feeds directly into three downstream artifacts:
- **VP** — the validation approach section references risk levels to justify testing strategy
- **OQ Protocol** — test case count and design technique selection scale by risk level
- **Traceability Matrix** — the `risk_level` field on each requirement drives gap severity classification

---

## 2. Predecessor Dependencies

| Predecessor | What It Provides | Required? |
|---|---|---|
| **URS** | The functions and requirements to assess — without defined requirements, there is nothing to evaluate for risk | Yes |
| **Discovery Report** | Component inventory, architecture context, GAMP category assignments, integration points — these inform occurrence and detectability scores | Yes |
| **VP** (if available) | Regulatory context, CSA vs CSV stance, GAMP category — shapes the severity scale emphasis | Recommended |

When generating before the VP exists, default to a balanced severity scale. When the VP later declares CSA-aligned, revisit the assessment to ensure patient safety and data integrity risks are weighted appropriately over business-impact risks.

---

## 3. Required Sections

### 3.1 Front Matter

```markdown
**Document ID:** RA-001  |  **Version:** {version}  |  **Date:** {date}
**System:** {system_name}  |  **GAMP Category:** {category}
**Prepared by:** {vendor_name}  |  **Reviewed by:** {customer_qa}
**Assessment methodology:** FMEA (Failure Mode and Effects Analysis)
**Status:** {draft | approved}

#### Revision History
| Version | Date | Author | Changes |
|---|---|---|---|
| 0.1 | {date} | {author} | Initial draft |
```

### 3.2 Purpose and Scope

Define the boundaries of the assessment: which system components are included, which are excluded (separately validated, out of scope), and which regulatory frameworks apply. Reference the URS and discovery report by document ID.

### 3.3 System Description

Brief system overview drawn from the VP system description section or discovery report. Include the component inventory with GAMP category assignments — these directly inform failure mode generation (Section 5).

### 3.4 Risk Assessment Methodology

State the methodology (FMEA), the scoring scales (Section 4), the classification thresholds (Section 6), and the decision rules for risk-to-testing mapping (Section 7). An auditor must be able to reproduce your risk classification from the documented methodology alone.

**EU GMP Annex 11 Considerations:**

- For EU GMP-regulated systems, Annex 11 Clause 1 explicitly requires risk management throughout the computerised system lifecycle. The risk assessment methodology and results should be documented to demonstrate compliance with this clause.
- Risk-based decisions (e.g., which data elements to audit trail, which test cases to automate vs. manual) must be documented and defensible per Annex 11 Clause 9's risk-based approach.

### 3.5 Risk Classification Criteria

The severity, occurrence, and detectability scales with pharma-relevant definitions (Section 4).

### 3.6 Risk Assessment Table (FMEA)

The core deliverable. Each row is a failure mode with severity, occurrence, detectability scores, RPN, risk level, and recommended controls. See Section 9 for a worked example.

### 3.7 Risk-to-Testing Mapping

Table mapping risk levels to testing depth across IQ, OQ, and PQ (Section 7).

### 3.8 Residual Risk Summary

After applying controls (testing, validation, procedural mitigations), summarize the residual risk profile. State whether residual risks are acceptable per the defined thresholds.

### 3.9 Recommendations

Specific actions for the validation team: which areas need the most OQ attention, which components warrant additional IQ verification, where procedural controls supplement testing.

---

## 4. FMEA Methodology

Failure Mode and Effects Analysis evaluates each potential failure mode across three dimensions. The product of these three scores is the Risk Priority Number (RPN):

**RPN = Severity x Occurrence x Detectability**

RPN range: 1 (lowest risk) to 125 (highest risk) on a 1-5 scale.

### 4.1 Severity (S) — Impact If the Failure Occurs

| Score | Level | Pharma Definition | Examples |
|---|---|---|---|
| 5 | Catastrophic | Direct patient safety impact; potential for patient harm or death | Incorrect dosing calculation, failure to detect out-of-range critical process parameter |
| 4 | Critical | Data integrity violation affecting regulated records; 21 CFR Part 11 / ALCOA+ breach | Audit trail disabled, electronic signatures bypassable, GxP data modified without traceability |
| 3 | Major | Product quality impact; batch release or manufacturing decision affected | Incorrect batch record data, alarm suppression for quality-critical parameter, wrong material substitution |
| 2 | Minor | Business process disruption with no patient, data integrity, or product quality impact | Report generation failure, non-critical notification delay, UI display error in non-regulated field |
| 1 | Negligible | Cosmetic or convenience issue; no regulatory, quality, or safety consequence | Color scheme preference, non-critical log verbosity, sort order on non-regulated listing |

> **Coaching:** "Severity is the one score you cannot reduce through testing or controls. A dosing calculation error is always severity 5, regardless of how many tests you write. Be honest about severity — underscoring it is the single most dangerous mistake in risk assessment."

### 4.2 Occurrence (O) — Likelihood of the Failure Happening

| Score | Level | Definition | Indicators |
|---|---|---|---|
| 5 | Very High | Failure is almost certain in normal operation | Known defect, no error handling, untested code path, new custom code with no unit tests |
| 4 | High | Failure is likely under foreseeable conditions | Complex custom logic, multiple integration points, limited vendor testing |
| 3 | Moderate | Failure is possible but not expected in normal use | Configured COTS with some customization, standard integration patterns |
| 2 | Low | Failure is unlikely given the component maturity | Established COTS product, proven architecture, extensive vendor test history |
| 1 | Very Low | Failure is implausible under any foreseeable condition | Infrastructure component (Cat 1), hardened platform, decades of production use |

GAMP category informs occurrence scoring: Cat 5 custom components typically score 3-5; Cat 4 configured products score 2-4; Cat 3 non-configured COTS scores 1-2; Cat 1 infrastructure scores 1.

### 4.3 Detectability (D) — Ability to Detect the Failure Before Impact

| Score | Level | Definition | Examples |
|---|---|---|---|
| 5 | Undetectable | No mechanism exists to detect the failure before it reaches the end user or regulated record | Silent data corruption, background process failure with no alerting, calculation error with no independent check |
| 4 | Low Detection | Failure may be detected but only through manual review or post-hoc analysis | Errors visible only in audit trail review, discrepancies found during periodic reconciliation |
| 3 | Moderate Detection | Automated monitoring exists but does not guarantee real-time detection | Batch log review, scheduled integrity checks, periodic report comparison |
| 2 | High Detection | System has built-in validation or alerting that catches most failures promptly | Input validation, range checks, automated alerts on threshold violations |
| 1 | Immediate Detection | Failure is automatically detected and blocked before any impact occurs | Database constraint enforcement, real-time redundancy check, transaction rollback on error |

> **Coaching:** "Detectability is counterintuitive — a score of 1 means the failure is easily detected (good), while 5 means it is nearly undetectable (bad). This trips up teams every time. Double-check your D scores are oriented correctly."

### 4.4 AP (Action Priority) — AIAG-VDA Alternative

The AIAG-VDA FMEA Handbook (2019) introduced Action Priority (AP) as an alternative to RPN. AP uses a lookup table rather than simple multiplication, addressing the known weakness of RPN where different S-O-D combinations produce the same number but have very different risk profiles (e.g., S=5/O=1/D=5 = 25 vs S=1/O=5/D=5 = 25 — these are not equivalent risks).

| AP Level | Meaning | Action Required |
|---|---|---|
| **High** | Unacceptable risk; action required to improve prevention or detection controls | Mandatory — must implement controls before proceeding |
| **Medium** | Risk should be reduced; action recommended | Should take action — document justification if deferred |
| **Low** | Acceptable risk; no additional action required | Optional — current controls are adequate |

AP prioritizes severity over occurrence and occurrence over detectability. A high-severity failure mode receives High AP even if occurrence is low. This aligns better with pharma risk philosophy where patient safety cannot be traded against probability.

**When to use AP vs RPN:** Use RPN as the default — it is well understood by pharma QA teams and auditors. Offer AP as an alternative when the customer's QA team follows the AIAG-VDA methodology or when RPN produces misleading equivalences in the assessment.

---

## 5. Pre-Seeding from Discovery

The discovery report provides a component inventory with GAMP category assignments. Use this to automatically generate candidate failure modes before the risk assessment workshop.

### Pre-Seeding Rules by GAMP Category

| GAMP Category | Candidate Failure Modes | Rationale |
|---|---|---|
| **Cat 5** (Custom) | 8-15 candidates per component: functional errors, calculation errors, data handling failures, integration failures, concurrency issues, error handling gaps, security vulnerabilities, upgrade/migration failures | Custom code has the widest failure surface; every function is a potential failure mode |
| **Cat 4** (Configured) | 4-8 candidates per component: misconfiguration, workflow logic errors, report/output errors, integration failures, access control gaps | Configuration is the primary risk vector; underlying platform is vendor-tested |
| **Cat 3** (Non-configured) | 1-3 candidates per component: installation failure, version incompatibility, platform interaction | Product is used as-is; failures are environmental, not functional |
| **Cat 1** (Infrastructure) | 1-2 candidates per component: installation/configuration error, capacity/performance | Mature platform; risks are operational, not functional |

### Pre-Seeding Process

1. Parse the discovery report's component inventory
2. For each component, apply the category-appropriate failure mode templates
3. Pre-populate severity scores based on the component's regulatory touchpoints (components handling GxP data start at S >= 3)
4. Pre-populate occurrence scores based on GAMP category (see Section 4.2 indicators)
5. Leave detectability blank — it requires system-specific knowledge of monitoring and alerting capabilities
6. Present the pre-seeded table to the vendor team for review, refinement, and completion

> **Coaching:** "Pre-seeded failure modes are starting points, not final answers. The team must review every row, adjust scores, add failure modes the template missed, and remove any that do not apply. A risk assessment that looks exactly like the template is a risk assessment that was not actually performed."

### OT / IEC 62443 Pre-Seeded Failure Modes

**When to apply:** When `regulatory_context` includes IEC 62443 or system type is OT/SCADA/ICS.

For Operational Technology environments, the standard GAMP-category-based pre-seeding must be supplemented with OT-specific failure modes that address cybersecurity risks at zone and conduit boundaries. These failure modes reflect the unique threat landscape of industrial control systems where cyber-physical consequences are possible.

**Pre-seeded failure modes for OT systems:**

| ID | Function/Component | Failure Mode | Potential Effect | IEC 62443 Reference |
|---|---|---|---|---|
| RA-OT-001 | Network segmentation | Unauthorized access from enterprise zone to process control zone | Unauthorized process modification, potential safety impact | IEC 62443-3-3 SR 5.1 (Network Segmentation) |
| RA-OT-002 | Remote access | Unauthorized remote access to OT network | Process manipulation, data exfiltration, safety impact | IEC 62443-3-3 SR 1.13 (Access via untrusted networks) |
| RA-OT-003 | Malware propagation | Malware spreads from IT to OT via shared services | System downtime, process disruption, data corruption | IEC 62443-3-3 SR 3.2 (Malicious code protection) |
| RA-OT-004 | Denial of service | Network flood or resource exhaustion on OT network | Loss of control visibility, delayed operator response | IEC 62443-3-3 SR 7.1 (Denial of service protection) |
| RA-OT-005 | Safety system interaction | Validated system interferes with Safety Instrumented System (SIS) | Compromised safety function, potential patient/product harm | IEC 62443-3-3 SR 5.2 (Zone boundary protection) |
| RA-OT-006 | Patch management | Delayed or untested security patch on OT system | Known vulnerability exploited, system compromise | IEC 62443-2-3 (Patch management) |
| RA-OT-007 | Historian data integrity | Unauthorized modification of historian records | Falsified batch/process records, compliance violation | IEC 62443-3-3 SR 3.4 (Software and information integrity) |
| RA-OT-008 | Time synchronization | NTP/PTP failure or manipulation | Incorrect timestamps on GxP records, broken audit trail sequencing | IEC 62443-3-3 SR 7.7 (Least functionality) |
| RA-OT-009 | Portable media | Unauthorized USB/portable media introduced to OT environment | Malware introduction, data exfiltration | IEC 62443-3-3 SR 2.3 (Use control for portable/mobile devices) |
| RA-OT-010 | Wireless access | Unauthorized wireless access point in OT environment | Network intrusion, process manipulation | IEC 62443-3-3 SR 1.6 (Wireless access management) |

**OT-Specific Detectability Considerations:**
- Many OT systems lack centralized security monitoring (SIEM) — detectability scores should reflect this
- Real-time process data may mask slow-acting attacks — consider "low and slow" detection difficulty
- OT protocol analysis (Modbus, OPC-UA, EtherNet/IP) may not be part of standard monitoring — score detectability accordingly
- Physical indicators (unexpected process behavior) may be the primary detection mechanism — factor operator vigilance into detectability

---

## 6. Risk Classification Thresholds

RPN scores map to four risk levels. These levels drive testing depth (Section 7) and feed the manifest's `risk_level` field for traceability gap severity classification.

**These thresholds are examples, not prescriptive.** Different organizations use different scales, and some pharma companies reject RPN entirely in favor of Action Priority (Section 4). The customer's corporate risk management procedure always takes precedence. Present these as starting-point defaults the customer can override.

| Risk Level | RPN Range | Action Required |
|---|---|---|
| **Critical** | 80-125 | Mandatory dedicated testing with boundary analysis, negative testing, and error recovery. Requires specific OQ test cases with pre-defined acceptance criteria. Cannot be addressed by vendor standard testing alone. |
| **High** | 45-79 | Dedicated scripted test cases in OQ. Boundary value analysis recommended. Negative test cases required for error-handling paths. |
| **Medium** | 15-44 | Standard functional test coverage in OQ. Positive testing with representative data. Boundary analysis where practical. |
| **Low** | 1-14 | Covered by vendor standard testing, IQ verification, or visual inspection. Document the rationale for reduced testing — do not simply skip it. |

### Threshold Override

These thresholds are defaults. Override them in the manifest under `overrides.risk_assessment.thresholds` when:
- The customer's QA team has established corporate thresholds
- The regulatory context demands tighter controls (e.g., safety-critical systems may lower the Critical threshold)
- A CSA-aligned approach permits wider Medium bands for non-patient-safety risks

---

## 7. Risk-to-Testing Mapping

Each risk level maps to a specific testing depth across qualification protocols. This table is the bridge between risk assessment and test design — it is what makes the risk assessment actionable rather than decorative.

| Risk Level | IQ Coverage | OQ Coverage | PQ Coverage |
|---|---|---|---|
| **Critical** | Full installation verification including component integrity checks | Dedicated scripted tests with boundary value analysis + negative testing + error recovery scenarios; minimum 3 test cases per failure mode | Mandatory PQ scenarios covering the critical function in production workflows; 3-consecutive-run reproducibility |
| **High** | Standard installation verification | Dedicated scripted tests with boundary analysis; negative test cases for primary error paths | PQ scenarios recommended; include in end-to-end workflow coverage |
| **Medium** | Standard installation verification | Functional test cases with representative positive data; boundary analysis where practical | Covered within standard PQ workflow scenarios if the function appears in tested workflows |
| **Low** | Configuration verification or checklist | Covered by vendor standard testing evidence or spot-check verification; document rationale | No dedicated PQ coverage required; incidental coverage through workflow scenarios acceptable |

> **Coaching:** "This table is a commitment. When you assign a risk level, you are committing to the testing depth in the right column. If the OQ protocol does not deliver the promised coverage, the traceability engine will flag it as a gap — and the gap severity will match the risk level."

---

## 8. Integration with Manifest

The risk assessment populates the `risk_level` field on each requirement in the project manifest. This field is consumed by the traceability engine for gap severity classification.

### Manifest Integration Rules

1. Every requirement in the manifest `requirements` array receives a `risk_level` value: `critical`, `high`, `medium`, or `low`
2. The traceability engine uses `risk_level` to classify gap severity:
   - A **critical**-risk requirement with no test coverage = **Critical** gap (audit showstopper, blocks publish)
   - A **high**-risk requirement with no test coverage = **Major** gap (likely audit finding)
   - A **medium**-risk requirement with no test coverage = **Minor** gap (observation)
   - A **low**-risk requirement with no test coverage = **Informational** gap (housekeeping)
3. When the risk assessment is updated, requirement `risk_level` values must be synchronized — run the traceability check after any risk reassessment
4. Requirements not yet assessed default to `risk_level: null`; the traceability engine treats unassessed requirements as **Major** gaps to force assessment before publish

### Manifest Schema Addition

```json
{
  "id": "URS-001",
  "text": "System shall authenticate users via SSO",
  "source_document": "urs",
  "risk_level": "high",
  "traces_to": ["FS-003", "FS-004"],
  "tested_by": ["OQ-005"]
}
```

---

## 9. Example FMEA Table

A realistic risk assessment for a SCADA/MES system managing manufacturing process data.

| ID | Component | Failure Mode | Effect | S | O | D | RPN | Risk Level | Recommended Control |
|---|---|---|---|---|---|---|---|---|---|
| RA-001 | Data Acquisition Engine (Cat 5) | Sensor data sampled outside tolerance window | Process parameter recorded at wrong time; batch decision based on non-representative data | 4 | 3 | 4 | 48 | High | Dedicated OQ tests for sampling timing under load; boundary analysis on tolerance thresholds |
| RA-002 | Alarm Management Module (Cat 4) | Critical alarm suppressed during operator acknowledgment race condition | Operator unaware of out-of-spec condition; product quality risk per ISA-18.2 | 5 | 2 | 4 | 40 | Medium | OQ test cases for concurrent alarm scenarios; verify ISA-18.2 shelving/suppression rules |
| RA-003 | Audit Trail Service (Cat 5) | Audit trail entries written without timestamp or user identity | ALCOA+ violation (Attributable, Contemporaneous); 21 CFR Part 11 finding | 4 | 2 | 5 | 40 | Medium | OQ tests verifying all CRUD operations generate complete audit entries; negative tests for missing fields |
| RA-004 | Electronic Signature Module (Cat 5) | Signature applied without re-authentication on meaning change | 21 CFR Part 11 §11.100 violation; signed record does not reflect signer's intent | 5 | 2 | 3 | 30 | Medium | OQ test cases for signature workflow including meaning modification; negative test for bypass attempt |
| RA-005 | Role-Based Access Control (Cat 4) | Privilege escalation through direct API call bypassing UI role checks | Unauthorized access to GxP functions; data integrity risk | 5 | 3 | 5 | 75 | High | OQ security test cases: API-level access verification per role; negative tests for unauthorized endpoints |
| RA-006 | Report Generation Engine (Cat 4) | Batch report renders stale cached data instead of current values | Batch release decision based on outdated data; product quality impact | 3 | 3 | 3 | 27 | Medium | OQ test verifying report data freshness; compare report output to source data timestamps |
| RA-007 | System Backup Service (Cat 1) | Backup completes but data restoration fails silently | Disaster recovery compromised; no detection until recovery is needed | 4 | 1 | 5 | 20 | Medium | IQ verification of backup/restore cycle; periodic restore test in OQ |
| RA-008 | Integration Gateway (Cat 5) | Message queue overflow drops inbound records from upstream ERP | GxP data lost without error notification; traceability gap in batch genealogy | 4 | 3 | 4 | 48 | High | OQ load tests at queue capacity limits; verify dead-letter queue and alerting; negative test for overflow behavior |

> **Coaching:** "Notice the severity scores are not all 3s and 4s. A real risk assessment has variance. If your table has uniform scoring, you are probably applying default scores instead of thinking through each failure mode. Also notice RA-002 — an alarm suppression race condition scores S=5 because ISA-18.2 safety implications are real, even though occurrence is low."

---

## 10. Coaching Prompts

Use these during Phase 2 (coached refinement) when reviewing the risk assessment with the vendor team.

**Failure mode completeness:**
- "Have you considered what happens if this component fails silently — no error, no log entry, no alert? Silent failures are the highest-detectability-score scenarios."
- "What failure modes exist at integration boundaries? Data format mismatches, timeout behaviors, and retry exhaustion are common omissions."
- "Are there failure modes related to concurrent access? Multi-user systems often have race conditions that single-user testing misses."

**Score calibration:**
- "Is the detectability score realistic or optimistic? Score based on what detection mechanisms exist today, not what you plan to build."
- "You scored occurrence as 1 (very low) for a custom component. What evidence supports that — is there production history, or is this a new code path?"
- "This severity score of 2 assumes no patient impact. Walk me through the data flow — does this field ever influence a GxP decision downstream?"

**Coverage and completeness:**
- "Every Cat 5 component should have at least 3-5 failure modes assessed. This component has one. What else can go wrong?"
- "I see failure modes for data entry but none for data retrieval. What if the system stores data correctly but returns the wrong result on query?"
- "No failure modes address the upgrade/migration path. What happens to in-flight transactions during a system update?"

**Risk-to-testing alignment:**
- "This failure mode is rated High but I see no corresponding OQ test case in the testing plan. The traceability engine will flag this as a Major gap."
- "Three failure modes share the same OQ test case. Does that single test actually cover all three failure scenarios, or is it testing one and claiming coverage for three?"

---

## 11. Anti-Patterns

### AP-1: All-Medium Scoring
Every failure mode scores in the 15-44 RPN range. This indicates the team avoided committing to high or low scores — a defensive posture that produces a risk assessment without discriminating power. If everything is medium risk, the assessment provides no guidance on where to concentrate testing effort. **Fix:** Re-assess with the team, starting from severity. Force at least one score of 5 and one score of 1 across the table.

### AP-2: Risk Assessment Performed After Testing
The risk assessment was written to justify testing that already occurred, rather than to drive testing decisions. Auditors detect this immediately — the risk levels perfectly match the existing test coverage, with no gaps and no over-testing. **Fix:** Time-stamp the risk assessment before protocol authoring. If it genuinely was performed late, be transparent and note it as a deviation with corrective action.

### AP-3: Copy-Paste from Another Project
Failure modes, scores, and components lifted from a previous system's risk assessment. Component names may not match the current system. Scores reflect a different architecture. **Fix:** Pre-seed from discovery (Section 5) and require the team to review every row against the actual system.

### AP-4: No Patient Safety Consideration
The severity scale omits patient safety entirely, focusing only on business impact and system availability. In a pharma context, patient safety is always the highest severity category. A system that appears low-risk from a business perspective may be high-risk if it influences patient-facing decisions. **Fix:** Ensure the severity scale includes patient safety as the top tier (S=5). Walk through each failure mode asking "could this ultimately affect a patient?"

### AP-5: Detectability Scores Ignore Monitoring Gaps
The team scores detectability based on what monitoring they intend to build, not what exists today. A system with no alerting infrastructure should not score D=2 because "we plan to add alerts." **Fix:** Score detectability based on current-state controls. If planned controls will reduce detectability, note the planned improvement as a recommended control and reassess after implementation.

### AP-6: Risk Assessment as a One-Time Event
The risk assessment is performed once and never revisited, even as the system evolves, new components are added, or the operational environment changes. **Fix:** Include a review trigger list — major version upgrade, new integration, regulatory change, post-incident — and date the next scheduled review.

### AP-7: Conflating Occurrence with Severity
The team scores high occurrence because the impact would be severe, or low severity because the failure is unlikely. Severity and occurrence are independent dimensions. A catastrophic failure that is unlikely still scores S=5, O=1. **Fix:** Assess severity first in isolation ("if this failure happens, what is the impact?"), then occurrence separately ("how likely is this failure to happen?").

---

## Override Points

These sections accept company-specific customization via the manifest `overrides.risk_assessment` configuration.

| Override Key | What It Controls | Default |
|---|---|---|
| `methodology` | FMEA, HAZOP, or custom risk methodology name | FMEA |
| `severity_scale` | Custom severity scale definitions (must maintain 1-5 range) | Pharma scale (Section 4.1) |
| `occurrence_scale` | Custom occurrence scale definitions | Standard scale (Section 4.2) |
| `detectability_scale` | Custom detectability scale definitions | Standard scale (Section 4.3) |
| `thresholds` | RPN-to-risk-level mapping boundaries | Critical: 80-125, High: 45-79, Medium: 15-44, Low: 1-14 |
| `use_action_priority` | Use AIAG-VDA AP instead of RPN for classification | false |
| `pre_seed_templates` | Custom failure mode templates per GAMP category | Built-in templates (Section 5) |
| `custom_sections` | Additional sections injected after the FMEA table | None |
| `residual_risk_template` | Company-specific residual risk acceptance format | Default summary format |

---

## GAMP 5 Addenda

### Risk-Based Validation Under GAMP 5 2nd Edition

GAMP 5 2nd Edition (2022) elevates risk assessment from a recommended practice to the central driver of validation scope. It is the engine that determines:
- Which requirements receive detailed specification (FS/DS depth)
- Which test design techniques are applied (boundary analysis vs spot-check)
- How much vendor testing evidence the customer can leverage vs must independently verify
- Whether unscripted testing is appropriate for a given function
- What constitutes sufficient evidence for each risk tier

### CSA Alignment

Under FDA CSA guidance (September 2025), risk assessment explicitly determines the assurance activities applied to each software function:

| CSA Risk Tier | Assurance Activities | Risk Assessment Mapping |
|---|---|---|
| High (patient safety) | Scripted testing with pre-defined acceptance criteria; independent verification | Critical and High risk levels |
| Moderate (product quality, data integrity) | Combination of scripted and unscripted testing; vendor evidence leverage | Medium risk level |
| Low (no direct patient/product impact) | Unscripted testing, vendor evidence review, or inspection | Low risk level |

When the VP declares CSA-aligned, the risk assessment must explicitly map each failure mode to a CSA risk tier and document the corresponding assurance activity justification.

### Periodic Risk Reassessment

GAMP 5 2nd Edition requires periodic risk reassessment as part of the system's validated lifecycle. Triggers include:
- Major system version upgrades
- New integrations with GxP systems
- Regulatory guidance changes affecting the system's compliance scope
- Post-incident review revealing previously unidentified failure modes
- Changes to the operational environment (new user populations, new sites, new workflows)

Document the reassessment schedule in the risk assessment itself. The vendor provides updated failure mode analysis; the customer's QA team reassesses operational risks.
