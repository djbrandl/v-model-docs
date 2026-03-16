# Data Migration Validation Protocol — Reference File

## 1. Purpose

The Data Migration Validation Protocol verifies that data migrated from a legacy source system to the validated target system is complete, accurate, and maintains its integrity throughout the migration process. Data migration is consistently among the top 5 audit focus areas for regulated systems — a single unexplained discrepancy in migrated data can delay go-live by weeks and erode customer trust.

**Vendor framing:** The vendor authors the Data Migration Validation Protocol; the customer reviews, approves, and participates in execution. The vendor has the technical expertise to design the migration approach, build the migration tooling, and define transformation rules. The customer has the regulatory responsibility to verify data integrity and to confirm that migrated records retain their ALCOA+ properties.

**Regulatory context:** 21 CFR Part 11 and EU GMP Annex 11 require that electronic records maintain their integrity throughout their lifecycle — including during migration. FDA CSA guidance (Sept 2025) permits risk-based scaling of migration verification but does not eliminate the requirement for documented evidence. GAMP 5 (2nd Edition, 2022) treats data migration as a qualification activity that must be planned, executed, and documented within the validation lifecycle.

---

## 2. Predecessor Dependencies

| Dependency | Why Required |
|---|---|
| **User Requirements Specification (URS)** | URS Section 3.16 defines Migration and Data Conversion Requirements. The migration protocol must verify that these requirements are met. |
| **Functional Specification (FS)** | FS defines the functional behavior of the target system, including data entities and business rules that constrain how migrated data must behave post-migration. |
| **Design Specification (DS)** | DS defines the target data structures, schemas, and data architecture. The data mapping specification is built against DS-defined structures. |
| **Validation Plan (VP)** | VP defines the overall qualification strategy, including where data migration validation fits in the qualification sequence and its acceptance criteria. |
| **Risk Assessment (RA)** | RA identifies migration-specific failure modes and their risk ratings, which drive the verification depth and sampling strategy. |
| **IQ Protocol (approved)** | Target system must be installed and IQ-approved before production migration. Migration into an unqualified system invalidates the qualification chain. |

**Hard rule:** Do not generate migration protocol content until a DS and URS exist (at minimum in draft). The data mapping specification cannot be authored without knowing the target data structures (DS) and the migration requirements (URS). If the user requests migration validation without these predecessors, coach them to create the missing documents first.

---

## 3. Required Sections

Generate every Data Migration Validation Protocol with these sections. Mark sections as `[REQUIRED]` or `[RECOMMENDED]` — required sections cannot be removed via overrides.

| # | Section | Status | Content Guidance |
|---|---|---|---|
| 1 | Cover Page | `[REQUIRED]` | Document title, document ID, system name, source system name, version, author, date, approval signature block (prepared by, reviewed by, approved by, QA approval) |
| 2 | Revision History | `[REQUIRED]` | Table: version, date, author, description of changes. First row is always "1.0 — Initial release" |
| 3 | Table of Contents | `[REQUIRED]` | Auto-generated from headings |
| 4 | Purpose and Scope | `[REQUIRED]` | What data is being migrated, from where, to where. What is IN scope and OUT of scope. Reference URS Section 3.16, FS, and DS for target data structures |
| 5 | References | `[REQUIRED]` | URS, FS, DS, VP, RA document IDs and versions. Migration tool documentation. Source system documentation |
| 6 | Definitions and Abbreviations | `[REQUIRED]` | Source System, Target System, Migration Package, Reconciliation, Dry Run, Cutover, Rollback, Delta Migration, Data Cleansing, plus standard glossary references |
| 7 | Roles and Responsibilities | `[REQUIRED]` | Who designs, who executes, who reviews, who approves. RACI for migration activities. Source system SME involvement |
| 8 | Migration Strategy | `[REQUIRED]` | Approach (big-bang/phased/parallel-run), data mapping specification, transformation rules, data cleansing rules, migration tool identification, data volumes (see Section 4 below) |
| 9 | Data Mapping Specification | `[REQUIRED]` | Full source-to-target field mapping with transformation rules and validation rules (see Section 5 below) |
| 10 | Risk Assessment Cross-Reference | `[REQUIRED]` | Migration-specific risks, mitigations, and cross-reference to project Risk Assessment (see Section 6 below) |
| 11 | Prerequisites Checklist | `[REQUIRED]` | Conditions that must be true before migration execution begins (see Section 7 below) |
| 12 | Migration Verification Protocol | `[REQUIRED]` | Test cases organized by verification type: completeness, accuracy, transformation, referential integrity, audit trail, ALCOA+ (see Section 8 below) |
| 13 | Dry Run Requirements | `[REQUIRED]` | Minimum dry run count, dry run environment, documentation requirements (see Section 9 below) |
| 14 | Cutover Plan | `[REQUIRED]` | Step-by-step production cutover procedure (see Section 10 below) |
| 15 | Rollback Plan | `[REQUIRED]` | Rollback triggers, procedure, verification, communication (see Section 11 below) |
| 16 | Pass/Fail Criteria | `[REQUIRED]` | Overall and per-verification-type acceptance rules (see Section 12 below) |
| 17 | Deviation Log | `[REQUIRED]` | Blank template for recording deviations during execution (see Section 13 below) |
| 18 | Execution Summary | `[REQUIRED]` | Post-execution sign-off: reconciliation metrics, verification results, deviations, overall result, signatures |
| 19 | Appendices | `[RECOMMENDED]` | Full data mapping specification, reconciliation reports, sample comparison evidence, migration tool qualification evidence |

### Override Points

- Sections 1-18 are locked. Section 19 (Appendices) can be extended or removed.
- Additional sections can be injected between sections 15 and 16 (e.g., company-specific "Post-Migration Monitoring" or "Parallel Operation" sections).
- Cover page signature block roles are configurable via manifest overrides.

---

## 4. Migration Strategy

The migration strategy section defines the overall approach and serves as the architectural foundation for all subsequent verification activities.

### Migration Approach

| Approach | Description | When to Use | Risk Profile |
|---|---|---|---|
| **Big-bang** | All data migrated in a single cutover window | Small-to-medium data volumes, acceptable downtime window, single source system | Higher risk, shorter timeline, simpler rollback |
| **Phased** | Data migrated in stages (by entity, business unit, or geography) | Large data volumes, minimal downtime tolerance, multiple source systems | Lower risk per phase, longer timeline, complex state management |
| **Parallel-run** | Source and target systems operate simultaneously with data synchronized | Highly regulated environments, zero-tolerance for data loss, complex business logic | Lowest risk, highest cost, requires synchronization mechanism |

### Data Volume Estimation

Document estimated record counts per entity in a table format:

| Source Entity | Record Count | Data Size (est.) | GxP Critical? | Migration Priority |
|---|---|---|---|---|
| {Entity name} | {Count} | {Size} | Yes/No | {1-N} |
| ... | ... | ... | ... | ... |
| **Total** | **{Sum}** | **{Sum}** | | |

**Coaching note:** Data volume estimation is not optional — it drives the sampling strategy, the cutover window estimation, and the infrastructure sizing for the migration environment. Underestimating volumes is a common cause of cutover window overruns.

---

## 5. Data Mapping Specification

The data mapping specification is the most labor-intensive artifact in the migration protocol. It drives every downstream verification activity — transformation testing, accuracy verification, and reconciliation. Start it early.

### Mapping Table Format

Every migrated entity must have a complete source-to-target mapping:

| Source System | Source Table/Field | Source Data Type | Target Table/Field | Target Data Type | Transformation Rule | Validation Rule | GxP Critical? |
|---|---|---|---|---|---|---|---|
| {System name} | {Table.Field} | {e.g., VARCHAR(50)} | {Table.Field} | {e.g., NVARCHAR(100)} | {e.g., "Trim + uppercase"} | {e.g., "Not null, max 100 chars"} | Yes/No |

### Transformation Rules

Document every data transformation applied during migration. Each rule must have a unique identifier:

| Rule ID | Description | Source Format | Target Format | Example | Boundary Conditions |
|---|---|---|---|---|---|
| TR-001 | {e.g., Date format conversion} | {e.g., MM/DD/YYYY} | {e.g., YYYY-MM-DD} | {e.g., 12/31/2025 -> 2025-12-31} | {e.g., Leap year dates, century boundaries} |
| TR-002 | {e.g., Unit conversion} | {e.g., Fahrenheit} | {e.g., Celsius} | {e.g., 212F -> 100.0C} | {e.g., Precision at extreme values} |

### Data Cleansing Rules

Document data quality rules applied during migration:

| Rule ID | Description | Condition | Action | Audit Trail |
|---|---|---|---|---|
| DC-001 | {e.g., Deduplication} | {e.g., Duplicate patient IDs} | {e.g., Merge, keep most recent} | {e.g., Logged in cleansing report} |
| DC-002 | {e.g., Orphan record handling} | {e.g., Child record without parent} | {e.g., Reject and report} | {e.g., Logged in exception report} |
| DC-003 | {e.g., Invalid value correction} | {e.g., State code not in lookup} | {e.g., Map to "UNKNOWN", flag for review} | {e.g., Logged in correction report} |

### Migration Tool

| Attribute | Detail |
|---|---|
| Tool Name | {e.g., Custom ETL scripts, Informatica, SSIS} |
| Version | {Version number} |
| Qualification Status | Qualified / Unqualified-with-enhanced-verification |
| Qualification Evidence | {Reference to qualification document or rationale for unqualified use} |

> **Note:** The migration tool is part of the validated process. GAMP 5 expects that tools used in qualification activities are themselves qualified, or that their output is independently verified. If an unqualified tool is used, the protocol must include enhanced output verification to compensate.

---

## 6. Migration Risk Assessment

Migration-specific risks must be identified, rated, and mitigated. Cross-reference the project Risk Assessment for migration-related failure modes.

### Common Migration Risks

| Risk ID | Risk Description | Likelihood | Impact | Risk Level | Mitigation |
|---|---|---|---|---|---|
| MR-001 | Data loss during migration (records not transferred) | {L/M/H} | High | {Score} | Record count reconciliation, completeness verification |
| MR-002 | Data corruption (field values altered incorrectly) | {L/M/H} | High | {Score} | Field-level accuracy verification on sampled records |
| MR-003 | Data truncation (values exceed target field length) | {L/M/H} | Medium | {Score} | Pre-migration field length analysis, validation rules |
| MR-004 | Transformation errors (incorrect rule application) | {L/M/H} | High | {Score} | Transformation verification test cases, boundary testing |
| MR-005 | Orphan records (broken relationships in target) | {L/M/H} | Medium | {Score} | Referential integrity verification |
| MR-006 | Duplicate records (same source record migrated twice) | {L/M/H} | Medium | {Score} | Unique constraint verification, record count reconciliation |
| MR-007 | Referential integrity violations (foreign key breaks) | {L/M/H} | High | {Score} | Post-migration integrity checks |
| MR-008 | Encoding issues (character set conversion errors) | {L/M/H} | Medium | {Score} | Character encoding verification on sample data |
| MR-009 | Audit trail discontinuity (history lost or misattributed) | {L/M/H} | High | {Score} | Audit trail continuity verification |
| MR-010 | Cutover window overrun (migration takes longer than planned) | {L/M/H} | High | {Score} | Dry runs with timing, contingency time buffer |

---

## 7. Prerequisites Checklist

Include this checklist at the start of every Data Migration Validation Protocol. Items are verified before any migration execution begins.

| # | Prerequisite | Verified (Y/N) | Verified By | Date |
|---|---|---|---|---|
| 1 | Source system data freeze completed (or delta migration approach documented and approved) | | | |
| 2 | Target system IQ protocol {IQ-DOC-ID} approved | | | |
| 3 | Design Specification {DS-DOC-ID} version {X.X} approved and available | | | |
| 4 | URS {URS-DOC-ID} version {X.X} approved, migration requirements (Section 3.16) reviewed | | | |
| 5 | Validation Plan {VP-DOC-ID} approved and available | | | |
| 6 | Data mapping specification reviewed and approved by source system SME and target system SME | | | |
| 7 | Migration tool qualified (or rationale for unqualified use with enhanced verification documented) | | | |
| 8 | Full backup of source system completed and verified (restore test passed) | | | |
| 9 | Rollback plan documented, reviewed, and tested (restore of target to pre-migration state verified) | | | |
| 10 | Migration environment (test/staging) provisioned and accessible for dry run | | | |
| 11 | Dry run(s) completed with acceptable results (or this is the first dry run) | | | |
| 12 | Reconciliation scripts/tools tested and operational | | | |
| 13 | Execution personnel trained on migration protocol procedures | | | |
| 14 | Blank deviation log forms available | | | |
| 15 | Communication plan distributed to all stakeholders | | | |

**Coaching note:** Items 1-6 are non-negotiable. Items 7-15 can be tailored — but item 8 (source backup) and item 9 (rollback plan) should only be waived with documented QA justification. Migrating without a verified rollback capability is a regulatory red flag.

---

## 8. Migration Verification Protocol

Test cases are organized into six verification types. Each type addresses a distinct aspect of data integrity.

### 8.1 Completeness Verification

Completeness verification confirms that all source records arrived in the target system — nothing was lost or duplicated.

**Test Case Format:**

```
Test Case ID:    DM-CMP-{NNN}
Title:           {Concise description}
Verification:    Completeness
URS Trace:       URS Section 3.16.{X}
Priority:        {Critical | Major | Minor}
Prerequisites:   Migration execution completed for {entity}
```

**Required test cases per migrated entity:**

| Step | Action | Expected Result | Actual Result | Pass/Fail | Executed By | Date |
|---|---|---|---|---|---|---|
| 1 | Execute record count query on source system for {entity}: `SELECT COUNT(*) FROM {source_table}` | Record count = {N} | {Filled during execution} | {P/F} | {Initials} | {Date} |
| 2 | Execute record count query on target system for {entity}: `SELECT COUNT(*) FROM {target_table}` | Record count = {N} (matches source) | | | | |
| 3 | Compare source and target counts. Record any delta | Delta = 0 | | | | |
| 4 | Execute orphan record check on target: records in target with no source counterpart | Orphan count = 0 | | | | |
| 5 | Execute missing record check: source records not present in target | Missing count = 0 | | | | |

> **Note:** For entities where data cleansing rules reduce record counts (e.g., deduplication), the expected target count is source count minus documented exclusions. The delta must be fully explained by the cleansing report.

### 8.2 Accuracy Verification

Accuracy verification confirms that migrated field values match the source — data was not corrupted, truncated, or incorrectly transformed.

**Sampling Strategy:**

| Source Record Count | Minimum Sample Size | Sampling Method |
|---|---|---|
| < 1,000 | 100% (all records) | Full comparison |
| 1,000 - 10,000 | 10% or 100 records (whichever is greater) | Random sample + boundary cases + GxP-critical records |
| > 10,000 | 1% or 500 records (whichever is greater) | Risk-based stratification: random sample + all GxP-critical records + boundary cases |

**Sampling composition for stratified samples:**

- 50% random selection (uniformly distributed across source data)
- 25% boundary cases (first/last records, max/min values, null-heavy records, records at field length limits)
- 25% high-risk records (GxP-critical data, records with complex transformations, records flagged during dry run)

**Required test cases per migrated entity:**

| Step | Action | Expected Result | Actual Result | Pass/Fail | Executed By | Date |
|---|---|---|---|---|---|---|
| 1 | Select sample records per sampling strategy. Document sample selection rationale and record IDs | Sample of {N} records selected | {Filled during execution} | {P/F} | {Initials} | {Date} |
| 2 | For each sampled record, compare every mapped field: source value vs. target value | All fields match (or match after documented transformation) | | | | |
| 3 | Record any field-level discrepancies with record ID, field name, source value, and target value | Zero discrepancies | | | | |
| 4 | Where automated checksum comparison is feasible, execute and compare checksums | Checksums match | | | | |

> **Note:** The sampling strategy must be documented and defensible. An auditor will ask: why this sample size? why these records? "We picked some records" is not a defensible strategy.

### 8.3 Transformation Verification

Transformation verification confirms that every transformation rule was applied correctly.

**Required test cases per transformation rule:**

| Step | Action | Expected Result | Actual Result | Pass/Fail | Executed By | Date |
|---|---|---|---|---|---|---|
| 1 | Identify records where transformation rule {TR-NNN} applies | Records identified | {Filled during execution} | {P/F} | {Initials} | {Date} |
| 2 | For sample records, verify source value, apply transformation rule manually, compare to target value | Target value matches manually computed transformation result | | | | |
| 3 | Test boundary conditions for this transformation (per transformation rule boundary conditions column) | Boundary values transformed correctly | | | | |
| 4 | Verify null/empty value handling: apply transformation rule to null and empty source values | Null/empty values handled per transformation rule specification | | | | |

### 8.4 Referential Integrity Verification

Referential integrity verification confirms that relationships between data entities survived migration.

**Required test cases:**

| Step | Action | Expected Result | Actual Result | Pass/Fail | Executed By | Date |
|---|---|---|---|---|---|---|
| 1 | For each foreign key relationship in the target schema, query for orphan child records (child records with no matching parent) | Zero orphan child records per relationship | {Filled during execution} | {P/F} | {Initials} | {Date} |
| 2 | For each lookup table reference, query for invalid lookup values in migrated data | Zero invalid lookup references | | | | |
| 3 | For each parent-child relationship, compare parent-child counts: source vs. target | Parent-child counts match source | | | | |
| 4 | Verify cascade relationships: where parent records were excluded by cleansing rules, verify child records were handled per cleansing specification | Child records handled per DC rules | | | | |

### 8.5 Audit Trail Continuity Verification

Audit trail continuity is a frequent audit finding. Migrated records must not appear to have been "created" by the migration user — they must be clearly identified as migrated historical records.

**Regulatory requirement:** 21 CFR Part 11 / EU GMP Annex 11: Migrated electronic records must maintain their ALCOA+ properties. The audit trail is not optional ancillary data — it is an integral part of the electronic record.

**Required test cases:**

| Step | Action | Expected Result | Actual Result | Pass/Fail | Executed By | Date |
|---|---|---|---|---|---|---|
| 1 | For sampled records, compare audit trail entries: source system audit trail vs. target system audit trail | Audit trail entries migrated completely (who/what/when preserved) | {Filled during execution} | {P/F} | {Initials} | {Date} |
| 2 | Verify that migrated records are identified as migrated in the target system (migration flag, migration marker, or equivalent) | Migrated records clearly distinguishable from natively created records | | | | |
| 3 | Verify that the migration event itself is recorded in the target system's audit trail (who executed, when, what was migrated) | Migration event logged in target audit trail | | | | |
| 4 | Verify that original author/modifier attribution is preserved — migrated records are not attributed to the migration service account | Original author attribution retained | | | | |

### 8.6 Data Integrity (ALCOA+) Verification

ALCOA+ properties must be verified for migrated records. This verification type provides the overarching data integrity assessment.

| ALCOA+ Property | Verification | Test Approach |
|---|---|---|
| **Attributable** | Migrated records retain original author/modifier attribution | Compare author fields: source vs. target for sampled records |
| **Legible** | Migrated data is readable and displayable in the target system | Open sampled records in the target system UI; verify all fields render correctly (no encoding artifacts, no truncation) |
| **Contemporaneous** | Original timestamps preserved (not overwritten with migration timestamp) | Compare created/modified timestamps: source vs. target for sampled records |
| **Original** | Migrated record identified as migrated copy; original source preserved until retention period expires | Verify migration flag on target records; verify source system data retained per retention policy |
| **Accurate** | Field-by-field accuracy verified per sampling plan | Cross-reference with Accuracy Verification (Section 8.2) results |
| **Complete** | All records and all fields migrated | Cross-reference with Completeness Verification (Section 8.1) results |
| **Consistent** | Data is consistent across related entities and time periods | Cross-reference with Referential Integrity Verification (Section 8.4) results |
| **Enduring** | Migrated data is stored in a durable format accessible throughout its retention period | Verify target system storage, backup, and archival configuration covers migrated data |
| **Available** | Migrated data is accessible to authorized users when needed | Verify migrated records are retrievable via normal target system access paths |

---

## 9. Dry Run Requirements

A dry run is a full rehearsal of the migration in a non-production environment. It validates the migration package, identifies issues, and provides timing data for cutover window planning.

### Dry Run Rules

1. **Minimum one full dry run** in a test/staging environment before production migration. For complex migrations (multiple source systems, >1M records, or >10 transformation rules), a minimum of two dry runs is recommended.
2. **Dry run must execute the complete migration package** — not a subset. Partial dry runs do not validate the full migration sequence and miss interaction effects.
3. **Dry run results documented using the same verification protocol** — the same test cases, the same sampling strategy, the same reconciliation procedures. The dry run is a dress rehearsal, not a smoke test.
4. **All dry run issues resolved before production cutover.** Unresolved dry run issues are open risks that must be formally accepted (with documented justification) or remediated.
5. **Dry run timing recorded.** Document elapsed time per migration phase to validate cutover window estimates.

### Dry Run Documentation

| Attribute | Detail |
|---|---|
| Dry Run Number | {1, 2, ...} |
| Environment | {Test/Staging/Pre-production} |
| Date | {Execution date} |
| Source Data Snapshot Date | {Date of source data used} |
| Migration Package Version | {Version of scripts/tools used} |
| Total Elapsed Time | {HH:MM} |
| Completeness Result | {Pass/Fail with record count deltas} |
| Accuracy Result | {Pass/Fail with discrepancy count} |
| Issues Found | {Count and severity summary} |
| Issues Resolved | {Count and resolution summary} |
| Go/No-Go for Next Step | {Proceed to production / Repeat dry run / Escalate} |

---

## 10. Cutover Plan

The cutover plan is the step-by-step procedure for executing the production migration. It must be executable under pressure — clear, sequenced, and unambiguous.

### Cutover Procedure Template

| Step | Action | Responsible Party | Estimated Time | Actual Time | Status | Notes |
|---|---|---|---|---|---|---|
| 1 | Notify all stakeholders that cutover is beginning | {Project Manager} | {MM} min | | | |
| 2 | Freeze source system (disable user access or set to read-only) | {Source System Admin} | {MM} min | | | |
| 3 | Execute final source system backup and verify | {DBA / Sys Admin} | {MM} min | | | |
| 4 | Execute delta migration (if applicable — changes since last freeze point) | {Migration Engineer} | {MM} min | | | |
| 5 | Execute primary migration package | {Migration Engineer} | {HH:MM} | | | |
| 6 | Execute completeness verification (record count reconciliation) | {QA / Validation} | {MM} min | | | |
| 7 | Execute accuracy verification (sample-based field comparison) | {QA / Validation} | {MM} min | | | |
| 8 | Execute referential integrity verification | {QA / Validation} | {MM} min | | | |
| 9 | **Go/No-Go decision point** | {Cutover Lead + QA} | {MM} min | | | |
| 10 | Enable target system for user access | {Target System Admin} | {MM} min | | | |
| 11 | Execute post-go-live smoke test (key business workflows using migrated data) | {Business SME} | {MM} min | | | |
| 12 | Notify all stakeholders that cutover is complete | {Project Manager} | {MM} min | | | |

### Go/No-Go Decision Criteria

| Criterion | Required for Go | Threshold |
|---|---|---|
| Record count reconciliation | Yes | 100% match (after documented exclusions) |
| Accuracy verification (sampled) | Yes | 100% accuracy on sampled records |
| Referential integrity | Yes | Zero violations |
| Elapsed time vs. window | Yes | Within planned cutover window (or approved extension) |
| Critical deviations | Yes | Zero open critical deviations |

### Delta Migration

If the migration strategy requires a delta migration (handling changes between the initial data freeze and final cutover):

1. Document the delta identification method (timestamp-based, trigger-based, log-based).
2. Document the delta migration procedure (same tool? separate script?).
3. Include delta records in the verification scope — they are subject to the same completeness and accuracy requirements.
4. Verify that delta records do not conflict with previously migrated records (no duplicates, no version conflicts).

---

## 11. Rollback Plan

The rollback plan defines how to reverse the migration if critical issues are discovered during or after cutover.

### Rollback Triggers

Define conditions that trigger rollback. These must be agreed upon before cutover begins:

| Trigger | Description |
|---|---|
| Record count mismatch | Completeness verification fails: source count does not match target count (after documented exclusions) beyond tolerance |
| Data corruption detected | Accuracy verification identifies systematic field-level errors (not isolated discrepancies) |
| Referential integrity failure | Foreign key violations detected in GxP-critical entities |
| Cutover window exceeded | Migration or verification exceeds the maximum allowed cutover window with no resolution path |
| Critical business process blocked | Post-go-live smoke test reveals that a critical business process cannot function with migrated data |

### Rollback Procedure

| Step | Action | Responsible Party | Estimated Time |
|---|---|---|---|
| 1 | Declare rollback decision (documented with rationale) | {Cutover Lead + QA} | {MM} min |
| 2 | Disable target system user access | {Target System Admin} | {MM} min |
| 3 | Restore target system to pre-migration state from verified backup | {DBA / Sys Admin} | {HH:MM} |
| 4 | Verify target system restored correctly (compare against pre-migration baseline) | {QA / Validation} | {MM} min |
| 5 | Re-enable source system for user access (if previously frozen) | {Source System Admin} | {MM} min |
| 6 | Notify all stakeholders of rollback and next steps | {Project Manager} | {MM} min |
| 7 | Document rollback in deviation log with root cause and remediation plan | {QA / Validation} | {MM} min |

### Rollback Constraints

- **Maximum rollback window:** Define the time limit after cutover beyond which rollback is no longer feasible (e.g., "rollback is feasible for 48 hours post-cutover; after that, new data in the target system makes rollback destructive").
- **Post-rollback verification:** The rollback itself must be verified — restoring a backup is not sufficient evidence that the system is in the correct state.
- **Rollback testing:** The rollback procedure must be tested during at least one dry run.

---

## 12. Pass/Fail Criteria

### Test Case Level

- **Pass:** All steps within the test case have "Pass" recorded, and actual results match expected results.
- **Fail:** Any step records "Fail." A deviation must be logged immediately.

### Verification Type Level

| Verification Type | Pass Criteria |
|---|---|
| Completeness | 100% record count reconciliation per entity (after documented exclusions). Zero unexplained missing or orphan records |
| Accuracy | 100% field-level accuracy on all sampled records |
| Transformation | 100% correct transformation on all tested records, including boundary cases |
| Referential Integrity | Zero referential integrity violations |
| Audit Trail Continuity | 100% audit trail preservation on sampled records. Migration event logged in target |
| ALCOA+ | All ALCOA+ properties verified for sampled records |

### Protocol Level

- **Overall Pass:** All verification types pass. Zero open critical or major deviations. All minor deviations resolved or accepted with documented justification.
- **Overall Fail:** Any verification type fails AND the failure cannot be resolved within the cutover window. Rollback triggered.
- **Conditional Pass:** Minor deviations accepted with justification. Requires QA sign-off on each accepted deviation and a documented remediation plan with timeline.

### Design Principles

1. **Pre-define criteria before execution.** Never decide the acceptance rules after seeing results.
2. **GxP-critical data has zero tolerance.** For entities identified as GxP-critical in the data mapping specification, any accuracy failure is a critical deviation.
3. **Require deviation closure.** No protocol can be approved with open deviations — they must be resolved, accepted-with-justification, or deferred with documented risk assessment.
4. **Migration protocol approval is one input to go-live.** It does not replace OQ/PQ or the overall release decision.

---

## 13. Deviation Handling

When a verification step fails, a deviation is recorded immediately. The deviation lifecycle follows the same 10-step process as IQ/OQ protocols (detect, log, classify, notify, investigate, impact assess, resolve, re-test, close, summarize).

### Deviation Log Format

| Field | Description |
|---|---|
| Deviation ID | DEV-DM-{NNN} (sequential within this protocol execution) |
| Test Case ID | The DM test case that failed |
| Step Number | The specific step that failed |
| Verification Type | Completeness / Accuracy / Transformation / Referential Integrity / Audit Trail / ALCOA+ |
| Date Detected | Date of failure observation |
| Detected By | Name and role of tester |
| Description | What happened vs. what was expected — factual, no interpretation. Include record IDs, field names, source values, target values |
| Severity | Critical / Major / Minor |
| Root Cause | Category: transformation error / mapping error / data quality issue / tool defect / configuration error / specification error |
| Corrective Action | What was done to resolve |
| Re-test Result | Pass / Fail after correction (with date and tester) |
| Impact Assessment | Effect on other migrated entities and data integrity |
| Closed By | QA reviewer name, signature, and date |

### Deviation Severity Definitions

| Severity | Definition | Protocol Impact |
|---|---|---|
| **Critical** | GxP-critical data loss, corruption, or integrity violation. Audit trail discontinuity for regulated records. Systematic (non-isolated) data errors | Migration halted. Rollback evaluation triggered. Cannot proceed without resolution |
| **Major** | Non-GxP data errors affecting multiple records. Transformation errors on non-critical fields. Isolated referential integrity issues with workaround | Migration may continue for unaffected entities. Resolution required before protocol approval |
| **Minor** | Isolated discrepancies in non-critical data. Formatting differences that do not affect data meaning. Documentation gaps | Migration continues. Deviation resolved before protocol approval |

---

## 14. GAMP-Scaled Depth

Migration verification depth scales with GAMP 5 software category. The differences are in verification rigor, sampling requirements, and tool qualification expectations — not in structure.

### Scaling by GAMP Category

| Dimension | Cat 3 (COTS) | Cat 4 (Configured) | Cat 5 (Custom) |
|---|---|---|---|
| **Migration tool** | Vendor-provided migration utility — verify configuration, not tool internals | Vendor or third-party ETL tool — qualify tool, verify configuration mappings | Custom migration scripts — full code review, unit testing, tool qualification |
| **Data mapping** | Configuration parameters only (settings, preferences) | All configured data entities and their field mappings | Full mapping specification including custom transformations and business logic |
| **Transformation verification** | Minimal (COTS handles standard conversions) | Verify each configured transformation rule | Verify every custom transformation, including boundary values and error paths |
| **Sampling depth** | Standard sampling per Section 8.2 table | Standard sampling with enhanced coverage for configured entities | Enhanced sampling: increase minimum percentages by 50% for GxP-critical entities |
| **Dry runs** | Minimum 1 | Minimum 1 | Minimum 2 |
| **Audit trail** | Verify migration event logged | Verify migration event + audit history preserved for configured workflows | Verify complete audit trail migration with attribution, timestamps, and chain of custody |
| **Rollback testing** | Documented procedure | Documented and tested during dry run | Documented, tested during dry run, and independently verified |

### CSA Alignment

Under FDA Computer Software Assurance (CSA) guidance:

- **Unscripted testing** may be used for migration verification of low-risk data entities (operational data, reference data, non-GxP configuration) where the tester has domain expertise and can exercise professional judgment.
- **Scripted testing** is required for GxP-critical records, audit trail migration, and any data entity where a migration error could directly affect product quality, patient safety, or data integrity.
- **Risk-based sampling** is explicitly supported by CSA. The risk assessment should identify which data entities are GxP-critical. Critical entities receive 100% verification or enhanced sampling; non-critical entities use standard sampling.
- **Documentation proportionality:** For low-risk entities, a reconciliation summary may replace detailed step-by-step evidence. For high-risk entities, full step-by-step evidence with screenshots or exports is required.

---

## 15. Example Test Cases

### Example 1: Record Count Reconciliation

**Header:** `DM-CMP-001 | Verification: Completeness | URS Trace: URS-3.16.1 | Priority: Critical`

| Step | Action | Expected Result |
|---|---|---|
| 1 | Execute on source system: `SELECT COUNT(*) FROM patients WHERE status = 'active'` | Count = {N} |
| 2 | Execute on target system: `SELECT COUNT(*) FROM Patient WHERE IsActive = 1` | Count = {N} (matches source) |
| 3 | Calculate delta: source count - target count | Delta = 0 |
| 4 | If delta != 0, identify discrepant records by comparing source and target primary keys | All records accounted for (documented exclusions or deviation logged) |

### Example 2: Field-Level Accuracy Check

**Header:** `DM-ACC-001 | Verification: Accuracy | URS Trace: URS-3.16.2 | Priority: Critical`

| Step | Action | Expected Result |
|---|---|---|
| 1 | Select sample of {N} patient records per sampling strategy. Document record IDs | Sample selected and documented |
| 2 | For each sampled record, export source fields: PatientID, Name, DOB, MRN, Allergies | Source data exported |
| 3 | For each sampled record, export target fields: PatientId, FullName, DateOfBirth, MedicalRecordNumber, AllergyList | Target data exported |
| 4 | Compare field-by-field, applying transformation rules (TR-001 for date format, TR-003 for name concatenation) | All fields match after transformation |
| 5 | Record any discrepancies: record ID, field, source value, target value, expected transformation | Zero discrepancies |

### Example 3: Audit Trail Continuity

**Header:** `DM-AUD-001 | Verification: Audit Trail | URS Trace: URS-3.16.5 | Priority: Critical`

| Step | Action | Expected Result |
|---|---|---|
| 1 | Select 10 patient records from the accuracy sample that have modification history in the source system | Records with audit trail entries selected |
| 2 | For each record, export the source system audit trail (user, action, timestamp, old value, new value) | Source audit trail exported |
| 3 | For each record, view the target system audit trail for the same record | Target audit trail displayed |
| 4 | Compare: are all source audit trail entries present in the target? | All entries present |
| 5 | Verify original user attribution is preserved (not replaced with migration service account) | Original usernames retained |
| 6 | Verify original timestamps are preserved (created date, modified dates) | Original timestamps retained |
| 7 | Verify the migration event itself is logged (entry showing record was migrated, by whom, when) | Migration event entry present |

---

## 16. Coaching Questions

Use these questions during coached refinement to strengthen the migration protocol before finalization.

### Completeness

- "Does the data mapping specification cover every entity listed in URS Section 3.16? Let's walk through the URS migration requirements and check."
- "Are there data entities in the source system that are explicitly OUT of scope? Document the exclusion rationale — an auditor will ask why."
- "Have you accounted for all data types — not just transactional data, but also configuration data, lookup tables, user accounts, and audit trails?"

### Accuracy

- "What is the sampling strategy, and can you defend it to an auditor? 'We checked some records' is not defensible. Document the statistical basis or risk-based rationale."
- "For each transformation rule, have you identified the boundary conditions? Date conversions at year boundaries, unit conversions at precision limits, text truncation at field length limits?"
- "Are null and empty values handled explicitly in every transformation rule? What happens when the source field is null?"

### Data Integrity

- "After migration, can you tell which records are migrated vs. natively created? If not, you have an ALCOA+ problem — 'Original' requires that migrated copies are identifiable."
- "Are original timestamps preserved, or does the migration overwrite them? Overwritten timestamps violate 'Contemporaneous.'"
- "Is the audit trail migrating with the data? Audit trail data left behind in the source system is a Part 11/Annex 11 finding waiting to happen."

### Risk

- "Which data entities are GxP-critical? These get enhanced sampling or 100% verification. Everything else gets standard sampling. Is this documented in the risk assessment?"
- "What happens if the cutover window is exceeded? Is there a documented decision point and an escalation path?"
- "Has the rollback plan been tested? An untested rollback is not a rollback plan — it's a hope."

### Tool Qualification

- "Is the migration tool qualified? If not, have you documented the rationale and added enhanced output verification to compensate?"
- "For custom migration scripts — have they been code-reviewed? Unit-tested? Version-controlled?"

---

## 17. Anti-Patterns

The reviewer agent checks for these common data migration mistakes. Each anti-pattern includes what is wrong and how to fix it.

| # | Anti-Pattern | What's Wrong | Fix |
|---|---|---|---|
| AP-1 | **The Trust-Me Migration** | Migration executed without reconciliation — "we ran the scripts and it worked." No verification evidence | Always execute the full verification protocol. Record count reconciliation + field-level accuracy + referential integrity at minimum |
| AP-2 | **The Snapshot-Only Validation** | Comparing record counts but not field-level accuracy. Count matching is necessary but not sufficient — counts can match while every field is wrong | Add field-level accuracy verification with documented sampling strategy |
| AP-3 | **The Missing Dry Run** | Going straight to production migration without a full rehearsal. First-time execution in production is unacceptable risk | Execute minimum one full dry run in test/staging. Document results. Resolve issues before production |
| AP-4 | **The Orphan Audit Trail** | Migrating data but leaving audit trails behind in the source system. Audit trail is part of the electronic record | Audit trail data MUST migrate with the primary records for Part 11/Annex 11 compliance. Include audit trail in data mapping specification |
| AP-5 | **The Frozen-in-Time Assumption** | Assuming source data will not change between mapping specification and cutover. Source systems do not stop while you plan | Plan for delta changes. Document the freeze point. Define delta migration approach if applicable |
| AP-6 | **The Black Box Tool** | Using a migration tool without qualification or documentation. The tool is part of the validated process | Qualify the migration tool per GAMP 5, or independently verify all tool output with enhanced verification |
| AP-7 | **The Undocumented Transformation** | Applying data transformations during migration without documenting the rules. "The developer handled the date formats" | Every transformation must have a documented rule (ID, source format, target format, boundary conditions) and a verification test case |
| AP-8 | **The Missing Rollback** | No rollback plan, or a rollback plan that has never been tested | Document rollback triggers, procedure, and maximum rollback window. Test during dry run |
| AP-9 | **The Sample-of-Convenience** | Sampling records for accuracy verification by picking "a few" records without a documented strategy | Define sampling strategy with statistical or risk-based rationale. Document selection criteria. Ensure sample includes boundary cases and GxP-critical records |
| AP-10 | **The One-Dimension Check** | Running completeness checks only, or accuracy checks only, without covering all six verification types | Execute all six verification types: completeness, accuracy, transformation, referential integrity, audit trail, ALCOA+ |

---

## 18. Protocol-Level Override Points

The following aspects of the migration protocol can be customized via manifest overrides. Each override must be documented with justification.

| # | Override Point | Default | Customizable Range |
|---|---|---|---|
| 1 | Sampling strategy and minimum sample sizes | Per Section 8.2 table | May increase minimums; decreasing requires documented risk-based justification |
| 2 | Number of required dry runs | 1 (Cat 3/4), 2 (Cat 5) | May increase; decreasing below 1 is not permitted |
| 3 | Rollback window duration | 48 hours post-cutover | Site-specific based on data accumulation rate in target system |
| 4 | Source system freeze approach | Full freeze before cutover | Delta migration approach if business cannot tolerate freeze |
| 5 | Migration tool qualification requirements | Full qualification per GAMP 5 | Unqualified tool with enhanced output verification if justified |
| 6 | Delta migration approach | Not applicable (full freeze) | Timestamp-based, trigger-based, or log-based delta capture |
| 7 | Post-migration parallel operation period | None | 1-30 days of parallel operation if risk profile warrants it |
| 8 | Accuracy verification method | Manual field-by-field comparison | Automated comparison tooling if tool is qualified |
| 9 | Audit trail migration scope | Full audit trail history | Truncated history with documented retention justification |
| 10 | Pass/fail tolerance for non-GxP data | Zero tolerance (same as GxP) | Minor tolerance for non-critical, non-GxP operational data with QA approval |
