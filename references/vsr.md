# Validation Summary Report (VSR) — Vendor Evidence Summary Reference File

> **Ownership model:** Customer-assist. The vendor provides a structured evidence summary of all vendor-delivered qualification artifacts. The customer's QA team incorporates this into their corporate VSR, adds PQ results, acceptance decisions, and the validation conclusion.

> **Framing note:** The vendor does not write the VSR. The customer's QA team owns it as the final validation deliverable. The vendor provides a **vendor evidence summary** — a complete, auditable inventory of everything delivered, with qualification results, deviation dispositions, and traceability metrics. This feeds directly into the customer's VSR without requiring them to reconstruct vendor-side evidence from scattered documents.

---

## 1. Purpose

The VSR is the bookend to the Validation Plan. Where the VP says "here is how we will validate this system," the VSR says "here is what we did, what we found, and whether the system is fit for intended use."

The customer's QA team writes the VSR. They need vendor-side evidence consolidated in one place — not buried across six documents. The vendor evidence summary gives them a single-document inventory of everything delivered (with versions and dates), IQ/OQ pass/fail summaries, deviation dispositions for residual risk assessment, traceability coverage metrics, and a vendor statement of conformance.

**What the customer's QA team expects:** A document they can attach as a VSR appendix. If an auditor asks "what did the vendor deliver and what were the results?", this answers it without opening any other file.

---

## 2. Predecessor Dependencies

The vendor evidence summary is the **last vendor deliverable**. It summarizes everything else.

| Predecessor | Status Required | Why |
|---|---|---|
| FS | Approved | Referenced in document inventory |
| DS | Approved | Referenced in document inventory |
| IQ Protocol | Executed, results documented | Pass/fail counts feed qualification summary |
| OQ Protocol | Executed, results documented | Pass/fail counts feed qualification summary |
| Risk Assessment | Approved | Risk-based testing rationale referenced |
| Traceability Matrix | Current | Coverage metrics extracted directly |
| Vendor Assessment Package | Delivered | Listed in document inventory |
| All deviations | Dispositioned | Deviation summary requires resolution status |

**Hard gate:** Do not generate until IQ and OQ execution results are available. In fast draft mode, produce a skeleton with `<!-- TODO: Populate after IQ/OQ execution -->` markers in results sections. Document inventory and traceability metrics can populate from the manifest.

---

## 3. Required Sections for Vendor Evidence Summary

### 3.1 Cover Page

System name, version, vendor name, document ID and version, date prepared, preparer name and role. Include a **Document Versions Delivered** table listing every vendor deliverable with its version and delivery date.

> **Coaching:** "Every document the customer received should appear here with its exact version. If an auditor compares this list against the customer's document control system and finds a mismatch, that is a finding."

### 3.2 Vendor Qualification Evidence Summary

Summarize IQ and OQ results without reproducing full protocols. For each qualification stage, provide a table with: total checks/cases, passed count, failed count, deviations raised, deviations resolved, deviations open. Follow each table with a one-sentence conclusion referencing the source specification and version.

```
IQ Conclusion pattern:  "All installation verification checks passed [with
  deviations resolved]. {System} is correctly installed and configured per
  the Design Specification v{version}."

OQ Conclusion pattern:  "All functional test cases passed [with deviations
  resolved]. {System} operates in accordance with the Functional
  Specification v{version}."
```

> **Coaching:** "If any deviations remain open, state their IDs explicitly and reference the deviation summary table. Do not bury open items."

### 3.3 Traceability Coverage Metrics

Pull directly from `traceability_check.py` output. Required metrics:

| Metric | Value |
|---|---|
| Total URS requirements | {n} |
| URS traced to FS | {n} ({%}) |
| FS traced to DS | {n} ({%}) |
| FS items with OQ coverage | {n} ({%}) |
| DS items with IQ coverage | {n} ({%}) |
| URS with PQ coverage | {n} ({%}) — customer-owned |
| Orphan test cases | {n} |
| Broken trace links | {n} |

Follow with a gap summary table: gap type, count, severity, brief description.

> **Coaching:** "100% forward traceability from URS to test is the target. Each gap below 100% needs a documented justification — risk-based exclusion, deferred phase, or covered by vendor internal testing. Unexplained gaps are audit findings."

### 3.4 Deviation Summary Table

Every deviation raised during IQ and OQ, consolidated in one table.

Columns: Dev ID, Source (originating test case), Classification (Critical/Major/Minor), Description, Root Cause, Resolution, Impact Assessment, Status (Open/Closed).

**Classification definitions:** Critical = data integrity risk, patient safety, or regulatory non-compliance (resolution required before acceptance). Major = core functionality affected (resolution required; documented risk acceptance possible). Minor = non-critical (documented with resolution plan; does not block acceptance).

> **Coaching:** "Every deviation needs a root cause and impact assessment — not just 'fixed.' The customer needs to know whether it is systemic or one-time."

### 3.5 Outstanding Items and Conditions

Table with columns: item, type (open deviation / known limitation / pending TODO), description, planned resolution, target date.

Follow with a **Conditions and Caveats** list: environmental constraints, version-specific applicability, customer-side prerequisites not yet confirmed.

> **Coaching:** "If this section is empty, state it explicitly: 'No outstanding items or conditions exist at the time of this summary.' An empty section with no statement looks like an oversight. A deliberate 'none' looks like diligence."

### 3.6 Vendor Statement of Conformance

```
{Vendor} confirms that {system} version {version} has been qualified in
accordance with GAMP 5 (2nd Edition) principles and the validation approach
defined in the Validation Plan ({VP_doc_id}, v{VP_version}).

All vendor deliverables listed in this summary are current, complete, and
accurately reflect the qualification activities performed. Deviations were
dispositioned per the vendor's quality management system, and traceability
from user requirements through specifications to test protocols has been
established and verified.

This statement covers vendor-owned qualification activities only. Performance
Qualification (PQ), the validation conclusion, and go-live authorization
remain the responsibility of {customer}'s quality organization.

Authorized Signature: ____________________
Name / Title / Date
```

> **Coaching:** "The vendor confirms *qualification*, not *validation*. Only the customer declares validation. Auditors check for this distinction."

### 3.7 Appendix: Document Inventory

Full table with columns: #, Document Title, Doc ID, Version, Date, Status, File Reference. Include every vendor deliverable plus this evidence summary itself. The file reference column uses exact delivered filenames so the customer's document control team can cross-check.

### 3.8 Annex 11 Compliance Summary

**Purpose:** For EU GMP-regulated customers, the VSR must demonstrate that the validation lifecycle addressed all applicable Annex 11 clauses. The vendor evidence summary should include a clause-by-clause summary of how each Annex 11 requirement was addressed.

**Annex 11 Clause Coverage Table:**

| Annex 11 Clause | Addressed By | Evidence Location | Status |
|---|---|---|---|
| 1. Risk Management | Risk Assessment | [doc reference] | Complete / Partial / Open |
| 2. Personnel | VP Roles & Responsibilities | [doc reference] | — |
| 3. Supplier | Vendor Assessment | [doc reference] | — |
| 4. Validation | VP, IQ, OQ, PQ protocols | [doc references] | — |
| 5. Data | FS data validation rules, OQ test cases | [doc references] | — |
| 7. Data Storage | DS data design, IQ backup verification | [doc references] | — |
| 8. Printouts | FS print functionality, OQ test cases | [doc references] | — |
| 9. Audit Trails | FS audit trail spec, DS audit design, OQ verification | [doc references] | — |
| 10. Change/Config Mgmt | DS config management, VP change control | [doc references] | — |
| 11. Periodic Evaluation | VP periodic review section | [doc reference] | — |
| 12. Security | DS security design, IQ security verification | [doc references] | — |
| 13. Incident Management | FS error handling, DS logging design | [doc references] | — |
| 14. Electronic Signature | DS e-signature design, OQ verification | [doc references] | — |
| 16. Business Continuity | DS reliability design, IQ DR verification | [doc references] | — |
| 17. Archiving | DS data design, archive verification | [doc references] | — |

> **Coaching:** "For EU-regulated customers, the Annex 11 clause coverage table is a powerful audit artifact. An auditor can quickly verify that every clause has been addressed. Incomplete rows should be flagged as open items in the VSR Outstanding Items section."

> **Note:** This table supplements the Part 11 compliance evidence already required. For dual-regulated systems, both the Part 11 and Annex 11 compliance summaries should appear in the VSR.

---

## 4. What the Vendor Does NOT Include

- **Acceptance decision.** The vendor summarizes evidence; the customer decides whether to accept.
- **PQ results.** Customer-owned and customer-executed. The vendor may note that PQ guidance was provided, but outcomes belong in the customer's VSR.
- **Corporate validation conclusion.** "The system is validated for intended use" is the customer's determination.
- **Go-live authorization.** A customer decision involving QA, IT, operations, and management.
- **Customer's risk acceptance.** The vendor documents open deviations; the customer decides whether to accept the residual risk.

> **Coaching:** "The line is qualification vs validation. The vendor qualifies (IQ, OQ). The customer validates (PQ, acceptance, go-live). The evidence summary stays on the qualification side."

---

## 5. Coaching Prompts

**Completeness:** "Does every document you delivered appear in the inventory? Cross-check against the VP deliverables list."

**Deviation quality:** "Could the customer's QA team assess risk from each deviation entry without calling you? If the impact says only 'resolved,' it is incomplete."

**Traceability:** "Run `traceability_check.py` one final time before populating metrics. Stale numbers from an earlier run may not reflect late-stage updates."

**Conformance statement:** "Does it reference the correct VP version? Does it explicitly exclude PQ and the validation conclusion?"

**Outstanding items:** "Disclosed limitations with workarounds demonstrate maturity. Undisclosed ones that an auditor discovers destroy credibility."

**Version alignment:** "If the FS was updated after OQ execution, flag this — the customer needs to assess impact."

---

## 6. Anti-Patterns

### AP-1: Vendor Claims System Is "Validated"
Only the customer can declare validation. The vendor confirms *qualification* activities are complete. Use "qualified" for vendor activities.

### AP-2: Missing Deviation Details
Deviation table lists IDs and status but no root cause or impact assessment. The customer cannot assess residual risk from ticket numbers alone.

### AP-3: No Version Tracking
Documents referenced without version numbers or dates. The evidence summary must answer "which FS version was OQ tested against?" without opening another document.

### AP-4: Stale Traceability Metrics
Coverage percentages from an earlier traceability run that do not reflect the final document set. Regenerate from the current manifest immediately before populating.

### AP-5: Omitting Outstanding Items Section
No section at all — not even a "none" statement. Absence is ambiguous; explicit "none" is a quality signal.

### AP-6: Inflated Pass Rates
Reporting "100% pass" when deviations were raised and resolved. Accurate: "X passed, Y deviations raised, all resolved." This is still a strong result and it is honest.

---

## 7. Override Points

| Override Point | Default |
|---|---|
| `deviation_classification_scheme` | Critical / Major / Minor |
| `conformance_standards_referenced` | GAMP 5 (2nd Edition) |
| `document_inventory_columns` | Title, ID, Version, Date, Status, File Reference |
| `traceability_metrics_source` | `traceability_check.py` output |
| `signature_block_format` | Single authorized vendor signature |
| `outstanding_items_categories` | Open deviation, Known limitation, Pending TODO |

---

## 8. GAMP 5 Addenda

When the manifest indicates GAMP 5 regulatory context:

- **Scaled evidence depth.** Category 3 needs a lightweight summary — document inventory, brief IQ results, vendor statement. Category 5 warrants the full structure with detailed deviation analysis and comprehensive traceability metrics.
- **Leveraged testing.** If the customer leveraged vendor OQ evidence per GAMP 5 2nd Edition, state which results were provided for leverage and confirm their currency.
- **Risk-based testing rationale.** Reference the risk assessment to explain testing depth variations. Make the risk-based scoping decision visible to auditors.
- **CSA alignment.** Per FDA CSA guidance, the evidence summary supports proportionate documentation — one consolidated reference point rather than scattered artifacts.
